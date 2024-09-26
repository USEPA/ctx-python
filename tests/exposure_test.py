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
        word = "DTXSID7020182"
        doc_types = ['Chemical presence list','Composition','Function']
        test = self._conn.search(by="fc",word=word)
        self.assertTrue(all([i['dtxsid']==word for i in test]))
        self.assertTrue(all([i['datatype'] in doc_types for i in test]))
        self.assertTrue(all([isinstance(i['reportedfunction'],str) for i in test]))

    def test_search_chem_qsur(self):
        keys = ['harmonizedFunctionalUse','probability']
        test = self._conn.search(by='qsur',word='DTXSID7020182')
        self.assertTrue(all([k in keys for i in test for k in i.keys()]))
        self.assertTrue(all([isinstance(i[keys[0]],str) for i in test]))
        self.assertTrue(all([isinstance(i[keys[1]],float) for i in test]))

    def test_search_chem_puc(self):
        keys = ['gencat','rawmincomp','rawmaxcomp','rawcentralcomp']
        test = self._conn.search(by='puc',word='DTXSID7020182')
        self.assertTrue(all(any([isinstance(i[k],str) for k in keys]) for i in test))

    def test_search_chem_lpk(self):
        test = self._conn.search(by='lpk', word='DTXSID7020182')
        ## There's some weird values returned here, I don't know what to test
        ## other than to ensure that you get a list of dictionaries back
        self.assertTrue(isinstance(test,list))
        self.assertTrue([isinstance(i,dict) for i in test])

    def test_fc_vocabulary(self):
        keys = ['id','title','description']
        test = self._conn.vocabulary(by='fc')
        self.assertTrue(all([k in keys for i in test for k in i.keys()]))

    def test_puc_vocabulary(self):
        keys = ['id','kindName','genCat','prodfam','prodtype','definition']
        test = self._conn.vocabulary(by='puc')
        self.assertTrue(all([k in keys for i in test for k in i.keys()]))

    def test_lpk_vocabulary(self):
        keys = ['id','tagName','tagDefinition','kindName']
        test = self._conn.vocabulary(by='lpk')
        self.assertTrue(all([k in keys for i in test for k in i.keys()]))


if __name__ == "__main__":
    unittest.main()