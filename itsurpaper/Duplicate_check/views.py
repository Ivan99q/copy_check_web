from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from sql_script.mysql_op import *
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
        items = []
        # TODO 判断传入文本是否过短
        if len(s_hash) == 0:
            return render(request, "no_result.html", context=context)
        items = select_by_simhash(s_hash["paragraphs"])
        # TODO 判断是否所有句子都没有查询到结果
        if len(items) == 0:
            return render(request, "no_result.html", context=context)
        context["items"] = items
        context["items_count"] = str(len(items))
        return render(request, "result.html", context=context)
    else:
        return render(request, "index.html")  # 在非 POST 请求时返回 index 页面


def shash(content: str) -> dict:
    res = init_with_sentence(content, "Duplicate_check/static/stop_words.txt")

    return res


def select_by_simhash(shashs: list) -> list:
    # 多线程查询数据库
    with multiprocessing.Pool(processes=12) as pool:
        return pool.map(sub_select, shashs)


def sub_select(shash: dict) -> dict:
    # 阈值
    thr = 0.92

    # TODO

    # 查询数据库
    sql = """
        SELECT id, `index`, content, title, author, `from`, shash
            FROM corpus 
            WHERE similarity(shash, '{}') > {} ;
    """
    para_id = shash["para_id"]
    para_sentence = []
    for s in shash["para_sentence"]:
        if s["shash"] == "":
            continue
        this_s = execute_query(sql.format(s["shash"], thr))
        might_copy_from = [
            {
                "title": res[3],
                "author": res[4],
                "from": res[5],
                "content": res[2],
            }
            for res in this_s
        ]
        para_sentence.append({"sentence": s["sentence"], "copy_from": might_copy_from})
    return {
        "para_id": para_id,
        "para_sentence": para_sentence,
    }


def similarity(shash_a: str, shash_b: str) -> float:
    # 计算相似度
    hanming = hammingDis(shash_a, shash_b)
    res = 1 - (float(hanming) / len(shash_a))
    return res
