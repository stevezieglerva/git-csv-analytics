import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from analyze_git_csv import *


class UnitTests(unittest.TestCase):
    def test_read_analytics__given_valid_csv_file__then_df_returned(self):
        # Arrange
        input = "tests/data/short_sample.csv"

        # Act
        results = read_analytics(input)
        print(results.columns)
        print(results)

        # Assert
        self.assertEqual(results.shape, (1, 14))

    def test_calculate_file_complexity__given_input_dir_of_files__files_scores_returned(self):
        # Arrange
    
        # Act
    
        # Assert
    
        

if __name__ == "__main__":
    unittest.main()
