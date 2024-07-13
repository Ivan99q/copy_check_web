import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from mysql_script.mysql_op import *
from text._2txt import *
from ckg import *


if __name__ == "__main__":
    file_path = "text/excel/SmoothNLP专栏资讯数据集样本10k.xlsx"
    df = get_excel(file_path, "Sheet1")
    for index, row in df.iterrows():
        content, author = get_content_and_author(row)
        id = row["id"]
        title = row["title"]
        dict_with_shash = init(content=content, name=title, idx=id)
        # 进行入库
        for item in dict_with_shash:
            item["id"] = id
            item["title"] = title
            item["author"] = author
            print(item)
            mysql_insert("corpus", item)
