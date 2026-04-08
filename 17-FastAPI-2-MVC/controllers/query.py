from google import genai
from dotenv import load_dotenv
import os

# pip install google-genai dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_query_answer(q: str):
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=q
    )
    return {q: response.text}