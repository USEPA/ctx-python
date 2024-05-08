import json
from urllib.parse import quote
import warnings
from ctepy.base import CTEQuery


class Exposure(CTEQuery):
    def __init__(self,stage=False):
        super().__init__(stage)
        
    def search(self,by,word):
        
        word = quote(word,safe="")
        print(by)
        if by == "fc":
            suffix = f"/exposure/functional-use/search/by-dtxsid/{word}"
        elif by == "qsur":
            suffix = f"/exposure/functional-use/probability/search/by-dtxsid/{word}"
        elif by == "puc":
            suffix = f"/exposure/product-data/search/by-dtxsid/{word}"
        elif by == "lpk":
            suffix = f"/exposure/list-presence/search/by-dtxsid/{word}"
        else:
            warnings.warn(f"{by} is not a valid value to search by.")

        self.conn.request( "GET", suffix, headers=self.headers)
        res = self.conn.getresponse()
        print(res)
        data = res.read()

        try:
            info = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            warnings.warn(f"{self.conn.host+suffix} not a valid URL.")
            info = None

        return info


    def vocabulary(self,ont):
        match ont:
            case "fc":
                suffix = "/exposure/functional-use/category"
            case "lpk":
                suffix = "/exposure/list-presence/tags"
            case "puc":
                suffix = "/exposure/product-data/puc"
            case _:
                warnings.warn(f"{ont} is not a valid ontology with categories.")
            
        self.conn.request( "GET", suffix, headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        try:
            info = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            warnings.warn(f"{self.conn.host+suffix} not a valid URL.")

        return info