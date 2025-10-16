import json
import warnings
from pathlib import Path
from typing import Optional, Union, Iterable, Callable

import pandas as pd
import requests
from urllib.parse import quote
from pandas.api.types import is_list_like

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
        
        query = [quote(q, safe="") for q in query]
        if bracketed:
            query = '["' + '","'.join(query) + '"]'
        else:
            ## '"DTXSID001"\n"DTXSID002"'
            query = "\n".join(query)
        return query


    def _get_request_method(self,query):
        ## Get request type and format query
        if (is_list_like(query)) and (not isinstance(query,dict)):
            method = 'POST'
        elif isinstance(query,str):
            method = "GET"
        elif isinstance(query,dict):
            method = 'GET'
        elif query is None:
            method = "GET"
        else:
            raise TypeError("Expected 'query' to be type `str`, `list`, or `None`"
                            f"but is {type(query).__name__} instead.")
        return method

    def _get_quoted_query(self,query,quote_method='default', bracketed=True):
        if quote_method == "default":
            if is_list_like(query):
                query = self._format_post_query(query=query, bracketed=bracketed)
            elif isinstance(query,str):
                query = quote(query,safe="")
        elif callable(quote_method):
            query = quote_method(query)
        return query

    def _get_url_and_data(self,method:str, endpoint:str, query:Optional[str]=None):

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
        return url, data
        

    def _request(self, endpoint: str, query: Optional[str]=None,
                 params: Optional[dict]=None, bracketed:bool=True,
                 quote_method: Union[str, Callable]='default'):

        method = self._get_request_method(query=query)
        query = self._get_quoted_query(query=query,
                                       quote_method=quote_method,
                                       bracketed=bracketed)
        url, data = self._get_url_and_data(method=method,
                                           endpoint=endpoint,
                                           query=query)
        
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
                 batched:bool=False, batch_size:int=200,
                 quote_method='default'):

        if batched:
            info = self._batch(endpoint=endpoint, query=query, params=params,
                               bracketed=bracketed, batch_size=batch_size,
                               quote_method=quote_method)
        else:
            if (pd.api.types.is_list_like(query)) and (len(query) > batch_size):
                warnings.warn("Length of query's iterable is larger than `batch_size`, "
                              "performing batched search.")
                info = self._batch(endpoint=endpoint, query=query, params=params,
                                   bracketed=bracketed, batch_size=batch_size,
                                   quote_method=quote_method)
                
            info = self._request(endpoint=endpoint, query=query, params=params,
                                 bracketed=bracketed, quote_method=quote_method)
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
