from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from werkzeug.utils import secure_filename
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from mysql_script.mysql_op import *


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

        # TODO
        # 1. 计算simhash
        # 2. 查询数据库
        # 3. 返回结果
        data["from"] = "test"

        items = []
        items.append(data)
        context = {"items": items, "items_count": len(items)}
        return render(request, "result.html", context=context)
    else:
        return render(request, "index.html")  # 在非 POST 请求时返回 index 页面


def shash(content: str):
    # TODO 计算simhash
    return 1515165153123123


def select_by_simhash(shash: int):
    # TODO 查询数据库
    return [{"title": "test", "author": "test"}]
