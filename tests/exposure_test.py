import unittest
import time
import ctxpy as ctx


class TestExposure(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._conn = ctx.Exposure()
        
    def tearDown(self):
        time.sleep(3)

    def test_connection(self):
        self.assertEqual(self._conn.host, "https://api-ccte.epa.gov/")
        self.assertEqual(self._conn.headers["accept"], "application/json")
        self.assertIsNotNone(self._conn.headers['x-api-key'])
        self.assertEqual(self._conn.kind,'exposure')
        
    def test_search_chem_fc(self):
        dtxsid = "DTXSID7020182"
        doc_types = ['Chemical presence list','Composition','Function']
        test = self._conn.search_cpdat(vocab_name="fc",dtxsid=dtxsid)
        self.assertTrue(all([i['dtxsid']==dtxsid for i in test]))
        self.assertTrue(all([i['datatype'] in doc_types for i in test]))
        self.assertTrue(all([isinstance(i['reportedfunction'],str) for i in test]))

    def test_search_chem_puc(self):
        keys = ['gencat','rawmincomp','rawmaxcomp','rawcentralcomp']
        test = self._conn.search_cpdat(vocab_name='puc',dtxsid='DTXSID7020182')
        self.assertTrue(all(any([isinstance(i[k],str) for k in keys]) for i in test))

    def test_search_chem_lpk(self):
        test = self._conn.search_cpdat(vocab_name='lpk', dtxsid='DTXSID7020182')
        ## There's some weird values returned here, I don't know what to test
        ## other than to ensure that you get a list of dictionaries back
        self.assertTrue(isinstance(test,list))
        self.assertTrue([isinstance(i,dict) for i in test])

    def test_search_chem_qsur(self):
        keys = ['harmonizedFunctionalUse','probability']
        test = self._conn.search_qsurs(dtxsid='DTXSID7020182')
        self.assertTrue(all([k in keys for i in test for k in i.keys()]))
        self.assertTrue(all([isinstance(i[keys[0]],str) for i in test]))
        self.assertTrue(all([isinstance(i[keys[1]],float) for i in test]))
        
    def test_search_chem_httk(self):
        test = self._conn.search_httk(dtxsid='DTXSID7020182')
        self.assertEqual([i['measured'] for i in test if i['id'] == 101171],[0.0083])

    def test_search_chem_exposure_paths(self):
        test = self._conn.search_exposures(by='pathways',dtxsid='DTXSID7020182')
        expected = [{'dtxsid': 'DTXSID7020182',
                     'productionVolume': 2780000,
                     'units': 'kg/day',
                     'stockholmConvention': 0,
                     'probabilityDietary': 1.0,
                     'probabilityResidential': 1.0,
                     'probabilityPesticde': 0.0,
                     'probabilityIndustrial': 0.0,
                     'dataVersion': None,
                     'importDate': '2024-06-13T22:07:19.484632Z'}]
        self.assertEqual(test, expected)

    def test_search_chem_exposure_estimates(self):
        test = self._conn.search_exposures(by='seem',dtxsid='DTXSID7020182')
        expected = [{'id': 488214,
                     'dtxsid': 'DTXSID7020182',
                     'demographic': 'Total',
                     'predictor': 'SEEM3 Consensus',
                     'median': 5.497e-05,
                     'medianText': '5.497e-05',
                     'l95': 1.923e-07,
                     'l95Text': '1.923e-07',
                     'u95': 0.02044,
                     'u95Text': '0.02044',
                     'units': 'mg/kg/day',
                     'ad': 1,
                     'reference': 'Ring 2018',
                     'dataVersion': None,
                     'importDate': '2024-06-13T19:25:16.277317Z'}]
        self.assertEqual([i for i in test if i['predictor'] == 'SEEM3 Consensus'],expected)

    def test_fc_vocabulary(self):
        keys = ['id','title','description']
        test = self._conn.get_cpdat_vocabulary(vocab_name='fc')
        self.assertTrue(all([k in keys for i in test for k in i.keys()]))

    def test_puc_vocabulary(self):
        keys = ['id','kindName','genCat','prodfam','prodtype','definition']
        test = self._conn.get_cpdat_vocabulary(vocab_name='puc')
        self.assertTrue(all([k in keys for i in test for k in i.keys()]))

    def test_lpk_vocabulary(self):
        keys = ['id','tagName','tagDefinition','kindName']
        test = self._conn.get_cpdat_vocabulary(vocab_name='lpk')
        self.assertTrue(all([k in keys for i in test for k in i.keys()]))


if __name__ == "__main__":
    unittest.main()