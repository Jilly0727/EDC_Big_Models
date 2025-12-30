from langchain_openai import OpenAIEmbeddings
# from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings

# 加载环境变量
load_dotenv()

# local PDF file path
file_path ="/Users/liyangqi/Desktop/李江/杨老师-习大大课程资料/15040思想概论【讲义】.pdf"
loader =PyPDFLoader(file_path)
docs =loader.load()

# 基于字符划分简单的分割方式
splitter =RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=200
)
splits = splitter.split_documents(docs)
print("拆分后的文档数量：",len(splits))

# 文档向量化
embedding = DashScopeEmbeddings(
    model = "text-embedding-v4",
)


print(splits[0].page_content)
print("\n==============================\n")
print(splits[1].page_content)
vector1 =embedding.embed_query(splits[0].page_content)

print("向量的长度:",len(vector1))
print("\n==============================\n")
print(vector1[:50])
