import tomli
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
        # if conn_type == "http":
        #     self.conn = http.client.HTTPSConnection(config['host'])
        #     self.headers = {'Content-Type': config['content_type'],
        #                     'x-api-key': config['x_api_key']}
        # elif conn_type == "requests":
        # self.conn =requests.get(config.pop('host'),headers=config)