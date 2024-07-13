import sys
import os
import multiprocessing

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from mysql_script.mysql_op import *
from text._2txt import *
from ckg import *
from text.sparkAPI import *


def init_row(index, row):
    content = row["content"].replace("'", "\\'")

    llm_res = get_Author_and_From(content)

    author = llm_res["作者"]
    from_ = llm_res["来源"]
    title = row["title"]

    dict_with_shash = init(content=content, name=title, idx=index)
    # 进行入库
    for item in dict_with_shash:
        item["title"] = title
        item["author"] = author
        item["`from`"] = from_
        print(item)
        mysql_insert("corpus", item)


if __name__ == "__main__":
    file_path = "text/excel/SmoothNLP专栏资讯数据集样本10k.xlsx"
    df = get_excel(file_path, "Sheet1")

    # TODO 使用多进程进行灌库

    indexs = [A for A, _ in df.iterrows()]
    rows = [B for _, B in df.iterrows()]

    with multiprocessing.Pool(processes=3) as pool:
        # 使用map方法将任务分配到进程池中
        results = pool.starmap(init_row, zip(indexs, rows))
