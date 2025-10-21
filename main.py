import gradio as gr
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_react_agent, AgentExecutor
from tools import search_tool, save_tool

load_dotenv()

# Define output model
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Parser setup
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt setup
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Tools and agent setup
tools = [search_tool, save_tool]
agent = create_react_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

# Function to handle chat
def chat(query):
    raw_response = agent_executor.invoke({"query": query})
    text_part = raw_response["output"].split("```json")[0].strip()
    return text_part

# Gradio UI
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    user_input = gr.Textbox(label="Your Query")
    submit_btn = gr.Button("Send")

    def respond(user_message, chat_history):
        reply = chat(user_message)
        chat_history.append((user_message, reply))
        return "", chat_history

    submit_btn.click(respond, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

demo.launch()
