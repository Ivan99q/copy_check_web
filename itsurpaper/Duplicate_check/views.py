from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from mysql_script.mysql_op import *
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
            "original_content": data["content"].split("\n"),
        }
        context["original_content"].remove("\r")

        # 计算simhash
        s_hash = shash(data["content"])
        items = []
        if len(s_hash) == 0:
            return render(request, "no_result.html", context=context)
        items = select_by_simhash(s_hash)
        # 返回结果
        if len(items) == 0:
            return render(request, "no_result.html", context=context)
        context["items"] = items
        context["items_count"] = str(len(items))
        return render(request, "result.html", context=context)
    else:
        return render(request, "index.html")  # 在非 POST 请求时返回 index 页面


def shash(content: str) -> list:
    res = init_with_unabled(
        content, stop_words_path="Duplicate_check/static/stop_words.txt"
    )

    return res


def select_by_simhash(shashs: list) -> dict:
    # 多线程查询数据库
    with multiprocessing.Pool(processes=8) as pool:
        return pool.map(sub_select, shashs)


def sub_select(shash: dict) -> dict:
    # 阈值
    thr = 0.92

    # 查询数据库
    sql = """
        SELECT id, `index`, content, title, author, `from`, shash, similarity(shash, '{}') 
            FROM corpus 
            WHERE similarity(shash, '{}') > {} ;
    """
    if shash["shash"] == "":
        res_select = []
    else:
        res_select = execute_query(sql.format(shash["shash"], shash["shash"], thr))

    res = {
        "copy": shash["id"],
        "items": [
            {
                "title": res[3],
                "author": res[4],
                "from": res[5],
                "content": res[2],
                "similarity": res[7],
            }
            for res in res_select
        ],
    }
    return res


def similarity(shash_a: str, shash_b: str) -> float:
    # 计算相似度
    hanming = hammingDis(shash_a, shash_b)
    res = 1 - (float(hanming) / len(shash_a))
    return res
