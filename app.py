import streamlit as st
from main import agent_executor

# --- Page setup ---
st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Research Assistant")
st.caption("Ask any research question — I’ll summarize and cite my findings for you!")

# --- Initialize session state for chat history ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Options")
    if st.button("🧹 Clear Chat"):
        st.session_state["messages"] = []
        st.experimental_rerun()

# --- Display previous messages ---
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input area ---
if prompt := st.chat_input("Ask me something..."):
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Run your agent with the query
                raw_response = agent_executor.invoke({"query": prompt})
                
                # Extract the clean output text
                output = raw_response.get("output", "")
                if isinstance(output, str):
                    text_part = output.split("```json")[0].strip()
                else:
                    text_part = str(output)

                st.markdown(text_part)
                st.session_state["messages"].append({"role": "assistant", "content": text_part})

            except Exception as e:
                st.error(f"⚠️ Error: {e}")