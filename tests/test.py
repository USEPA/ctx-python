import unittest

from chemical_test import TestChemical
from exposure_test import TestExposure
from hazard_test import TestHazard
from chemical_list_test import TestChemicalLists
from utilities_test import TestUtilities

loader = unittest.TestLoader()
suite = unittest.TestSuite([
                            loader.loadTestsFromTestCase(TestUtilities),
                            loader.loadTestsFromTestCase(TestChemical),
                            loader.loadTestsFromTestCase(TestChemicalLists),
                            loader.loadTestsFromTestCase(TestExposure),
                            loader.loadTestsFromTestCase(TestHazard)
                            ])
runner = unittest.TextTestRunner()
results = runner.run(suite)

