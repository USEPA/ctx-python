from typing import Optional
from urllib.parse import quote
from time import sleep

import pandas as pd
from pandas.api.types import is_list_like

from .base import CTXConnection


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

    def __init__(self, x_api_key: Optional[str] = None):
        super().__init__(x_api_key=x_api_key)
        self.kind = "exposure"


    def _search(self, by: str, word: Optional[str] = None):
        """

        """
        if word is not None:
            word = quote(word, safe="")
            suffix = f"{self.kind}/{by}/{word}"
        else:
            suffix = f"{self.kind}/{by}"

        info = pd.DataFrame(super(Exposure, self).get(suffix=suffix))

        return info.fillna(pd.NA).replace("-",pd.NA).replace("",pd.NA)

    def _batch(self,by,words,insert_id=False):
        ## TODO: when post is added to exposure endpoints replace this with
        ## `super().batch()`
        info = []
        for word in words:
            word = quote(word, safe="")
            df = self._search(by=by,word=word)
            if insert_id:
                df.insert(loc=0,column='dtxsid',value=word)
            info.append(df)
            sleep(0.1)

        info = pd.concat(info,ignore_index=True)
        return info

    def search_cpdat(self, vocab_name, dtxsid):
        """
        Search for a DTXSID's categorization within a specified CPDat vocabulary.

        For a single chemical, search for 1) reported functional uses,
        2) predicted functional uses, 3) product that report this chemical as an
        ingredient, or 4) annotated lists of chemicals that contain this
        chemical.

        Parameters
        ----------
        vocab_name : string
            The type of search method to use. Options are "fc", "qsur",
            "puc", or "lpk". "fc" is reported functional use, "qsur" is
            predicted functional use, "puc" is product information, and "lpk" is
            chemical list presence information.

        dtxsid : string or list-like
            If string, the single chemical identifer (or part of the identifier)
            to search for. If list-like, a list or tuple of identifiers to search
            for.

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

        ## Make sure its a list-like objects of strings
        if is_list_like(dtxsid):
            info = self._batch(by=options[vocab_name],words=dtxsid)
        elif isinstance(dtxsid,str):
            dtxsid = quote(dtxsid, safe="")
            info = self._search(by=options[vocab_name],word=dtxsid)
        else:
            raise TypeError("`dtxsid` must either be string or list-like of strings.")

        return info



    def search_qsurs(self, dtxsid):
        """
        Search for Quantitative Structure-Use Relationship (QSUR) predictions by DTXSID.

        For a single chemical, search for 1) consensus, general population exposure 
        estimate using the SEEM 3 Framework or 2) component model predictions that make
        up the consensus SEEM 3 estimate.

        Parameters
        ----------
        dtxsid : string
            If string, the single chemical identifer (or part of the identifier)
            to search for. If iterable, a list or tuple of identifiers to search
            for.

        Return
        ------
        pandas DataFrame
            DataFrame containing the chemical identifier, harmonized functional use, and
            probability of the chemical having that use for each "in domain" prediction
            of a model.

        Examples
        --------
        Search for predicted functional uses:
        
        >>> expo.search_qsurs(dtxsid='DTXSID7020182')

           harmonizedFunctionalUse  probability
        0            antimicrobial       0.3722
        1              antioxidant       0.8941
        2                 catalyst       0.2031
        3                 colorant       0.1560
        4              crosslinker       0.7743
        5          flame_retardant       0.2208

        """
        endpoint = "functional-use/probability/search/by-dtxsid"
        
        ## Make sure its a list-like objects of strings
        if is_list_like(dtxsid):
            info = self._batch(by=endpoint,words=dtxsid,insert_id=True)
        elif isinstance(dtxsid,str):
            dtxsid = quote(dtxsid, safe="")
            info = self._search(by=endpoint,word=dtxsid)
        else:
            raise TypeError("`dtxsid` must either be string or list-like of strings.")

        return info


    def search_exposures(self, by, dtxsid):
        """
        Search for exposure estimates by DTXSID.

        For a single chemical, search for 1) exposure estimates for a chemical based on
        the SEEM 3 framework published in Ring 2018 or 2) exposure pathway predictions 
        that are sourced from pathway prediction models (also published in Ring 2018).

        Parameters
        ----------
        by : string
            The type of search method to use. Options are "pathways" or "seem".
            The "pathways" argument option returns the probability of exposure occuring
            along four exposure pathways defined in Ring 2018 (dietary, consumer, 
            far-field pesticide source, and far-field industrial source); information is
            also provided on the reported production volume from the 2015 Chemical Data
            Reporting cycle in the U.S. as well as the Stockholm Convention for
            Persistent Organic Pollutants list. These two sources were crucial inputs
            for predicting exposure pathways.
            "seem" returns the different model predictions that lead to the "consensus"
            estimate.

        dtxsid : string
            A DSSTox Substance Identifier that is used for search for a specific
            chemical.

        Return
        ------
        list
            a list of dicts with each dict being a reported value -- controlled
            vocabulary pair along with information about the reporting document


        Examples
        --------
        Search for consensus model inputs into seem
        >>> expo.search_exposures(by="consensus",dtxsid="DTXSID7020182")

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

        """

        options = {
            "pathways": "seem/general/search/by-dtxsid",
            "seem": "seem/demographic/search/by-dtxsid"
        }
        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        ## Make sure its a list-like objects of strings
        if is_list_like(dtxsid):
            info = self._batch(by=options[by],words=dtxsid)
        elif isinstance(dtxsid,str):
            dtxsid = quote(dtxsid, safe="")
            info = self._search(by=options[by],word=dtxsid)
        else:
            raise TypeError("`dtxsid` must either be string or list-like of strings.")

        return info


    def search_httk(self, dtxsid):
        """
        Search for High-Throughput Toxicokinetics data by DTXSID.

        
        Parameters
        ----------
        dtxsid : string
            If string, the single chemical identifer (or part of the identifier)
            to search for. If iterable, a list or tuple of identifiers to search
            for.

        Return
        ------
        list
            a list of dicts with each dict being a reported value -- controlled
            vocabulary pair along with information about the reporting document


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
        
        endpoint = "httk/search/by-dtxsid"
        ## Make sure its a list-like objects of strings
        if is_list_like(dtxsid):
            info = self._batch(by=endpoint,words=dtxsid,insert_id=False)
        elif isinstance(dtxsid,str):
            dtxsid = quote(dtxsid, safe="")
            info = self._search(by=endpoint,word=dtxsid)
        else:
            raise TypeError("`dtxsid` must either be string or list-like of strings.")

        return info

    def get_cpdat_vocabulary(self, vocab_name):
        """
        Search for a type of exposure information using a DTXSID.

        Retrieve the entire controlled vocabulary (with definintions) for 1) function
        categories (FCs), 2) product categories (puc), or 3) list presence keywords
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

        return self._search(by=options[vocab_name],)

