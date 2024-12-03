from importlib import resources
from typing import Iterable, Optional, Union
from urllib.parse import quote

from .base import CTXConnection


class Chemical(CTXConnection):
    """
    An API Connection to CCTE's chemical data.

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
    CTXConnection specific to chemical searching endpoints

    See Also
    --------
    ccte_init
    Exposure
    Hazard

    Examples
    --------
    Make a Connection with stored API Key in ~/.config/ccte_api/config.toml:
    >>> chem = ctx.Chemical()

    Make a Connection by providing an API Key
    >>> chem = ctx.Chemical(x_api_key='648a3d70')

    """

    def __init__(self, x_api_key: Optional[str] = None):
        super().__init__(x_api_key=x_api_key)
        self.kind = "chemical"
        self.batch_size = 1000


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
            "batch": "equal",
        }

        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        if by == "batch":
            suffix = f"{self.kind}/search/{options[by]}/"
            
            if (not isinstance(word, Iterable)) or (isinstance(word, str)):
                raise TypeError(
                    "Arugment `by` is 'batch', " "but `word` is not an list-type."
                )

                info = super(Chemical,self).batch(suffix=suffix,
                                                  word=word,
                                                  batch_size=self.batch_size,
                                                  bracketed=False)

                ## Convert to warning
                raise ValueError(
                    "API will not accept more than 200 words at a "
                    "time. Chunk list and resubmit."
                )

            else:
                word = "\n".join([quote(w, safe="") for w in word])

                info = super(Chemical, self).post(suffix=suffix, word=word)

        else:
            word = quote(word, safe="")
            suffix = f"{self.kind}/search/{options[by]}/{word}"

            info = super(Chemical, self).get(suffix=suffix)

        return info

    def details(
        self, by: str, word: Union[str, Iterable[str]], subset: Optional[str] = "all"
    ):
        ## TODO: add exactly what each subset returns
        """
        Get detailed information about chemical(s) via CCTE's APIs.

        Using a DTXSID, DTXCID, or batch list of DTXSIDs, retrieve detailed
        information about chemical identifiers, structures, Mass Spectormetry
        data, physicochemical properties, exposure, toxicity values, and more.


        Parameters
        ----------
        by : string
            The type of search method to use. Options are "dtxsid", "dtxcid",
            or "batch".

        word : string or list-like
            If string, the single chemical identifer (or part of the identifier)
            to search for. If list-like, a list or other iterable of identifiers to 
            search for.

        subset: string (optional)
            If None, then default values are returned from call. If string, then
            one of six valid subsets of data to call. Options are 'default',
            'all','details','identifiers', 'structures', and 'nta'.

        Return
        ------
        dict or list
            a dict containing information for a single chemical or a list of
            dicts containing information for a list of chemicals

        Notes
        -----
        Batch searching only allows for 200 items in a list. For lists of more
        than 200 items, the search will be broken into 200-item chunks with a 3
        second wait between searches. These searches may take longer than
        expected due to this limitation.

        Batch looks only for exact string matches to a chemical identifier.


        Examples
        --------
        Get details for a single DTXSID
        >>> chem.details(by='dtxsid', word='DTXSID7020182')
        {'id': '337693',
         'expocatMedianPrediction': '5.50E-05',
         'expocat': 'Y',
         'nhanes': 'Y',
         'toxvalData': 'Y',
         'waterSolubilityTest': 0.00124451,
         'waterSolubilityOpera': 0.000745153,
         'viscosityCpCpTestPred': 9.66051,
         ...}

        Get details for a single DTXCID

        >>> chem.details(by='dtxcid', word='DTXCID701805')
        {'id': '1742004',
         'expocatMedianPrediction': '1.89E-06',
         'expocat': 'Y',
         'nhanes': None,
         'toxvalData': 'Y',
         'waterSolubilityTest': 0.000129718,
         'waterSolubilityOpera': 0.000346778,
         'viscosityCpCpTestPred': 41.6869,
         ...}

        Get a details for a batch of chemicals:

        >>> chem.details(by='batch', word=['DTXSID7020182','DTXSID3021805'])
        [{'id': '1742004',
          'expocatMedianPrediction': '1.89E-06',
          'expocat': 'Y',
          'nhanes': None,
          'toxvalData': 'Y',
          'waterSolubilityTest': 0.000129718,
          'waterSolubilityOpera': 0.000346778,
          'viscosityCpCpTestPred': 41.6869,
          ...},
         {'id': '337693',
          'expocatMedianPrediction': '5.50E-05',
          'expocat': 'Y',
          'nhanes': 'Y',
          'toxvalData': 'Y',
          'waterSolubilityTest': 0.00124451,
          'waterSolubilityOpera': 0.000745153,
          'viscosityCpCpTestPred': 9.66051,
          ...}]
        """

        by_options = {
            "dtxsid": "by-dtxsid",
            "dtxcid": "by-dtxcid",
            "batch": "by-dtxsid",
        }
        subset_options = {
            "default": None,
            "all": "chemicaldetailall",
            "details": "chemicaldetailstandard",
            "identifiers": "chemicalidentifier",
            "structures": "chemicalstructure",
            "nta": "ntatoolkit",
        }

        if by not in by_options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        if subset not in subset_options.keys():
            raise KeyError(f"Value {subset} is invalid option for argument `subset`.")

        if by == "batch":
            if (not isinstance(word, Iterable)) or (isinstance(word, str)):
                raise TypeError(
                    "Arugment `by` is 'batch', " "but `word` is not an list-type."
                )

            suffix = f"{self.kind}/detail/search/{by_options[by]}/"
            info = super(Chemical,self).batch(suffix=suffix,
                                              word=word,
                                              batch_size=self.batch_size,
                                              bracketed=True)

        else:
            if not isinstance(word, str):
                raise TypeError(
                    f"Argument `by` is {by}, " f"but `word` is not string {word}."
                )

            word = quote(word, safe="")

            if subset is None:
                suffix = f"{self.kind}/detail/search/{by_options[by]}/{word}"
            else:
                suffix = (
                    f"{self.kind}/detail/search/{by_options[by]}/{word}"
                    f"?projection={subset_options[subset]}"
                )

            info = super(Chemical, self).get(suffix=suffix)

        return info

    def msready(
        self,
        by: str,
        word: Optional[str] = None,
        start: Optional[float] = None,
        end: Optional[float] = None,
    ):
        """
        Search for chemical(s) using Mass Spectrometry information via CCTE's
        APIs.

        Search for chemicals that match a Mass Spectral structure (via DTXCID),
        a range of atomic mass (mass-range), or a specific molecular formula.


        Parameters
        ----------
        by : string
            The type of search method to use. Options are "dtxcid", "mass-range",
            or "formula". "dtxcid" option returns all mixtures, compenents, and 
            isotopes of the chemical structure. "mass-range" returns all chemicals that
            exist within the specific monoisotopic mass range. "formula" returns all
            chemicals having that molecular formula.

        word : Optional[string]
            If string, the single chemical identifer (or part of the identifier)
            to search for. If no string is supplied, searching by mass-range is
            assumed

        start : Optional[float]
            lower bound molecular mass for search

        end : Optional[float]
            upper bound molecular mass for search

        Return
        ------
        list
            a list of dicts with each dict being a match to supplied a chemical
            identifier

        Examples
        --------
        Search for chemical(s) by DTXCID:

        >>> chem.msready(by='dtxcid',word='DTXCID30182')

        ['DTXSID0027480',
         'DTXSID00584370',
         'DTXSID10675703',
         'DTXSID10724048',
         'DTXSID10741891',
         ...]


        Search for chemical(s) by molecular formula:

        >>> chem.msready(by='formula', word='C17H19NO3')
        ['DTXSID001016149',
         'DTXSID001165714',
         'DTXSID001178945',
         'DTXSID001229530',
         'DTXSID001244732',
         ...]

        Search for chemical(s) by mass range:

        >>> chem.msready(by='mass', start=200.9, end=200.93)

        ['DTXSID101263341',
         'DTXSID10355992',
         'DTXSID10441723',
         'DTXSID10621205',
         'DTXSID40543643',
         ...]
        """

        if (word is None) and (by != "mass"):
            raise ValueError("No search term provided to `word` argument.")

        if ((start is None) or (end is None)) and (by == "mass"):
            raise ValueError(
                "Searching by mass range, but no mass values "
                "provided start and end of range."
            )

        options = {
            "dtxcid": "by-dtxcid",
            "mass": "by-mass",
            "formula": "by-formula",
        }

        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        if by == "mass":
            if (start is None) or (end is None):
                raise ValueError(
                    "Argument `by` is 'mass', but no `start` or "
                    "`end` mass values are provided."
                )

            word = f"{start}/{end}"
            suffix = f"{self.kind}/msready/search/{options[by]}/{word}"

        else:
            word = quote(word, safe="")
            suffix = f"{self.kind}/msready/search/{options[by]}/{word}"

            if not isinstance(word, str):
                raise TypeError(f"Argument `by` is {by}, " "but `word` is not string.")

        ## TODO: test that this works for mass -- does safe quote mess
        ## with the floats?
        word = quote(word, safe="")

        info = super(Chemical, self).get(suffix=suffix)

        return info
