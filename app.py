import streamlit as st
from main import agent_executor

# --- Page setup ---
st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AI Research Assistant")
st.write("Ask me anything related to research, and I’ll find information and summarize it for you!")

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chat UI ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("What can I help you with?")
if user_query:
    # Display user message
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent_executor.invoke({"query": user_query})
                bot_reply = response.get("output", "I couldn’t generate a response.")
                st.markdown(bot_reply)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Error: {e}")