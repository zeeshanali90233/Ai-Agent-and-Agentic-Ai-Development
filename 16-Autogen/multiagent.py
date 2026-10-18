import asyncio
import datetime
import sys

import httpx
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from urllib.parse import quote

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-120b",
    api_key="API_KEY",
    base_url="https://api.groq.com/openai/v1",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": False,
        "family": "unknown",
    },
)

# ============================================================
# 2) TOOLS (type hints + docstrings = auto tool schema)
# ============================================================

def get_current_time(timezone_offset_hours: float = 5.0) -> str:
    """Get current date/time. Default offset is +5 (Pakistan Standard Time)."""
    tz = datetime.timezone(datetime.timedelta(hours=timezone_offset_hours))
    return datetime.datetime.now(tz).strftime("%A, %d %B %Y, %I:%M %p (UTC%z)")



async def get_weather(city: str) -> str:
    """Get current weather for a city (temperature, condition, humidity, wind)."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"https://wttr.in/{city}", params={"format": "j1"})
            r.raise_for_status()
            c = r.json()["current_condition"][0]
            return (f"{city}: {c['temp_C']}°C (feels {c['FeelsLikeC']}°C), "
                    f"{c['weatherDesc'][0]['value']}, humidity {c['humidity']}%, "
                    f"wind {c['windspeedKmph']} km/h")
    except Exception as e:
        return f"Weather error: {e}"


async def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount between currencies using live exchange rates (e.g. USD -> PKR)."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"https://open.er-api.com/v6/latest/{from_currency.upper()}")
            r.raise_for_status()
            rate = r.json()["rates"][to_currency.upper()]
            return (f"{amount} {from_currency.upper()} = {amount * rate:,.2f} "
                    f"{to_currency.upper()} (rate {rate})")
    except Exception as e:
        return f"Currency error: {e}"

WIKI_HEADERS = {
    "User-Agent": "AutoGenClassDemo/1.0 (contact: your-email@example.com)"
}


async def wikipedia_search(query: str) -> str:
    """Search Wikipedia and return a short summary of the top result."""
    try:
        async with httpx.AsyncClient(timeout=15, headers=WIKI_HEADERS,
                                     follow_redirects=True) as client:
            s = await client.get("https://en.wikipedia.org/w/api.php", params={
                "action": "query", "list": "search", "srsearch": query,
                "format": "json", "srlimit": 1,
            })
            s.raise_for_status()
            hits = s.json()["query"]["search"]
            if not hits:
                return "No results found."
            title = hits[0]["title"]
            p = await client.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title.replace(' ', '_'))}"
            )
            p.raise_for_status()
            return f"{title}: {p.json().get('extract', 'No summary.')}"
    except Exception as e:
        return f"Wikipedia error: {e}"

planner = AssistantAgent(
    name="Planner",
    model_client=model_client,
    description="Breaks the task into steps and assigns them. Speaks first.",
    system_message=(
        "You are the Planner. Break the user's task into clear subtasks and assign each:\n"
        "- Researcher: weather, time, Wikipedia facts\n"
        "- Analyst: calculations, currency conversion\n"
        "- Writer: final answer\n"
        "Keep the plan short. Do not do the work yourself."
    ),
)

researcher = AssistantAgent(
    name="Researcher",
    model_client=model_client,
    description="Finds facts using weather, time, and Wikipedia tools.",
    tools=[get_weather, get_current_time, wikipedia_search],
    reflect_on_tool_use=True,
    system_message="You are the Researcher. Use your tools to gather facts. Report findings briefly.",
)

analyst = AssistantAgent(
    name="Analyst",
    model_client=model_client,
    description="Does math and currency conversions using tools.",
    tools=[ convert_currency],
    reflect_on_tool_use=True,
    system_message="You are the Analyst. Always use tools for numbers; never guess. Report results briefly.",
)

writer = AssistantAgent(
    name="Writer",
    model_client=model_client,
    description="Writes the final answer once all subtasks are done.",
    system_message=(
        "You are the Writer. Once research and analysis are complete, combine everything "
        "into a clean, concise final answer for the user. End your message with: TERMINATE"
    ),
)

# ============================================================
# 4) TEAM (LLM selects the next speaker)
# ============================================================

SELECTOR_PROMPT = """Select the next agent to perform the task.

{roles}

Conversation so far:
{history}

Rules:
- Planner speaks first only.
- Pick Researcher or Analyst for pending subtasks.
- Pick Writer only when all subtasks are done.
Read the conversation, then select ONE agent from {participants}. Reply with the name only."""

termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)

team = SelectorGroupChat(
    participants=[planner, researcher, analyst, writer],
    model_client=model_client,
    termination_condition=termination,
    selector_prompt=SELECTOR_PROMPT,
    allow_repeated_speaker=True,
)

# ============================================================
# 5) RUN
# ============================================================

DEFAULT_TASK = (
    "What's the current weather and time in Lahore? Convert 1500 USD to PKR, "
    "then calculate 18% tax on that PKR amount. Also give a 2-line Wikipedia summary of Lahore."
)

async def main():
    task = " ".join(sys.argv[1:]) or DEFAULT_TASK
    try:
        await Console(team.run_stream(task=task))
    finally:
        await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())