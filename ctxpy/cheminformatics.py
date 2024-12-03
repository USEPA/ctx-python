from importlib import resources

from .chemical import Chemical
from .base import HCDConnection

def toxprints():
    """
    Get names of ToxPrints.

    This function will retrieve the name of ToxPrints fingerprints, so that they
    can be applied to the string of ToxPrints for a chemical or chemicals.

    Parameters
    ---------
    None

    Returns
    -------
    list
        The names of the 729 ToxPrint fingerprints.

    Examples
    --------
    >>> toxprints()

    """

    with open(resources.path("ctxpy.data", "toxprints.txt"), "r") as f:
        toxps = f.read().splitlines()

    return toxps



def get_toxprints(by,word):
    """
    place holder for passing a list of ids and returning a dataframe of just
    toxprints
    """
    if by == 'dtxsid':
        info = Chemical().details(by=by,word=word)
    elif by == 'smiles':
        info = HCDConnection().get(by=by,smiles=word)

    return info