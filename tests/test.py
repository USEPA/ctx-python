import unittest

from chemical_test import TestChemical
from exposure_test import TestExposure
from hazard_test import TestHazard

loader = unittest.TestLoader()
suite = unittest.TestSuite([loader.loadTestsFromTestCase(TestChemical),
                            loader.loadTestsFromTestCase(TestExposure),
                            loader.loadTestsFromTestCase(TestHazard)])
runner = unittest.TextTestRunner()
results = runner.run(suite)

