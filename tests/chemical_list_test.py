import unittest
import time
import ctxpy as ctx

class TestChemical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._conn = ctx.ChemicalList()

    def tearDown(self):
        time.sleep(1)

    def test_connection(self):
        self.assertEqual(self._conn.host, "https://api-ccte.epa.gov/")
        self.assertEqual(self._conn.headers["accept"], "application/json")
        self.assertEqual(self._conn.kind, "chemical/list")
        self.assertIsNotNone(self._conn.headers["x-api-key"])

    def test_get_list_chemicals(self):
        test = self._conn.get_full_list(list_name="VITAMINS")
        vitamins = ['DTXSID0022519', 'DTXSID0026339', 'DTXSID1026295',
                    'DTXSID1052743', 'DTXSID2020929', 'DTXSID2023648',
                    'DTXSID3023556', 'DTXSID4023541', 'DTXSID5020106',
                    'DTXSID7022679', 'DTXSID7044346', 'DTXSID7047229',
                    'DTXSID8021777', 'DTXSID9051458']

        self.assertEqual(len(test), 14)
        self.assertEqual(test,vitamins)
        
    def test_public_lists(self):
        test = self._conn.public_list_names()
        self.assertIsInstance(test,list)
        self.assertTrue([i==i.upper() for i in test])



if __name__ == "__main__":
    unittest.main()
