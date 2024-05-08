import json
import requests
import numpy as np
import pandas as pd
import time
import warnings
from urllib.parse import quote
from importlib import resources
from typing import Union, Iterable, Optional
from ctepy.base import CTEQuery


def toxprints():
    """Read in column names for ToxPrints"""

    with open(resources.path("ctepy.data","toxprints.txt"),'r') as f:
        toxps = f.read().splitlines()

    return toxps


class Chemical(CTEQuery):
    
    def __init__(self,stage=False):
        super().__init__(stage)


    ## TODO:
    ## 1. Get a static method that handles the get/post commands
    ## 2. see if it's possible to put that static method in the base class,
    ## instead of having to code it up for each individual sub-class


    def search(self,by: str,word: Union[str,Iterable[str]]):
        
        options = {"starts-with":"start-with",
                   "equals":"equal",
                   "contains":"contain",
                   "batch":'equal'}
        
        if not by in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")
        
        if by == 'batch':
            if not isinstance(word,list):
                raise TypeError("Arugment `by` is 'batch', "
                                "but `word` is not an Iterable.")
            ## API only handles 200 at a time.
            if len(word) > 200:
                raise ValueError("API will not accept more than 200 words at a "
                                 "time. Chunk list and resubmit.")
                
            word = "\n".join([quote(w,safe="") for w in word])
            
            self.suffix = f"chemical/search/{options[by]}/"
            self.headers = {**self.headers,
                            **{"content-type":"application/json"}}

            self.response = requests.post(f"{self.host}{self.suffix}",
                                          headers=self.headers,
                                          data=word)
            
            
        else:
            word = quote(word,safe="")
            self.suffix = f"chemical/search/{by}/{word}"
        
            try:
                self.response = requests.get(f"{self.host}{self.suffix}",
                                            headers=self.headers)
            except Exception as e:
                ## TODO: make this a more informative error message
                raise SystemError(e)
        
        
            
        try:
            info = json.loads(self.response.content.decode("utf-8"))
        except json.JSONDecodeError as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)

        return info


    def details(self,by: str,word: Union[str,Iterable[str]]):

        options = {"dtxsid":"by-dtxsid",
                   "dtxcid":"by-dtxcid",
                   "batch":"by-dtxsid"}
        
        if not by in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")
        
        if by == "batch":
            if not isinstance(word,list):
                raise TypeError("Arugment `by` is 'batch', "
                                "but `word` is not an Iterable.")
                
            word = [quote(w,safe="") for w in word]
            word = '["'+'","'.join(word)+'"]'

            self.suffix = f"chemical/detail/search/{options[by]}/"
            self.headers = {**self.headers,
                            **{"content-type":"application/json"}}

            self.response = requests.post(f"{self.host}{self.suffix}",
                                          headers=self.headers,
                                          data=word)

        else:
            if not isinstance(word,str):
                raise TypeError(f"Argument `by` is {by}, "
                                f"but `word` is not string {word}.")
                    
            word = quote(word,safe="")
            self.suffix = f"chemical/detail/search/{options[by]}/{word}"
            
            try:
                self.response = requests.get(f"{self.host}{self.suffix}",
                                            headers=self.headers)
            except Exception as e:
                ## TODO: make this a more informative error message
                raise SystemError(e)

        try:
            info = json.loads(self.response.content.decode("utf-8"))
        except json.JSONDecodeError as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)

        return info
    
    
    def msready(self,by: str,word: str,
                start:Optional[float]=None, end:Optional[float]=None):
        
        
        options = {"dtxcid":"by-dtxcid",
                   "mass":"by-mass",
                   "formula":"by-formula",}
        
        if not by in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")
        
        word = quote(word,safe="")
        self.suffix = f"chemical/msready/search/by-formula/{formula}"
        
        if by == "mass":
            if (start == None) or (end == None):
                raise ValueError("Argument `by` is 'mass', but no `start` or "
                                 "`end` mass values are provided.")
                
            word = f"{start}/{end}"
            
        else:
            if not isinstance(word,str):
                raise TypeError(f"Argument `by` is {by}, "
                                "but `word` is not string.")
                
        ## TODO: test that this works for mass -- does safe quote mess 
        ## with the floats?
        word = quote(word,safe="")
        
        try:
            self.response = requests.get(f"{self.host}{self.suffix}",
                                        headers=self.headers)
        except Exception as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)
            
        try:
            info = json.loads(self.response.content.decode("utf-8"))
        except json.JSONDecodeError as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)

        return info



# def chemical_batch(by,words,how='search',wait=None):
#     """
#     Perform the equivalent of a batch search of the CCD using the API call.
    
#     Parameters
#     ----------
#     by: string, what type of search will be called; options are `starts-with`, 
#     `equals`, `contains`, or `dtxsid`
#     words: list-like, collection of search terms to look for
#     how: string, option of what will be returned in the search; for simple
#         chemical identifiers choose `search`, but for more details like structure,
#         and ToxPrint fingerprints, choose `details` (note: `details` will only
#         take `dtxsid` or `dtxcid` as a `by` option)
#     wait: integer, how many seconds to wait between API calls; default = 1
#     """
#     dtx = DTXQuery()
#     words = np.unique([word for word in words if pd.notnull(word)])
#     if isinstance(wait,type(None)):
#         wait = 1
    
#     if how == 'search':
#         df = []
#         for word in tqdm(words,ascii=True,desc=f"Batch {by} Search"):
#             try:
#                 j = dtx.search(by=by,word=word)
#             except http.client.InvalidURL:
#                 j = [{"searchName":"No Match",
#                           "searchValue": word,
#                           "rank":pd.NA,
#                           "casrn":pd.NA,
#                           "preferredName":pd.NA,
#                           "hasStructureImage":pd.NA,
#                           "smiles":pd.NA,
#                           "isMarkush":pd.NA,
#                           "dtxsid":pd.NA,
#                           "dtxcid":pd.NA}]
#             # df.append(pd.DataFrame.from_records(j))
#             if isinstance(j,dict):
#                 if j['status'] == 400:
#                     j = [{"searchName":"No Match",
#                           "searchValue": word,
#                           "rank":pd.NA,
#                           "casrn":pd.NA,
#                           "preferredName":pd.NA,
#                           "hasStructureImage":pd.NA,
#                           "smiles":pd.NA,
#                           "isMarkush":pd.NA,
#                           "dtxsid":pd.NA,
#                           "dtxcid":pd.NA}]
#                 df += j
#             elif isinstance(j,list):
#                 df += j
#             else:
#                 raise TypeError("CCD API batch search returned type ",
#                                 f"({type(j).__name__}) for {j}")
#             time.sleep(wait)
#         df = pd.DataFrame(df).sort_values(['dtxsid','dtxcid','casrn',
#                                            'preferredName','searchValue','rank'],
#                                           ascending=[False,False,False,
#                                                      False,False,True])
#         df.drop_duplicates(subset=['dtxsid','dtxcid','casrn',
#                                    'preferredName','searchValue'],
#                            keep='last',inplace=True)
#     elif how == 'details':
#         ## TODO: raise error if by != dtxsid or dtxcid
#         if (by != 'dtxsid') or (by != "dtxcid"):
#             raise ValueError(f"{by} must be either `dtxsid` or `dtxcid` for"
#                              "detail search.")
#         df = []
#         for word in tqdm(words,ascii=True,desc="Batch Detail Search"):
#             j = dtx.get_details(by=by,word=word)
#             df.append(j)
#             time.sleep(wait)
#         df = pd.DataFrame(df)
        
#     return df.copy()

