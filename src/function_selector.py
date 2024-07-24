import pandas as pd

class BaseFunctionSelector:
    """
    Base class for selecting ideal functions based on deviations.
    """
    def __init__(self, train_df, ideal_df):
        self.train_df = train_df
        self.ideal_df = ideal_df

class FunctionSelector(BaseFunctionSelector):
    """
    FunctionSelector class for selecting the best ideal functions.

    Attributes:
        deviation_df (DataFrame): DataFrame to store the deviations.
        best_ideal_functions (DataFrame): DataFrame to store the best ideal functions.
    """
    def __init__(self, train_df, ideal_df):
        super().__init__(train_df, ideal_df)
        self.deviation_df = pd.DataFrame()
        self.best_ideal_functions = pd.DataFrame()

    def calculate_deviations(self):
        """
        Calculate the sum of squared deviations between training data and ideal functions.
        """
        print("Calculating deviations...") 
        try:
            results = []
            for train_col in self.train_df.columns[1:]:
                for ideal_col in self.ideal_df.columns[1:]:
                    deviation = 0
                    for index in range(len(self.train_df)):
                        train_value = self.train_df.at[index, train_col]
                        ideal_value = self.ideal_df.at[index, ideal_col]
                        deviation += (train_value - ideal_value) ** 2

                    results.append((train_col, ideal_col, deviation))      
                        
            self.deviation_df = pd.DataFrame(results, columns=['Train Function', 'Ideal Function', 'Deviation'])

        except KeyError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def select_ideal_functions(self):
        """
        Select the ideal functions that minimize the sum of squared deviations.

        Returns:
            DataFrame: DataFrame containing the best ideal functions for each training function.
        """
        try:
            self.deviation_df = self.deviation_df.sort_values(by='Deviation')
            best_ideal_functions = self.deviation_df.groupby('Train Function').first().reset_index()
            print("Best ideal functions DataFrame:\n", best_ideal_functions)

            # Validate if the selected ideal functions exist in both DataFrame columns
            valid_ideal_functions = best_ideal_functions[
                best_ideal_functions['Ideal Function'].isin(self.ideal_df.columns)
            ]
            valid_ideal_functions = valid_ideal_functions[
                valid_ideal_functions['Train Function'].isin(self.train_df.columns)
            ]
            self.best_ideal_functions = valid_ideal_functions

            print("Selected ideal functions:")
            print(self.best_ideal_functions)

            return self.best_ideal_functions
        except KeyError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise
