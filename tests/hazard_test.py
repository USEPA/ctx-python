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

class TestHazard(unittest.TestCase, CustomAssertions):

    """
    All endpoint endpointes and response examplesa are taken from:
    https://comptox.epa.gov/ctx-api/docs/hazard.html
    """
    

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_cancer_serial(self, mocker):

        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "source": "AAAAAA",
                "exposureRoute": "AAAAAA",
                "cancerCall": "AAAAAA",
                "url": "AAAAAA"}]
        dtxsid = 'DTXSID7020182'

        mocker.return_value = hit

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='cancer',
                                     dtxsid=dtxsid)

        endpoint = 'hazard/cancer-summary/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_cancer_batch(self, mocker):
        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "source": "AAAAAA",
                "exposureRoute": "AAAAAA",
                "cancerCall": "AAAAAA",
                "url": "AAAAAA"}]
        dtxsid = ['DTXSID7020182','DTXSID2021868']
        mocker.return_value = hit

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='cancer',
                                     dtxsid=dtxsid)
        
        dtxsid = ['DTXSID7020182','DTXSID2021868']
        endpoint = 'hazard/cancer-summary/search/by-dtxsid/'
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_skin_eye_serial(self, mocker):

        hit = [{"id": 0,
                "authority": "AAAAAA",
                "classification": "AAAAAA",
                "dtxsid": "AAAAAA",
                "endpoint": "AAAAAA",
                "glp": "string",
                "guideline": "string",
                "recordUrl": "AAAAAA",
                "reliability": "AAAAAA",
                "resultText": "AAAAAA",
                "score": "AAAAAA",
                "skinEyeHash": "AAAAAA",
                "skinEyeId": 0,
                "skinEyeUuid": "AAAAAA",
                "source": "AAAAAA",
                "species": "AAAAAA",
                "strain": "AAAAAA",
                "studyType": "AAAAAA",
                "year": 0}]
        dtxsid = 'DTXSID7020182'

        mocker.return_value = hit

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='skin-eye', dtxsid=dtxsid)

        endpoint = 'hazard/skin-eye/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_skin_eye_batch(self, mocker):
        hit = [{"id": 0,
                "authority": "AAAAAA",
                "classification": "AAAAAA",
                "dtxsid": "AAAAAA",
                "endpoint": "AAAAAA",
                "glp": "string",
                "guideline": "string",
                "recordUrl": "AAAAAA",
                "reliability": "AAAAAA",
                "resultText": "AAAAAA",
                "score": "AAAAAA",
                "skinEyeHash": "AAAAAA",
                "skinEyeId": 0,
                "skinEyeUuid": "AAAAAA",
                "source": "AAAAAA",
                "species": "AAAAAA",
                "strain": "AAAAAA",
                "studyType": "AAAAAA",
                "year": 0}]
        mocker.return_value = hit
        dtxsid = ['DTXSID7020182','DTXSID2021868']

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='skin-eye', dtxsid=dtxsid)

        endpoint = 'hazard/skin-eye/search/by-dtxsid/'
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_all_serial(self, mocker):

        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "casrn": "string",
                "name": "string",
                "source": "AAAAAA",
                "subsource": "AAAAAA",
                "toxvalType": "AAAAAA",
                "toxvalTypeDefinition": "string",
                "toxvalSubtype": "AAAAAA",
                "toxvalTypeSuperCategory": "AAAAAA",
                "qualifier": "AAAAAA",
                "toxvalNumeric": 0,
                "toxvalUnits": "AAAAAA",
                "riskAssessmentClass": "AAAAAA",
                "humanEco": "AAAAAA",
                "studyType": "AAAAAA",
                "studyDurationClass": "AAAAAA",
                "studyDurationValue": 0,
                "studyDurationUnits": "AAAAAA",
                "speciesCommon": "AAAAAA",
                "strain": "AAAAAA",
                "latinName": "AAAAAA",
                "speciesSupercategory": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifestage": "AAAAAA",
                "exposureRoute": "AAAAAA",
                "exposureMethod": "AAAAAA",
                "exposureForm": "AAAAAA",
                "media": "AAAAAA",
                "toxicologicalEffect": "string",
                "experimentalRecord": "string",
                "studyGroup": "AAAAAA",
                "longRef": "string",
                "doi": "string",
                "title": "string",
                "author": "AAAAAA",
                "year": "AAAAAA",
                "guideline": "AAAAAA",
                "quality": "AAAAAA",
                "qcCategory": "string",
                "sourceHash": "AAAAAA",
                "externalSourceId": "string",
                "externalSourceIdDesc": "string",
                "sourceUrl": "AAAAAA",
                "subsourceUrl": "AAAAAA",
                "storedSourceRecord": "AAAAAA",
                "toxvalTypeOriginal": "AAAAAA",
                "toxvalSubtypeOriginal": "AAAAAA",
                "toxvalNumericOriginal": 0,
                "toxvalUnitsOriginal": "AAAAAA",
                "studyTypeOriginal": "AAAAAA",
                "studyDurationClassOriginal": "AAAAAA",
                "studyDurationValueOriginal": "AAAAAA",
                "studyDurationUnitsOriginal": "AAAAAA",
                "speciesOriginal": "AAAAAA",
                "strainOriginal": "AAAAAA",
                "sexOriginal": "AAAAAA",
                "generationOriginal": "AAAAAA",
                "lifestageOriginal": "AAAAAA",
                "exposureRouteOriginal": "AAAAAA",
                "exposureMethodOriginal": "AAAAAA",
                "exposureFormOriginal": "AAAAAA",
                "mediaOriginal": "AAAAAA",
                "toxicologicalEffectOriginal": "string",
                "originalYear": "AAAAAA"}]
        dtxsid = 'DTXSID7020182'

        mocker.return_value = hit

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='all', dtxsid=dtxsid)

        endpoint = 'hazard/toxval/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_all_batch(self, mocker):
        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "casrn": "string",
                "name": "string",
                "source": "AAAAAA",
                "subsource": "AAAAAA",
                "toxvalType": "AAAAAA",
                "toxvalTypeDefinition": "string",
                "toxvalSubtype": "AAAAAA",
                "toxvalTypeSuperCategory": "AAAAAA",
                "qualifier": "AAAAAA",
                "toxvalNumeric": 0,
                "toxvalUnits": "AAAAAA",
                "riskAssessmentClass": "AAAAAA",
                "humanEco": "AAAAAA",
                "studyType": "AAAAAA",
                "studyDurationClass": "AAAAAA",
                "studyDurationValue": 0,
                "studyDurationUnits": "AAAAAA",
                "speciesCommon": "AAAAAA",
                "strain": "AAAAAA",
                "latinName": "AAAAAA",
                "speciesSupercategory": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifestage": "AAAAAA",
                "exposureRoute": "AAAAAA",
                "exposureMethod": "AAAAAA",
                "exposureForm": "AAAAAA",
                "media": "AAAAAA",
                "toxicologicalEffect": "string",
                "experimentalRecord": "string",
                "studyGroup": "AAAAAA",
                "longRef": "string",
                "doi": "string",
                "title": "string",
                "author": "AAAAAA",
                "year": "AAAAAA",
                "guideline": "AAAAAA",
                "quality": "AAAAAA",
                "qcCategory": "string",
                "sourceHash": "AAAAAA",
                "externalSourceId": "string",
                "externalSourceIdDesc": "string",
                "sourceUrl": "AAAAAA",
                "subsourceUrl": "AAAAAA",
                "storedSourceRecord": "AAAAAA",
                "toxvalTypeOriginal": "AAAAAA",
                "toxvalSubtypeOriginal": "AAAAAA",
                "toxvalNumericOriginal": 0,
                "toxvalUnitsOriginal": "AAAAAA",
                "studyTypeOriginal": "AAAAAA",
                "studyDurationClassOriginal": "AAAAAA",
                "studyDurationValueOriginal": "AAAAAA",
                "studyDurationUnitsOriginal": "AAAAAA",
                "speciesOriginal": "AAAAAA",
                "strainOriginal": "AAAAAA",
                "sexOriginal": "AAAAAA",
                "generationOriginal": "AAAAAA",
                "lifestageOriginal": "AAAAAA",
                "exposureRouteOriginal": "AAAAAA",
                "exposureMethodOriginal": "AAAAAA",
                "exposureFormOriginal": "AAAAAA",
                "mediaOriginal": "AAAAAA",
                "toxicologicalEffectOriginal": "string",
                "originalYear": "AAAAAA"}]
        mocker.return_value = hit
        dtxsid = ['DTXSID7020182','DTXSID2021868']

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='all', dtxsid=dtxsid)
        endpoint = 'hazard/toxval/search/by-dtxsid/'
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_all_genetox_serial(self, mocker):

        hit = [{"id": 0,
                "assayCategory": "AAAAAA",
                "assayCode": "AAAAAA",
                "assayPotency": 0,
                "assayResult": "AAAAAA",
                "assayType": "AAAAAA",
                "assayTypeStandard": "AAAAAA",
                "chemicalId": "AAAAAA",
                "clowderDocId": "AAAAAA",
                "comment": "string",
                "cytotoxicity": "AAAAAA",
                "dataQuality": 0,
                "documentNumber": 0,
                "documentSource": "AAAAAA",
                "doseResponse": "AAAAAA",
                "dtxsid": "AAAAAA",
                "duration": 0,
                "genetoxCall": "AAAAAA",
                "genetoxDetailsId": 0,
                "genetoxNote": "AAAAAA",
                "genetoxResults": "AAAAAA",
                "genetoxSummaryId": 0,
                "glp": 0,
                "guideline": "string",
                "index": "string",
                "metabolicActivation": 0,
                "micronucleus": "string",
                "panelReport": "AAAAAA",
                "protocolEra": "AAAAAA",
                "reference": "AAAAAA",
                "referenceUrl": "AAAAAA",
                "reportsNeg": "string",
                "reportsOther": "string",
                "reportsPos": "string",
                "sex": "AAAAAA",
                "source": "AAAAAA",
                "species": "AAAAAA",
                "strain": "AAAAAA",
                "title": "AAAAAA",
                "useme": 0,
                "year": 0}]
        dtxsid = 'DTXSID7020182'

        mocker.return_value = hit

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='genetox', dtxsid=dtxsid)

        endpoint = 'hazard/genetox/details/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_all_genetox_batch(self, mocker):
        hit = [{"id": 0,
                "assayCategory": "AAAAAA",
                "assayCode": "AAAAAA",
                "assayPotency": 0,
                "assayResult": "AAAAAA",
                "assayType": "AAAAAA",
                "assayTypeStandard": "AAAAAA",
                "chemicalId": "AAAAAA",
                "clowderDocId": "AAAAAA",
                "comment": "string",
                "cytotoxicity": "AAAAAA",
                "dataQuality": 0,
                "documentNumber": 0,
                "documentSource": "AAAAAA",
                "doseResponse": "AAAAAA",
                "dtxsid": "AAAAAA",
                "duration": 0,
                "genetoxCall": "AAAAAA",
                "genetoxDetailsId": 0,
                "genetoxNote": "AAAAAA",
                "genetoxResults": "AAAAAA",
                "genetoxSummaryId": 0,
                "glp": 0,
                "guideline": "string",
                "index": "string",
                "metabolicActivation": 0,
                "micronucleus": "string",
                "panelReport": "AAAAAA",
                "protocolEra": "AAAAAA",
                "reference": "AAAAAA",
                "referenceUrl": "AAAAAA",
                "reportsNeg": "string",
                "reportsOther": "string",
                "reportsPos": "string",
                "sex": "AAAAAA",
                "source": "AAAAAA",
                "species": "AAAAAA",
                "strain": "AAAAAA",
                "title": "AAAAAA",
                "useme": 0,
                "year": 0}]
        mocker.return_value = hit
        dtxsid = ['DTXSID7020182','DTXSID2021868']

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='genetox', dtxsid=dtxsid)
        endpoint = 'hazard/genetox/details/search/by-dtxsid/'
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_all_genetox_summary_serial(self, mocker):

        hit = [{"id": 0,
                "ames": "AAAAAA",
                "clowderDocId": "AAAAAA",
                "dtxsid": "AAAAAA",
                "genetoxCall": "AAAAAA",
                "genetoxSummaryId": 0,
                "micronucleus": "AAAAAA",
                "reportsNegative": 0,
                "reportsOther": 0,
                "reportsPositive": 0}]
        dtxsid = 'DTXSID7020182'

        mocker.return_value = hit

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='genetox-summary', dtxsid=dtxsid)

        endpoint = 'hazard/genetox/summary/search/by-dtxsid/'

        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result, right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_tovaldb_all_genetox_summary_batch(self, mocker):
        hit = [{"id": 0,
                "ames": "AAAAAA",
                "clowderDocId": "AAAAAA",
                "dtxsid": "AAAAAA",
                "genetoxCall": "AAAAAA",
                "genetoxSummaryId": 0,
                "micronucleus": "AAAAAA",
                "reportsNegative": 0,
                "reportsOther": 0,
                "reportsPositive": 0}]
        mocker.return_value = hit
        dtxsid = ['DTXSID7020182','DTXSID2021868']

        haz = ctxpy.Hazard()
        result = haz.search_toxvaldb(by='genetox-summary', dtxsid=dtxsid)
        endpoint = 'hazard/genetox/summary/search/by-dtxsid/'
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_effects_by_study_id(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseDuration": 0,
                "doseDurationUnit": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "dosePeriod": "AAAAAA",
                "doseLevel": 0,
                "conc": 0,
                "concUnit": "AAAAAA",
                "vehicle": "AAAAAA",
                "doseComment": "AAAAAA",
                "doseAdjusted": 0,
                "doseAdjustedUnit": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifeStage": "AAAAAA",
                "numAnimals": 0,
                "tgComment": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "effectDesc": "AAAAAA",
                "effectDescFree": "AAAAAA",
                "cancerRelated": False,
                "targetSite": "AAAAAA",
                "direction": 0,
                "effectComment": "AAAAAA",
                "treatmentRelated": False,
                "criticalEffect": False,
                "sampleSize": "AAAAAA",
                "effectVal": 0,
                "effectValUnit": "AAAAAA",
                "effectVar": 0,
                "effectVarType": "AAAAAA",
                "time": 0,
                "timeUnit": "AAAAAA",
                "noQuantDataReported": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        study_id = "12"
        endpoint = 'hazard/toxref/effects/search/by-study-id/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='study-id',
                                     domain='effects',
                                     query=study_id)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=study_id,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_effects_by_study_type(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseDuration": 0,
                "doseDurationUnit": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "dosePeriod": "AAAAAA",
                "doseLevel": 0,
                "conc": 0,
                "concUnit": "AAAAAA",
                "vehicle": "AAAAAA",
                "doseComment": "AAAAAA",
                "doseAdjusted": 0,
                "doseAdjustedUnit": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifeStage": "AAAAAA",
                "numAnimals": 0,
                "tgComment": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "effectDesc": "AAAAAA",
                "effectDescFree": "AAAAAA",
                "cancerRelated": False,
                "targetSite": "AAAAAA",
                "direction": 0,
                "effectComment": "AAAAAA",
                "treatmentRelated": False,
                "criticalEffect": False,
                "sampleSize": "AAAAAA",
                "effectVal": 0,
                "effectValUnit": "AAAAAA",
                "effectVar": 0,
                "effectVarType": "AAAAAA",
                "time": 0,
                "timeUnit": "AAAAAA",
                "noQuantDataReported": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        study_type = 'MGR'
        endpoint = 'hazard/toxref/effects/search/by-study-type/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='study-type',
                                     domain='effects',
                                     query=study_type)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=study_type,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_effects_by_dtxsid(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseDuration": 0,
                "doseDurationUnit": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "dosePeriod": "AAAAAA",
                "doseLevel": 0,
                "conc": 0,
                "concUnit": "AAAAAA",
                "vehicle": "AAAAAA",
                "doseComment": "AAAAAA",
                "doseAdjusted": 0,
                "doseAdjustedUnit": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifeStage": "AAAAAA",
                "numAnimals": 0,
                "tgComment": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "effectDesc": "AAAAAA",
                "effectDescFree": "AAAAAA",
                "cancerRelated": False,
                "targetSite": "AAAAAA",
                "direction": 0,
                "effectComment": "AAAAAA",
                "treatmentRelated": False,
                "criticalEffect": False,
                "sampleSize": "AAAAAA",
                "effectVal": 0,
                "effectValUnit": "AAAAAA",
                "effectVar": 0,
                "effectVarType": "AAAAAA",
                "time": 0,
                "timeUnit": "AAAAAA",
                "noQuantDataReported": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        dtxsid = 'DTXSID7020182'
        endpoint = 'hazard/toxref/effects/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='dtxsid',
                                     domain='effects',
                                     query=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_summary_by_study_type(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        study_type = 'MGR'
        endpoint = 'hazard/toxref/summary/search/by-study-type/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='study-type',
                                     domain='summary',
                                     query=study_type)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=study_type,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_summary_by_study_id(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        study_id = "12"
        endpoint = 'hazard/toxref/summary/search/by-study-id/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='study-id',
                                     domain='summary',
                                     query=study_id)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=study_id,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_summary_by_dtxsid(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        dtxsid = 'DTXSID7020182'
        endpoint = 'hazard/toxref/summary/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='dtxsid',
                                     domain='summary',
                                     query=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_data_by_study_type(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseDuration": 0,
                "doseDurationUnit": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "dosePeriod": "AAAAAA",
                "doseLevel": 0,
                "conc": 0,
                "concUnit": "AAAAAA",
                "vehicle": "AAAAAA",
                "doseComment": "AAAAAA",
                "doseAdjusted": 0,
                "doseAdjustedUnit": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifeStage": "AAAAAA",
                "numAnimals": 0,
                "tgComment": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "effectDesc": "AAAAAA",
                "effectDescFree": "AAAAAA",
                "cancerRelated": False,
                "targetSite": "AAAAAA",
                "direction": 0,
                "effectComment": "AAAAAA",
                "treatmentRelated": False,
                "criticalEffect": False,
                "sampleSize": "AAAAAA",
                "effectVal": 0,
                "effectValUnit": "AAAAAA",
                "effectVar": 0,
                "effectVarType": "AAAAAA",
                "time": 0,
                "timeUnit": "AAAAAA",
                "noQuantDataReported": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        study_type = 'MGR'
        endpoint = 'hazard/toxref/data/search/by-study-type/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='study-type',
                                     domain='data',
                                     query=study_type)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=study_type,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_data_by_study_id(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseDuration": 0,
                "doseDurationUnit": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "dosePeriod": "AAAAAA",
                "doseLevel": 0,
                "conc": 0,
                "concUnit": "AAAAAA",
                "vehicle": "AAAAAA",
                "doseComment": "AAAAAA",
                "doseAdjusted": 0,
                "doseAdjustedUnit": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifeStage": "AAAAAA",
                "numAnimals": 0,
                "tgComment": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "effectDesc": "AAAAAA",
                "effectDescFree": "AAAAAA",
                "cancerRelated": False,
                "targetSite": "AAAAAA",
                "direction": 0,
                "effectComment": "AAAAAA",
                "treatmentRelated": False,
                "criticalEffect": False,
                "sampleSize": "AAAAAA",
                "effectVal": 0,
                "effectValUnit": "AAAAAA",
                "effectVar": 0,
                "effectVarType": "AAAAAA",
                "time": 0,
                "timeUnit": "AAAAAA",
                "noQuantDataReported": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        study_id = "12"
        endpoint = 'hazard/toxref/data/search/by-study-id/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='study-id',
                                     domain='data',
                                     query=study_id)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=study_id,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_data_by_dtxsid(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": 0,
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseDuration": 0,
                "doseDurationUnit": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "dosePeriod": "AAAAAA",
                "doseLevel": 0,
                "conc": 0,
                "concUnit": "AAAAAA",
                "vehicle": "AAAAAA",
                "doseComment": "AAAAAA",
                "doseAdjusted": 0,
                "doseAdjustedUnit": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifeStage": "AAAAAA",
                "numAnimals": 0,
                "tgComment": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "effectDesc": "AAAAAA",
                "effectDescFree": "AAAAAA",
                "cancerRelated": False,
                "targetSite": "AAAAAA",
                "direction": 0,
                "effectComment": "AAAAAA",
                "treatmentRelated": False,
                "criticalEffect": False,
                "sampleSize": "AAAAAA",
                "effectVal": 0,
                "effectValUnit": "AAAAAA",
                "effectVar": 0,
                "effectVarType": "AAAAAA",
                "time": 0,
                "timeUnit": "AAAAAA",
                "noQuantDataReported": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        dtxsid = 'DTXSID7020182'
        endpoint = 'hazard/toxref/data/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='dtxsid',
                                     domain='data',
                                     query=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_observations_by_study_type(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studyType": "AAAAAA",
                "guidelineNumber": "AAAAAA",
                "guidelineName": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "status": "AAAAAA",
                "defaultStatus": False,
                "testedStatus": False,
                "reportedStatus": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        study_type = 'MGR'
        endpoint = 'hazard/toxref/observations/search/by-study-type/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='study-type',
                                     domain='observations',
                                     query=study_type)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=study_type,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_observations_by_study_id(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studyType": "AAAAAA",
                "guidelineNumber": "AAAAAA",
                "guidelineName": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "status": "AAAAAA",
                "defaultStatus": False,
                "testedStatus": False,
                "reportedStatus": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        study_id = "12"
        endpoint = 'hazard/toxref/observations/search/by-study-id/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='study-id',
                                     domain='observations',
                                     query=study_id)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=study_id,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_observations_by_dtxsid(self,mocker):
        hit = [{"id": 0,
                "studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studyType": "AAAAAA",
                "guidelineNumber": "AAAAAA",
                "guidelineName": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "status": "AAAAAA",
                "defaultStatus": False,
                "testedStatus": False,
                "reportedStatus": False,
                "exportDate": "1970-01-01",
                "version": "string"}]
        mocker.return_value = hit
        dtxsid = 'DTXSID7020182'
        endpoint = 'hazard/toxref/observations/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='dtxsid',
                                     domain='observations',
                                     query=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_toxrefdb_dtxsid_batch(self,mocker):
        hit = [{"studyId": 0,
                "dtxsid": "AAAAAA",
                "casrn": "AAAAAA",
                "name": "AAAAAA",
                "studySource": "AAAAAA",
                "studySourceId": "AAAAAA",
                "citation": "AAAAAA",
                "studyYear": "string",
                "studyType": "AAAAAA",
                "studyTypeGuideline": "AAAAAA",
                "species": "AAAAAA",
                "strainGroup": "AAAAAA",
                "strain": "AAAAAA",
                "adminRoute": "AAAAAA",
                "adminMethod": "AAAAAA",
                "doseDuration": "string",
                "doseDurationUnit": "AAAAAA",
                "doseStart": 0,
                "doseStartUnit": "AAAAAA",
                "doseEnd": 0,
                "doseEndUnit": "AAAAAA",
                "dosePeriod": "AAAAAA",
                "doseLevel": 0,
                "conc": "string",
                "concUnit": "AAAAAA",
                "vehicle": "AAAAAA",
                "doseComment": "AAAAAA",
                "doseAdjusted": "string",
                "doseAdjustedUnit": "AAAAAA",
                "sex": "AAAAAA",
                "generation": "AAAAAA",
                "lifeStage": "AAAAAA",
                "numAnimals": "AAAAAA",
                "tgComment": "AAAAAA",
                "endpointCategory": "AAAAAA",
                "endpointType": "AAAAAA",
                "endpointTarget": "AAAAAA",
                "effectDesc": "AAAAAA",
                "effectDescFree": "AAAAAA",
                "cancerRelated": False,
                "targetSite": "AAAAAA",
                "direction": 0,
                "effectComment": "AAAAAA",
                "treatmentRelated": "string",
                "criticalEffect": False,
                "sampleSize": "AAAAAA",
                "effectVal": "string",
                "effectValUnit": "AAAAAA",
                "effectVar": "string",
                "effectVarType": "AAAAAA",
                "time": "string",
                "timeUnit": "AAAAAA",
                "noQuantDataReported": False,
                "tbsKey": 0}]
        mocker.return_value = hit
        dtxsid = ['DTXSID7020182','DTXSID2021868']
        endpoint = 'hazard/toxref/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_toxrefdb(by='dtxsid',domain='all',query=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid,
                                       batch_size=200)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_pprtv(self,mocker):
        hit = [{"id": 0,
                "dtxsid": "AAAAAA",
                "pprtvSubstanceId": 0,
                "name": "string",
                "casrn": "string",
                "lastReviosn": 0,
                "pprtvAssessment": "string",
                "irisLink": "string",
                "rfcValue": "string",
                "rfdValue": "string",
                "woe": "string"}]
        mocker.return_value = hit
        dtxsid = 'DTXSID7020182'
        endpoint = '/hazard/pprtv/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_pprtv(dtxsid=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_hawc(self,mocker):
        hit = [{"id": 0,
                "name": "string",
                "year": 0,
                "dtxsid": "string",
                "ccdUrl": "string",
                "hawcUrl": "string"}]
        mocker.return_value = hit
        dtxsid = 'DTXSID7020182'
        endpoint = '/hazard/hawc/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_hawc(dtxsid=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_iris(self,mocker):
        hit = [{"dtxsid": "string",
                "chemicalName": "string",
                "casrn": "string",
                "lastSignificantRevision": "1970-01-01T00:00:00.000Z",
                "literatureScreeningReview": "string",
                "criticalEffectsSystems": "string",
                "rfdChronic": "string",
                "rfdSubchronic": "string",
                "rfcChronic": "string",
                "rfcSubchronic": "string",
                "tumorSite": "string",
                "irisUrl": "string"}]
        mocker.return_value = hit
        dtxsid = 'DTXSID7020182'
        endpoint = '/hazard/iris/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_iris(dtxsid=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_adme_ivive(self,mocker):
        hit = [{"id": 0,
                "dtxsid": "string",
                "description": "string",
                "measured": "string",
                "predicted": "string",
                "unit": "AAAAAA",
                "model": "string",
                "reference": "string",
                "percentile": "string",
                "species": "string",
                "dataSourceSpecies": "string"}]
        mocker.return_value = hit
        dtxsid = 'DTXSID7020182'
        endpoint = '/hazard/adme-ivive/search/by-dtxsid/'
        haz = ctxpy.Hazard()
        result = haz.search_adme_ivive(dtxsid=dtxsid)
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=dtxsid)
        self.assertFramesEqual(left=result,right=pd.DataFrame(hit))

if __name__ == "__main__":
    unittest.main()