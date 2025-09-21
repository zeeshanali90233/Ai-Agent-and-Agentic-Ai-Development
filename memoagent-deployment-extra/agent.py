
from langgraph.prebuilt import create_react_agent

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

llm = ChatGoogleGenerativeAI(
    api_key="API_KEY",
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


# Create an agent with Checkpointer Memory
memory = InMemorySaver()

memory_agent = create_react_agent(
    model=llm,
    tools=[get_weather],
    prompt="You are a helpful assistant",
    checkpointer=memory
)

