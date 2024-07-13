# coding=utf-8

import codecs
import numpy as np
import jieba
import jieba.analyse
from collections import OrderedDict
import os

os.path.join(os.path.dirname(__file__), "..text/txt")


class CreateMethod(object):
    @classmethod
    # def create_mdb(cls, idx, name, paragraph, strKeyWord, shash):
    def create_lib(cls, idx, name, paragraph, shash):
        return {
            "idx": idx,
            "name": name,
            "paragraph": paragraph,
            # 'strKeyWord': strKeyWord,
            "shash": str(shash),
        }

    @classmethod
    def create_idx(cls, idx, name):
        return {"idx": idx, "name": name}

    @classmethod
    def create_details(
        cls, idx_a, idx_b, name_a, parag_a, name_b, parag_b, hamming_dis
    ):
        return {
            "idx_a": idx_a,
            "idx_b": idx_b,
            "name_a": name_a,
            "parag_a": parag_a,
            "name_b": name_b,
            "parag_b": parag_b,
            "hamming_dis": hamming_dis,
        }

    @classmethod
    def create_sum(cls, idx_a, idx_b, name_a, name_b, dupl_with_b, plagiarism_rate):
        return {
            "idx_a": idx_a,
            "idx_b": idx_b,
            "name_a": name_a,
            "name_b": name_b,
            "dupl_with_b": dupl_with_b,
            "plagiarism_rate": plagiarism_rate,
        }


# 计算汉明距离
def hammingDis(simhash1, simhash2):
    t1 = "0b" + simhash1
    t2 = "0b" + simhash2
    n = int(t1, 2) ^ int(t2, 2)
    i = 0
    while n:
        n &= n - 1
        i += 1
    return i


# 哈希函数
def string_hash(source):
    if source == "":
        return 0
    else:
        x = ord(source[0]) << 7
        m = 1000003
        mask = 2**128 - 1
        for c in source:
            x = ((x * m) ^ ord(c)) & mask
        x ^= len(source)
        if x == -1:
            x = -2
        x = bin(x).replace("0b", "").zfill(64)[-64:]
    return str(x)


# Simhash 算法
def simhash(content):
    PATH_stop = "init_database\stop_words.txt"
    jieba.analyse.set_stop_words(PATH_stop)  # 去除停用词
    keyWord = jieba.analyse.extract_tags(
        content, topK=20, withWeight=True, allowPOS=()
    )  # 根据 TD-IDF 提取关键词，并按照权重排序
    if len(keyWord) < 6:  # 少于5个词放弃这个句子
        return ""
    keyList = []
    for feature, weight in keyWord:  # 对关键词进行 hash
        weight = int(weight * 20)
        feature = string_hash(feature)
        temp = []
        for i in feature:
            if i == "1":
                temp.append(weight)
            else:
                temp.append(-weight)
        # print(temp)
        keyList.append(temp)
    list1 = np.sum(np.array(keyList), axis=0)
    if keyList == []:  # 编码读不出来
        return "00"
    simhash = ""
    for i in list1:  # 权值转换成 hash 值
        if i > 0:
            simhash = simhash + "1"
        else:
            simhash = simhash + "0"
    return simhash


import time  # 不知道为什么写在开头会报错，提示找不到这个库，写在这里就不会……


# 初始化，将论文的名称/片段/Simhash保存到数据库
def init(content, name, idx):
    content = content.split("\n")
    print("init() starting …")
    clock_0 = time.time()
    lib = {}
    for paragraph in content:
        paragraph = (
            paragraph.replace("\u3000", "")
            .replace("\t", "")
            .replace("  ", "")
            .replace("\r", " ")
        )  # 去除全角空格和制表符，换行替换为空格
        if paragraph == "" or paragraph == " ":
            continue
        shash = simhash(paragraph)
        if shash == "":
            continue
        lib = CreateMethod.create_lib(idx, name, paragraph, shash)
        for k, v in lib.items():
            print(k + ":" + str(v))
    clock_1 = time.time()
    print("【init time】【", clock_1 - clock_0, "】")
    print("init() executed!")


