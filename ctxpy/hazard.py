import pandas as pd
from pandas.api.types import is_list_like
from typing import Optional, Iterable
from urllib.parse import quote

from .base import CTXConnection


class Hazard(CTXConnection):
    """
    An API Connection to CCTE's hazard data.

    Connection allows users to search for .

    Parameters
    ----------
    x_api_key : Optional[str]
        A personal key for using CCTE's APIs, if left blank, it assumes a key is
        already stored in ~/.config/ccte_api/config.toml

    Returns
    -------
    CTXConnection specific to hazard endpoints

    See Also
    --------
    ccte_init
    Chemical
    Exposure

    Examples
    --------
    Make a Connection with stored API Key in ~/.config/ccte_api/config.toml:
    >>> haz = ctx.Hazard()

    Make a Connection by providing an API Key
    >>> haz = ctx.Hazard(x_api_key='648a3d70')

    """

    def __init__(self, x_api_key: Optional[str] = None):
        super().__init__(x_api_key=x_api_key)
        self.kind = "hazard"
        self.batch_size = 200



    def __str__(self):
        if hasattr(self,'data'):
            return self.data
        else:
            return f"CTXConnection.{str.title(self.kind)}"



    def search(self, by: str, dtxsid: str, summary:bool=True):
        """
        Search for hazard information for a single chemical.

        Retrieve a specific sub-domain of hazard information (from EPA's ToxValDB and 
        other hazard resources) for a DTXSID identifier. If only the chemical name or 
        CASRN is known, then the ctxpy.Chemical class can be used to search for DTXSIDs.


        Parameters
        ----------
        by : string
            The type of search method to use. Options are "all", "human", "eco", 
            "skin-eye", "cancer", or "genetox".

        dtxsid : string
            A valid DSSTox Substance Identifier (DTXSID)
            
        summary: bool
            If `by` is genetox, this determines whether summary or detailed information 
            about a chemical's genetic toxicity is returned.

        Return
        ------
        pandas DataFrame
            contains requested hazard data from specified API endpoints


        Examples
        --------

        Search for all ToxValDB information for a chemical:
        >>> haz.search(by='all',dtxsid='DTXSID7021360')

               id  year       source         dtxsid  ... humanEcoNt
        0  718311  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        1  718313  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        2  718131  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        3  718198  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        4  717897  <NA>  DOE ECORISK  DTXSID7021360  ...        eco

        Search for a chemical's ToxValDB human information:
        >>> haz.search(by='human',dtxsid='DTXSID7021360')

               id  year           source         dtxsid exposureRoute  ...    humanEcoNt
        0  374062  <NA>       Alaska DEC  DTXSID7021360        dermal  ...  human health
        1  378344  <NA>       Alaska DEC  DTXSID7021360    inhalation  ...  human health
        2  377820  <NA>       Alaska DEC  DTXSID7021360    inhalation  ...  human health
        3  374756  <NA>       Alaska DEC  DTXSID7021360          oral  ...  human health
        4  251049  2017  ATSDR MRLs 2020  DTXSID7021360    inhalation  ...  human health

        Search for a chemical's ToxValDB ecological information:
        >>> haz.search(by='eco',dtxsid='DTXSID7021360')

               id  year       source         dtxsid  ... humanEcoNt
        0  718131  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        1  718313  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        2  718311  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        3  718198  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        4  717897  <NA>  DOE ECORISK  DTXSID7021360  ...        eco

        Search for a chemical's skin/eye sensitization information :
        >>> haz.search(by='skin-eye',dtxsid='DTXSID7021360')

              id  year            source                 endpoint  ...            strain
        0  24214    -1             Japan       Skin Sensitization  ...              <NA>
        1  24213    -1             Japan          Skin Irritation  ...              <NA>
        2  22350    -1            Canada          Skin Irritation  ...              <NA>
        3    518    -1          ECHA CLP          Skin Irritation  ...              <NA>
        4  91325  1982  ECHA eChemPortal  eye irritation: in vivo  ... New Zealand White

        Search for a chemical's cancer hazard information:
        >>> haz.search(by='cancer',dtxsid='DTXSID701015778')

             id   source  ...           dtxsid exposureRoute
        0  2062     IARC  ...  DTXSID701015778          <NA>
        1  2063  NTP RoC  ...  DTXSID701015778          <NA>

        Search for a chemical's summary genetic toxicity data:
        >>> haz.search(by='genetox',dtxsid='DTXSID7021360')

               id         dtxsid  reportsPositive ...  ames micronucleus
        0  518845  DTXSID7021360                2 ...  <NA>     positive

        Search for a chemicals's detailed genetic toxicity data:
        >>> haz.search(by='genetox',dtxsid='DTXSID7021360',summary=False)

                id    year       source         dtxsid  ...  strain
        0  1186322  1981.0  eChemPortal  DTXSID7021360  ...    <NA>
        1  1186321  1983.0  eChemPortal  DTXSID7021360  ...    <NA>
        2  1186323  1978.0  eChemPortal  DTXSID7021360  ...    <NA>
        3  1186324  1981.0  eChemPortal  DTXSID7021360  ...    CD-1
        4  1186325     NaN          NTP  DTXSID7021360  ...    <NA>
        """

        options = {
            "all": None,
            "human": "human",
            "eco": "eco",
            "skin-eye":"skin-eye",
            "cancer":"cancer-summary",
            "genetox":"genetox",
        }

        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        if by == "all":
            suffix = f"{self.kind}/search/by-dtxsid/{dtxsid}"
        elif by == "genetox":
            if summary:
                suffix = f"{self.kind}/{options[by]}/summary/search/by-dtxsid/{dtxsid}"
            else:
                suffix = f"{self.kind}/{options[by]}/details/search/by-dtxsid/{dtxsid}"
        else:
            suffix = f"{self.kind}/{options[by]}/search/by-dtxsid/{dtxsid}"


        if (not isinstance(dtxsid,str)):
            raise TypeError("`dtxsid` is not string.")

        
        dtxsid = quote(dtxsid, safe="")
        info = super(Hazard, self).get(suffix=suffix)

        return pd.DataFrame(info).fillna(pd.NA).replace({"-":pd.NA})



    def batch_search(self, by: str, dtxsid: Iterable[str],summary:bool=True):
        """
        Search for hazard information for multiple chemicals.

        Retrieve a specific sub-domain of hazard information for a batch of chemical
        identifiers. Chemical identifiers must be DTXSIDs. If only names or CASRNs are
        known, then the ctxpy.Chemical class can be used to search for DTXSIDs.


        Parameters
        ----------
        by : string
            The type of search method to use. Options are "all", "human", "eco", 
            "skin-eye", "cancer", or "genetox".

        dtxsid : string
            A valid DSSTox Substance Identifier (DTXSID)
            
        summary: bool
            If `by` is genetox, this determines whether summary or detailed information 
            about a chemical's genetic toxicity is returned.

        Return
        ------
        pandas DataFrame
            contains requested hazard data from specified API endpoints


        Examples
        --------

        Search for all ToxValDB information for chemicals:
        >>> haz.batch_search(by='all',dtxsid=["DTXSID7021360","DTXSID2021868"])

               id  year       source         dtxsid  ... humanEcoNt
        0  718311  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        1  718313  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        2  718131  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        3  718198  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        4  717897  <NA>  DOE ECORISK  DTXSID7021360  ...        eco

        Search for chemicals' ToxValDB human information:
        >>> haz.batch_search(by='human',dtxsid=["DTXSID7021360","DTXSID2021868"])

               id  year           source         dtxsid exposureRoute  ...    humanEcoNt
        0  374062  <NA>       Alaska DEC  DTXSID7021360        dermal  ...  human health
        1  378344  <NA>       Alaska DEC  DTXSID7021360    inhalation  ...  human health
        2  377820  <NA>       Alaska DEC  DTXSID7021360    inhalation  ...  human health
        3  374756  <NA>       Alaska DEC  DTXSID7021360          oral  ...  human health
        4  251049  2017  ATSDR MRLs 2020  DTXSID7021360    inhalation  ...  human health

        Search for chemicals' ToxValDB ecological information:
        >>> haz.batch_search(by='eco',dtxsid=["DTXSID7021360","DTXSID2021868"])

               id  year       source         dtxsid  ... humanEcoNt
        0  718131  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        1  718313  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        2  718311  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        3  718198  <NA>  DOE ECORISK  DTXSID7021360  ...        eco
        4  717897  <NA>  DOE ECORISK  DTXSID7021360  ...        eco

        Search for chemicals' skin/eye sensitization information :
        >>> haz.batch_search(by='skin-eye',dtxsid=["DTXSID7021360","DTXSID2021868"])

              id  year            source                 endpoint  ...            strain
        0  24214    -1             Japan       Skin Sensitization  ...              <NA>
        1  24213    -1             Japan          Skin Irritation  ...              <NA>
        2  22350    -1            Canada          Skin Irritation  ...              <NA>
        3    518    -1          ECHA CLP          Skin Irritation  ...              <NA>
        4  91325  1982  ECHA eChemPortal  eye irritation: in vivo  ... New Zealand White

        Search for chemicals' cancer hazard information:
        >>> haz.batch_search(by='cancer',dtxsid=["DTXSID701015778","DTXSID3039242"])

             id         source  ...         dtxsid exposureRoute
        0  1142         CalEPA  ...  DTXSID3039242          <NA>
        1  1143        EPA OPP  ...  DTXSID3039242          <NA>
        2  1144  Health Canada  ...  DTXSID3039242    inhalation
        3  1145  Health Canada  ...  DTXSID3039242  oral: gavage
        4  1146           IARC  ...  DTXSID3039242          <NA>

        Search for a chemical's summary genetic toxicity data:
        >>> haz.batch_search(by='genetox',dtxsid=["DTXSID7021360","DTXSID2021868"])

               id         dtxsid  reportsPositive  ...  ames micronucleus
        0  518659  DTXSID2021868                0  ...  <NA>     negative
        1  518845  DTXSID7021360                2  ...  <NA>     positive

        Search for a chemical's detailed genetic toxicity data:
        >>> haz.batch_search(by='genetox',dtxsid=["DTXSID7021360","DTXSID2021868"],
                             summary=False)
                 id    year       source         dtxsid  ...  assayResult       strain
        0   1184853  1985.0  eChemPortal  DTXSID2021868  ...     negative         <NA>
        1   1184843  1981.0  eChemPortal  DTXSID2021868  ...     negative         <NA>
        2   1184846  1980.0  eChemPortal  DTXSID2021868  ...     negative         <NA>
        3   1184845  1978.0  eChemPortal  DTXSID2021868  ...     negative         <NA>
        4   1184842  1983.0  eChemPortal  DTXSID2021868  ...     negative         <NA>
        """

        options = {
            "all": None,
            "human": "human",
            "eco": "eco",
            "skin-eye":"skin-eye",
            "cancer":"cancer-summary",
            "genetox":"genetox",
        }

        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        if by == "all":
            suffix = f"{self.kind}/search/by-dtxsid/"
        elif by == "genetox":
            if summary:
                suffix = f"{self.kind}/{options[by]}/summary/search/by-dtxsid/"
            else:
                suffix = f"{self.kind}/{options[by]}/details/search/by-dtxsid/"
        else:
            suffix = f"{self.kind}/{options[by]}/search/by-dtxsid/"

        if (not is_list_like(dtxsid)):
            raise TypeError(
                "`dtxsid` is not list-like for batch searching,"
            )

        info = super(Hazard,self).batch(suffix=suffix,
                                        word=dtxsid,
                                        batch_size=self.batch_size,
                                        bracketed=True)

        return pd.DataFrame(info).fillna(pd.NA).replace({"-":pd.NA})
