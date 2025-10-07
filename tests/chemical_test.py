import unittest
from unittest.mock import patch
import ctxpy

class TestChemical(unittest.TestCase):


    @patch('ctxpy.base.CTXConnection.get')
    def test_search_equals(self, mocker):
        # Mock the response from the get method
        mocker.return_value = [{'dtxsid': 'DTXSID7021360',
                                'preferredName': 'Toluene'}]

        chem = ctxpy.Chemical()
        result = chem.search(by='equals', word='toluene')

        # Assertions to verify the behavior
        mocker.assert_called_once_with(suffix='chemical/search/equal/toluene')
        self.assertEqual(result, [{'dtxsid': 'DTXSID7021360',
                                   'preferredName': 'Toluene'}])


    @patch('ctxpy.base.CTXConnection.get')
    def test_search_starts_with(self, mocker):
        # Mock the response from the get method
        mocker.return_value = [{'dtxsid': 'DTXSID7021360', 'preferredName': 'Toluene'}]

        chem = ctxpy.Chemical()
        result = chem.search(by='starts-with', word='toluene')

        # Assertions to verify the behavior
        mocker.assert_called_once_with(suffix='chemical/search/start-with/toluene')
        self.assertEqual(result, [{'dtxsid': 'DTXSID7021360',
                                   'preferredName': 'Toluene'}])


    @patch('ctxpy.base.CTXConnection.get')
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

        chem = ctxpy.Chemical()
        result = chem.search(by='contains', word='toluene')

        # Assertions to verify the behavior
        mocker.assert_called_once_with(suffix='chemical/search/contain/toluene')
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_search_batch_greater_than_batch_size(self, mocker):
        hit = [{'dtxsid': 'DTXSID7021360',
                'preferredName': 'Toluene'},
               {'dtxsid': 'DTXSID001009823',
                'preferredName': 'Balsams, tolu'}]
        # Mock the response from the get method
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.search(by='batch',
                             word=['DTXSID7021360', 'DTXSID001009823'],
                             batch_size=1)

        # Assertions to verify the behavior
        mocker.assert_called_once_with(suffix='chemical/search/equal/',
                                       word=['DTXSID7021360',
                                             'DTXSID001009823'],
                                       batch_size=1,
                                       bracketed=False)
        self.assertEqual(result, hit)


    @patch('ctxpy.base.CTXConnection.batch')
    def test_search_batch_less_than_batch_size(self, mocker):
        hit = [{'dtxsid': 'DTXSID7021360',
                'preferredName': 'Toluene'},
               {'dtxsid': 'DTXSID001009823',
                'preferredName': 'Balsams, tolu'}]
        # Mock the response from the get method
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.search(by='batch',
                             word=['DTXSID7021360',
                                   'DTXSID001009823'])

        # Assertions to verify the behavior
        mocker.assert_called_once_with(suffix='chemical/search/equal/',
                                       word=['DTXSID7021360','DTXSID001009823'],
                                       batch_size=200,
                                       bracketed=False)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.get')
    def test_details_dtxsid_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}

        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='dtxsid',word='DTXSID7021360',subset=None)

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxsid/DTXSID7021360')
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.get')
    def test_details_dtxsid_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='dtxsid',word='DTXSID7021360',subset='nta')

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxsid/DTXSID7021360?projection=ntatoolkit')
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_details_dtxsid_batch_less_than_batch_size_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxsid',
                              word=['DTXSID7021360', 'DTXSID001009823'],
                              subset=None)

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxsid/',
                                       word=["DTXSID7021360","DTXSID001009823"],
                                       batch_size=1000,
                                       bracketed=True)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_details_dtxsid_batch_less_than_batch_size_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxsid',
                              word=['DTXSID7021360', 'DTXSID001009823'],
                              subset='nta')

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxsid/?projection=ntatoolkit',
                                       word=["DTXSID7021360","DTXSID001009823"],
                                       batch_size=1000,
                                       bracketed=True)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_details_dtxsid_batch_greater_than_batch_size_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxsid',
                              word=['DTXSID7021360', 'DTXSID001009823'],
                              batch_size=1,
                              subset=None)

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxsid/',
                                       word=['DTXSID7021360', 'DTXSID001009823'],
                                       batch_size=1,
                                       bracketed=True)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_details_dtxsid_batch_greater_than_batch_size_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxsid',
                              word=['DTXSID7021360', 'DTXSID001009823'],
                              batch_size=1,
                              subset='nta')

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxsid/?projection=ntatoolkit',
                                       word=['DTXSID7021360', 'DTXSID001009823'],
                                       batch_size=1,
                                       bracketed=True)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.get')
    def test_details_dtxcid_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='dtxcid',word='DTXCID501360',subset=None)

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxcid/DTXCID501360')
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.get')
    def test_details_dtxcid_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='dtxcid',word='DTXCID501360',subset='nta')

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxcid/DTXCID501360?projection=ntatoolkit')
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_details_dtxcid_batch_less_than_batch_size_no_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxcid',word=['DTXCID501360','DTXCID701868'],subset=None)

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxcid/',
                                       word=["DTXCID501360","DTXCID701868"],
                                       batch_size=1000,
                                       bracketed=True)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_details_dtxcid_batch_less_than_batch_size_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxcid',
                              word=['DTXCID501360','DTXCID701868'],
                              subset='nta')

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxcid/?projection=ntatoolkit',
                                       word=["DTXCID501360","DTXCID701868"],
                                       batch_size=1000,
                                       bracketed=True)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_details_dtxscid_batch_greater_than_batch_size_no_subset(self,mocker):
        hit = [{"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'},
               {'inchikey': 'URLKBWYHVLBVBO-UHFFFAOYSA-N',
                'dtxsid': 'DTXSID2021868',
                'dtxcid': 'DTXCID701868',
                'preferredName': 'p-Xylene',}]
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxcid',
                              word=['DTXCID501360','DTXCID701868'],
                              batch_size=1,
                              subset=None)

        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxcid/',
                                       word=['DTXCID501360','DTXCID701868'],
                                       batch_size=1,
                                       bracketed=True)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.batch')
    def test_details_dtxcid_batch_greater_than_batch_size_nta_subset(self,mocker):
        hit = {"inchikey":"YXFVVABEGXRONW-UHFFFAOYSA-N",
               'dtxsid': 'DTXSID7021360',
               'dtxcid': 'DTXCID501360',
               'preferredName': 'Toluene'}
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.details(by='batch-dtxcid',
                              word=['DTXCID501360','DTXCID701868'],
                              batch_size=1,
                              subset='nta')

        
        mocker.assert_called_once_with(suffix='chemical/detail/search/by-dtxcid/?projection=ntatoolkit',
                                       word=['DTXCID501360','DTXCID701868'],
                                       batch_size=1,
                                       bracketed=True)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.get')
    def test_msready_dtxsid(self,mocker):
        hit = ['DTXSID00184990','DTXSID00370457','DTXSID00454524','DTXSID00480404',
               'DTXSID00566454','DTXSID00578496','DTXSID00746158','DTXSID00749720']
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.msready(by='dtxcid',
                              word='DTXCID30182')

        mocker.assert_called_once_with(suffix='chemical/msready/search/by-dtxcid/DTXCID30182')
        self.assertEqual(result, hit)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.get')
    def test_msready_mass(self,mocker):
        hit = ['DTXSID00184990','DTXSID00370457','DTXSID00454524','DTXSID00480404',
               'DTXSID00566454','DTXSID00578496','DTXSID00746158','DTXSID00749720']
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.msready(by='mass',
                              start=200.9, end=200.95)

        mocker.assert_called_once_with(suffix='chemical/msready/search/by-mass/200.9/200.95')
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.get')
    def test_msready_formula(self,mocker):
        hit = ['DTXSID00184990','DTXSID00370457','DTXSID00454524','DTXSID00480404',
               'DTXSID00566454','DTXSID00578496','DTXSID00746158','DTXSID00749720']
        mocker.return_value = hit

        chem = ctxpy.Chemical()
        result = chem.msready(by='formula',
                              word='C16H24N2O5S')

        mocker.assert_called_once_with(suffix='chemical/msready/search/by-formula/C16H24N2O5S')
        self.assertEqual(result, hit)


if __name__ == "__main__":
    unittest.main()
