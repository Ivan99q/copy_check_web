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
        txt = """"""
        counter_doc += 1
        # 在外面设置好文档index，直接传入，原来的逻辑是直接一个个导入，直接按顺序记数，到几index就是几
        idx = counter_doc
        init(txt, doc_name, idx)
