import unittest

from chemical_test import TestChemical
from exposure_test import TestExposure

loader = unittest.TestLoader()
suite = unittest.TestSuite([loader.loadTestsFromTestCase(TestChemical),
                            loader.loadTestsFromTestCase(TestExposure)])
runner = unittest.TextTestRunner()
results = runner.run(suite)

