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
            ## Need this here in case there is no .env file
            self.host = "https://comptox.epa.gov/ctx-api/"
            self.headers = {"accept": "application/json", "x-api-key": x_api_key}

        else:
            config = read_env()
            self.host = config["ctx_api_host"]
            self.headers = {"accept":config['ctx_api_accept'],
                            "x-api-key":config['ctx_api_x_api_key']}


    def _format_post_query(self,query:str, bracketed:bool=True):
        
        query = query = [quote(q, safe="") for q in query]
        if bracketed:
            query = '["' + '","'.join(query) + '"]'
        else:
            ## '"DTXSID001"\n"DTXSID002"'
            query = "\n".join(query)
        return query

    def _request(self, endpoint: str, query: Optional[str]=None,
                params: Optional[dict]=None, bracketed:bool=True):

        ## Get request type and format query
        if pd.api.types.is_list_like(query):
            method='POST'
            query = self._format_post_query(query=query, bracketed=bracketed)
            self.headers = {**self.headers, **{"content-type":"application/json"}}
        elif isinstance(query,str):
            method = "GET"
            query = quote(query, safe="")
        else:
            raise TypeError("Expected 'query' to be type `str`, "
                            f"but is {type(query).__name__} instead.")

        ## Construct URL
        if query is not None:
            if method == "POST":
                url = f'{self.host}{endpoint}'
                data = query
            elif method == "GET":
                url = f'{self.host}{endpoint}{query}'
                data = None
        else:
            url = f'{self.host}{endpoint}'
            data = None

        
        ## Try the request, raise errors if there are any
        try:
            self.response = requests.request(method=method,
                                             url=url,
                                             data=data,
                                             headers=self.headers,
                                             params=params)
            self.response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise err


        try:
            info = json.loads(self.response.content.decode("utf-8"))
        except json.JSONDecodeError as err:
            raise err

        return info

    # def get(self, endpoint: str, query: Optional[str]=None, params: Optional[dict]=None):
    #     """
    #     Request informaiton via API call
        
    #     Paramters
    #     ---------
    #     suffix : string
    #         the suffix of the API call that will determine what is searched for and how
        
    #     Returns
    #     -------
    #     dict, JSON information that was requested in the API call
    #     """
    #     if query is not None:
    #         url = f'{self.host}{endpoint}{quote(query, safe="")}'
    #     else:
    #         url = f'{self.host}{endpoint}'
        
    #     try:
    #         self.response = requests.request(method='GET',
    #                                          url=url,
    #                                          headers=self.headers,
    #                                          params=params)
    #     except Exception as e:
    #         raise e
    #     # print(self.response.content)
    #     print(self.response.status_code)
    #     try:
    #         info = json.loads(self.response.content.decode("utf-8"))
    #     except json.JSONDecodeError as e:
    #         raise e

    #     return info

    # def post(self, endpoint: str, query: str, bracketed:bool, params: Optional[dict]=None):
    #     """
    #     Request information via API call, but also supply stipulations on subsets or
    #     specific aspects of returned information
        
    #     Paramters
    #     ---------
    #     endpoint : string
    #         the suffix of the API call that will determine what is searched for and how

    #     query : string
    #         extra data passed to the API call; used by batch search calls

    #     Returns
    #     -------
    #     dict, JSON information that was requested in the API call
    #     """
    #     ## POSTs only happen with a list of data, which is why this should work.
    #     ## If that ever changes, I'd need to check that `word` is a list-like first
    #     if bracketed:
    #         ## '["DTXSID001", "DTXSID002"]'
    #         query = [quote(q, safe="") for q in query]
    #         query = '["' + '","'.join(query) + '"]'
    #     else:
    #         ## '"DTXSID001"\n"DTXSID002"'
    #         query = "\n".join([quote(q, safe="") for q in query])

    #     try:
    #         self.headers = {**self.headers, **{"content-type": "application/json"}}
    #         self.response = requests.request(method='POST',
    #                                          url=f"{self.host}{endpoint}",
    #                                          headers=self.headers,
    #                                          data=query,
    #                                          params=params)
    #     except Exception as e:
    #         ## TODO: make this a more informative error message
    #         raise SystemError(e)

    #     try:
    #         info = json.loads(self.response.content.decode("utf-8"))
    #     except json.JSONDecodeError as e:
    #         ## TODO: make this a more informative error message
    #         raise SystemError(e)

    #     return info
    
    def _batch(self, endpoint: str, query: Iterable[str], batch_size: int, bracketed:bool=True):
        """
        There are some inconsistencies in how to provide 'batch' data to the API.
        Sometimes the list of identifiers needs to be a bracketed list, other times it
        needs to be a new-line separated, unbracketed list. The `bracketed` argument
        here will help the users specify this.
        """

        ## Remove duplicated DTXSIDs
        query = list(set(query))

        chunks = []
        for chunk in chunker(query, batch_size):

            ## TODO: Check that suffix is re-written on each loop,
            ## not appended to
            chunks.extend(self.request(endpoint=endpoint, query=query, bracketed=bracketed))
            
        return chunks

    def ctx_call(self, endpoint:str, query:Optional[str]=None,
                 params:Optional[dict]=None, bracketed:bool=True,
                 batched:bool=False, batch_size:int=200):

        if batched:
            info = self._batch(endpoint=endpoint, query=query, params=params,
                               bracketed=bracketed, batch_size=batch_size)
        else:
            if (pd.api.types.is_list_like(query)) and (len(query) > batch_size):
                warnings.warn("Length of query's iterable is larger than `batch_size`, "
                              "performing batched search.")
                info = self._batch(endpoint=endpoint, query=query, params=params,
                                bracketed=bracketed, batch_size=batch_size)
                
            info = self._request(endpoint=endpoint, query=query, params=params,
                                 bracketed=bracketed)
        return info


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
        query = quote(smiles, safe="")
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore",category=requests.urllib3.connectionpool.InsecureRequestWarning)
                self.response = requests.get(
                    f"{self.host}{self.descriptors}{query}{self.headers}",
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


class ResponseTransformer:
    def __init__(self,data):
        self._data = data

    def __iter__(self):
        """
        Implements iteration over the PostResponse object, 
        allowing it to be used in loops and other iterable contexts, 
        returning the raw list of dictionaries.
        """
        return iter(self._data)

    def __getitem__(self,index):
        """
        Supports indexing, enabling access to individual elements of 
        the raw data.
        """
        return self._data[index]

    def __repr__(self):
        """
        Provides a string representation of the raw data, which is 
        useful for debugging and when printing the object.
        """
        return repr(self._data)
    
    def to_df(self):
        df = pd.DataFrame(self._data).fillna(pd.NA).replace("-",pd.NA).replace("",pd.NA)
        df.attrs = {"response":self._data}
        return df
