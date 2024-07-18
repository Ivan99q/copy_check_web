from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os


# 初始化，将论文的名称/片段/Simhash保存到数据库
def vector(content: str):
    model_name = "BAAI/bge-large-zh-v1.5"
    model = SentenceTransformer(model_name)
    embeddings = model.encode(content)
    return embeddings
