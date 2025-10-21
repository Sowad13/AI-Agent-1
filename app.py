import streamlit as st
from main import agent_executor
import json

# --- Page setup ---
st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="centered")

st.title("AI Research Assistant")
st.write("Ask me anything! I’ll search, summarize, and give you structured research answers.")

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
if prompt := st.chat_input("Type your query here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = agent_executor.invoke({"query": prompt})
            ai_text = response.get("output", "No response generated.")
        except Exception as e:
            ai_text = f"Error: {str(e)}"

        message_placeholder.markdown(ai_text)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_text})
