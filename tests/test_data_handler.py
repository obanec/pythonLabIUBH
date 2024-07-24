import unittest
import os
import pandas as pd
from sqlalchemy import create_engine
from src.data_handler import DataHandler

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.train_path = '..data/train.csv'
        self.ideal_path = '..data/ideal.csv'
        self.test_path = '..data/test.csv'
        self.db_path = 'sqlite:///test_data.db'
        self.handler = DataHandler(self.train_path, self.ideal_path, self.test_path, self.db_path)
        
        # Create a small dataset for testing
        self.train_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [1, 2, 3]})
        self.ideal_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [1, 2, 3], 'y3': [0, 1, 2]})
        self.test_data = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 4, 6]})
        
        self.train_data.to_csv(self.train_path, index=False)
        self.ideal_data.to_csv(self.ideal_path, index=False)
        self.test_data.to_csv(self.test_path, index=False)

    def tearDown(self):
        """
        Clean up the test environment.
        """
        if os.path.exists(self.train_path):
            os.remove(self.train_path)
        if os.path.exists(self.ideal_path):
            os.remove(self.ideal_path)
        if os.path.exists(self.test_path):
            os.remove(self.test_path)
        if os.path.exists('test_data.db'):
            os.remove('test_data.db')

    def test_load_data(self):
        """
        Test loading data from CSV files.
        """
        self.handler.load_data()
        train_df = self.handler.get_train_data()
        ideal_df = self.handler.get_ideal_data()
        test_df = self.handler.get_test_data()
        
        self.assertFalse(train_df.empty)
        self.assertFalse(ideal_df.empty)
        self.assertFalse(test_df.empty)
        
        self.assertEqual(len(train_df), 3)
        self.assertEqual(len(ideal_df), 3)
        self.assertEqual(len(test_df), 3)

    def test_save_to_db(self):
        """
        Test saving data to the SQLite database.
        """
        self.handler.load_data()
        self.handler.save_to_db()
        
        engine = create_engine(self.db_path)
        train_df = pd.read_sql('train', engine)
        ideal_df = pd.read_sql('ideal', engine)
        test_df = pd.read_sql('test', engine)
        
        self.assertFalse(train_df.empty)
        self.assertFalse(ideal_df.empty)
        self.assertFalse(test_df.empty)
        
        self.assertEqual(len(train_df), 3)
        self.assertEqual(len(ideal_df), 3)
        self.assertEqual(len(test_df), 3)

    def test_load_data_file_not_found(self):
        """
        Test handling of file not found exception.
        """
        self.handler.train_path = 'non_existent_train.csv'
        with self.assertRaises(FileNotFoundError):
            self.handler.load_data()

    def test_load_data_empty_file(self):
        """
        Test handling of empty file exception.
        """
        with open(self.train_path, 'w') as f:
            pass
        with self.assertRaises(pd.errors.EmptyDataError):
            self.handler.load_data()

    def test_load_data_parse_error(self):
        """
        Test handling of parse error exception.
        """
        with open(self.train_path, 'w') as f:
            f.write("x,y1,y2\n1,2,a\n2,4,2\n3,6,3")
        with self.assertRaises(pd.errors.ParserError):
            self.handler.load_data()

if __name__ == '__main__':
    unittest.main()
