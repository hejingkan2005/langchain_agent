import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# chatbot_prompt = ChatPromptTemplate.from_messages([
#     ("system", "Geoffrey Hinton，是AI神经网络之父。"),
#     ("user", "{input}")
# ])

model = init_chat_model(
    model=os.getenv("LLM_Model"),
    model_provider="openai",
    base_url=os.getenv("LLM_Base_URL"),
    api_key="dummy",
)
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Geoffrey Hinton，是AI神经网络之父。"),
    MessagesPlaceholder(variable_name="messages"),
])

chain = prompt | model | parser

messages_list = []  # 初始化历史
print("  输入 exit 结束对话")
while True:
    user_query = input("你：")
    if user_query.lower() in {"exit", "quit"}:
        break

    # 1) 追加用户消息
    messages_list.append(HumanMessage(content=user_query))

    # 2) 调用模型
    # assistant_reply = chain.invoke({"messages": messages_list})
    # print("Geoffrey：", assistant_reply)
    assistant_reply=''
    print('Geoffrey:', end=' ')
    for chunk in chain.stream({"messages": messages_list}):
        assistant_reply+=chunk
        print(chunk, end="", flush=True)
    print()

    # 3) 追加 AI 回复
    messages_list.append(AIMessage(content=assistant_reply))

    # 4) 仅保留最近 50 条
    messages_list = messages_list[-50:]