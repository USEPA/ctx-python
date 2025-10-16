from pandas.api.types import is_list_like
from typing import Optional, Iterable

from .base import CTXConnection, ResponseTransformer


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

    KIND = "hazard"

    def __init__(self, x_api_key: Optional[str] = None):
        super().__init__(x_api_key=x_api_key)
        self.batch_size = 200



    def __str__(self):
        if hasattr(self,'data'):
            return self.data
        else:
            return f"CTXConnection.{str.title(self.kind)}"



    def search_toxvaldb(self, by: str, dtxsid: str):
        """
        Search ToxValDb for hazard information for a single chemical.

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


        """

        options = {
            "cancer":"cancer-summary",
            "skin-eye":"skin-eye",
            "all": "toxval",
            "genetox":"genetox/details",
            "genetox-summary":"genetox/summary"
        }
        
        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        endpoint = f"{self.KIND}/{options[by]}/search/by-dtxsid/"
        info = super(Hazard,self).ctx_call(endpoint=endpoint,
                                           query=dtxsid,
                                           batch_size=self.batch_size)

        return ResponseTransformer(info).to_df()



    def search_toxrefdb(self, by: str, domain:str, query: Iterable[str]):
        """
        Search for hazard information for multiple chemicals.

        Retrieve a specific sub-domain of hazard information for a batch of chemical
        identifiers. Chemical identifiers must be DTXSIDs. If only names or CASRNs are
        known, then the ctxpy.Chemical class can be used to search for DTXSIDs.


        Parameters
        ----------
        by : string
            The type of search method to use. Options are "study-type", "study-id", 
            or "dtxsid".
            
        domain: string
            Type of information to search for. Options are "effects", "summary", 
            "data", "observation", or "all".

        query : string
            If `by` is "study-type" then `query` can be "ACU" (acute) "CHR" (chronic), 
            "DEV" (developmental), "DNT" (developmental neurotoxicity), 
            "MGR" (multigenerational reproductive), "NEU" (neurotoxicity), 
            "OTH" (other), "REP" (reproductive), "SAC" (sub-acute), 
            or "SUB" (sub-chronic)

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
        """

        domains = ['effects','summary','data','observations',"all"]
        options = {"study-type":"by-study-type",
                   "dtxsid":"by-dtxsid",
                   "study-id":"by-study-id"}

        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        if domain not in domains:
            raise ValueError(f"Value {domain} is invalid option for argument `domain`.")

        if isinstance(query,int):
            if by != "study-id":
                raise TypeError("`query` is integer type, but domain is not 'study-id'")
            query = str(query)
            
        if (is_list_like(query)) and (by != 'dtxsid'):
            raise NotImplementedError(f"Batch searching is not available for {by}")

        endpoint = f"{self.KIND}/toxref/{domain}/search/{options[by]}/"
        endpoint = endpoint.replace("/all","")

        info = super(Hazard,self).ctx_call(endpoint=endpoint,
                                           query=query,
                                           batch_size=self.batch_size)

        return ResponseTransformer(info).to_df()

    def _search_other(self,other,dtxsid):
        endpoint = f"/{self.KIND}/{other}/search/by-dtxsid/"
        info = super(Hazard,self).ctx_call(endpoint=endpoint, query=dtxsid)
        return ResponseTransformer(info).to_df()

    def search_pprtv(self,dtxsid:str):
        """
        get /hazard/pprtv/search/by-dtxsid/{dtxsid}
        """
        
        return self._search_other(other='pprtv',dtxsid=dtxsid)

    def search_hawc(self,dtxsid:str):
        """
        /hazard/hawc/search/by-dtxsid/{dtxsid}
        """
        return self._search_other(other='hawc',dtxsid=dtxsid)

    def search_iris(self,dtxsid:str):
        """
        /hazard/iris/search/by-dtxsid/{dtxsid}
        """
        return self._search_other(other='iris',dtxsid=dtxsid)

    def search_adme_ivive(self,dtxsid:str):
        """
        /hazard/adme-ivive/search/by-dtxsid/{dtxsid}
        """
        return self._search_other(other='adme-ivive',dtxsid=dtxsid)