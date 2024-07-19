from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os


# 初始化，将论文的名称/片段/Simhash保存到数据库
def vector(content: str):
    model_name = "BAAI/bge-large-zh-v1.5"
    model = SentenceTransformer(model_name)
    embeddings = model.encode(content)
    return embeddings


if __name__ == "__main__":
    print(
        vector(
            "近年来，随着深度学习技术的飞速发展，在自然语言处理领域中，深度学习模型逐渐成为研究热点。"
        )
    )
