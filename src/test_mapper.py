import pandas as pd

class BaseTestMapper:
    """
    Base class for mapping test data to ideal functions.
    """
    def __init__(self, test_df, ideal_df, train_df, best_ideal_functions):
        self.test_df = test_df
        self.ideal_df = ideal_df
        self.train_df = train_df
        self.best_ideal_functions = best_ideal_functions

class TestMapper(BaseTestMapper):
    """
    TestMapper class for mapping test data to the best ideal functions.

    Attributes:
        test_results_df (DataFrame): DataFrame to store the mapping results.
    """
    def __init__(self, test_df, ideal_df, train_df, best_ideal_functions):
        super().__init__(test_df, ideal_df, train_df, best_ideal_functions)
        self.test_results_df = pd.DataFrame()

    def map_test_data(self):
        """
        Map test data to the selected ideal functions based on the deviation criterion.

        Returns:
            DataFrame: DataFrame containing the test data mapped to the ideal functions with deviations.
        """
        try:
            test_results = []
            for index, row in self.test_df.iterrows():
                x_value = row['x']
                y_value = row['y']
                for _, ideal_row in self.best_ideal_functions.iterrows():
                    ideal_func = ideal_row['Ideal Function']
                    train_func = ideal_row['Train Function']
                    max_deviation = ((self.ideal_df[ideal_func] - self.train_df[train_func]) ** 2).max() ** 0.5
                    if abs(y_value - self.ideal_df.loc[self.ideal_df['x'] == x_value, ideal_func].values[0]) <= max_deviation * (2 ** 0.5):
                        test_results.append((x_value, y_value, y_value - self.ideal_df.loc[self.ideal_df['x'] == x_value, ideal_func].values[0], ideal_func, train_func))
                        break
            self.test_results_df = pd.DataFrame(test_results, columns=['x', 'y', 'Delta y', 'Ideal Function', 'Train Function'])
            return self.test_results_df
        except KeyError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise
