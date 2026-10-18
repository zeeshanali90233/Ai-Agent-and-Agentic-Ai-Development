import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console

# Use GROQ
model_client = OpenAIChatCompletionClient(
   model="openai"
   
)

async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is 73 degrees and Sunny."


# The system message instructs the agent via natural language.
agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant.",
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)


# Run the agent and stream the messages to the console.
async def main() -> None:
    await Console(agent.run_stream(task="What is the weather in New York?"))
    # Close the connection to the model client.
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())