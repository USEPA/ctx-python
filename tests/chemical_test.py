import unittest
from unittest.mock import patch
import ctxpy

class TestChemical(unittest.TestCase):


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_equals(self, mocker):
        # Mock the response from the get method
        mocker.return_value = [{'dtxsid': 'DTXSID7021360',
                                'preferredName': 'Toluene'}]

        chemical = 'toluene'
        chem = ctxpy.Chemical()
        result = chem.search(by='equals', query=chemical)

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint='chemical/search/equal/',
                                       query=chemical,
                                       batch_size=200,
                                       bracketed=False)
        self.assertEqual(result, [{'dtxsid': 'DTXSID7021360',
                                   'preferredName': 'Toluene'}])


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_starts_with(self, mocker):
        # Mock the response from the get method
        mocker.return_value = [{'dtxsid': 'DTXSID7021360',
                                'preferredName': 'Toluene'}]

        chemical = 'toluene'
        chem = ctxpy.Chemical()
        result = chem.search(by='starts-with', query=chemical)

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint='chemical/search/start-with/',
                                       query=chemical,
                                       batch_size=200,
                                       bracketed=False)
        self.assertEqual(result, [{'dtxsid': 'DTXSID7021360',
                                   'preferredName': 'Toluene'}])


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_contains(self, mocker):
        hit = [{'dtxsid': 'DTXSID001009823',
                'preferredName': 'Balsams, tolu'},
               {'dtxsid': 'DTXSID00101006',
                'preferredName': ('Soybean oil, polymer with dipentaerythritol, '
                                  'pentaerythritol, phthalic anhydride, styrene, '
                                  'tung oil and vinyltoluene')},
               {'dtxsid': 'DTXSID001014729',
                'preferredName': 'Diethyltoluamide'},
               {'dtxsid': 'DTXSID00101829',
                'preferredName': ('Fatty acids, tall-oil, polymers with glycerol, '
                                  'maleic anhydride, phthalic anhydride, soybean oil '
                                  'and vinyltoluene')}]
        # Mock the response from the get method
        mocker.return_value = hit

        chemical = 'toluene'
        chem = ctxpy.Chemical()
        result = chem.search(by='contains', query=chemical)

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint='chemical/search/contain/',
                                       query=chemical,
                                       batch_size=200,
                                       bracketed=False)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_batch_greater_than_batch_size(self, mocker):
        hit = [{'dtxsid': 'DTXSID7021360',
                'preferredName': 'Toluene'},
               {'dtxsid': 'DTXSID001009823',
                'preferredName': 'Balsams, tolu'}]
        # Mock the response from the get method
        mocker.return_value = hit

        dtxsid = ['DTXSID7021360', 'DTXSID001009823']
        chem = ctxpy.Chemical()
        result = chem.search(by='batch',
                             query=dtxsid,
                             batch_size=1)

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint='chemical/search/equal/',
                                       query=dtxsid,
                                       batch_size=1,
                                       bracketed=False)
        self.assertEqual(result, hit)


    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_search_batch_less_than_batch_size(self, mocker):
        hit = [{'dtxsid': 'DTXSID7021360',
                'preferredName': 'Toluene'},
               {'dtxsid': 'DTXSID001009823',
                'preferredName': 'Balsams, tolu'}]
        # Mock the response from the get method
        mocker.return_value = hit

        dtxsid = ['DTXSID7021360', 'DTXSID001009823']
        chem = ctxpy.Chemical()
        result = chem.search(by='batch',
                             query=dtxsid)

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint='chemical/search/equal/',
                                       query=dtxsid,
                                       batch_size=200,
                                       bracketed=False)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxsid_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}

        mocker.return_value = hit

        dtxsid = 'DTXSID7021360'
        params = {"projection":"chemicaldetailall"}
        chem = ctxpy.Chemical()
        result = chem.details(by='dtxsid',query=dtxsid,subset=None)

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxsid/',
                                       query=dtxsid,
                                       params=params,
                                       batch_size=1000)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxsid_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxsid = 'DTXSID7021360'
        params = {"projection":"ntatoolkit"}
        chem = ctxpy.Chemical()
        result = chem.details(by='dtxsid',query=dtxsid,subset='nta')

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxsid/',
                                       query=dtxsid,
                                       params=params,
                                       batch_size=1000)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxsid_batch_less_than_batch_size_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxsid = ['DTXSID7021360', 'DTXSID001009823']
        params = {"projection":"chemicaldetailall"}
        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxsid',
                              query=dtxsid,
                              subset=None)

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxsid/',
                                       query=dtxsid,
                                       params=params,
                                       batch_size=1000)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxsid_batch_less_than_batch_size_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxsid = ['DTXSID7021360', 'DTXSID001009823']
        params = {"projection":"ntatoolkit"}
        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxsid',
                              query=dtxsid,
                              subset='nta')

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxsid/',
                                       query=dtxsid,
                                       params=params,
                                       batch_size=1000)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxsid_batch_greater_than_batch_size_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxsid = ['DTXSID7021360', 'DTXSID001009823']
        params = {"projection":"chemicaldetailall"}
        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxsid',
                              query=dtxsid,
                              batch_size=1,
                              subset=None)

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxsid/',
                                       query=dtxsid,
                                       params=params,
                                       batch_size=1)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxsid_batch_greater_than_batch_size_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit


        dtxsid = ['DTXSID7021360', 'DTXSID001009823']
        params = {'projection':'ntatoolkit'}
        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxsid',
                              query=dtxsid,
                              batch_size=1,
                              subset='nta')

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxsid/',
                                       query=dtxsid,
                                       params=params,
                                       batch_size=1)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxcid_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxcid = 'DTXCID501360'
        params = {"projection":"chemicaldetailall"}
        chem = ctxpy.Chemical()
        result = chem.details(by='dtxcid',query=dtxcid,subset=None)

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxcid/',
                                       query=dtxcid,
                                       params=params,
                                       batch_size=1000)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxcid_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxcid = "DTXCID501360"
        params = {"projection":"ntatoolkit"}
        chem = ctxpy.Chemical()
        result = chem.details(by='dtxcid',query=dtxcid,subset='nta')

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxcid/',
                                       query=dtxcid,
                                       params=params,
                                       batch_size=1000)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxcid_batch_less_than_batch_size_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxcid = ['DTXCID501360','DTXCID701868']
        params = {"projection":"chemicaldetailall"}
        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxcid',query=dtxcid,subset=None)

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxcid/',
                                       query=dtxcid,
                                       params=params,
                                       batch_size=1000)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxcid_batch_less_than_batch_size_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxcid = ['DTXCID501360','DTXCID701868']
        params = {"projection":"ntatoolkit"}
        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxcid',
                              query=dtxcid,
                              subset='nta')

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxcid/',
                                       query=dtxcid,
                                       params=params,
                                       batch_size=1000)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxcid_batch_greater_than_batch_size_no_subset(self,mocker):
        hit = [{"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'},
               {'inchikey': 'URLKBWYHVLBVBO-UHFFFAOYSA-N',
                'dtxsid': 'DTXSID2021868',
                'dtxcid': 'DTXCID701868',
                'preferredName': 'p-Xylene',}]
        mocker.return_value = hit

        dtxcid = ['DTXCID501360','DTXCID701868']
        params = {"projection":"chemicaldetailall"}
        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxcid',
                              query=dtxcid,
                              batch_size=1,
                              subset=None)

        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxcid/',
                                       query=dtxcid,
                                       params=params,
                                       batch_size=1)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_details_dtxcid_batch_greater_than_batch_size_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        dtxcid = ['DTXCID501360','DTXCID701868']
        params = {"projection":"ntatoolkit"}
        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxcid',
                              query=dtxcid,
                              batch_size=1,
                              subset='nta')

        
        mocker.assert_called_once_with(endpoint='chemical/detail/search/by-dtxcid/',
                                       query=dtxcid,
                                       params=params,
                                       batch_size=1)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_msready_dtxcid(self,mocker):
        hit = ['DTXSID00184990','DTXSID00370457','DTXSID00454524','DTXSID00480404',
               'DTXSID00566454','DTXSID00578496','DTXSID00746158','DTXSID00749720']
        mocker.return_value = hit

        dtxcid = 'DTXCID30182'
        chem = ctxpy.Chemical()
        result = chem.msready(by='dtxcid',
                              query=dtxcid)

        mocker.assert_called_once_with(endpoint='chemical/msready/search/by-dtxcid/',
                                       query=dtxcid)
        self.assertEqual(result, hit)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_msready_mass(self,mocker):
        hit = ['DTXSID00184990','DTXSID00370457','DTXSID00454524','DTXSID00480404',
               'DTXSID00566454','DTXSID00578496','DTXSID00746158','DTXSID00749720']
        mocker.return_value = hit

        start = 200.9
        end = 200.95
        chem = ctxpy.Chemical()
        result = chem.msready(by='mass',
                              start=start, end=end)

        mocker.assert_called_once_with(endpoint='chemical/msready/search/by-mass/',
                                       query=f'{start}/{end}')
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_msready_formula(self,mocker):
        hit = ['DTXSID00184990','DTXSID00370457','DTXSID00454524','DTXSID00480404',
               'DTXSID00566454','DTXSID00578496','DTXSID00746158','DTXSID00749720']
        mocker.return_value = hit

        formula = 'C16H24N2O5S'
        chem = ctxpy.Chemical()
        result = chem.msready(by='formula',
                              query='C16H24N2O5S')

        mocker.assert_called_once_with(endpoint='chemical/msready/search/by-formula/',
                                       query=formula)
        self.assertEqual(result, hit)


if __name__ == "__main__":
    unittest.main()
