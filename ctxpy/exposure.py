from typing import Optional
from time import sleep

from pandas.api.types import is_list_like

from .base import CTXConnection, ResponseTransformer


class Exposure(CTXConnection):
    """
    An API Connection to CCTE's exposure data.

    Connection allows users to search for a single chemicals': reported
    functional use, predicted functional use, products it has been reported to
    be in, and presence on various lists organized by keywords. This search is
    performed by submitting a single chemical DTXSID. Connection also allows
    for retrieval of controlled vocabularies, namely, function categories (fc),
    list presence keywords (lpk), and product use categories (puc).

    Parameters
    ----------
    x_api_key : Optional[str]
        A personal key for using CCTE's APIs, if left blank, it assumes a key is
        already stored in ~/.config/ccte_api/config.toml

    Returns
    -------
    CTXConnection specific to exposure endpoints

    See Also
    --------
    ccte_init
    Chemical
    Hazard

    Examples
    --------
    Make a Connection with stored API Key in ~/.config/ccte_api/config.toml:
    >>> expo = ctx.Exposure()

    Make a Connection by providing an API Key
    >>> expo = ctx.Exposure(x_api_key='648a3d70')

    """

    KIND = "exposure"

    def __init__(self, x_api_key: Optional[str] = None):
        super().__init__(x_api_key=x_api_key)


    def _batch(self, endpoint:str, query:str):
        """
        There are currently no batch searches for the `search_qsurs` and `search_mmdb` 
        methods. This function allows a list of dtxsids to be sumitted to the 
        `search_qsurs` method and run each dtxsid as its own get call to the 
        CTXConnection. While the same could be done for the `search_mmdb` method, it is
        not yet implemented because of the bandwidth/memory that is required for a call
        of a single medium or chemical to that endpoint.
        """
        
        
        ## Remove duplicated DTXSIDs
        query = list(set(query))
        
        df = []
        for q in query:
            df.extend(self.request(endpoint=endpoint,query=q))
            sleep(0.1)
        return df


    def search_cpdat(self, vocab_name, dtxsid, batch_size=200):
        """
        Search for CPDat information by CPDat vocabulary and DTXSID(s).

        CPDat vocabularies are defined in Handa et al. 2025. For a single chemical or 
        list of chemicals search for 1) reported functional uses, 2) products that 
        report this chemical as an ingredient, or 3) annotated lists of chemicals that
        contain the searched chemical(s).

        Parameters
        ----------
        vocab_name : string
            The type of search method to use. Options are "fc", "qsur",
            "puc", or "lpk". "fc" is reported functional use, "qsur" is
            predicted functional use, "puc" is product information, and "lpk" is
            chemical list presence information.

        dtxsid : string or list-like
            If string, then a single DTXSID is expected. If list like, then a list of 
            DTXSIDs is expected.

        Return
        ------
        pandas DataFrame
            a DataFrame of all the infomration returned for a specific vocabulary for
            all matching entries for the searched chemical or chemicals within CPDat.


        Examples
        --------
        Search for reported functional uses
        >>> expo.search_cpdat(vocab_name="fc",dtxsid="DTXSID7020182")
               id         dtxsid                datatype  ...  functioncategory
        0   22724  DTXSID7020182  Chemical presence list  ...   Flame retardant
        1   22722  DTXSID7020182  Chemical presence list  ...              <NA>
        2   22728  DTXSID7020182             Composition  ...          Monomers
        3   22726  DTXSID7020182             Composition  ...          Hardener
        4   22727  DTXSID7020182             Composition  ...              <NA>
        5   22732  DTXSID7020182             Composition  ...          Monomers

        Search for product information

        >>> expo.search_cpdat(vocab_name='puc',dtxsid='DTXSID7020182')

               id         dtxsid  ...  weightfractiontype  component
        0  589086  DTXSID7020182  ...            reported       <NA>
        1  657348  DTXSID7020182  ...            reported       <NA>
        2  192133  DTXSID7020182  ...            reported       <NA>
        3  655734  DTXSID7020182  ...            reported       <NA>
        4   85935  DTXSID7020182  ...            reported       <NA>

        >>> expo.search_cpdat(vocab_name='lpk', dtxsid='DTXSID7020182')

               id         dtxsid  ...                                         keywordset
        0  127967  DTXSID7020182  ...                             Canada; pharmaceutical
        1    9997  DTXSID7020182  ...                      active_ingredient; Pesticides
        2   40538  DTXSID7020182  ...          Indirect additives food contact (10/2018)
        3  135524  DTXSID7020182  ...                                           children
        4  113048  DTXSID7020182  ...  children; WA Children's Safe Product Act (4/2020)
        5   76175  DTXSID7020182  ...                         Europe; Food contact items
        """

        options = {
            "fc":   "functional-use/search/by-dtxsid",
            "puc":  "product-data/search/by-dtxsid",
            "lpk":  "list-presence/search/by-dtxsid",
        }
        
        if vocab_name not in options.keys():
            raise KeyError(f"Value {vocab_name} is invalid option for argument `by`.")

        endpoint = f"{self.KIND}/{options[vocab_name]}/"
        info = super(Exposure, self).ctx_call(endpoint=endpoint,
                                              query=dtxsid,
                                              batch_size=batch_size,
                                              bracketed=True)

        return ResponseTransformer(info).to_df()



    def search_qsurs(self, dtxsid):
        """
        Search for Quantitative Structure-Use Relationship (QSUR) predictions by
        DTXSID(s).

        QSURs are defined in Phillips et al. 2017 (DOI: 10.1039/C6GC02744J). Predicted
        functional uses are returned for the provided DTXSID(s). Only predictions that 
        are within the domain of applicability for a model are returned.

        Parameters
        ----------
        dtxsid : string or list-like
            If string, then a single DTXSID is expected. If list like, then a list of 
            DTXSIDs is expected.

        Return
        ------
        pandas DataFrame
            DataFrame containing the chemical identifier, harmonized functional use, and
            probability of the chemical having that use for each "in domain" prediction
            of a model.

        Examples
        --------
        Search for predicted functional uses of a single chemical:
        
        >>> expo.search_qsurs(dtxsid='DTXSID7020182')

           harmonizedFunctionalUse  probability
        0            antimicrobial       0.3722
        1              antioxidant       0.8941
        2                 catalyst       0.2031
        3                 colorant       0.1560
        4              crosslinker       0.7743
        5          flame_retardant       0.2208

        Search for predicted functional uses of multiple chemicals

        >>> expo.search_qsurs(dtxsid=['DTXSID2021868','DTXSID7021360'])
                   dtxsid harmonizedFunctionalUse  probability
        0   DTXSID7021360           antimicrobial       0.2656
        1   DTXSID7021360             antioxidant       0.3572
        2   DTXSID7021360                catalyst       0.6912
        3   DTXSID7021360                colorant       0.0889
        4   DTXSID7021360             crosslinker       0.1637
        5   DTXSID7021360               flavorant       0.4565
        6   DTXSID7021360               fragrance       0.9633
        7   DTXSID7021360            preservative       0.4460
        8   DTXSID7021360        skin_conditioner       0.0150
        9   DTXSID7021360         skin_protectant       0.1062
        10  DTXSID7021360             uv_absorber       0.2577
        11  DTXSID2021868           antimicrobial       0.2953
        12  DTXSID2021868             antioxidant       0.3482
        13  DTXSID2021868                catalyst       0.5329
        14  DTXSID2021868                colorant       0.1129
        15  DTXSID2021868             crosslinker       0.1402
        16  DTXSID2021868               flavorant       0.3221
        17  DTXSID2021868               fragrance       0.9874
        18  DTXSID2021868        skin_conditioner       0.0289
        19  DTXSID2021868         skin_protectant       0.1560
        """
        endpoint = f"{self.KIND}/functional-use/probability/search/by-dtxsid/"
        
        ## Make sure its a list-like objects of strings
        if is_list_like(dtxsid):
            info = self._batch(endpoint=endpoint,query=dtxsid)
        elif isinstance(dtxsid,str):
            info = super(Exposure,self).ctx_call(endpoint=endpoint, query=dtxsid)
        else:
            raise TypeError("`dtxsid` must either be string or list-like of strings.")

        return ResponseTransformer(info).to_df()



    def search_mmdb(self, by, query, aggregate=False):
        """
        Search the Multimedia Monitoring Database (MMDB) either via medium name or via
        DTXSID(s).


        Parameters
        ----------
        by : string
            Method for searching MMDB. Options `medium`, 'aggregate`, or `dtxsid`. 
            `medium` returns all single-source type chemical records for a single  
            medium category, `aggregate` returns all aggregate type chemical records 
            for a single medium category, and `dtxsid` returns all single source type
            records for a single chemical substance across all media categories.

        query: string
            When searching MMDB only a single medium or chemical is searchable due to 
            call time contraints.

        Return
        ------
        pandas DataFrame
            DataFrame containing the chemical identifier, harmonized functional use, and
            probability of the chemical having that use for each "in domain" prediction
            of a model.

        Examples
        --------
        Search for predicted functional uses of a single chemical:
        
        >>> expo.search_mmdb(by='medium',query='livestock/meat')


        Search for predicted functional uses of multiple chemicals

        >>> expo.search_mmdb(by='dtxsid',query='DTXSID7020182')

        """
        if is_list_like(query):
            raise NotImplementedError(
                "Batch mode has not been implemented for searching MMDB."
                )

        options = {"medium":"/mmdb/single-sample/by-medium",
                   "aggregate": "/mmdb/aggregate/by-medium",
                   "dtxsid":"/mmdb/single-sample/by-dtxsid/"}
        endpoint = f"{self.KIND}{options[by]}"

        if by == 'dtxsid':
            params = None
            info = super(Exposure,self).ctx_call(endpoint=endpoint,
                                                 query=query,
                                                 params=params)
            info = ResponseTransformer(info).to_df()
        elif (by == 'medium') or (by == 'aggregate'):
            params = {"medium":query}
            info = super(Exposure,self).ctx_call(endpoint=endpoint,
                                                 query=query,
                                                 params=params)
            info = ResponseTransformer(info['data']).to_df()
            meta = {k:v for k,v in info.items() if k!="data"}
            info.attrs = meta
        else:
            raise ValueError(f"{by} not a valid option for `by` parameter.")

        return info


    def search_exposures(self, by, dtxsid):
        """
        Search for exposure estimates by DTXSID.

        Search for 1) exposure estimates for a chemical or chemicals based on
        the SEEM 3 framework published in Ring 2018 or 2) exposure pathway predictions 
        that are sourced from pathway prediction models (also published in Ring 2018; 
        DOI: 10.1021/acs.est.8b04056).

        Parameters
        ----------
        by : string
            The type of search method to use. Options are "pathways" or "seem".
            The "pathways" argument option returns the probability of exposure occuring
            along four exposure pathways defined in Ring 2018 (dietary, residential, 
            far-field pesticide, and far-field industrial); information is
            also provided on the reported production volume from the 2015 Chemical Data
            Reporting cycle in the U.S. as well as the Stockholm Convention for
            Persistent Organic Pollutants list. These two sources were crucial inputs
            for predicting exposure pathways.
            "seem" returns the consensus exposure estimate as well as the individual 
            exposure model predictions that lead to the consensus value. These estimates
            are also broken out by demographic information.

        dtxsid : string or list-like
            If string, then a single DTXSID is expected. If list like, then a list of 
            DTXSIDs is expected.

        Return
        ------
        pandas DataFrame
            dataframe of requested exposure pathway or exposure prediction values


        Examples
        --------
        Search for exposure pathway predictions for a single chemical
        >>> expo.search_exposures(by="pathways",dtxsid="DTXSID7020182")

                  dtxsid  productionVolume   units  probabilityPesticde  ...
        0  DTXSID7020182           2780000  kg/day                  0.0  ...

        Search for single exposure estimate provided by consensus
        >>> expo.search_exposures(by="seem",dtxsid="DTXSID7020182")

                id         dtxsid         demographic        predictor    median  ...
        0   768361  DTXSID7020182               Total     Food.Contact  0.017660  ...
        1   769393  DTXSID7020182               Total             FINE  0.000009  ...
        2   772655  DTXSID7020182               Total           RAIDAR  3.770000  ...
        3   784083  DTXSID7020182               Total      USETox.Pest  0.056240  ...
        4   785935  DTXSID7020182               Total    USETox.Indust  0.000137  ...
        5   749502  DTXSID7020182             Age 66+  SEEM2 Heuristic  0.000066  ...

        Search for exposure pathway predictions for multiple chemicals
        >>> expo.search_exposures(by='pathways',
                                  dtxsid=['DTXSID2021868','DTXSID7021360'])

                  dtxsid  productionVolume   units  probabilityPesticde  ...
        0  DTXSID2021868           8780000  kg/day                0.640  ...
        1  DTXSID7021360          17600000  kg/day                0.325  ...

        """

        options = {
            "pathways": "seem/general/search/by-dtxsid",
            "seem": "seem/demographic/search/by-dtxsid"
        }
        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        endpoint = f"{self.KIND}/{options[by]}/"

        info = super(Exposure,self).ctx_call(endpoint=endpoint,
                                             query=dtxsid)

        return ResponseTransformer(info).to_df()


    def search_httk(self, dtxsid):
        """
        Search for High-Throughput Toxicokinetics data by DTXSID.

        
        Parameters
        ----------
        dtxsid : string or list-like
            If string, then a single DTXSID is expected. If list like, then a list of 
            DTXSIDs is expected.

        Return
        ------
        pandas DataFrame
            a data frame containing high-througput toxicokinetic data for the submitted 
            chemical or chemicals.


        Examples
        --------
        Search for reported functional uses
        >>> expo.search_httk(dtxsid="DTXSID7020182")

                id         dtxsid     parameter measuredText  measured  ...
        0   101171  DTXSID7020182           Css       0.0083    0.0083  ...
        1   101172  DTXSID7020182           Css       0.0083    0.0083  ...
        2   101173  DTXSID7020182           Css       0.0083    0.0083  ...
        3   101174  DTXSID7020182           Css       0.0083    0.0083  ...
        4   101175  DTXSID7020182  TK.Half.Life         0.19    0.1900  ...
        5   101176  DTXSID7020182      Days.Css           NA       NaN  ...

        """

        endpoint = f"{self.KIND}/httk/search/by-dtxsid/"
        info = super(Exposure,self).ctx_call(endpoint=endpoint,
                                             query=dtxsid)
        return ResponseTransformer(info).to_df()

    def get_mmdb_vocabulary(self):
        """
        Retrieve the harmonized media vocabulary for MMDB.

        Parameters
        ----------
        None

        Return
        ------
        pandas.DataFrame
            DataFrame with every entry and its defintion in the controlled vocabulary.


        Examples
        --------

        Retrieve MMDB vocabulary

        >>> expo.get_mmdb_vocabulary()


        """


        endpoint = f"{self.KIND}/mmdb/mediums"
        info = super(Exposure,self).ctx_call(endpoint=endpoint)
        return ResponseTransformer(info).to_df()


    def get_cpdat_vocabulary(self, vocab_name):
        """
        Retrieve a contolled vocabulary from CPDat.

        Retrieve one of three controlled vocabularies (with definintions) in CPDat. 
        CPDat vocabularies are defined in Handa et al. 2025. Options are function
        categories (FCs), product use categories (puc) and list presence keywords
        (lpk).

        Parameters
        ----------
        vocab_name : string
            Name of the vocabulary to return. Options are "fc", "puc", or "lpk".
            "puc", or "lpk".

        Return
        ------
        pandas.DataFrame
            DataFrame with every entry and its defintion in the controlled vocabulary.


        Examples
        --------

        Get Function Category (FC) vocabulary

        >>> expo.get_cpdat_vocabulary(vocab_name='fc')

           id                 title                                        description
        0  28      Coalescing agent  Chemical substance used in polymer emulsions t...
        1  29      Conductive agent  Chemical substance used to conduct electrical ...
        2  30   Corrosion inhibitor  Chemical substance used to prevent or retard c...
        3  16     Anti-static agent  Chemical substance that prevents or reduces th...
        4  17  Anti-streaking agent  Chemical substance which serves to enhance eva...

        Get Product Use Category (PUC) vocabulary

        >>> expo.get_cpdat_vocabulary(vocab_name='lpk')

           id                                            tagName ...          kindName
        0  52                                           detected ...         Modifiers
        1  53                                     drinking_water ...             Media
        2  54  Electronics/small appliances - computers and a... ... PUC - formulation
        3  25                                             Canada ...          Location
        4  26                                               CEDI ...    Specialty list

        Get List Presence Keyword (LPK) vocabulary

        >>> expo.get_cpdat_vocabulary(vocab_name='puc')

            id     kindName                                genCat  ... definition
        0   45  Formulation  Cleaning products and household care  ... cleaning or ot...
        1   44  Formulation  Cleaning products and household care  ... cleaning or ca...
        2   43  Formulation  Cleaning products and household care  ... Cleaning or ca...
        3   42  Formulation  Cleaning products and household care  ... anti-static sp...
        4  291  Formulation  Cleaning products and household care  ... Includes urina...
        """
        options = {
            "fc": "functional-use/category",
            "lpk": "list-presence/tags",
            "puc": "product-data/puc",
        }

        if vocab_name not in options.keys():
            raise KeyError(f"{vocab_name} is invalid Exposure vocabulary name.")

        endpoint = f"{self.KIND}/{options[vocab_name]}"
        info = super(Exposure,self).ctx_call(endpoint=endpoint)
        return ResponseTransformer(info).to_df()

