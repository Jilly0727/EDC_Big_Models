from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_postgres import PGVector

# 加载环境变量
load_dotenv()

# local PDF file path
file_path ="/Users/liyangqi/Desktop/李江/杨老师-习大大课程资料/15040思想概论【讲义】.pdf"
loader =PyPDFLoader(file_path)
docs =loader.load()

# 基于字符划分简单的分割方式
try:
    splitter =RecursiveCharacterTextSplitter(
        chunk_size=200, 
        chunk_overlap=100
    )
    splits = splitter.split_documents(docs)
except Exception as e:
    print(f"Error:{e}")

# 清理文本中的换行符/NULL字符
for doc in splits:
    doc.page_content = doc.page_content.replace("\n", " ")

# 实例化向量模型
embedding = DashScopeEmbeddings(
    model = "text-embedding-v4"
)

# 实例化向量数据库
try:
    vector_store = PGVector(
        embeddings=embedding,
        collection_name="document",
        connection="postgresql+psycopg://postgres:Jilly0727@47.108.163.152:5432/knowledge"
    )

    vector_store.create_collection()
    print("创建向量集合成功")
except Exception as e:
    print(f"Error:{e}")

# 向数据库中存储向量
ids =vector_store.add_documents(splits)
print(f"已添加向量到数据库: {len(ids)}")
