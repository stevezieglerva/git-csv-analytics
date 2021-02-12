import glob
import os

import pandas as pd


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
    file_commits = df.groupby("file")["commit_hash"].count()
    # file_commits = df.groupby(["file"]).max()
    print("\n\n___")
    print(file_commits)
    return file_commits
