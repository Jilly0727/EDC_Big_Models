from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage, AIMessage

# 加载环境变量
load_dotenv()

model = init_chat_model("deepseek-chat") #可以设置其他参数，参考文档

# 创建输入消息
messages = [
    SystemMessage(content="你是乐于助人的AI助手"),
    HumanMessage(content="请帮我背诵一首诗词《鹅鹅鹅》")
]

# 3. 正确调用
try:
    response = model.invoke(messages) # 注意参数名是 messages
    print(response.content)
except Exception as e:
    print(f"发生错误：{type(e).__name__}: {e}")