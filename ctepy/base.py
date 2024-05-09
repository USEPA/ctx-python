import toml
import json
from pathlib import Path
import requests
from typing import Optional
from .exceptions import TableNotFoundError


class Connection:
    def __init__(self,x_api_key: Optional[str]=None):
        
        if isinstance(x_api_key,str):
            self.host = "https://api-ccte.epa.gov/"
            self.headers = {"accept":"application/json",
                            "x-api-key":x_api_key}

        else:
            ## Standard path to ccte_api's config file
            path = Path.home() / ".config" / "ccte_api" / "config.toml"
            
            if not path.is_file():
                raise FileNotFoundError(f"{path.as_posix()} does not exist.")
        
            with open(path,'r') as fp:
                config = toml.load(fp)

            if not 'public_ccte_api' in config.keys():
                TableNotFoundError("`public_ccte_api` table not found in "
                                   "config.toml.")
                
            config = config['public_ccte_api']
                
            self.host = config.pop('host')
            self.headers = config


    def get(self):
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


    def post(self,word:str):
        try:
            self.headers = {**self.headers,
                            **{"content-type":"application/json"}}

            self.response = requests.post(f"{self.host}{self.suffix}",
                                          headers=self.headers,
                                          data=word)
        except Exception as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)
        
        try:
            info = json.loads(self.response.content.decode("utf-8"))
        except json.JSONDecodeError as e:
            ## TODO: make this a more informative error message
            raise SystemError(e)
        
        return info