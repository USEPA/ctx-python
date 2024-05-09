import json
from urllib.parse import quote
import warnings
from ctepy.base import Connection


class Exposure(Connection):
    def __init__(self,stage=False):
        super().__init__(stage)
        self.kind = "exposure"
        
    def search(self,by,word):
        
        word = quote(word,safe="")
        
        options = {"fc":"functional-use/search/by-dtxsid",
                   "qsur":"functional-use/probability/search/by-dtxsid",
                   "puc":"product-data/search/by-dtxsid",
                   "lpk":"list-presence/search/by-dtxsid"}

        self.suffix = f"{self.kind}/{options[by]}/{word}"
        info = super(Exposure,self).get()

        return info


    def vocabulary(self,by):

        options = {"fc":"functional-use/category",
                   "lpk":"list-presence/tags",
                   "puc":"product-data/puc"}

        self.suffix = f"{self.kind}/{options[by]}"
        info = super(Exposure,self).get()

        return info
