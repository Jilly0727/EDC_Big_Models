from dotenv import load_dotenv
from langchain_community.document_loaders import Textloader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_postgres import PGVector


# 1.加载文本文件
try:
    loader = Textloader(
        "/root/matadata/Text_Data/Test_Doc.txt",
        encoding="utf-8"
    )
    
    documents =loader.load()
    print(f"已加载文档数量: {len(documents)}")
except Exception as e:
    print(f"Error:{e}")

# # 2.文本拆分
# text_splitter =RecursiveCharacterTextSplitter(
#     chunk_size=100,
#     chunk_overlap=20
#     )
# split_docs =text_splitter.split_documents(documents)

# # 3.创建Embedding向量模型
# embeddings =DashScopeEmbeddings(
#     model="text-embedding-v4"
# )

# # 4.实例化向量数据库
# try:
#     vector_store = PGVector(
#         embeddings=embedding,
#         collection_name="document",
#         connection="postgresql+psycopg://postgres:Jilly0727@47.108.163.152:5432/knowledge"
#     )

#     vector_store.create_collection()
#     print("创建向量集合成功")
# except Exception as e:
#     print(f"Error:{e}")

# # 向数据库中存储向量
# ids =vector_store.add_documents(split_docs)
# print(f"已添加向量到数据库: {len(ids)}")