import pandas as pd
from typing import Optional
from urllib.parse import quote

from .base import Connection


class Exposure(Connection):
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
    CCTE API Connection

    See Also
    --------
    ccte_init
    Chemical

    Examples
    --------
    Make a Connection with stored API Key in ~/.config/ccte_api/config.toml:
    >>> expo = cte.Exposure()

    Make a Connection by providing an API Key
    >>> expo = cte.Exposure(x_api_key='648a3d70')

    """

    def __init__(self, x_api_key: Optional[str] = None):
        super().__init__(x_api_key=x_api_key)
        self.kind = "exposure"
        
    # def __repr__(self):
        
    def __str__(self):
        if hasattr(self,'data'):
            return self.data
        else:
            return f"Connection.{str.title(self.kind)}"

    def search(self, by, word):
        """
        Search for a type of exposure information using a DTXSID.

        For a single chemical, search for 1) reported functional uses,
        2) predicted functional uses, 3) product that report this chemical as an
        ingredient, or 4) annotated lists of chemicals that contain this
        chemical.

        Parameters
        ----------
        by : string
            The type of search method to use. Options are "fc", "qsur",
            "puc", or "lpk". "fc" is reported functional use, "qsur" is
            predicted functional use, "puc" is product information, and "lpk" is
            chemical list presence information.

        word : string
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
        >>> expo.search(by="fc",word="DTXSID7020182")
        [{'id': 22724,
          'dtxsid': 'DTXSID7020182',
          'datatype': 'Chemical presence list',
          'docid': 1371471,
          'doctitle': 'The 25 Chemicals Found in All Nine of the Biosolids Studied',
          'docdate': '',
          'reportedfunction': 'fire retardant',
          'functioncategory': 'Flame retardant'},
         ...]

        Search for predicted functional uses:

        >>> expo.search(by='qsur',word='DTXSID7020182')

        [{'probability': 0.3722,
          'harmonizedFunctionalUse': 'antimicrobial'},
         {'probability': 0.8941,
         'harmonizedFunctionalUse': 'antioxidant'},
         {'probability': 0.2031,
         'harmonizedFunctionalUse': 'catalyst'},
         ...]

        Search for product information

        >>> expo.search(by='puc',word='DTXSID7020182')

        [{'id': 657348,
          'dtxsid': 'DTXSID7020182',
          'docid': 1314861,
          'doctitle': 'EPOCAST 87005 B-80, FPC2248',
          'docdate': '08/04/1992',
          'productname': 'epocast 87005 b-80_ fpc2248',
          'gencat': 'Raw materials',
          'prodfam': 'adhesives',
          'prodtype': '',
          'classificationmethod': 'Manual',
          'rawmincomp': '',
          'rawmaxcomp': '',
          'rawcentralcomp': ' 2',
          'unittype': 'percent',
          'lowerweightfraction': None,
          'upperweightfraction': None,
          'centralweightfraction': 0.02,
          'weightfractiontype': 'reported',
          'component': ''},
         ...]

        >>> expo.search(by='lpk', word='DTXSID7020182')

        [{'id': 127967,
          'dtxsid': 'DTXSID7020182',
          'docid': 1557970,
          'doctitle': 'Experimental Small Molecule Drugs',
          'docsubtitle': '',
          'docdate': '',
          'organization': 'DrugBank',
          'reportedfunction': None,
          'functioncategory': None,
          'component': '',
          'keywordset': 'Canada; pharmaceutical'},
         ...]
        """
        word = quote(word, safe="")

        options = {
            "fc": "functional-use/search/by-dtxsid",
            "qsur": "functional-use/probability/search/by-dtxsid",
            "puc": "product-data/search/by-dtxsid",
            "lpk": "list-presence/search/by-dtxsid",
        }
        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        self.suffix = f"{self.kind}/{options[by]}/{word}"
        self.data = super(Exposure, self).get()

        return self

    def vocabulary(self, by):
        """
        Search for a type of exposure information using a DTXSID.

        For a single chemical, search for 1) reported functional uses,
        2) predicted functional uses, 3) product that report this chemical as an
        ingredient, or 4) annotated lists of chemicals that contain this
        chemical.

        Parameters
        ----------
        by : string
            The type of vocabulary to return. Options are "fc", "qsur",
            "puc", or "lpk". "fc" is Function Category, "puc" is product use
            category, and "lpk" is list presence keyword.

        Return
        ------
        list
            a list of dicts with each dict being an entry in the specified
            controlled vocabulary


        Examples
        --------

        Get Function Category (FC) vocabulary

        >>> expo.vocabulary(by='fc')

        [{'id': 28,
          'title': 'Coalescing agent',
          'description': 'Chemical substance used in polymer emulsions ...'},
         {'id': 29,
          'title': 'Conductive agent',
          'description': 'Chemical substance used to conduct electrical ...'},
         ...]

        Get Product Use Category (PUC) vocabulary

        >>> expo.vocabulary(by='puc')

        [{'id': 45,
          'kindName': 'Formulation',
          'genCat': 'Cleaning products and household care',
          'prodfam': 'oven',
          'prodtype': '',
          'definition': 'cleaning or other products used in or on ovens ...'},
         {'id': 44,
          'kindName': 'Formulation',
          'genCat': 'Cleaning products and household care',
          'prodfam': 'metal specific',
          'prodtype': '',
          'definition': 'cleaning or care products specific to metals, ...'},
          ...]

        Get List Presence Keyword (LPK) vocabulary

        >>> expo.vobabulary(by='lpk')

        [{'id': 52,
          'tagName': 'detected',
          'tagDefinition': 'chemicals measured or identified in ...',
          'kindName': 'Modifiers'},
         {'id': 53,
          'tagName': 'drinking_water',
          'tagDefinition': 'water intended for drinking, or related to ...',
          'kindName': 'Media'},
         ...]
        """
        options = {
            "fc": "functional-use/category",
            "lpk": "list-presence/tags",
            "puc": "product-data/puc",
        }

        if by not in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")

        self.suffix = f"{self.kind}/{options[by]}"
        self.data = super(Exposure, self).get()

        return self.data
    

    def to_df(self):
        if not hasattr(self,'data'):
            raise AttributeError("No data to convert to DataFrame")
        return pd.DataFrame(self.data)
