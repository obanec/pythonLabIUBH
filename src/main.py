import sys
import os

# Add the parent directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_handler import DataHandler
from src.function_selector import FunctionSelector
from src.test_mapper import TestMapper
from src.visualizer import Visualizer

class Main:
    """
    Main class to orchestrate the data loading, processing, and visualization tasks.
    """
    def __init__(self, train_path, ideal_path, test_path):
        self.data_handler = DataHandler(train_path, ideal_path, test_path)

    def run(self):
        """
        Run the main process: load data, calculate deviations, select ideal functions,
        map test data, and visualize results.
        """
        try:
            # Load and save data
            self.data_handler.load_data()
            self.data_handler.save_to_db()

            # Get data
            train_df = self.data_handler.get_train_data()
            ideal_df = self.data_handler.get_ideal_data()

            # Calculate deviations and select ideal functions
            selector = FunctionSelector(train_df, ideal_df)
            selector.calculate_deviations()
            best_ideal_functions = selector.select_ideal_functions()

            # Map test data to ideal functions
            test_df = self.data_handler.get_test_data()
            mapper = TestMapper(test_df, ideal_df, train_df, best_ideal_functions)
            test_results_df = mapper.map_test_data()

            # Visualize results
            visualizer = Visualizer(train_df, ideal_df, test_results_df)
            visualizer.visualize()
        
        except Exception as e:
            print(f"An error occurred during the main process: {e}")
            raise

if __name__ == "__main__":
    # Determine absolute paths based on the location of this script
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    train_path = os.path.join(base_path, 'data/train.csv')
    ideal_path = os.path.join(base_path, 'data/ideal.csv')
    test_path = os.path.join(base_path, 'data/test.csv')

    main = Main(train_path, ideal_path, test_path)
    main.run()
