import asyncio
import json
from fastmcp import Client
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import BaseTool
import os 
import dotenv
from pydantic import BaseModel  

dotenv.load_dotenv()

class EmailInput(BaseModel):
    to: str
    subject: str
    body: str

class AddInput(BaseModel):
    a: int
    b: int

client = Client("http://localhost:8000/mcp")

async def call_mcp_tool(tool_name: str, **kwargs):
    async with client:
        return await client.call_tool(tool_name, kwargs)

async def get_all_tools():
    async with client:
        return await client.list_tools()

# Get available tools
mcp_tools = asyncio.run(get_all_tools())
print(f"Available MCP tools: {[tool.name for tool in mcp_tools]}")

class MCPTool(BaseTool):
    """Wrapper for an MCP tool to be used in LangGraph ReAct."""
    name: str
    description: str
    mcp_tool_name: str

    class Config:
        arbitrary_types_allowed = True

    def _run(self, **kwargs) -> str:
        print(f"Calling MCP tool '{self.mcp_tool_name}' with params: {kwargs}")
        result = asyncio.run(call_mcp_tool(self.mcp_tool_name, **kwargs))
        return str(result)

    async def _arun(self, tool_input: str) -> str:
        params = json.loads(tool_input)
        result = await call_mcp_tool(self.mcp_tool_name, **params)
        return str(result)

tools = [
    MCPTool(
        name="send_email",
        description="Send an email. Requires: to (email), subject, body",
        mcp_tool_name="send_email",
        args_schema=EmailInput
    ),
    MCPTool(
        name="add",
        description="Add two numbers. Requires: a (int), b (int)",
        mcp_tool_name="add",
        args_schema=AddInput
    ),
]

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
)

memory = InMemorySaver()

helpful_assistant = create_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,
    system_prompt = """
You are a helpful assistant.
"""
)

user_input = "send email to zeeshan@gmail.com the leave request also check whatr is the sum of 500 , 600 "
response = helpful_assistant.invoke(
    {"messages": [{"role": "user", "content": user_input}]},
    config={"configurable": {"thread_id": "123"}}
)

print(response["messages"][-1].content if "messages" in response else response)
