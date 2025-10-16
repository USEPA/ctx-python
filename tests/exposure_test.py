import unittest
from unittest.mock import patch
import pandas as pd
import ctxpy

class CustomAssertions:
    def assertFramesEqual(self,left,right,**kwargs):
        try:
            pd.testing.assert_frame_equal(left=left,right=right,**kwargs)
        except AssertionError as e:
            raise e

class TestExposure(unittest.TestCase, CustomAssertions):

    """
    All endpoint suffixes and response examplesa are taken from:
    https://comptox.epa.gov/ctx-api/docs/exposure.html
    """

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_cpdat_fc_batch(self, mocker):

        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "datatype": "AAAAAA",
                "docid": 0,
                "doctitle": "AAAAAA",
                "docdate": "AAAAAA",
                "reportedfunction": "AAAAAA",
                "functioncategory": "AAAAAA"}]

        dtxsid = ['DTXSID7020182','DTXSID2021868']

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_cpdat(vocab_name='fc', dtxsid=dtxsid)

        endpoint = 'exposure/functional-use/search/by-dtxsid/'
        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200,
                                       bracketed=True)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_cpdat_fc_serial(self, mocker):

        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "datatype": "AAAAAA",
                "docid": 0,
                "doctitle": "AAAAAA",
                "docdate": "AAAAAA",
                "reportedfunction": "AAAAAA",
                "functioncategory": "AAAAAA"}]
        
        dtxsid = 'DTXSID7020182'

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_cpdat(vocab_name='fc',dtxsid=dtxsid)

        endpoint = "exposure/functional-use/search/by-dtxsid/"

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200,
                                       bracketed=True)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_qsurs_serial(self, mocker):

        hit = [{"dtxsid": "string",
                "harmonizedFunctionalUse": "string",
                "probability": 0}]
        
        dtxsid = 'DTXSID7020182'
        
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_qsurs(dtxsid=dtxsid)

        endpoint = "exposure/functional-use/probability/search/by-dtxsid/"
        
        mocker.assert_called_once_with(endpoint=endpoint, query=dtxsid)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))
        

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_cpdat_vocabulary_fc(self, mocker):

        hit = [{"id": 0,
                "category": "AAAAAA",
                "definition": "string"}]

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.get_cpdat_vocabulary(vocab_name='fc')

        endpoint = 'exposure/functional-use/category'

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_cpdat_puc_serial(self, mocker):

        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "docid": 0,
                "doctitle": "AAAAAA",
                "docdate": "AAAAAA",
                "productname": "AAAAAA",
                "gencat": "AAAAAA",
                "prodfam": "AAAAAA",
                "prodtype": "AAAAAA",
                "classificationmethod": "AAAAAA",
                "rawmincomp": "AAAAAA",
                "rawmaxcomp": "AAAAAA",
                "rawcentralcomp": "AAAAAA",
                "unittype": "AAAAAA",
                "lowerweightfraction": 0,
                "upperweightfraction": 0,
                "centralweightfraction": 0,
                "weightfractiontype": "AAAAAA",
                "component": "AAAAAA"}]

        dtxsid = 'DTXSID7020182'

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_cpdat(vocab_name='puc',dtxsid=dtxsid)

        endpoint = 'exposure/product-data/search/by-dtxsid/'
        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200,
                                       bracketed=True)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_cpdat_puc_batch(self, mocker):

        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "docid": 0,
                "doctitle": "AAAAAA",
                "docdate": "AAAAAA",
                "productname": "AAAAAA",
                "gencat": "AAAAAA",
                "prodfam": "AAAAAA",
                "prodtype": "AAAAAA",
                "classificationmethod": "AAAAAA",
                "rawmincomp": "AAAAAA",
                "rawmaxcomp": "AAAAAA",
                "rawcentralcomp": "AAAAAA",
                "unittype": "AAAAAA",
                "lowerweightfraction": 0,
                "upperweightfraction": 0,
                "centralweightfraction": 0,
                "weightfractiontype": "AAAAAA",
                "component": "AAAAAA"}]

        dtxsid = ['DTXSID7020182','DTXSID2021868']

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_cpdat(vocab_name='puc',dtxsid=dtxsid)

        endpoint = 'exposure/product-data/search/by-dtxsid/'
        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200,
                                       bracketed=True)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_cpdat_vocabulary_puc(self,mocker):
        hit = [{"id": 0,
                "kindName": "AAAAAA",
                "genCat": "AAAAAA",
                "prodfam": "AAAAAA",
                "prodtype": "AAAAAA",
                "definition": "string"}]

        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.get_cpdat_vocabulary(vocab_name='puc')

        endpoint = 'exposure/product-data/puc'

        mocker.assert_called_once_with(endpoint=endpoint)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_cpdat_lpk_serial(self, mocker):

        hit = [{"id": 0,
                "dtxsid": "string",
                "docid": 0,
                "doctitle": "AAAAAA",
                "docsubtitle": "AAAAAA",
                "docdate": "AAAAAA",
                "organization": "AAAAAA",
                "reportedfunction": "AAAAAA",
                "functioncategory": "AAAAAA",
                "component": "AAAAAA",
                "keywordset": "string"}]

        dtxsid = 'DTXSID7020182'

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_cpdat(vocab_name='lpk',dtxsid=dtxsid)

        endpoint = 'exposure/list-presence/search/by-dtxsid/'
        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200,
                                       bracketed=True)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_cpdat_lpk_batch(self, mocker):

        hit = [{"id": 0,
                "dtxsid": "string",
                "docid": 0,
                "doctitle": "AAAAAA",
                "docsubtitle": "AAAAAA",
                "docdate": "AAAAAA",
                "organization": "AAAAAA",
                "reportedfunction": "AAAAAA",
                "functioncategory": "AAAAAA",
                "component": "AAAAAA",
                "keywordset": "string"}]

        dtxsid = ['DTXSID7020182','DTXSID2021868']

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_cpdat(vocab_name='lpk',dtxsid=dtxsid)

        endpoint = 'exposure/list-presence/search/by-dtxsid/'
        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200,
                                       bracketed=True)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_cpdat_vocabulary_lpk(self,mocker):
        hit = [{"id": 0,
                "tagName": "AAAAAA",
                "tagDefinition": "AAAAAA",
                "tagKind": "AAAAAA"}]

        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.get_cpdat_vocabulary(vocab_name='lpk')

        endpoint = 'exposure/list-presence/tags'

        mocker.assert_called_once_with(endpoint=endpoint)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_httk_batch(self, mocker):
        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "parameter": "AAAAAA",
                "measuredText": "AAAAAA",
                "measured": 0,
                "predictedText": "AAAAAA",
                "predicted": 0,
                "units": "AAAAAA",
                "model": "AAAAAA",
                "reference": "AAAAAA",
                "percentile": "AAAAA",
                "species": "AAAAAA",
                "dataSourceSpecies": "AAAAAA"}]

        dtxsid = ['DTXSID7020182','DTXSID2021868']

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_httk(dtxsid=dtxsid)

        endpoint = 'exposure/httk/search/by-dtxsid/'
        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_httk_serial(self, mocker):
        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "parameter": "AAAAAA",
                "measuredText": "AAAAAA",
                "measured": 0,
                "predictedText": "AAAAAA",
                "predicted": 0,
                "units": "AAAAAA",
                "model": "AAAAAA",
                "reference": "AAAAAA",
                "percentile": "AAAAA",
                "species": "AAAAAA",
                "dataSourceSpecies": "AAAAAA"}]

        dtxsid = 'DTXSID7020182'

        # Mock the response from the get method
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_httk(dtxsid=dtxsid)

        endpoint = 'exposure/httk/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint, query=dtxsid)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_pathways_exposures_batch(self,mocker):
        hit = [{"dtxsid": "AAAAAA",
                "productionVolume": 0,
                "units": "AAAAAA",
                "stockholmConvention": 0,
                "probabilityDietary": 0,
                "probabilityResidential": 0,
                "probabilityPesticde": 0,
                "probabilityIndustrial": 0}]

        dtxsid = ['DTXSID7020182','DTXSID2021868']
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_exposures(by='pathways',dtxsid=dtxsid)

        endpoint = 'exposure/seem/general/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_pathways_exposures_serial(self,mocker):
        hit = [{"dtxsid": "AAAAAA",
                "productionVolume": 0,
                "units": "AAAAAA",
                "stockholmConvention": 0,
                "probabilityDietary": 0,
                "probabilityResidential": 0,
                "probabilityPesticde": 0,
                "probabilityIndustrial": 0}]

        dtxsid = 'DTXSID7020182'
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_exposures(by='pathways',dtxsid=dtxsid)

        endpoint = 'exposure/seem/general/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint, query=dtxsid)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_seem_exposures_batch(self,mocker):
        hit = [{"dtxsid": "AAAAAA",
                "productionVolume": 0,
                "units": "AAAAAA",
                "stockholmConvention": 0,
                "probabilityDietary": 0,
                "probabilityResidential": 0,
                "probabilityPesticde": 0,
                "probabilityIndustrial": 0}]

        dtxsid = ['DTXSID7020182','DTXSID2021868']
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_exposures(by='seem',dtxsid=dtxsid)

        endpoint = 'exposure/seem/demographic/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_seem_exposures_serial(self,mocker):
        hit = [{"dtxsid": "AAAAAA",
                "productionVolume": 0,
                "units": "AAAAAA",
                "stockholmConvention": 0,
                "probabilityDietary": 0,
                "probabilityResidential": 0,
                "probabilityPesticde": 0,
                "probabilityIndustrial": 0}]

        dtxsid = 'DTXSID7020182'
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_exposures(by='seem',dtxsid=dtxsid)

        endpoint = 'exposure/seem/demographic/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint, query=dtxsid)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_mmdb_by_medium(self, mocker):
        hit = {"medium": "livestock/meat",
               "totalRecords": 380,
               "recordsOnPage": 380,
               "pageNumber": 1,
               "totalPages": 1,
               "data":[{"id": 0,
                        "fullSourceName": "AAAAAA",
                        "chemicalName": "AAAAAA",
                        "dtxsid": "AAAAAA",
                        "preferredName": "AAAAAA",
                        "casrn": "AAAAAA",
                        "result": "string",
                        "units": "AAAAAA",
                        "cleanedUnits": "string",
                        "statistic": "AAAAAA",
                        "sampleSize": "string",
                        "lod": "string",
                        "loq": "string",
                        "numDetects": "string",
                        "numNonDetects": "string",
                        "rateDetects": "string",
                        "detected": 0,
                        "detectedConflict": 0,
                        "notesDetects": "string",
                        "species": "AAAAAA",
                        "media": "AAAAAA",
                        "harmonizedMedium": "AAAAAA",
                        "population": "AAAAAA",
                        "subPopulation": "string",
                        "collectionActivityId": "AAAAAA",
                        "dates": "string",
                        "years": "string",
                        "location": "AAAAAA",
                        "stateOrProvince": "string",
                        "county": "AAAAAA",
                        "country": "string",
                        "qualityFlag": "AAAAAA",
                        "link": "AAAAAA",
                        "reference": "AAAAAA",
                        "version": "string",
                        "exportDate": "1970-01-01",
                        "casnumber": "string"}]}

        query = 'soil'
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_mmdb(by='medium',query=query)

        endpoint = "exposure/mmdb/single-sample/by-medium"
        params = {"medium":query}

        mocker.assert_called_once_with(endpoint=endpoint, query=query, params=params)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit['data']))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_mmdb_by_aggregate(self, mocker):
        hit = {"medium": "livestock/meat",
               "totalRecords": 380,
               "recordsOnPage": 380,
               "pageNumber": 1,
               "totalPages": 1,
               "data":[{"id": 0,
                        "fullSourceName": "AAAAAA",
                        "chemicalName": "AAAAAA",
                        "dtxsid": "AAAAAA",
                        "preferredName": "AAAAAA",
                        "casrn": "AAAAAA",
                        "result": "string",
                        "units": "AAAAAA",
                        "cleanedUnits": "string",
                        "statistic": "AAAAAA",
                        "sampleSize": "string",
                        "lod": "string",
                        "loq": "string",
                        "numDetects": "string",
                        "numNonDetects": "string",
                        "rateDetects": "string",
                        "detected": 0,
                        "detectedConflict": 0,
                        "notesDetects": "string",
                        "species": "AAAAAA",
                        "media": "AAAAAA",
                        "harmonizedMedium": "AAAAAA",
                        "population": "AAAAAA",
                        "subPopulation": "string",
                        "collectionActivityId": "AAAAAA",
                        "dates": "string",
                        "years": "string",
                        "location": "AAAAAA",
                        "stateOrProvince": "string",
                        "county": "AAAAAA",
                        "country": "string",
                        "qualityFlag": "AAAAAA",
                        "link": "AAAAAA",
                        "reference": "AAAAAA",
                        "version": "string",
                        "exportDate": "1970-01-01",
                        "casnumber": "string"}]}
        query = 'soil'
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_mmdb(by='aggregate',query=query)

        endpoint = "exposure/mmdb/aggregate/by-medium"
        params = {"medium":query}

        mocker.assert_called_once_with(endpoint=endpoint, query=query, params=params)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit['data']))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_mmdb_by_dtxsid(self, mocker):
        hit = [{"id": 0,
                "fullSourceName": "AAAAAA",
                "chemicalName": "AAAAAA",
                "dtxsid": "AAAAAA",
                "preferredName": "AAAAAA",
                "casrn": "AAAAAA",
                "result": "AAAAAA",
                "units": "AAAAAA",
                "cleanedUnits": "string",
                "lod": "AAAAAA",
                "loq": "AAAAAA",
                "detectionFlag": "AAAAAA",
                "resultFlag": "AAAAAA",
                "detected": 0,
                "detectedConflict": 0,
                "notesDetects": "string",
                "species": "AAAAAA",
                "media": "AAAAAA",
                "harmonizedMedium": "AAAAAA",
                "method": "AAAAAA",
                "collectionActivityId": "AAAAAA",
                "sampleId": "AAAAAA",
                "mmdbSampleId": "string",
                "dates": "AAAAAA",
                "year": "AAAA",
                "month": "AAAA",
                "time": "string",
                "location": "AAAAAA",
                "stateOrProvince": "string",
                "county": "AAAAAA",
                "country": "AAAAAA",
                "qualityFlag": "AAAAAA",
                "link": "AAAAAA",
                "reference": "AAAAAA",
                "version": "string",
                "exportDate": "1970-01-01",
                "casnumber": "string"}]

        dtxsid = 'DTXSID7020182'
        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.search_mmdb(by='dtxsid',query=dtxsid)

        endpoint = "exposure/mmdb/single-sample/by-dtxsid/"

        mocker.assert_called_once_with(endpoint=endpoint, query=dtxsid, params=None)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_mmdb_vocabulary(self,mocker):

        hit = [{"harmonizedMediumDesc": "string",
                "harmonizedMedium": "string"}]

        mocker.return_value = hit

        expo = ctxpy.Exposure()
        result = expo.get_mmdb_vocabulary()

        endpoint = 'exposure/mmdb/mediums'

        mocker.assert_called_once_with(endpoint=endpoint)
        self.assertFramesEqual(left=result,right=pd.DataFrame(result))


if __name__ == "__main__":
    unittest.main()