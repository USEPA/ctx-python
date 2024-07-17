import json
from pathlib import Path
from typing import Optional, Union

import requests

from .utils import read_env


class Connection:
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
            self.host = config.pop("host")
            self.headers = config

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
