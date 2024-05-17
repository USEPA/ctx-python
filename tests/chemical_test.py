import unittest
import ccte_api as cte


class TestChemical(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._conn = cte.Chemical()


    def test_connection(self):
        self.assertEqual(self._conn.host, "https://api-ccte.epa.gov/")
        self.assertEqual(self._conn.headers["accept"], "application/json")
        self.assertIsNotNone(self._conn.headers['x-api-key'])


    def test_search_equals(self):
        test_search = self._conn.search(by='equals',word='toluene')
        
        self.assertEqual(len(test_search),1)
        self.assertEqual(
            self._conn.search(by="equals", word="toluene")[0]["dtxcid"], "DTXCID501360"
        )
        self.assertEqual(
            self._conn.search(by="equals", word="108-88-3")[0]["dtxcid"], "DTXCID501360"
        )


    def test_search_contains(self):
        test_search = self._conn.search(by='contains',word='8-88-3')
        
        self.assertTrue(any('108-88-3' in chem.values() for chem in test_search))
        self.assertTrue(any("Toluene" in chem.values() for chem in test_search))


    def test_search_starts_with(self):
        test_search = self._conn.search(by='starts-with',word='tolu')
        
        self.assertTrue(any('108-88-3' in chem.values() for chem in test_search))
        self.assertTrue(any("Toluene" in chem.values() for chem in test_search))


    def test_search_batch(self):
        chemicals = {'toluene': 'DTXSID7021360',
                     'p-xylene': 'DTXSID2021868',
                     'o-xylene': 'DTXSID3021807',
                     '108-38-3': 'DTXSID6026298'}
        test_search = self._conn.search(by = 'batch', word = chemicals)
        self.assertEqual(len(test_search),4)
        
        ## TODO: the API does something with the search string such that the
        # `searchValue` is not the same as the string I feed it -- need to figure out
        # what this is, so that I can check it. I could then use 
        # `self.assertCountEqual([i['searchValue'] for i in test_search],chemicals)`
        
        for chem in test_search:
            sv = chem['searchValue'].lower().replace(" ","-")
            self.assertEqual(chem['dtxsid'].strip(),chemicals[sv])


    def test_details_dtxsid_default(self):
        test_search = self._conn.details(by='dtxsid',word='DTXSID7021360')
        self.assertTrue(len(test_search),73)
        self.assertEqual(test_search['inchiString'].strip(),'InChI=1S/C7H8/c1-7-5-3-2-4-6-7/h2-6H,1H3')


    def test_details_dtxcid_default(self):
        test_search = self._conn.details(by='dtxcid',word='DTXCID501360')
        self.assertTrue(len(test_search),73)
        self.assertEqual(test_search['inchiString'].strip(),'InChI=1S/C7H8/c1-7-5-3-2-4-6-7/h2-6H,1H3')


    def test_details_batch_default(self):
        chemicals = {'DTXSID7021360': "InChI=1S/C7H8/c1-7-5-3-2-4-6-7/h2-6H,1H3",
                     'DTXSID2021868': "InChI=1S/C8H10/c1-7-3-5-8(2)6-4-7/h3-6H,1-2H3",
                     'DTXSID3021807': "InChI=1S/C8H10/c1-7-5-3-4-6-8(7)2/h3-6H,1-2H3",
                     'DTXSID6026298': "InChI=1S/C8H10/c1-7-4-3-5-8(2)6-7/h3-6H,1-2H3"}
        test_search = self._conn.details(by='batch',word=chemicals.keys())
        self.assertTrue(len(test_search),4)
        
        for chem in test_search:
            self.assertEqual(chem['inchiString'].strip(),chemicals[chem['dtxsid']])


    @unittest.skip("Not yet implemented")
    def test_details_dtxsid_all(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxcid_all(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_batch_all(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxsid_details(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxcid_details(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_batch_details(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxsid_identifiers(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxcid_identifiers(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_batch_identifiers(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxsid_structures(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxcid_structures(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_batch_structures(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxsid_nta(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_dtxcid_nta(self):
        return

    @unittest.skip("Not yet implemented")
    def test_details_batch_nta(self):
        return

    @unittest.skip("Not yet implemented")
    def test_msready_dtxcid(self):
        return

    @unittest.skip("Not yet implemented")
    def test_msready_mass(self):
        return

    @unittest.skip("Not yet implemented")
    def test_msready_formula(self):
        return


if __name__ == "__main__":
    unittest.main()