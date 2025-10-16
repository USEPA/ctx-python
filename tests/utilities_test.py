import unittest
import requests
from importlib import resources

import ctxpy

class TestUtilities(unittest.TestCase):
        
        
    def test_ctx_connection(self):
        url = ("https://comptox.epa.gov/ctx-api/"
               "chemical/detail/search/by-dtxsid/DTXSID7020182")
        config = ctxpy.utils.read_env()
        headers = {"accept":config['ctx_api_accept'],
                   "x-api-key":config['ctx_api_x_api_key']}

        
        response = requests.get(url,headers=headers)
        
        self.assertEqual(response.status_code,200)

    def test_toxprint_file_exists(self):
        exists = resources.is_resource('ctxpy.data','toxprints.txt')
        self.assertTrue(exists)
        
    def test_correct_toxprint_contents(self):
        contents = resources.read_text('ctxpy.data',"toxprints.txt")
        self.assertEqual(len(contents.split("\n")),729)