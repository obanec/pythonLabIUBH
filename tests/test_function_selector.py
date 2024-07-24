import unittest
import pandas as pd
from src.function_selector import FunctionSelector

class TestFunctionSelector(unittest.TestCase):
    def setUp(self):
        self.train_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [1, 2, 3]})
        self.ideal_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [1, 2, 3], 'y3': [0, 1, 2]})
        self.selector = FunctionSelector(self.train_data, self.ideal_data)

    def test_calculate_deviations(self):
        self.selector.calculate_deviations()
        deviation_df = self.selector.deviation_df

        self.assertFalse(deviation_df.empty)
        self.assertEqual(len(deviation_df), 6) 

    def test_select_ideal_functions(self):
        self.selector.calculate_deviations()
        best_ideal_functions = self.selector.select_ideal_functions()

        self.assertFalse(best_ideal_functions.empty)
        self.assertEqual(len(best_ideal_functions), 2)  

    def test_calculate_deviations_key_error(self):
        self.selector.train_df = pd.DataFrame({'a': [1, 2, 3], 'b': [2, 4, 6]})
        with self.assertRaises(KeyError):
            self.selector.calculate_deviations()

    def test_select_ideal_functions_key_error(self):
        self.selector.calculate_deviations()
        self.selector.deviation_df = pd.DataFrame({'a': [1], 'b': [2]})
        with self.assertRaises(KeyError):
            self.selector.select_ideal_functions()

if __name__ == '__main__':
    unittest.main()
