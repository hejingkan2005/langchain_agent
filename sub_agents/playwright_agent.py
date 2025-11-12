import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from playwright.async_api import async_playwright

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)



from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Using Azure OpenAI Service with Managed Identity
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21",
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL_NAME"),
)



async def main():
    # 初始化 Playwright 浏览器（手动创建异步版本）
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    tools = toolkit.get_tools()
    
    # 使用 create_react_agent 创建代理
    agent_executor = create_react_agent(llm, tools)
    
    # 定义任务
    command = {
        "messages": [HumanMessage(content="访问这个网站 https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure 并帮我总结一下这个网站的内容")]
    }
    
    # 执行任务
    response = await agent_executor.ainvoke(command)
    print(response["messages"][-1].content)
    
    # 关闭浏览器
    await browser.close()
    await playwright.stop()

if __name__ == "__main__":
    asyncio.run(main())