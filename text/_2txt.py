import pandas as pd


def get_excel(file_path: str, sheet_name: str):
    df = pd.read_excel(file_path, sheet_name)
    return df


def get_content_and_author(row) -> tuple:
    content = row["content"]
    index = content.find("\n")
    author = content[:index]
    content = content[index:]
    return content, author
