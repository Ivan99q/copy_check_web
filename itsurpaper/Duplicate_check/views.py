from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from sql_script.mysql_op import *
from sql_script.postgresql_op import *
from init_database.ckg import *

import multiprocessing


def index(request):
    return render(request, "index.html")


@csrf_exempt
def submit(request):
    if request.method == "POST":
        data = {
            "title": request.POST.get("title", ""),
            "author": request.POST.get("author", ""),
            "content": request.POST.get("content", ""),
        }

        context = {
            "author": data["author"],
            "title": data["title"],
            "original_content": spilt_content(data["content"]),
        }

        # 计算simhash
        s_hash = shash(data["content"])

        items = select_by_simhash(s_hash["paragraphs"])

        context["items"] = items
        context["items_count"] = str(len(items))
        return render(request, "result.html", context=context)
    else:
        return render(request, "index.html")  # 在非 POST 请求时返回 index 页面


def shash(content: str) -> dict:
    # TODO simhash、minhash切换
    res = init_with_sentence(content, "Duplicate_check/static/stop_words.txt")

    return res


def select_by_simhash(shashs: list) -> list:
    # 多线程查询数据库
    with multiprocessing.Pool(processes=12) as pool:
        return pool.map(sub_select, shashs)


def sub_select(shash: dict) -> dict:
    # 阈值
    thr = 0.85

    # TODO simhash、minhash切换

    # 查询数据库

    # 使用海明距离计算相似度
    hamming = True
    # 使用余弦相似度计算相似度
    cos = False

    if hamming:
        sql = """
            SELECT sentence, title, author, "from"
                FROM corpus_sentence 
                WHERE (1 - ROUND(((shash <-> '{}'::vector) ^ 2)::numeric) / 64) > {} 
            """
    elif cos:
        sql = """
            SELECT sentence, title, author, "from"
                FROM corpus_sentence 
                WHERE shash <=> '{}'::vector(64) > {};
            """

    para_id = shash["para_id"]
    para_sentence = []
    for s in shash["para_sentence"]:
        if s["shash"] == "":
            might_copy_from = []

        else:
            v = [int(_) for _ in s["shash"]]
            this_s = postgresql_execute(sql.format(v, thr))
            might_copy_from = [
                {
                    "title": res[1],
                    "author": res[2],
                    "from": res[3],
                    "content": res[0],
                }
                for res in this_s
            ]
        para_sentence.append(
            {
                "sentence": s["sentence"],
                "copy": 1 if len(might_copy_from) > 0 else 0,
                "copy_from": might_copy_from,
            }
        )
    return {
        "para_id": para_id,
        "para_sentence": para_sentence,
    }


def similarity(shash_a: str, shash_b: str) -> float:
    # 计算相似度
    hanming = hammingDis(shash_a, shash_b)
    res = 1 - (float(hanming) / len(shash_a))
    return res
