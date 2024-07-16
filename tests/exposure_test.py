import unittest
import time
import ctxpy as ctx


class TestChemical(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._conn = ctx.Exposure()
        
    def tearDown(self):
        time.sleep(3)

    def test_connection(self):
        self.assertEqual(self._conn.host, "https://api-ccte.epa.gov/")
        self.assertEqual(self._conn.headers["accept"], "application/json")
        self.assertIsNotNone(self._conn.headers['x-api-key'])
        self.assertEqual(self._conn.kind,'exposure')



if __name__ == "__main__":
    unittest.main()