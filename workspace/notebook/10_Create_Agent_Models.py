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

# 定义工具
@tool
def get_weather(location: str) -> str:
    """
        根据指定地点获取天气信息
        location: 地点
    """
    weather =random.choice(["晴天","暴雨","阴天"])
    return f"{location}的天气是{weather}"

# 创建一个Agent
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一位天气预报专家"
)

messages ="今天成都的天气怎么样？适合进行哪些运动？"
response =agent.invoke(
input ={
    "messages":[HumanMessage(content=messages)]
}
)

print(response)
