import datetime
import sys
import os
import multiprocessing
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from sql_script.mysql_op import *
from text._2txt import *
from ckg import *
from text.sparkAPI import *

global start_time
start_time = time.time()


def processing_bar(total):
    global done
    progress = (done + 1) / total
    bar_length = 50
    block = int(round(bar_length * progress))
    now_time = time.time()
    runtime = now_time - start_time
    runtime = datetime.timedelta(seconds=int(runtime))
    text = f"\r处理进度: [{'=' * block}{' ' * (bar_length - block)}] {int(progress) * 100}%\t{runtime}"
    if done == total:
        text = f"\r处理进度: [{'=' * bar_length}] 100.0%\t{runtime}"
    sys.stdout.write(text)
    sys.stdout.flush()


def running_time():
    now_time = time.time()
    runtime = now_time - start_time
    runtime = datetime.timedelta(seconds=int(runtime))
    text = str(runtime)
    sys.stdout.write(text)
    sys.stdout.flush()
    return runtime


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
        running_time()


if __name__ == "__main__":
    file_path = "text/excel/SmoothNLP专栏资讯数据集样本10k.xlsx"
    df = get_excel(file_path, "Sheet1")

    # 使用多进程进行灌库

    indexs = [A for A, _ in df.iterrows()]
    rows = [B for _, B in df.iterrows()]

    total = [len(indexs) for _ in range(len(indexs))]
    with multiprocessing.Pool(processes=24) as pool:
        # 使用map方法将任务分配到进程池中
        pool.starmap(init_row, zip(indexs, rows))
