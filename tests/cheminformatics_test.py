import unittest
import json
from pandas import to_numeric
from numpy.testing import assert_array_equal
import time
import ctxpy as ctx

class TestCheminformatics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._conn = ctx.base.HCDConnection()

    def read_browser_return(self,file):
        with open(f"browser_api_returns/cheminformatics/{file}.json",'rb') as f:
            info = json.load(f)
        return info

    def tearDown(self):
        time.sleep(1)

    def test_connection(self):
        self.assertEqual(self._conn.host, "https://hcd.rtpnc.epa.gov/api/")
        self.assertEqual(self._conn.headers, "&headers=TRUE")
        self.assertEqual(self._conn.descriptors, "descriptors?type=toxprints&smiles=")
        
    def test_smiles_toxp_return(self):
        smiles = 'CC1=CC=CC=C1'
        info = self.read_browser_return("smiles_toxp_return")
        info = to_numeric(info['chemicals'][0]['descriptors'])
        test = ctx.cheminformatics.get_toxprints(by="smiles",chemical=smiles)
        assert_array_equal(info,test)
        
    def test_chemical_identifier(self):
        identifiers = ['O=C1CCC2CCCCCCCCCCC2=C1', 'DTXSID40959245', 'DTXCID20238909',
                       'DTXCID4081270', 'DTXSID30954784', 'DTXCID20382835',
                       'CCCN1C(=O)C(O)(CC(C)=O)C2=CC=CC=C12', 'DTXSID60844866',
                       'NC1=CC=C(CSC2=CC=NC=C2)C=C1']
        info = ['smiles','dtxsid','dtxcid','dtxcid',
                'dtxsid','dtxcid','smiles','dtxsid','smiles']
        test = [ctx.cheminformatics.chemical_identifier(i) for i in identifiers]
        
        self.assertListEqual(info,test)


if __name__ == "__main__":
    unittest.main()