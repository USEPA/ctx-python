import json
from urllib.parse import quote
import numpy as np
import pandas as pd
from tqdm import tqdm
import time
import warnings
from http.client import InvalidURL
from ctepy.base import CTEQuery
from importlib import resources


def toxprints():
    """Read in column names for ToxPrints"""
    with resources.path("ctepy.data","toxprints.txt") as f:
        toxps = f.readlines()

    return toxps


class ChemicalSearch(CTEQuery):
    def __init__(self,stage=False):
        super().__init__(stage)
        
        
    def search(self,by,word,start=None,end=None):
        
        word = quote(word,safe="")
        
        match by:
            case "starts-with":
                suffix = f"/chemical/search/start-with/{word}"
            case "equals":
                suffix = f"/chemical/search/equal/{word}"
            case "contains":
                suffix = f"/chemical/search/contain/{word}"
            case "dtxsid":
                suffix = f"/chemical/detail/search/by-dtxsid/{word}"
            case "dtxcid":
                suffix = f"/chemical/detail/search/by-dtxcid/{word}"
            case "mass-range":
                suffix = f"/chemical/detail/search/by-mass/{start}/{end}"
            case "formula":
                suffix = f"/chemical/detail/search/by-formula/{word}"
            case _:
                raise ValueError(f"{by} is not a valid value to search by.")

        self.conn.request( "GET", suffix, headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        try:
            info = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            ##TODO  make this a warning rather than an exception.
            warnings.warn(f"{self.conn.host+suffix} not a valid URL.")

        return info


    def get_details(self,by,word):

        match by:
            case "dtxsid":
                suffix = f"/chemical/detail/search/by-dtxsid/{word}"
            case "dtxcid":
                suffix = f"/chemical/detail/search/by-dtxcid/{word}"
            case "batch":
                if isinstance(word,list):
                    word = '["'+'","'.join(word)+'"]'
                else:
                    raise TypeError(f"If `by` argument is {by}, `word` "
                                    "argument must be a list of DTXSIDs.")
                    
                suffix = f"/chemical/detail/search/by-dtxsid/{word}"
            case _:
                warnings.warn(f"{by} is not a valid value to search by.")

        self.conn.request( "GET", suffix, headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        try:
            info = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            warnings.warn(f"{self.conn.host+suffix} not a valid URL.")

        return info



def chemical_batch(by,words,how='search',wait=None):
    """
    Perform the equivalent of a batch search of the CCD using the API call.
    
    Parameters
    ----------
    by: string, what type of search will be called; options are `starts-with`, 
    `equals`, `contains`, or `dtxsid`
    words: list-like, collection of search terms to look for
    how: string, option of what will be returned in the search; for simple
        chemical identifiers choose `search`, but for more details like structure,
        and ToxPrint fingerprints, choose `details` (note: `details` will only
        take `dtxsid` or `dtxcid` as a `by` option)
    wait: integer, how many seconds to wait between API calls; default = 1
    """
    dtx = DTXQuery()
    words = np.unique([word for word in words if pd.notnull(word)])
    if isinstance(wait,type(None)):
        wait = 1
    
    if how == 'search':
        df = []
        for word in tqdm(words,ascii=True,desc=f"Batch {by} Search"):
            try:
                j = dtx.search(by=by,word=word)
            except http.client.InvalidURL:
                j = [{"searchName":"No Match",
                          "searchValue": word,
                          "rank":pd.NA,
                          "casrn":pd.NA,
                          "preferredName":pd.NA,
                          "hasStructureImage":pd.NA,
                          "smiles":pd.NA,
                          "isMarkush":pd.NA,
                          "dtxsid":pd.NA,
                          "dtxcid":pd.NA}]
            # df.append(pd.DataFrame.from_records(j))
            if isinstance(j,dict):
                if j['status'] == 400:
                    j = [{"searchName":"No Match",
                          "searchValue": word,
                          "rank":pd.NA,
                          "casrn":pd.NA,
                          "preferredName":pd.NA,
                          "hasStructureImage":pd.NA,
                          "smiles":pd.NA,
                          "isMarkush":pd.NA,
                          "dtxsid":pd.NA,
                          "dtxcid":pd.NA}]
                df += j
            elif isinstance(j,list):
                df += j
            else:
                raise TypeError("CCD API batch search returned type ",
                                f"({type(j).__name__}) for {j}")
            time.sleep(wait)
        df = pd.DataFrame(df).sort_values(['dtxsid','dtxcid','casrn',
                                           'preferredName','searchValue','rank'],
                                          ascending=[False,False,False,
                                                     False,False,True])
        df.drop_duplicates(subset=['dtxsid','dtxcid','casrn',
                                   'preferredName','searchValue'],
                           keep='last',inplace=True)
    elif how == 'details':
        ## TODO: raise error if by != dtxsid or dtxcid
        if (by != 'dtxsid') or (by != "dtxcid"):
            raise ValueError(f"{by} must be either `dtxsid` or `dtxcid` for"
                             "detail search.")
        df = []
        for word in tqdm(words,ascii=True,desc="Batch Detail Search"):
            j = dtx.get_details(by=by,word=word)
            df.append(j)
            time.sleep(wait)
        df = pd.DataFrame(df)
        
    return df.copy()

