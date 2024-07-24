import unittest
import pandas as pd
from bokeh.plotting import figure
from src.visualizer import Visualizer

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.train_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [1, 2, 3]})
        self.ideal_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [1, 2, 3]})
        self.test_results_data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [2, 4, 6],
            'Delta y': [0, 0, 0],
            'Ideal Function': ['y1', 'y1', 'y1'],
            'Train Function': ['y1', 'y1', 'y1']
        })
        self.visualizer = Visualizer(self.train_data, self.ideal_data, self.test_results_data)

    def test_visualize(self):
        """
        Test visualization setup.
        """
        try:
            self.visualizer.visualize()
        except Exception as e:
            self.fail(f"Visualizer raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
