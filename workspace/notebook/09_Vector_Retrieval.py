from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv()

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

    print("向量数据库连接成功")
except Exception as e:
    print(f"Error:{e}")

# 实例化向量检索器（相似度检索）
retriever =vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5},
)

query_text ="简短说明人的器官是有什么组成的？"
# docs =retriever.invoke(query_text)
# print(docs)


prompt =ChatPromptTemplate.from_template(
    """
    请根据下面的内容回答用户的问题。
    资料:
    {context}

    问题:
    {question}
    """
)

# 定义一个函数，用于解析文档列表，并返回文档的内容
def DocsOutputParser(docs):
    return "\n\n".join([d.page_content for d in docs])

# 创建一个Chain，将检索器与输出解析器组合起来
chain = (
    {
        "context": retriever | DocsOutputParser,
        "question": lambda x:x
    } | prompt
)
response =chain.invoke(query_text)
print("===========AI开始回答问题了=================")
print(response)

