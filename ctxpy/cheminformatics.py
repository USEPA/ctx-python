import re
import pandas as pd
from pandas.api.types import is_list_like
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


def chemical_identifier(chemical):
    """
    Uses Regular Expressions to determine chemical identifier is DTXSID, DTXCID,
    or SMILES. Note: SMILES are only determined through a process of elimination.
    
    chemical: str
        the chemical identifier in DTXSID, DTXCID, or SMILES form.
        
    returns: str
        the type of identifier that was provided
    """
    
    ## TODO: more robust handling of identifiers would make resolving identifiers in the
    ## ChemicalConnection must easier.
    dtxsid = "^DTXSID[0-9][0-9]{1,10}$"
    dtxcid = "^DTXCID[0-9][0-9]{1,10}$"
    dtxid = re.compile(f'{dtxsid}|{dtxcid}')

    if dtxid.match(chemical) is None:
        identifier = 'smiles'
    else:
        dtxsid = re.compile(dtxsid).match(chemical)
        dtxcid = re.compile(dtxcid).match(chemical)

        if (dtxsid is not None) and (dtxcid is None):
            identifier = 'dtxsid'
        elif (dtxsid is None) and (dtxcid is not None):
            identifier = 'dtxcid'
        else:
            raise ValueError(f"`chemical` is not known input type {chemical}")
    return identifier



def get_toxprints(by,chemical):
    """
    Provide a single chemical identifier and return the ToxPrints chemotypes for that
    compound.
    
    by: str
        the type of chemical identifier (DTXSID, DTXCID, or SMILES)
    chemical: str
        the chemical identifier in DTXSID, DTXCID, or SMILES form.
        
    returns: array or None
        If ToxPrints could be found for the identifier, then a (729,) array is 
        returned. If no ToxPrints could be found, then None is returned.
    """
    if by == 'smiles':
        info = HCDConnection().get(smiles=chemical)
        if info is not None:
            info = pd.to_numeric(info)

    elif by == 'dtxsid':
        info = Chemical().details(by=by,word=chemical)
        if info['descriptorStringTsv'] is not None:
            info = pd.to_numeric(info['descriptorStringTsv'].split("\t"))
        else:
            info = None
    elif by == 'dtxcid':
        info = Chemical().details(by=by,word=chemical)
        if info['descriptorStringTsv'] is not None:
            info = pd.to_numeric(info['descriptorStringTsv'].split("\t"))
        else:
            info = None

    return info



def search_toxprints(chemical):
    """
    Provide ToxPrint chemoctypes for one chemical identifier or a list-like of multiple 
    chemical identifiers.
    
    Chemical Identifiers may be DTXSIDs, DTXCIDs, or SMILES strings. If a list is
    provided, the list can be of mixed types of identifiers. If a DTXSID or DTXCID is 
    given, then a Chemical().details() search is peformed to get the ToxPrints. If a 
    SMILES string is provied, then the HCDConnection.get() is used to calculate the 
    chemotypes "on-the-fly".
    
    Parameters
    ----------
    chemical: str or list-list
        chemical identifers that will be searched
        
    Returns
    -------
    pandas DataFrame
    a dataframe of len(chemical) rows and 729 columns. The index of the row returns the 
    chemical identifier supplied as well as that identifier's type.
    """
    info = {}
    if is_list_like(chemical):
        ## TODO: more robust handling of identifiers would make resolving identifiers in the
        ## ChemicalConnection must easier.
        for c in chemical:
            identifier = chemical_identifier(c)
            # print(c,identifier)
            datum = get_toxprints(by=identifier,chemical=c)
            
            if datum is None:
                datum = pd.to_numeric([pd.NA]*729)
            info[(c,identifier)] = datum
    if isinstance(chemical,str):
        identifier = chemical_identifier(chemical)
        datum = get_toxprints(by=identifier,chemical=chemical)
        if datum is None:
            datum = pd.to_numeric([pd.NA]*729)
        info = {(chemical,identifier):datum}

    info = pd.DataFrame(data=list(info.values()),
                        index=(pd.MultiIndex
                                .from_tuples(info.keys(),
                                            names=['chem_id','chem_id_type'])),
                        columns=toxprints())
    return info