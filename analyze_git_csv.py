import glob
import os
import json
import sys
from collections import namedtuple

import pandas as pd

FileInfo = namedtuple("FileInfo", "file commits complexity score")


def read_git_log_csv(filename):
    df = pd.read_csv(filename)
    return df


def calculate_file_complexity(source_path):
    glob_path = source_path + "/**/*.*"
    print(glob_path)
    results = {}

    for file in glob.glob(glob_path, recursive=True):
        file_size = os.path.getsize(file)
        relative_file = file.replace(source_path + "/", "")
        print(relative_file)
        results[relative_file] = file_size
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
        if file_complexity == 0:
            print(f"can't find '{file}'")
            pass
        else:
            # print(f"found '{file}': {file_complexity}")
            new_file = FileInfo(
                file=file,
                commits=commits,
                complexity=file_complexity,
                score=int(commits * file_complexity),
            )
            results.append(new_file)
            print(new_file)
    return results


def write_csv_result(file_info):
    with open("git_analysis_result.csv", "w") as results_file:
        results_file.write("file,commits,complexity,score\n")
        for file in file_info:
            results_file.write(
                f'"{file.file}",{file.commits},{file.complexity},{file.score}\n'
            )


def main(csv_file, source_path):
    print(f"csv_file: {csv_file}")
    print(f"source_path: {source_path}")
    df = read_git_log_csv(csv_file)
    file_commits = calculate_file_commits(df)
    print(f"Read file commits: {len(file_commits)}")

    file_complexities = calculate_file_complexity(source_path)
    print(f"Read file complexities: {len(file_complexities)}")

    hotspot_data = determine_hotspot_data(file_commits, file_complexities)
    write_csv_result(hotspot_data)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
