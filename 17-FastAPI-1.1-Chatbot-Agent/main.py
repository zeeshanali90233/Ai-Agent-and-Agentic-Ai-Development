from fastapi import FastAPI
from lib.agent import helpingagent
from lib.chatbot import guidingchatbot

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/agent")
def get_help(q: str | None = None, thread_id: str | None = None):
    response=helpingagent.invoke(
        {"messages": [{"role": "user", "content": q}]},
        config={"configurable": {"thread_id": thread_id}}
    )
    return {"message": response['messages'][-1]}

@app.get("/chatbot")
def get_chatbot_response(q: str | None = None):
    messages = [
        (
            "system",
            "You are an software engineer who only answer related queries.",
        ),
        ("human", q),
    ]
    ai_msg = guidingchatbot.invoke(messages)

    return {"message": ai_msg.content}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}