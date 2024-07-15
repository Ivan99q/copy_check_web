from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from mysql_script.mysql_op import *
from init_database.ckg import *

# from init_database import *


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
    # TODO 多线程查询数据库

    res = {}
    for shash in shashs:
        this_res = mysql_select("corpus", {"shash": shash})
        if len(this_res) > 0:
            items = []
            for i in this_res:
                items.append(
                    {
                        "title": str(i[3]),
                        "author": str(i[4]),
                        "from": str(i[5]),
                        "content": str(i[2]),
                    }
                )
            res[shash] = items
        else:
            res[shash] = []

    return items


def similarity(a, b):
    # TODO 计算相似度
    return 0
