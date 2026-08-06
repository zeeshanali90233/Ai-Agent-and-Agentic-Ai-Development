from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()

guidingchatbot = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")   
)