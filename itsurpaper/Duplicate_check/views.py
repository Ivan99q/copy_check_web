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


def select_by_simhash(shashs: list) -> dict:
    # 多线程查询数据库
    with multiprocessing.Pool(processes=12) as pool:
        return pool.map(sub_select, shashs)


def sub_select(shash: dict) -> dict:
    # 阈值
    thr = 0.92

    # TODO

    # 查询数据库
    sql = """
        SELECT id, `index`, content, title, author, `from`, shash, similarity(shash, '{}') 
            FROM corpus 
            WHERE similarity(shash, '{}') > {} ;
    """
    para_id = shash["para_id"]
    para_sentence = []
    for s in shash["para_sentence"]:
        if s["shash"] == "":
            continue
        # print(sql.format(s["shash"], s["shash"], thr))
        this_s = execute_query(sql.format(s["shash"], s["shash"], thr))
        might_copy_from = [
            {
                "title": res[3],
                "author": res[4],
                "from": res[5],
                "content": res[2],
                "similarity": res[7],
            }
            for res in this_s
        ]
        para_sentence.append({"sentence": s["sentence"], "copy_from": might_copy_from})
    return {
        "para_id": para_id,
        "para_sentence": para_sentence,
    }


def sub_select1111(shash: dict) -> dict:
    # 阈值
    thr = 0.92

    # 查询数据库
    sql = """
        SELECT id, `index`, content, title, author, `from`, shash 
            FROM corpus 
            WHERE content = {};
    """

    res_select = execute_query(sql.format(shash["para"]))

    res = {
        "copy": shash["id"],
        "items": [
            {
                "title": res[3],
                "author": res[4],
                "from": res[5],
                "content": res[2],
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


if __name__ == "__main__":

    para = {
        "para_id": 1,
        "para_sentence": [
            {
                "sentence": "在新零售业态当中，无人货架启动和运营成本貌似最低，主要面向2 亿白领人群的上班时间，是新的流量价值洼地。",
                "shash": "0010000011101000110001011101010110001011000101010001100100011111",
            },
            {
                "sentence": "因此无人货架成为新零售大潮中最先火起来的业态，半年多时间已有50多玩家入局：一类是创业玩家，以小e微店、猩便利、果小美、哈米科技为代表；一类是原有业务延展的创业玩家，以每日优鲜便利购、饿了么NOW、便利蜂为代表，多数在17年6月到9月入局；一类是巨头玩家，17年11月到12月入局，如有京东到家智能柜、顺丰丰e足食、阿里美的小卖柜。",
                "shash": "0010000000010010001100000111001011001001101111100100101101101111",
            },
        ],
    }
    print(sub_select(para))
