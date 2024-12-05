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
    Make a Connection with stored API Key in ~/.config/ccte_api/config.toml:
    >>> expo = cte.Chemical()

    Make a Connection by providing an API Key
    >>> expo = cte.Chemical(x_api_key='648a3d70')

    """

    def __init__(self, x_api_key: Optional[str] = None):
        super().__init__(x_api_key=x_api_key)
        self.kind = "chemical/list"

    def get_full_list(self, list_name: str,):
        
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

        word = quote(list_name.upper(), safe="")

        suffix = f"{self.kind}/chemicals/search/by-listname/{word}"
        info = super(ChemicalList, self).get(suffix=suffix)

        return info

    def public_list_names(self):
        ##TODO: there's a lot you can do with this, but I'm keeping it simple for now
        ## 1. Filter list with search string
        ## 2. Return dtxsids associated with the lists
        """
        Return all public lists available from the API service.

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

        suffix = f"{self.kind}/"

        info = super(ChemicalList, self).get(suffix=suffix)

        return [x['listName'] for x in info]