import glob
import os
from collections import namedtuple

import pandas as pd


FileInfo = namedtuple("FileInfo", "file commits complexity score")


def read_git_log_csv(filename):
    df = pd.read_csv(filename)
    return df


def calculate_file_complexity(source_path):
    glob_path = source_path + "/*"
    results = {}
    for file in glob.glob(glob_path):
        file_size = os.path.getsize(file)
        results[file] = file_size
    return results


def calculate_file_commits(df):
    results = {}
    file_commits = df.groupby("file")["commit_hash"].count()
    for file in file_commits.index:
        commits = file_commits.loc[file]
        results[file] = commits
    return results


def determine_hotspot_data(file_commits, file_complexities):
    results = []
    for file, commits in file_commits.items():
        file_complexity = file_complexities.get(file, 0)
        results.append(
            FileInfo(file, commits, file_complexity, commits * file_complexity)
        )
    return results


def write_csv_result(file_info):
    with open("git_analysis_result.csv", "w") as results_file:
        results_file.write("file,commits,complexity,score\n")
        for file in file_info:
            results_file.write(
                f'"{file.file}",{file.commits},{file.complexity},{file.score}\n'
            )


def main(csv_file, source_path):
    df = read_git_log_csv(csv_file)
    file_commits = calculate_file_commits(df)
    file_complexities = calculate_file_complexity(source_path)
    hotspot_data = determine_hotspot_data(file_commits, file_complexities)
    write_csv_result(hotspot_data)


if __name__ == "__main__":
    main("tests/data/git_log_analysis.csv", "tests/data/sample_source_files")
