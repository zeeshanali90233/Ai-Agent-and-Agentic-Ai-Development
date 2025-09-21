import streamlit as st
from agent import memory_agent


st.title("Talk to Agent")
st.write("This app demonstrates a conversational agent.")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_input = st.text_input("Ask a question:")
if st.button("Submit") and user_input:
    # Add user message to history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    with st.spinner("Agent is thinking..."):
        response = memory_agent.invoke(
            {"messages": st.session_state['messages']},
            config={"configurable": {"thread_id": "user123"}}
        )
    # Add agent response to history
    agent_message = response['messages'][-1].content
    st.session_state['messages'].append({"role": "assistant", "content": agent_message})

# Display conversation history
for msg in st.session_state['messages']:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Agent:** {msg['content']}")