
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

llm = ChatGoogleGenerativeAI(
    api_key="<API_KEY>",
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

# Create an agent with Checkpointer Memory
memory = InMemorySaver()

helpfull_assistant = create_agent(
    model=llm,
    tools=[],
    system_prompt="You are a helpful assistant",
    checkpointer=memory
)
