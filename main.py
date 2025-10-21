from dotenv import load_dotenv
from pydantic import BaseModel
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor

from tools import search_tool, save_tool

load_dotenv()

class ResearchResponse (BaseModel) :
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# llm1 = ChatOpenAI( model = "gpt-4o-mini")
# llm2 = ChatAnthropic( model = "claude-3-5-sonnet-20241022") 

llm = ChatGoogleGenerativeAI ( model = "gemini-2.5-flash")

parser = PydanticOutputParser (pydantic_object = ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
             You are a research assistant that will help generate a research paper.
             Answer the user query  and use necessary tools.
             Wrap the output in this format and provide no other text\n{format_instructions}
             """
            
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions = parser.get_format_instructions())

tools = [search_tool, save_tool]
agent = create_react_agent(
    llm = llm,
    prompt = prompt,
    tools = tools
)

agent_executor = AgentExecutor(agent = agent, tools = tools, verbose = True)

query = input("What can I help you with? \n")
raw_response = agent_executor.invoke({"query" : query})
text_part = raw_response["output"].split("```json")[0].strip()
print(text_part)

# try:
#     structured_response = parser.parse(raw_response.get("output")[0]["text"])
#     print(structured_response.topic)
# except Exception as e:
#     print("Error parsing response.", e, "Raw Response -", raw_response)


# print(structured_response.topic)