if __name__ == "__main__":
    PATH_lib = r"text/txt"
    counter_doc = 0
    doc_name = os.listdir(PATH_lib)
    for name in doc_name:
        txt = """"文/易北辰
在新零售业态当中，无人货架启动和运营成本貌似最低，主要面向2亿白领人群的上班时间，是新的流量价值洼地。因此无人货架成为新零售大潮中最先火起来的业态，半年多时间已有50多玩家入局：一类是创业玩家，以小e微店、猩便利、果小美、哈米科技为代表；一类是原有业务延展的创业玩家，以每日优鲜便利购、饿了么NOW、便利蜂为代表，多数在17年6月到9月入局；一类是巨头玩家，17年11月到12月入局，如有京东到家智能柜、顺丰丰e足食、阿里美的小卖柜。

相比于团购、O2O、网约车、共享单车而言，以无人货架为代表的近场零售发展更为迅猛，对操盘团队的要求更高，既要舍命狂奔的“攻”，又要稳健有序的“守”。在这场攻守大戏中，看似各路玩家刚刚起步，实际上已经棋到中局。
一、进攻的三要素：点位、资本、人
先做规模再谈盈亏是互联网的典型路径。点位之争，尤其是优质点位之争是无人货架规模化发展的第一步，也决定着终局时的位置。
从当前各路布局来看，猩便利6个月发展3万个左右点位，哈米科技9个月发展2万个左右，每日优鲜便利购6个月发展1.8万个左右，小e微店14个月发展5000多个点位。猩便利联合创始人司江华认为，30万个点位能够保证在市场上的绝对优势，也是其下阶段发展目标。每日优鲜便利购从点位数量和发展速度上看，处于第一梯队，同样将2018年的发展目标定为30万个，并将以最快速度达到50万个，成为2+N格局当中的头部玩家。
点位之争是效率和策略之争，资本和团队是最重要的保障。
从融资情况来看，每日优鲜便利购获2亿美元融资，是当前无人货架玩家当中公布融资额最大的一家，为即将到来的大战做好了准备。值得注意的是，腾讯领投A轮，巨头身影隐现，带来的不仅是资本，还可能有流量等诸多优势，也为最后的战局埋下了伏笔。
在人员及团队方面，无人货架创业公司创始人及团队中，阿里铁军及O2O地推团队身影较多。近日每日优鲜便利购公布，前美团外卖大连锁部总经理刘澍加盟便利购，担任合伙人兼CMO，负责整体市场工作，全力打造强执行力销售铁军。
作为原美团直销铁军核心人物，刘澍是个一直在打仗的人。他在2011年加入美团，7年时间轮岗8次。在苏州，月销售业绩破百万；在重庆时，保持7个月增长业绩破千万，从第6做到第1；在北京，月销售业绩从1000万提升到近3000万。刘澍是“团购三强争霸”时期美团的核心战将，在美团外卖扩张时期担任外卖大连锁部总经理，带领的餐饮KA团队迅速锁定了美团在白领外卖市场的领导地位。
刘澍的加盟，将帮助每日优鲜便利购迅速打造出一支具备极强执行力的直销铁军，同时带来发展战略和执行策略上的经验补充，助力便利购快速占据优势局面。
为便利购快速打造销售铁军，刘澍有三板斧。一是快速招人，1月份组建3000人的直销团队，3月达到5000人。二是中西药结合管人，以西药式管理在实战中练兵，以中药式理念在团建中打造理想主义色彩。三是结合自身经验，一套直销管理方法论培养人，实现从0分到80分的快速成长。
点位之争很重要，优质点位则是争斗的制高点。每日优鲜便利购有明确的策略：以金字塔模型将客户细分，主攻腰部以上及头部、超级头部客户，快速覆盖目标人群；将城市分级，提供不同的商品品类服务，拓展一、二、三线60个核心城市，加快前置仓铺设，快速满足日配交付需要。
二、防守的两个基本点：高效供应链和精品保障
无人货架是一个看似门槛低、谁都可以进入的行业，但真正的难点在于规模化之后的精细化运营，主要体现在，产品和体验如何更好满足用户需求。
供应链是需要长期磨合与沉淀的能力，也是这一轮无人货架创业企业的短板。小e微店、果小美、领蛙、哈米科技、猩便利，几乎都没有成熟的供应链。
相比之下，每日优鲜便利购的优势明显，依托生鲜电商平台每日优鲜的供应链，每日优鲜3年多时间做“到家”场景，让每日优鲜从无到有，积累了供应链、物流和一定的会员、数据等资源，可以为无人货架的铺设提供助力。尤其是供应链方面，“城市分选中心+社区前置仓”的二级仓储体系，在很大程度上解决了生鲜冷链运输的“成本难题”，这是纯粹创业玩家不具备的优势，甚至是多数电商不具备的。
在商品方面，一是每日优鲜已经建立起完整成熟的生鲜采购网络，每日优鲜便利购可直接嫁接每日优鲜完备的商品供应链，通过全温区货架作为载体，不仅能为办公室用户提供更为丰富的商品品类，还有效降低的采购成本，提升价格优势。
二是把控确保品质，专业的买手团队在原产地按照生产环境、口感、外观、重量的标准进行第一层把控，每日优鲜城市分选中心的品控实验室进行第二层把控，加工环节的全检是第三层。
在这个基础上，做好基于用户需求的产品品类更新、“千架千面”同样重要，考验对消费者理解、供应链支撑及产品选择的能力，每日优鲜便利购拥有业务基础和大数据能力，更具备优势。未来和腾讯数据、平台打通后，可带来大数据分析+人工智能技术业落地，为用户精准的提供高频消费产品。
三、无人货架决战年，什么是核心胜负手？
对于无人货架风口节奏，大家有着相似的判断：2017年是发展元年，实际上主要是下半年各路玩家入局；2018年上半年，一批缺少强有力地推团队的企业，会在以优质点位为核心的进攻之争中倒下；2018年下半年，边攻边守，一批企业会死在供应链运营上。2018年之后的格局预计是2+N，而2019年预计是巨头收场。
值得一提的是，两轮攻守下来，跟风者基本会倒掉。剩余第一梯队玩家的过招，可能不在招式，大家有相同的软硬件配置，胜负手在于对消费者、对商业本质的理解。
当然，企业愿景、发展策略、团队配置和能力储备只能对下一步发展做出预判，实际无人货架大战可能更为残酷，有待继续观察。
"
"""
        counter_doc += 1
        # 在外面设置好文档index，直接传入，原来的逻辑是直接一个个导入，直接按顺序记数，到几index就是几
        idx = counter_doc
        init(txt, doc_name, idx)
