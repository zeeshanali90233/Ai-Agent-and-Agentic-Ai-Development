import streamlit as st


from google import genai
from google.genai import types

client = genai.Client(api_key='APIKEy')

st.title("Talk to Agent")
st.write("This app demonstrates a conversational agent.")

user_input = st.text_input("Ask a question:")
if st.button("Submit"):
    with st.spinner("Agent is thinking..."):
        response = client.models.generate_content(
            model='gemini-3.5-flash', contents='Kia Mari Earning hogi',
            config=types.GenerateContentConfig(
            system_instruction="""
        You are an Experienced Sales Women named Alexa, 
        Who gives the best sales pitch to customers,
        Course Pricing
        Web with Agentic AI: $1000
        Data Science: $500
        """),
        )
    st.write(response.text)