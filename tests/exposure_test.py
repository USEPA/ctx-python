import pandas as pd
from pandas.testing import assert_frame_equal
import json
import unittest
import time
import ctxpy as ctx


class TestExposure(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._conn = ctx.Exposure()
        
    def tearDown(self):
        time.sleep(1)

    def read_browser_return(self,file):
        with open(f"browser_api_returns/exposure/{file}.json",'rb') as f:
            info = pd.DataFrame(json.load(f)).fillna(pd.NA).replace("-",pd.NA)
        info = info.fillna(pd.NA).replace("-",pd.NA).replace("",pd.NA).copy()
        info.sort_index(axis=1,inplace=True)
        info.sort_values(by=info.columns.tolist(),inplace=True)
        return info

    def test_connection(self):
        self.assertEqual(self._conn.host, "https://api-ccte.epa.gov/")
        self.assertEqual(self._conn.headers["accept"], "application/json")
        self.assertIsNotNone(self._conn.headers['x-api-key'])
        self.assertEqual(self._conn.kind,'exposure')
        
    def test_search_cpdat_by_fc(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search_cpdat(vocab_name="fc",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_cpdat_by_fc")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_batch_cpdat_by_fc(self):
        dtxsids = ['DTXSID2021868','DTXSID7021360']
        test = self._conn.search_cpdat(vocab_name='fc',dtxsid=dtxsids)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_batch_cpdat_by_fc")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_cpdat_by_puc(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search_cpdat(vocab_name="puc",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_cpdat_by_puc")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_batch_cpdat_by_puc(self):
        dtxsids = ['DTXSID2021868','DTXSID7021360']
        test = self._conn.search_cpdat(vocab_name='puc',dtxsid=dtxsids)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_batch_cpdat_by_puc")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_cpdat_by_lpk(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search_cpdat(vocab_name="lpk",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_cpdat_by_lpk")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_batch_cpdat_by_lpk(self):
        dtxsids = ['DTXSID2021868','DTXSID7021360']
        test = self._conn.search_cpdat(vocab_name='lpk',dtxsid=dtxsids)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_batch_cpdat_by_lpk")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_qsurs(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search_qsurs(dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_qsurs")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_batch_qsurs(self):
        dtxsids = ['DTXSID2021868','DTXSID7021360']
        test = self._conn.search_qsurs(dtxsid=dtxsids)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_batch_qsurs")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_httk(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search_httk(dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_httk")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_batch_httk(self):
        dtxsids = ['DTXSID4020458','DTXSID7020182']
        test = self._conn.search_httk(dtxsid=dtxsids)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_batch_httk")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_exposures_pathways(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search_exposures(by='pathways',dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_exposures_pathways")
        assert_frame_equal(test.reset_index(drop=True),
                           info.reset_index(drop=True),
                           check_dtype=False)

    def test_search_batch_exposures_pathways(self):
        dtxsids = ['DTXSID2021868','DTXSID7021360']
        test = self._conn.search_exposures(by='pathways',dtxsid=dtxsids)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_batch_exposures_pathways")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_exposures_seem(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search_exposures(by='seem',dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_batch_exposures_pathways")
        info = self.read_browser_return(file="search_exposures_seem")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_batch_exposures_seem(self):
        dtxsids = ['DTXSID2021868','DTXSID7021360']
        test = self._conn.search_exposures(by='seem',dtxsid=dtxsids)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_batch_exposures_seem")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_fc_vocabulary(self):
        test = self._conn.get_cpdat_vocabulary(vocab_name='fc')
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="fc_vocabulary")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_puc_vocabulary(self):
        test = self._conn.get_cpdat_vocabulary(vocab_name='puc')
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="puc_vocabulary")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_lpk_vocabulary(self):
        test = self._conn.get_cpdat_vocabulary(vocab_name='lpk')
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="lpk_vocabulary")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))


if __name__ == "__main__":
    unittest.main()