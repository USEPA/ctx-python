from typing import Optional
from urllib.parse import quote

from .base import CTXConnection


class ChemicalList(CTXConnection):
    """
    An API Connection to CCTE's chemical list data.

    Connection allows for 1) search for chemical(s) by names or other chemical
    identifiers, 2) search for chemical(s) via Mass Spectrometry ready
    properties, and 3) retreiving details about chemical(s) via DTXSID(s).

    Parameters
    ----------
    x_api_key : Optional[str]
        A personal key for using CCTE's APIs, if left blank, it assumes a key is
        already stored in ~/.config/ccte_api/config.toml

    Returns
    -------
    CCTE API Connection

    See Also
    --------
    ccte_init
    Exposure

    Examples
    --------
    Make a Connection with stored API Key in ~/.env:
    >>> clist = ctxpy.ChemicalList()

    Make a Connection by providing an API Key
    >>> clist = ctxpy.ChemicalList(x_api_key='648a3d70')

    """

    KIND = "chemical/list"

    def __init__(self, x_api_key: Optional[str] = None):
        super().__init__(x_api_key=x_api_key)

    def get_list_types(self):
        return super(ChemicalList, self).ctx_call(endpoint=f'{self.KIND}/type')

    def get_all_list_meta(self, output: Optional[str]=None):
        """
        Return names of all public lists available from the API service.

        Return
        ------
        list
            a list of dicts with each dict being a match to supplied a chemical
            identifier

        Examples
        --------
        Search for chemical(s) by DTXCID:

        >>> chemlist.public_list_names()

        """

        output_options = {"all":'chemicallistall',
                          "dtxsid":"chemicallistwithdtxsids",
                          "list-name":"chemicallistname",
                          "details":"ccdchemicaldetaillists"}
        ## HACK
        ## FIXME
        ## as of 10/15/2025 'details' option does not elict repsonse. Pop it now,
        ## and test it next time to see if it works
        output_options.pop('details')
        
        if output is None:
            output = "all"
        if output not in output_options.keys():
            raise KeyError(f"'output' option of `{output}` is not valid.")
        endpoint = f"{self.KIND}/"
        params = {"projection":output_options[output]}
        info = super(ChemicalList, self).ctx_call(endpoint=endpoint,
                                                  params=params)
        return info



    def get_list_meta_by_type(self, list_type:str, output: Optional[str]=None):
        output_options = {"all":'chemicallistall',
                          "dtxsid":"chemicallistwithdtxsids",
                          "list-name":"chemicallistname",
                          "details":"ccdchemicaldetaillists"}
        ## HACK
        ## FIXME
        ## as of 10/15/2025 'details' option does not elict repsonse. Pop it now,
        ## and test it next time to see if it works
        output_options.pop('details')
        if output is None:
            output = "all"
        if output not in output_options.keys():
            raise KeyError(f"'output' option of `{output}` is not valid.")
        endpoint = f'{self.KIND}/search/by-type/'
        params = {"projection":output_options[output]}
        info = super(ChemicalList, self).ctx_call(endpoint=endpoint,
                                                 query=list_type,
                                                 params=params)
        return info

    def get_list_meta_by_name(self, list_name:str, output: Optional[str]=None):
        output_options = {"all":'chemicallistall',
                          "dtxsid":"chemicallistwithdtxsids",
                          "list-name":"chemicallistname",
                          "details":"ccdchemicaldetaillists"}
        if output is None:
            output = 'all'
        if output not in output_options.keys():
            raise KeyError(f"'output' option of `{output}` is not valid.")
        endpoint = f'{self.KIND}/search/by-name/'
        params = {"projection":output_options[output]}
        info = super(ChemicalList, self).ctx_call(endpoint=endpoint,
                                                 query=list_name,
                                                 params=params)
        return info

    
    def _join_query(query: dict):
        query = {k:quote(v, safe="") for k,v in query.items()}
        return f"{query['list']}/{query['word']}"

    def filter_list_by_chemicals(self, list_name:str, chem_filter:str, how:str):

        options = {"contains":"contain",
                   "equals":"equal",
                   "starts-with":"start-with"}
        if how not in options.keys():
            raise KeyError(f"'how' value of `{how}` not a valid option.")
        query = {"list":list_name, "word": chem_filter}
        endpoint = f"{self.KIND}/chemicals/search/{options[how]}/"
        info = super(ChemicalList, self).ctx_call(endpoint=endpoint,
                                                  query=query,
                                                  quote_method=self._join_query)
        return info


    def get_list(self, list_name: str,):
        
        """
        Returns list of DTXSIDs for chemicals on the provided list.

        Provides the entire list of DTXSIDs for named lists found on the U.S. EPA's
        CompTox Chemicals Dashboard. For help with finding a list, use the
        `public_list_names` function.

        Parameters
        ----------
        list_name : string
            The name of the chemical list for which to retrieve DTXSIDs. 

        Return
        ------
        dict or list
            list of DTXSIDs

        Examples
        --------
        Get details for a single DTXSID
        >>> chemlist.get_full_list(list_name="FDAFOODSUBS")

        """

        endpoint = f"{self.KIND}/chemicals/search/by-listname/"
        info = super(ChemicalList, self).ctx_call(endpoint=endpoint,query=list_name)

        return info

    