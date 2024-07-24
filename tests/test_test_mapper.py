import unittest
import pandas as pd
from src.test_mapper import TestMapper

class TestTestMapper(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.test_data = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 4, 6]})
        self.ideal_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [1, 2, 3], 'y3': [0, 1, 2]})
        self.train_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [1, 2, 3], 'y3': [0, 1, 2]})
        self.best_ideal_functions = pd.DataFrame({
            'Train Function': ['y1', 'y2'],
            'Ideal Function': ['y1', 'y2'],
            'Deviation': [0, 0]
        })
        self.mapper = TestMapper(self.test_data, self.ideal_data, self.train_data, self.best_ideal_functions)

    def test_map_test_data(self):
        """
        Test mapping of test data to the selected ideal functions.
        """
        test_results_df = self.mapper.map_test_data()

        self.assertFalse(test_results_df.empty)
        self.assertEqual(len(test_results_df), 3)  # 3 test points

        expected_ideal_functions = ['y1', 'y1', 'y1']
        for index, row in test_results_df.iterrows():
            self.assertEqual(row['Ideal Function'], expected_ideal_functions[index])

    def test_map_test_data_key_error(self):
        """
        Test handling of key error exception during test data mapping.
        """
        self.mapper.ideal_df = pd.DataFrame({'a': [1, 2, 3], 'b': [2, 4, 6]})
        with self.assertRaises(KeyError):
            self.mapper.map_test_data()

    def test_map_test_data_unexpected_error(self):
        """
        Test handling of unexpected exception during test data mapping.
        """
        self.mapper.best_ideal_functions = pd.DataFrame({'Train Function': ['y1'], 'Deviation': [0]})
        with self.assertRaises(Exception):
            self.mapper.map_test_data()

if __name__ == '__main__':
    unittest.main()
