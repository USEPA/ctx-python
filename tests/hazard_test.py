import unittest
import time
import json
import pandas as pd
from pandas.testing import assert_frame_equal
import ctxpy as ctx


class TestHazard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._conn = ctx.Hazard()

    def tearDown(self):
        time.sleep(1)

    def read_browser_return(self,file):
        with open(f"browser_api_returns/hazard/{file}.json",'rb') as f:
            info = pd.DataFrame(json.load(f)).fillna(pd.NA).replace("-",pd.NA)
        info.sort_index(axis=1,inplace=True)
        info.sort_values(by=info.columns.tolist(),inplace=True)
        return info

    def test_connection(self):
        self.assertEqual(self._conn.host, "https://api-ccte.epa.gov/")
        self.assertEqual(self._conn.headers["accept"], "application/json")
        self.assertIsNotNone(self._conn.headers['x-api-key'])
        self.assertEqual(self._conn.kind,'hazard')
        
    def test_search_all_single_chem(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search(by="all",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_all_single_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_human_single_chem(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search(by="human",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_human_single_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))
        
    def test_search_eco_single_chem(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search(by="eco",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_eco_single_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_skin_eye_single_chem(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search(by="skin-eye",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_skin_eye_single_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_cancer_single_chem(self):
        dtxsid = "DTXSID701015778"
        test = self._conn.search(by="cancer",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_cancer_single_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_genetox_summary_single_chem(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search(by="genetox",dtxsid=dtxsid,summary=True)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_genetox_summary_single_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_genetox_details_single_chem(self):
        dtxsid = "DTXSID7020182"
        test = self._conn.search(by="genetox",dtxsid=dtxsid,summary=False)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_genetox_details_single_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_all_batch_chem(self):
        dtxsid = ["DTXSID7021360","DTXSID2021868",
                  "DTXSID3021807","DTXSID6026298"]
        test = self._conn.batch_search(by="all",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_all_batch_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_human_batch_chem(self):
        dtxsid = ["DTXSID7021360","DTXSID2021868",
                  "DTXSID3021807","DTXSID6026298"]
        test = self._conn.batch_search(by="human",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_human_batch_chemical")
        assert_frame_equal(test.reset_index(drop=True),
                           info.reset_index(drop=True),
                           check_dtype=False)

    def test_search_eco_batch_chem(self):
        dtxsid = ["DTXSID7021360","DTXSID2021868",
                  "DTXSID3021807","DTXSID6026298"]
        test = self._conn.batch_search(by="eco",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_eco_batch_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_skin_eye_batch_chem(self):
        dtxsid = ["DTXSID7021360","DTXSID2021868",
                  "DTXSID3021807","DTXSID6026298"]
        test = self._conn.batch_search(by="skin-eye",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_skin_eye_batch_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_cancer_batch_chem(self):
        dtxsid = ["DTXSID701015778","DTXSID3039242"]
        test = self._conn.batch_search(by="cancer",dtxsid=dtxsid)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_cancer_batch_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_genetox_summary_batch_chem(self):
        dtxsid = ["DTXSID7021360","DTXSID2021868",
                  "DTXSID3021807","DTXSID6026298"]
        test = self._conn.batch_search(by="genetox",dtxsid=dtxsid,summary=True)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_genetox_summary_batch_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))

    def test_search_genetox_details_batch_chem(self):
        dtxsid = ["DTXSID7021360","DTXSID2021868",
                  "DTXSID3021807","DTXSID6026298"]
        test = self._conn.batch_search(by="genetox",dtxsid=dtxsid,summary=False)
        test.sort_index(axis=1,inplace=True)
        test.sort_values(by=test.columns.tolist(),inplace=True)
        info = self.read_browser_return(file="search_genetox_details_batch_chemical")
        assert_frame_equal(test.reset_index(drop=True),info.reset_index(drop=True))


if __name__ == "__main__":
    unittest.main()