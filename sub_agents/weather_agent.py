import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

@tool
def get_weather(loc):
    """
        查询即时天气函数
        :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称，\
        :return：心知天气 API查询即时天气的结果，具体URL请求地址为："https://api.seniverse.com/v3/weather/now.json"
        返回结果对象类型为解析之后的JSON格式对象，并用字符串形式进行表示，其中包含了全部重要的天气信息
    """
    url = "https://api.seniverse.com/v3/weather/now.json"
    params = {
        "key": os.getenv("WEATHER_API_KEY"),
        "location": loc,
        "language": "zh-Hans", 
        "unit": "c",
    }
    response = requests.get(url, params=params)
    temperature = response.json()
    return temperature['results'][0]['now']

# 构建提示模版， 提示词模板对于Agent的构建是必须的
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是天气助手，请根据用户的问题，给出相应的天气信息,并具备将结果写入文件的能力"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), # 这部分agnet提示符写法是写死的不可以修改
    ]
)

# Set up the LLM with your LM Studio API endpoint
llm = ChatOpenAI(
    model=os.getenv("LLM_Model"),
    base_url=os.getenv("LLM_Base_URL"),
    api_key="dummy",  # Required parameter, even if not used
    temperature=0,
)

#定义工具
tools = [get_weather]

# 直接使用`create_tool_calling_agent`创建代理
agent_executor = create_agent(llm, tools)

# 运行 Agent
response = agent_executor.invoke({"messages": [HumanMessage(content="请问今天上海天气怎么样？适合户外运动吗?")]})

print(response["messages"][-1].content)