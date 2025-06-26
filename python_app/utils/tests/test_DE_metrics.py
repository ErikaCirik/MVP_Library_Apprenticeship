import unittest
import pandas as pd
from utils.DE_metrics import get_num_customers, get_num_books, get_num_api_requests

class TestDEMetrics(unittest.TestCase):
    def test_get_num_customers(self):
        df = pd.DataFrame({'Customer ID': [1, 2, 2, 3, 4, 4]})
        self.assertEqual(get_num_customers(df), 4)
        df_empty = pd.DataFrame({})
        self.assertEqual(get_num_customers(df_empty), 0)

    def test_get_num_books(self):
        df = pd.DataFrame({'Books': ['A', 'B', 'A', 'C', 'B']})
        self.assertEqual(get_num_books(df), 3)
        df_empty = pd.DataFrame({})
        self.assertEqual(get_num_books(df_empty), 0)

    def test_get_num_api_requests(self):
        df = pd.DataFrame({'col': [1, 2, 3]})
        self.assertEqual(get_num_api_requests(df), 3)
        df_empty = pd.DataFrame({})
        self.assertEqual(get_num_api_requests(df_empty), 0)

if __name__ == '__main__':
    unittest.main()
