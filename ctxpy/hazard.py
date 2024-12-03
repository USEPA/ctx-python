import pandas as pd
from pandas.api.types import is_list_like
from typing import Optional, Iterable
from urllib.parse import quote
from time import sleep

from .base import CTXConnection
from .utils import chunker


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

        Search for 1) a single chemical by chemical identifiers by the
        beinging of the identifier, the exact identifier, or a sub-string
        of the identifier or 2) a batch of chemical identifiers. Chemical
        identifiers can be chemical names, CAS-RNs, DTXSID, etc. that are used
        to distinguish one chemical substance from another.


        Parameters
        ----------
        by : string
            The type of search method to use. Options are "equals", "contains",
            "starts-with", or "batch".

        word : string or list-like
            If string, the single chemical identifer (or part of the identifier)
            to search for. If list-list, a list or other iterable of identifiers to 
            search for.

        Return
        ------
        list
            a list of dicts with each dict being a match to supplied a chemical
            identifier

        Notes
        -----
        Batch searching only allows for 200 items in a list. For lists of more
        than 200 items, the search will be broken into 200-item chunks with a 3
        second wait between searches. These searches may take longer than
        expected due to this limitation.

        Batch looks only for exact string matches to a chemical identifier.


        Examples
        --------

        Search for a chemical by name:

        >>> haz.search(by='all',dtxsid='DTXSID7021360')

        

        >>> haz.search(by='human',dtxsid='DTXSID7021360')

        

        >>> haz.search(by='eco',dtxsid='DTXSID7021360')

        

        >>> haz.search(by='skin-eye',dtxsid='DTXSID7021360')

        

        >>> haz.search(by='cancer',dtxsid='DTXSID7021360')

        

        >>> haz.search(by='genetox',dtxsid='DTXSID7021360')

        

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
            The type of search method to use. Options are "equals", "contains",
            "starts-with", or "batch".

        dtxsid : list-like
            A list or other iterable of DTXSIDs to search for.

        Return
        ------
        list
            a list of dicts with each dict being a match to supplied a chemical
            identifier

        Notes
        -----
        Batch searching only allows for 200 items in a list. For lists of more
        than 200 items, the search will be broken into 200-item chunks with a 3
        second wait between searches. These searches may take longer than
        expected due to this limitation.


        Examples
        --------

        Search for a chemical by name:

        >>> haz.batch_search(by='all',dtxsid='DTXSID7021360')

        

        >>> haz.batch_search(by='human',dtxsid='DTXSID7021360')

        

        >>> haz.batch_search(by='eco',dtxsid='DTXSID7021360')

        

        >>> haz.batch_search(by='skin-eye',dtxsid='DTXSID7021360')

        

        >>> haz.batch_search(by='cancer',dtxsid='DTXSID7021360')

        

        >>> haz.batch_search(by='genetox',dtxsid='DTXSID7021360')

        

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
