import unittest
from unittest.mock import patch
import ctxpy

class TestChemicalLists(unittest.TestCase):

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_list_types(self, mocker):
        hit = ["federal",
               'international',
               'other',
               'state']
        mocker.return_value = hit
        endpoint = 'chemical/list/type'

        clist = ctxpy.ChemicalList()
        result = clist.get_list_types()

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_all_list_meta_dtxsid(self, mocker):
        hit = [{"visibility": "PUBLIC",
                "id": 950,
                "type": "federal",
                "label": ("40 CFR 116.4 Designation of Hazardous Substances "
                          "(Above Ground Storage Tanks)"),
                "longDescription": ("Hazardous Substance List associated with the "
                                    "Federal Water Pollution Control Act, as amended "
                                    "by the Federal Water Pollution Control Act "
                                    "Amendments of 1972 (Pub. L. 92-500), and as "
                                    "further amended by the Clean Water Act of 1977 "
                                    "(Pub. L. 95-217), 33 U.S.C. 1251 et seq.; and as "
                                    "further amended by the Clean Water Act Amendments "
                                    "of 1978 (Pub. L. 95-676)"),
                "dtxsids": ("DTXSID901023224,DTXSID101022327,"
                            "DTXSID901014471,DTXSID501014962,DTXSID3032626"),
                "listName": "40CFR1164",
                "chemicalCount": 333,
                "createdAt": "2020-06-25T16:01:14Z",
                "updatedAt": "2022-05-16T14:02:18Z",
                "shortDescription": "Hazardous Substance List (40 CFR 116.4)"},
                {"visibility": "PUBLIC",
                "id": 561,
                "type": "other",
                "label": "LIST: Periodic Table of Elements",
                "longDescription": ("The list of all elements in the periodic table "
                                    "of element up to atomic number 108"),
                "dtxsids":("DTXSID7036402,DTXSID5036761,DTXSID4023913,DTXSID3023922,"
                           "DTXSID9027651,DTXSID40912315,DTXSID00170378,"
                           "DTXSID60872462"),
                "listName": "ELEMENTS",
                "chemicalCount": 108,
                "createdAt": "2018-11-11T00:01:40Z",
                "updatedAt": "2023-12-16T00:26:51Z",
                "shortDescription": ("The list of all elements in the periodic "
                                        "table of elements")}]
        mocker.return_value = hit
        query = None
        endpoint = 'chemical/list/'
        
        clist = ctxpy.ChemicalList()
        result = clist.get_all_list_meta(output='dtxsid')

        # Assertions to verify the behavior
        params = {'projection':'chemicallistwithdtxsids'}
        mocker.assert_called_once_with(endpoint=endpoint,
                                       params=params)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_list_by_type_meta_listname(self, mocker):
        hit = [{"listName": "40CFR1164"},
               {"listName": "40CFR302"},
               {"listName": "40CFR355"},
               {"listName": "AEGLVALUES"},
               {"listName": "ANTIMICROBIALS"},
               {"listName": "ASPECT"},
               {"listName": "ATSDRLST"},]
        mocker.return_value = hit
        query = 'federal'
        endpoint = 'chemical/list/search/by-type/'

        clist = ctxpy.ChemicalList()
        result = clist.get_list_meta_by_type(list_type=query,output='list-name')

        params = {"projection":"chemicallistname"}
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=query,
                                       params=params)
        self.assertEqual(result, hit)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_list_by_name_meta_all(self, mocker):
        hit = {"visibility": "PUBLIC",
                "id": 561,
                "type": "other",
                "label": "LIST: Periodic Table of Elements",
                "longDescription": ("The list of all elements in the periodic table "
                                    "of element up to atomic number 108"),
                "listName": "ELEMENTS",
                "chemicalCount": 108,
                "createdAt": "2018-11-11T00:01:40Z",
                "updatedAt": "2023-12-16T00:26:51Z",
                "shortDescription": ("The list of all elements in the periodic "
                                     "table of elements")}
        mocker.return_value = hit
        query = 'elements'
        
        endpoint = 'chemical/list/search/by-name/'

        clist = ctxpy.ChemicalList()
        result = clist.get_list_meta_by_name(list_name=query,output='all')

        params = {"projection":"chemicallistall"}
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=query,
                                       params=params)
        self.assertEqual(result, hit)

    @patch('ctxpy.chemical_list.ChemicalList._join_query')
    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_filter_list_by_chemicals_contains(self, mock_ctx_call,mock_join_query):
        hit = ["DTXSID00170378",
               "DTXSID00225392",
               "DTXSID0049658",
               "DTXSID0049816",
               "DTXSID0049818",
               "DTXSID0051441",
               "DTXSID0058641",
               "DTXSID0064674",
               "DTXSID0064676",
               "DTXSID0064678"]
        mock_ctx_call.return_value = hit
        list_name = 'elements'
        chem_filter = 'ma'
        mock_join_query.return_value = 'elements/ma'
        endpoint = 'chemical/list/chemicals/search/contain/'

        clist = ctxpy.ChemicalList()
        result = clist.filter_list_by_chemicals(how='contains',
                                                list_name=list_name,
                                                chem_filter=chem_filter)

        # Assertions to verify the behavior
        mock_ctx_call.assert_called_once_with(endpoint=endpoint,
                                              query={"list":list_name,
                                                     "word":chem_filter},
                                              quote_method=mock_join_query)
        self.assertEqual(result, hit)

    @patch('ctxpy.chemical_list.ChemicalList._join_query')
    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_filter_list_by_chemicals_starts_with(self, mock_ctx_call, mock_join_query):
        hit = ["DTXSID00170378",
               "DTXSID00225392",
               "DTXSID0049658",
               "DTXSID0049816",
               "DTXSID0049818",
               "DTXSID0051441",
               "DTXSID0058641",
               "DTXSID0064674",
               "DTXSID0064676",
               "DTXSID0064678"]
        mock_ctx_call.return_value = hit
        list_name = 'elements'
        chem_filter = 'ma'
        mock_join_query.return_value = 'elements/ma'
        endpoint = 'chemical/list/chemicals/search/start-with/'

        clist = ctxpy.ChemicalList()
        result = clist.filter_list_by_chemicals(how='starts-with',
                                                chem_filter=chem_filter,
                                                list_name=list_name)

        # Assertions to verify the behavior
        mock_ctx_call.assert_called_once_with(endpoint=endpoint,
                                              query={"list":list_name,
                                                     "word":chem_filter},
                                              quote_method=mock_join_query)
        self.assertEqual(result, hit)

    @patch('ctxpy.chemical_list.ChemicalList._join_query')
    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_filter_list_by_chemicals_equals(self, mock_ctx_call, mock_join_query):
        hit = ["DTXSID00170378",
               "DTXSID00225392",
               "DTXSID0049658",
               "DTXSID0049816",
               "DTXSID0049818",
               "DTXSID0051441",
               "DTXSID0058641",
               "DTXSID0064674",
               "DTXSID0064676",
               "DTXSID0064678"]
        mock_ctx_call.return_value = hit
        list_name = 'elements'
        chem_filter = 'ma'
        mock_join_query.return_value = 'elements/ma'
        endpoint = 'chemical/list/chemicals/search/equal/'

        clist = ctxpy.ChemicalList()
        result = clist.filter_list_by_chemicals(how='equals', 
                                                list_name=list_name,
                                                chem_filter=chem_filter)

        # Assertions to verify the behavior
        mock_ctx_call.assert_called_once_with(endpoint=endpoint,
                                              query={"list":list_name,
                                                     "word":chem_filter},
                                              quote_method=mock_join_query)
        self.assertEqual(result, hit)

    @patch('ctxpy.base.CTXConnection.ctx_call')
    def test_get_list(self, mocker):
        hit = ["DTXSID00170378",
               "DTXSID00225392",
               "DTXSID0049658",
               "DTXSID0049816",
               "DTXSID0049818",
               "DTXSID0051441",
               "DTXSID0058641",
               "DTXSID0064674",
               "DTXSID0064676",
               "DTXSID0064678"]
        mocker.return_value = hit
        query = 'elements'
        endpoint = 'chemical/list/chemicals/search/by-listname/'

        clist = ctxpy.ChemicalList()
        result = clist.get_list(list_name=query)

        # Assertions to verify the behavior
        mocker.assert_called_once_with(endpoint=endpoint,
                                       query=query)
        self.assertEqual(result, hit)




if __name__ == "__main__":
    unittest.main()
