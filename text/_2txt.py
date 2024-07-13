import pandas as pd


def get_excel(file_path: str, sheet_name: str):
    df = pd.read_excel(file_path, sheet_name)
    return df


