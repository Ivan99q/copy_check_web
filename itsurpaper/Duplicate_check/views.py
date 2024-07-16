from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from mysql_script.mysql_op import *
from init_database.ckg import *

from datasketch import MinHashLSH, MinHash



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

        # 计算simhash
        s_hash = shash(data["content"], data["title"])
        items = []
        if len(s_hash) == 0:
            return render(request, "no_result.html")
        items = select_by_simhash([i["shash"] for i in s_hash])
        # 返回结果
        if len(items) == 0:
            return render(request, "no_result.html")
        context = {"items": items, "items_count": str(len(items))}
        return render(request, "result.html", context=context)
    else:
        return render(request, "index.html")  # 在非 POST 请求时返回 index 页面


def shash(
    content: str,
    title: str,
):
    ckg = init(
        content, title, 0, stop_words_path="Duplicate_check/static/stop_words.txt"
    )
    res = []
    for i in ckg:
        res.append({"content": i["content"], "shash": i["shash"]})
    return res


def select_by_simhash(shashs: list) -> list:
    data_from_DB = mysql_select("corpus", {})

    items = []

    # 阈值
    thr = 0.92

    for data in data_from_DB:
        for shash in shashs:
            if similarity(shash, data[6]) > thr:
                items.append(
                    {
                        "title": str(data[3]),
                        "author": str(data[4]),
                        "from": str(data[5]),
                        "content": str(data[2]),
                    }
                )
    return items


def similarity(shash_a: str, shash_b: str) -> int:
    # 计算相似度
    hamming = hammingDis(shash_a, shash_b)
    res = 1 - (float(hamming) / len(shash_a))
    return res
