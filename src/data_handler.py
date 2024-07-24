import pandas as pd
from sqlalchemy import create_engine

class BaseDataHandler:
    """
    Base class for handling data loading and saving operations.
    """
    def __init__(self, db_path='sqlite:///data.db'):
        self.db_path = db_path
        self.engine = create_engine(self.db_path)

class DataHandler(BaseDataHandler):
    """
    DataHandler class for loading and saving CSV data to a SQLite database.

    Attributes:
        train_path (str): Path to the training data CSV file.
        ideal_path (str): Path to the ideal functions CSV file.
        test_path (str): Path to the test data CSV file.
    """
    def __init__(self, train_path, ideal_path, test_path, db_path='sqlite:///data.db'):
        super().__init__(db_path)
        self.train_path = train_path
        self.ideal_path = ideal_path
        self.test_path = test_path

    def load_data(self):
        """
        Load data from CSV files into pandas DataFrames.
        """
        try:
            self.train_df = pd.read_csv(self.train_path)
            self.ideal_df = pd.read_csv(self.ideal_path)
            self.test_df = pd.read_csv(self.test_path)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise
        except pd.errors.EmptyDataError as e:
            print(f"Error: {e}")
            raise
        except pd.errors.ParserError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def save_to_db(self):
        """
        Save pandas DataFrames to SQLite database.
        """
        try:
            self.train_df.to_sql('train', self.engine, if_exists='replace', index=False)
            self.ideal_df.to_sql('ideal', self.engine, if_exists='replace', index=False)
            self.test_df.to_sql('test', self.engine, if_exists='replace', index=False)
        except Exception as e:
            print(f"An error occurred while saving to the database: {e}")
            raise

    def get_train_data(self):
        """
        Get the training data DataFrame.

        Returns:
            DataFrame: Training data.
        """
        return self.train_df

    def get_ideal_data(self):
        """
        Get the ideal functions data DataFrame.

        Returns:
            DataFrame: Ideal functions data.
        """
        return self.ideal_df

    def get_test_data(self):
        """
        Get the test data DataFrame.

        Returns:
            DataFrame: Test data.
        """
        return self.test_df
