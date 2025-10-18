from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def get_query_answer(q: str):
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
    )
    return {q: response.text}