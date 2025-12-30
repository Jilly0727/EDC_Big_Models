from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# 加载环境变量
load_dotenv()

model = init_chat_model("deepseek-chat") #可以设置其他参数，参考文档

# lanchain_community.document_loaders.PyPDFLoader去加载PDF文档
    # CSVLoader去加载CSV文件
    # JsonLoader去加载JSON文件
    # DoclingLoader去加载DOCX文件
    # WebBaseLoader去加载网页

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


# local PDF file path
file_path ="/Users/liyangqi/Desktop/李江/杨老师-习大大课程资料/15040思想概论【讲义】.pdf"
loader =PyPDFLoader(file_path)
docs =loader.load()
# print("文档数量：",len(docs))

# if len(docs)>0:
#     print("文档内容：",docs[0].page_content[:100])

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter

# 基于字符划分简单的分割方式
splitter =RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=200
)
splits = splitter.split_documents(docs)
print("拆分后的文档数量：",len(splits))

