
from langchain.agents import create_agent

from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")  
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


# Create an agent with Checkpointer Memory
memory = InMemorySaver()

helpingagent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
    checkpointer=memory
)

