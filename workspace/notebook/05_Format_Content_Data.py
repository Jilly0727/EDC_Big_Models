from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# 加载环境变量
load_dotenv()

model = init_chat_model("deepseek-chat") #可以设置其他参数，参考文档

# 创建提示模版
prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="你是合同分析专家，请详细分析合同类容"),
    ("human", "{text}")
])

class Company_info(BaseModel):
    company_name: str = Field(default=None)
    company_address: str = Field(default=None)

class Contract_info(BaseModel):
    contract_name: str = Field(default=None)
    contract_date: str = Field(default=None)
    contract_amount: float = Field(default=None)
    company_info: Company_info = Field(default=None)

#转化信息为格式化输出
model =model.with_structured_output(Contract_info)
#创建链
chain = prompt_template | model
response =chain.invoke({"text": "请提供一份房屋租赁合同的模版，提取结构化信息"})
print(response)
