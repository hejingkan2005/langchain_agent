# Implement a demo agent by using langchain, it should call LM Studio API to get responses.
# The API based url is https://b90cdc2db71f.ngrok-free.app and model name is qwen2.5-14b-instruct-1m, it has no api key.
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

# Set up the LLM with your LM Studio API endpoint
llm = ChatOpenAI(
    model="qwen2.5-14b-instruct-1m",
    base_url="https://b90cdc2db71f.ngrok-free.app/v1",
    api_key="dummy",  # Required parameter, even if not used
    temperature=0,
)

@tool
def get_stock_price(stock_symbol: str) -> str:
    """Get the current price for a given stock symbol."""
    stock_prices = {
        "AAPL": "150.00 USD",
        "GOOGL": "2800.00 USD",
        "MSFT": "300.00 USD"
    }
    return stock_prices.get(stock_symbol.upper(), "Stock symbol not found.")

tools = [get_stock_price]

# Create a ReAct agent using LangGraph
agent_executor = create_agent(llm, tools)

def run_agent(query: str) -> str:
    result = agent_executor.invoke({"messages": [HumanMessage(content=query)]})
    return result["messages"][-1].content

if __name__ == "__main__":
    query = "What is the current stock price of AAPL? And suggest me whether to buy or sell."
    response = run_agent(query)
    print(response)