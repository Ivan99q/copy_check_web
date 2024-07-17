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
    with multiprocessing.Pool(processes=12) as pool:
        return pool.map(sub_select1111, shashs)


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
    s_l = [
        {
            "id": 0,
            "para": "二是把控确保品质，专业的买手团队在原产地按照生产环境、口感、外观、重量的标准进行第一层把控，每日优鲜城市分选中心的品控实验室进行第二层把控，加工环节的全检是第三层。",
        },
        {
            "id": 0,
            "para": "在商品方面，一是每日优鲜已经建立起完整成熟的生鲜采购网络，每日优鲜便利购可直接嫁接每日优鲜完备的商品供应链，通过全温区货架作为载体，不仅能为办公室用户提供更为丰富的商品品类，还有效降低的采购成本，提升价格优势。",
        },
        {
            "id": 0,
            "para": "相比之下，每日优鲜便利购的优势明显，依托生鲜电商平台每日优鲜的供应链，每日优鲜3年多时间做“到家”场景，让每日优鲜从无到有，积累了供应链、物流和一定的会员、数据等资源，可以为无人货架的铺设提供助力。尤其是供应链方面，“城市分选中心+社区前置仓”的二级仓储体系，在很大程度上解决了生鲜冷链运输的“成本难题”，这是纯粹创业玩家不具备的优势，甚至是多数电商不具备的。",
        },
        {
            "id": 0,
            "para": "供应链是需要长期磨合与沉淀的能力，也是这一轮无人货架创业企业的短板。小e微店、果小美、领蛙、哈米科技、猩便利，几乎都没有成熟的供应链。",
        },
        {
            "id": 0,
            "para": "无人货架是一个看似门槛低、谁都可以进入的行业，但真正的难点在于规模化之后的精细化运营，主要体现在，产品和体验如何更好满足用户需求。",
        },
        {
            "id": 0,
            "para": "在这个基础上，做好基于用户需求的产品品类更新、“千架千面”同样重要，考验对消费者理解、供应链支撑及产品选择的能力，每日优鲜便利购拥有业务基础和大数据能力，更具备优势。未来和腾讯数据、平台打通后，可带来大数据分析+人工智能技术业落地，为用户精准的提供高频消费产品。",
        },
        {
            "id": 0,
            "para": "二、防守的两个基本点：高效供应链和精品保障",
        },
        {
            "id": 0,
            "para": "点位之争很重要，优质点位则是争斗的制高点。每日优鲜便利购有明确的策略：以金字塔模型将客户细分，主攻腰部以上及头部、超级头部客户，快速覆盖目标人群；将城市分级，提供不同的商品品类服务，拓展一、二、三线60个核心城市，加快前置仓铺设，快速满足日配交付需要。",
        },
        {
            "id": 0,
            "para": "为便利购快速打造销售铁军，刘澍有三板斧。一是快速招人，1月份组建3000人的直销团队，3月达到5000人。二是中西药结合管人，以西药式管理在实战中练兵，以中药式理念在团建中打造理想主义色彩。三是结合自身经验，一套直销管理方法论培养人，实现从0分到80分的快速成长。",
        },
        {
            "id": 0,
            "para": "刘澍的加盟，将帮助每日优鲜便利购迅速打造出一支具备极强执行力的直销铁军，同时带来发展战略和执行策略上的经验补充，助力便利购快速占据优势局面。",
        },
        {
            "id": 0,
            "para": "作为原美团直销铁军核心人物，刘澍是个一直在打仗的人。他在2011年加入美团，7年时间轮岗8次。在苏州，月销售业绩破百万；在重庆时，保持7个月增长业绩破千万，从第6做到第1；在北京，月销售业绩从1000万提升到近3000万。刘澍是“团购三强争霸”时期美团的核心战将，在美团外卖扩张时期担任外卖大连锁部总经理，带领的餐饮KA团队迅速锁定了美团在白领外卖市场的领导地位。",
        },
        {
            "id": 0,
            "para": "对于无人货架风口节奏，大家有着相似的判断：2017年是发展元年，实际上主要是下半年各路玩家入局；2018年上半年，一批缺少强有力地推团队的企业，会在以优质点位为核心的进攻之争中倒下；2018年下半年，边攻边守，一批企业会死在供应链运营上。2018年之后的格局预计是2+N，而2019年预计是巨头收场。",
        },
        {
            "id": 0,
            "para": "当然，企业愿景、发展策略、团队配置和能力储备只能对下一步发展做出预判，实际无人货架大战可能更为残酷，有待继续观察。",
        },
        {
            "id": 0,
            "para": "在人员及团队方面，无人货架创业公司创始人及团队中，阿里铁军及O2O地推团队身影较多。近日每日优鲜便利购公布，前美团外卖大连锁部总经理刘澍加盟便利购，担任合伙人兼CMO，负责整体市场工作，全力打造强执行力销售铁军。",
        },
        {
            "id": 0,
            "para": "从融资情况来看，每日优鲜便利购获2亿美元融资，是当前无人货架玩家当中公布融资额最大的一家，为即将到来的大战做好了准备。值得注意的是，腾讯领投A轮，巨头身影隐现，带来的不仅是资本，还可能有流量等诸多优势，也为最后的战局埋下了伏笔。",
        },
    ]
    print(select_by_simhash(s_l))
