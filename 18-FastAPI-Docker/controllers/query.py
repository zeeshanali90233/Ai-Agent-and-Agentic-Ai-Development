from dotenv import load_dotenv
from agents.help import helping_agent as agent

load_dotenv()

def get_query_answer(q: str):
    try:
        res = agent.invoke(
            {"messages": [{"role": "user", "content": q}]}
        )
        print(res['messages'][-1].content)
        if isinstance(res['messages'][-1].content, list):
            answer = res['messages'][-1].content[-1]['text']
        else:
            answer = res['messages'][-1].content
        return {"query": q, "answer": answer}
    except Exception as e:
        return {"query": q, "error": str(e)}