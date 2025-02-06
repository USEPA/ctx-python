import json
import warnings
from pathlib import Path
from typing import Optional, Union, Iterable

import pandas as pd
import requests
from urllib.parse import quote

from .utils import read_env, chunker


class CTXConnection:
    """
    Connection that passes API key and other variables needed for GET and POST calls to
    API server.
    
    Parameters
    ----------
    x_api_key : str or None, default None
        A user's API key provided to them for accessing CCTE's APIs. Will use value
        provided in .env file if no key is provided.
    env_path : str or None, default None
        The .env file location. Will default to a user's home directory if no value is 
        provided.
        
    Attributes
    ----------
    headers : dict
        A dictionary of information used to make an API call
        
    Methods
    -------
    get
        request information from specified source using information in header
    post
        send data to resource and then retrieve information based on that data

    """
    def __init__(
        self,
        x_api_key: Optional[str] = None,
        env_path: Optional[Union[str, Path]] = None,
    ):
        if isinstance(x_api_key, str):
            self.host = "https://api-ccte.epa.gov/"
            self.headers = {"accept": "application/json", "x-api-key": x_api_key}

        else:
            config = read_env()
            self.host = config["ctx_api_host"]
            self.headers = {"accept":config['ctx_api_accept'],
                            "x-api-key":config['ctx_api_x_api_key']}

    def get(self, suffix: str):
        """
        Request informaiton via API call
        
        Paramters
        ---------
        suffix : string
            the suffix of the API call that will determine what is searched for and how
        
        Returns
        -------
        dict, JSON information that was requested in the API call
        """
        try:
            self.response = requests.get(
                f"{self.host}{suffix}", headers=self.headers
            )
        except Exception as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)
        try:
            info = json.loads(self.response.content.decode("utf-8"))
        except json.JSONDecodeError as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)

        return info

    def post(self, suffix: str, word: str):
        """
        Request information via API call, but also supply stipulations on subsets or
        specific aspects of returned information
        
        Paramters
        ---------
        suffix : string
            the suffix of the API call that will determine what is searched for and how

        word : string
            extra data passed to the API call; used by batch search calls

        Returns
        -------
        dict, JSON information that was requested in the API call
        """
        try:
            self.headers = {**self.headers, **{"content-type": "application/json"}}
            self.response = requests.post(
                f"{self.host}{suffix}", headers=self.headers, data=word
            )
        except Exception as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)

        try:
            info = json.loads(self.response.content.decode("utf-8"))
        except json.JSONDecodeError as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)

        return info
    
    def batch(self, suffix: str, word: Iterable[str], batch_size: int, bracketed:bool = False):
        """
        There are some inconsistencies in how to provide 'batch' data to the API.
        Sometimes the list of identifiers needs to be a bracketed list, other times it
        needs to be a new-line separated, unbracketed list. The `bracketed` argument
        here will help the users specify this.
        """

        ## Remove duplicated DTXSIDs
        word = list(set(word))

        chunks = []
        for chunk in chunker(word, batch_size):
            
            if bracketed:
                ## '["DTXSID001", "DTXSID002"]'
                words = [quote(w, safe="") for w in chunk]
                words = '["' + '","'.join(words) + '"]'
            else:
                ## '"DTXSID001"\n"DTXSID002"'
                words = "\n".join([quote(w, safe="") for w in chunk])

            ## TODO: Check that suffix is re-written on each loop,
            ## not appended to
            chunks.extend(self.post(suffix = suffix, word=words))
        return chunks



class HCDConnection:
    """
    Connection to the Hazard Comparison Dashboard APIs, no API key is needed, only GET 
    calls are allowed to the API server.
    

        
    Methods
    -------
    get
        request information from specified source using information in header

    """
    def __init__(self):
        
        self.host = "https://hcd.rtpnc.epa.gov/api/"
        self.descriptors = "descriptors?type=toxprints&smiles="
        self.headers = "&headers=TRUE"

    def get(self, smiles: str):
        """
        Request informaiton via API call
        
        Paramters
        ---------
        smiles : string
            the suffix of the API call that will determine what is searched for and how
        
        Returns
        -------
        dict, JSON information that was requested in the API call
        """
        word = quote(smiles, safe="")
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore",category=requests.urllib3.connectionpool.InsecureRequestWarning)
                self.response = requests.get(
                    f"{self.host}{self.descriptors}{word}{self.headers}",
                    verify = False
                )
        except Exception as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)

        try:
            info = json.loads(self.response.content.decode("utf-8"))
        except json.JSONDecodeError as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)
        if 'descriptors' not in info['chemicals'][0].keys():
            info = None
        else:
            info = info['chemicals'][0]['descriptors']

        return info
