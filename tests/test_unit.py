import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from analyze_git_csv import *


class UnitTests(unittest.TestCase):
    def test_read_analytics__given_valid_csv_file__then_df_returned(self):
        # Arrange
        input = "tests/data/git_log_analysis.csv"

        # Act
        results = read_git_log_csv(input)
        print(results.columns)
        print(results)

        # Assert
        self.assertEqual(results.shape, (17, 14))

    def test_calculate_file_complexity__given_input_dir_of_files__files_scores_returned(
        self,
    ):
        # Arrange
        input = "tests/data/sample_source_files"

        # Act
        results = calculate_file_complexity(input)

        # Assert
        self.assertEqual(
            results,
            {
                "tests/data/sample_source_files/test_1.py": 22,
                "tests/data/sample_source_files/test_2.py": 67,
            },
        )

    def test_calculate_file_commits__given_simple_test_data__then_correct_data_returned(
        self,
    ):
        # Arrange
        input = "tests/data/git_log_analysis.csv"
        df = read_git_log_csv(input)

        # Act
        results = calculate_file_commits(df)

        # Assert
        self.assertEqual(
            results,
            {
                ".gitignore": 2,
                "README.md": 1,
                "report_template_json.txt": 1,
                "requirements.txt": 1,
                "run_tests.sh": 1,
                "test_and_format.py": 1,
                "tests/analyze_git_csv.py": 1,
                "tests/data/forem_git_log.csv": 1,
                "tests/data/sample_source_files/test_1.py": 3,
                "tests/data/sample_source_files/test_2.py": 3,
                "tests/data/short_sample.csv": 1,
                "tests/test_unit.py": 1,
            },
        )

    def test_determine_hotspot_data__given_simple_data__then_correct_data_returned(
        self,
    ):
        # Arrange
        input = "tests/data/git_log_analysis.csv"
        df = read_git_log_csv(input)
        file_commits = calculate_file_commits(df)
        input = "tests/data/sample_source_files"
        file_complexities = calculate_file_complexity(input)

        # Act
        results = determine_hotspot_data(file_commits, file_complexities)
        print(results)

        # Assert
        expected = [
            FileInfo(file=".gitignore", commits=2, complexity=0, score=0),
            FileInfo(file="README.md", commits=1, complexity=0, score=0),
            FileInfo(file="report_template_json.txt", commits=1, complexity=0, score=0),
            FileInfo(file="requirements.txt", commits=1, complexity=0, score=0),
            FileInfo(file="run_tests.sh", commits=1, complexity=0, score=0),
            FileInfo(file="test_and_format.py", commits=1, complexity=0, score=0),
            FileInfo(file="tests/analyze_git_csv.py", commits=1, complexity=0, score=0),
            FileInfo(
                file="tests/data/forem_git_log.csv", commits=1, complexity=0, score=0
            ),
            FileInfo(
                file="tests/data/sample_source_files/test_1.py",
                commits=3,
                complexity=22,
                score=66,
            ),
            FileInfo(
                file="tests/data/sample_source_files/test_2.py",
                commits=3,
                complexity=67,
                score=201,
            ),
            FileInfo(
                file="tests/data/short_sample.csv", commits=1, complexity=0, score=0
            ),
            FileInfo(file="tests/test_unit.py", commits=1, complexity=0, score=0),
        ]
        self.assertEqual(results, expected)


if __name__ == "__main__":
    unittest.main()
