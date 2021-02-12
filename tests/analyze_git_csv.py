import pandas as pd


def read_analytics(filename):
    df = pd.read_csv(filename)
    return df
