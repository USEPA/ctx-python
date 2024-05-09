import json
import requests
import numpy as np
import pandas as pd
import time
import warnings
from urllib.parse import quote
from importlib import resources
from typing import Union, Iterable, Optional
from ccte_api.base import Connection


def toxprints():
    """Read in column names for ToxPrints"""

    with open(resources.path("ctepy.data","toxprints.txt"),'r') as f:
        toxps = f.read().splitlines()

    return toxps


class Chemical(Connection):
    
    def __init__(self,stage=False):
        super().__init__(stage)
        self.kind = "chemical"


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
            
            self.suffix = f"{self.kind}/search/{options[by]}/"
            
            info = super(Chemical,self).post(word=word)
            
        else:
            word = quote(word,safe="")
            self.suffix = f"{self.kind}/search/{options[by]}/{word}"
        
            info = super(Chemical,self).get()

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

            self.suffix = f"{self.kind}/detail/search/{options[by]}/"
            info = super(Chemical,self).post(word=word)

        else:
            if not isinstance(word,str):
                raise TypeError(f"Argument `by` is {by}, "
                                f"but `word` is not string {word}.")
                    
            word = quote(word,safe="")
            self.suffix = f"{self.kind}/detail/search/{options[by]}/{word}"
            
            info = super(Chemical,self).get()

        return info
    
    
    def msready(self,by: str,word: str,
                start:Optional[float]=None, end:Optional[float]=None):
        
        
        options = {"dtxcid":"by-dtxcid",
                   "mass":"by-mass",
                   "formula":"by-formula",}
        
        if not by in options.keys():
            raise KeyError(f"Value {by} is invalid option for argument `by`.")
        
        word = quote(word,safe="")
        self.suffix = f"{self.kind}/msready/search/by-formula/{word}"
        
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
        
        info = super(Chemical,self).get()

        return info

