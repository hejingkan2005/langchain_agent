import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser # 导入标准输出组件

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

model = init_chat_model(
    model=os.getenv("LLM_Model"),
    model_provider="openai",
    base_url=os.getenv("LLM_Base_URL"),
    api_key="dummy",
)

# 搭建链条，把model和字符串输出解析器组件连接在一起
basic_qa_chain = model #| StrOutputParser()

# 查看输出结果
question = "你好，请你介绍一下你自己。"
result = basic_qa_chain.invoke(question)

print(result)