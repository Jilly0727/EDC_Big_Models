from langchain.chat_models import BaseChatModel
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage, AIMessageChunk
from langchain_community.chat_models import ChatTongyi
from collections.abc import Iterator

# 加载环境变量
load_dotenv()

def stream(content: str | list[str | dict], model: BaseChatModel) -> None:
    # 验证模型和内容是否有效
    if model is None or not content:
        return

    # 创建输入消息
    messages = [
        SystemMessage(content="你是乐于助人的AI助手,可以回答用户的问题"),
        HumanMessage(content=content)
    ]

    response: Iterator[AIMessageChunk] = model.stream(messages)
    for chunk in response:
        # print(chunk)
        process_response(chunk)

response_end = False
def process_response(chunk: AIMessageChunk) -> None:
    global response_end
    for block in chunk.content_blocks:
        if block["type"] == 'reasoning':
            print(block['reasoning'], end="", flush=True)
        elif block["type"] == 'text':
            if not response_end:
                response_end = True
                print("\n\n==============正式回答===============\n")
            print(block["text"], end="", flush=True)
        else:
            pass

if __name__ == "__main__":
    # 使用Deepseek模型
    # stream("介绍一下Langchai的主要内容",ChatDeepSeek(model='deepseek-chat'))

    # 使用阿里千问大模型
    try:
        stream([
            {"text": "请描述一下图片中的内容"},
            {"image": "https://gips2.baidu.com/it/u=295419831,2920259701&fm=3028&app=3028&f=JPEG&fmt=auto?w=720&h=1280"}
            ], ChatTongyi(model='qwen-vl-plus'))
    except Exception as e:
        print(e)