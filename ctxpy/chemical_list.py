from importlib import resources
from typing import Iterable, Optional, Union
from urllib.parse import quote

from .base import Connection
from .utils import chunker


class ChemicalList(Connection):
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

    @classmethod
    def baby_search(cls, by: str, word: Union[str, Iterable[str]]):
        options = {
            "starts-with": "start-with",
            "equals": "equal",
            "contains": "contain",
            "batch": "equal",
        }
        word = quote(word, safe="")
        suffix = f"{cls.kind}/search/{options[by]}/{word}"

        info = super(ChemicalList, cls).get(suffix=suffix)
        return info

    def search(self, by: str, word: Union[str, Iterable[str]]):
        """
        Search for chemical(s) using chemical identifiers via CCTE's APIs.

        Search for 1) a single chemical by chemical identifiers by the
        beinging of the identifier, the exact identifier, or a sub-string
        of the identifier or 2) a batch of chemical identifiers. Chemical
        identifiers can be chemical names, CAS-RNs, DTXSID, etc. that are used
        to distinguish one chemical substance from another.


        Parameters
        ----------
        by : string
            The type of search method to use. Options are "equals", "contains",
            "starts-with", or "type".

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

        >>> chem.search(by='equals',word='toluene')

        [{'dtxsid': 'DTXSID7021360',
          'dtxcid': 'DTXCID501360',
          'casrn': '108-88-3',
          'preferredName': 'Toluene',
          'searchName': 'Approved Name',
          'searchValue': 'Toluene',
          'rank': 9,
          'hasStructureImage': 1,
          'smiles': 'CC1=CC=CC=C1',
          'isMarkush': False}]

        >>> chem.search(by='starts-with',word='atra')

        [{'dtxsid': 'DTXSID7021239',
          'dtxcid': 'DTXCID001239',
          'casrn': '302-79-4',
          'preferredName': 'Retinoic acid',
          'searchName': 'Synonym',
          'searchValue': 'ATRA',
          'rank': 15,
          'hasStructureImage': 1,
          'smiles': 'C\\C(\\C=C\\C1=C(C)CCCC1(C)C)=C/C=C/C(/C)=C/C(O)=O',
          'isMarkush': False},
         {'dtxsid': 'DTXSID801046158',
          'dtxcid': None,
          'casrn': '193981-10-1',
          'preferredName': 'Atracotoxin, omega- (Hadronyche versuta)',
          'searchName': 'Approved Name',
          'searchValue': 'Atracotoxin, omega- (Hadronyche versuta)',
          'rank': 9,
          'hasStructureImage': 0,
          'smiles': None,
          'isMarkush': True},
          ...]

        >>> chem.search(by='contains',word='-00-')
        [{'dtxsid': 'DTXSID001000057',
          'dtxcid': 'DTXCID001427025',
          'casrn': '78812-00-7',
          'preferredName': 'N-[(2-Methylquinolin-4-yl)methyl]guanidine--hydrogen chloride (1/1)',
          'searchName': 'CASRN',
          'searchValue': '78812-00-7',
          'rank': 5,
          'hasStructureImage': 1,
          'smiles': 'Cl.CC1=NC2=CC=CC=C2C(CNC(N)=N)=C1',
          'isMarkush': False},
         {'dtxsid': 'DTXSID001002558',
          'dtxcid': None,
          'casrn': '82209-00-5',
          'preferredName': 'Captan-metalaxyl mixt.',
          'searchName': 'CASRN',
          'searchValue': '82209-00-5',
          'rank': 5,
          'hasStructureImage': 0,
          'smiles': None,
          'isMarkush': True},
          ...]

        >>> chem.search(by='batch',word=['50-00-0','BPA'])
        [{'dtxsid': 'DTXSID7020637',
          'dtxcid': 'DTXCID30637',
          'casrn': '50-00-0',
          'smiles': 'C=O',
          'preferredName': 'Formaldehyde',
          'searchName': 'CASRN',
          'searchValue': '50-00-0',
          'rank': 5,
          'hasStructureImage': 1,
          'isMarkush': False,
          'searchMsgs': None,
          'suggestions': None,
          'isDuplicate': False},
         {'dtxsid': 'DTXSID7020182',
          'dtxcid': 'DTXCID30182',
          'casrn': '80-05-7',
          'smiles': 'CC(C)(C1=CC=C(O)C=C1)C1=CC=C(O)C=C1',
          'preferredName': 'Bisphenol A',
          'searchName': 'Synonym',
          'searchValue': 'BPA',
          'rank': 15,
          'hasStructureImage': 1,
          'isMarkush': False,
          'searchMsgs': None,
          'suggestions': None,
          'isDuplicate': False}]
        """

        options = {
            "starts-with": "start-with",
            "equals": "equal",
            "contains": "contain",
            "by-type": "equal",
        }

        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        if by == "batch":
            if (not isinstance(word, Iterable)) or (isinstance(word, str)):
                raise TypeError(
                    "Arugment `by` is 'batch', " "but `word` is not an list-type."
                )
            ## API only handles 200 at a time.
            if len(word) > 200:
                chunks = []
                for chunk in chunker(word, 200):
                    word = "\n".join([quote(w, safe="") for w in word])

                    ## TODO: Check that suffix is re-written on each loop,
                    ## not appended to
                    suffix = f"{self.kind}/search/{options[by]}/"
                    chunks.append(super(ChemicalList, self).post(suffix = suffix, word=word))

                ## Convert to warning
                raise ValueError(
                    "API will not accept more than 200 words at a "
                    "time. Chunk list and resubmit."
                )

            else:
                word = "\n".join([quote(w, safe="") for w in word])

                suffix = f"{self.kind}/search/{options[by]}/"

                info = super(ChemicalList, self).post(suffix=suffix, word=word)

        else:
            word = quote(word, safe="")
            suffix = f"{self.kind}/search/{options[by]}/{word}"

            info = super(ChemicalList, self).get(suffix=suffix)

        return info

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

        word = quote(list_name, safe="")

        suffix = f"{self.kind}/chemicals/search/by-listname/{word}"
        info = super(ChemicalList, self).get(word=word, suffix=suffix)

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

        return info