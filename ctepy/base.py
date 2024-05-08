import tomli
import json
from pathlib import Path
import http.client
import requests

class CTEQuery:
    def __init__(self,stage=False):
        path = Path.home().joinpath(".config.toml")
        if not path.is_file():
            raise FileExistsError(f"{path} does not exist.")
        with open(path,mode='rb') as fp:
            config = tomli.load(fp)

        if stage:
            config = config['ccd_api_stage']
        else:
            config = config['ccd_api']
            
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
        # if conn_type == "http":
        #     self.conn = http.client.HTTPSConnection(config['host'])
        #     self.headers = {'Content-Type': config['content_type'],
        #                     'x-api-key': config['x_api_key']}
        # elif conn_type == "requests":
        # self.conn =requests.get(config.pop('host'),headers=config)