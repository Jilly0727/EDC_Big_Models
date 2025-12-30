from langchain.chat_models import init_chat_model, BaseChatModel
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain.tools import tool
from langchain.agents import create_agent
import random

# 加载环境变量
load_dotenv()

model : BaseChatModel = init_chat_model(
    model ="deepseek-chat", #Model名称
    temperature=0.7, #温度设置
    max_tokens=1024, #最大Token数
    timeout=30 #超时退出
)

# 定义四个核心工具
@tool("query_knowledge_base")
def query_knowledge_base(query: str) -> str:
    """
        Addording to the user's query, search the knowledge base and return relevant information.
        query: {query}
    """

    results =kb_controller.search(knowledge_base_id,query)
    return json.dumps(results,ensure_ascii=False,indent=2)

@tool("get_files_meta")
def get_files_meta(filesIds: List[int]) -> str:
    """
        Get the files metadata by their IDs from knowledge base.
    """

    if not filesIds:
        return "The filesIds parameter is required, please provide valid file IDs."
    results =kb_controller.get_files_metadata(knowledge_base_id, filesIds)
    return json.dumps(results,ensure_ascii=False,indent=2)

@tool("read_file_chunks")
def read_file_chunks(chunks: List[Dict[str, int]]) -> str:
    """
        Read the content of specific file chunks in the current knowledge base.
    """

    if not chunks:
        return "The chunks parameter is required, please provide valid chunk IDs."
    results =kb_controller.read_file_chunks(knowledge_base_id, chunks)
    return json.dumps(results,ensure_ascii=False,indent=2)

@tool("list_files")
def list_files() -> str:
    """
        List all files in the current knowledge base.
    """
    results =kb_controller.readFilePaginated(knowledge_base_id, page, page_size)
    return json.dumps(results,ensure_ascii=False,indent=2)

# 创建一个Agent
agent = create_agent(
    model=model,
    tools=[get_weather,query_knowledge_base,get_files_meta,read_file_chunks,list_files],
    system_prompt=
    """
    你是一个 Agentic RAG 助手。请遵循以下策略逐步收集证据后回答用户的问题：
    1. 首先，使用 'query_knowledge_base' 工具在知识库中搜索相关信息。
    2. 如果搜索结果包含文件，输出最具相关性的文件ID，使用 'get_files_meta' 工具获取这些文件的元数据。
    3. 根据元数据，确定需要阅读的文件块，用“引用：”的格式列出实际读取的fileID和chunkIndex。
    4. 调用 'read_file_chunks' 工具获取时，参数必须是列表，每个元素为 {"fileId": 整数, "chunkIndex": 整数}。
    5. 如果需要了解知识库中的所有文件，使用 'list_files' 工具。
    6. 综合收集到的信息，
    生成对用户问题的详细回答.
    """
)

messages ="今天成都的天气怎么样？适合进行哪些运动？"
response =agent.invoke(
input ={
    "messages":[HumanMessage(content=messages)]
}
)
# This latest version codes 02
print(response)
