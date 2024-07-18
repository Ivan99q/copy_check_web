import datetime
import sys
import os
import multiprocessing
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from sql_script.postgresql_op import *
from sql_script.mysql_op import *
from text._2txt import *
from ckg import *
from text.sparkAPI import *

global start_time
start_time = time.time()
global done
done = 0


def processing_bar():
    total = 147415
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


def init_by_para(para: dict):
    sentence = []
    c = para["content"]
    while c.find("。") != -1:
        sentence.append(c[: c.find("。") + 1])
        c = c[c.find("。") + 1 :]
    sentence.append(c)
    for s in sentence:
        shash = simhash(s, "init_database/stop_words.txt")
        if shash == "":
            continue
        v = []
        for i in shash:
            v.append(int(i))
        mhash = minhash(s, "init_database/stop_words.txt")
        data = {
            "title": para["title"],
            "sentence": s,
            "author": para["author"],
            '"from"': para["`from`"],
            "shash": str(v),
            "mhash": str(mhash),
        }
        postgresql_insert("corpus_sentence", data)
        processing_bar()


if __name__ == "__main__":
    paras = mysql_select("corpus", {})
    paras = [
        {
            "title": para[3],
            "content": para[2],
            "author": para[4],
            "`from`": para[5],
        }
        for para in paras
    ]
    print("查询成功")
    with multiprocessing.Pool(processes=24) as pool:
        pool.map(init_by_para, paras)
