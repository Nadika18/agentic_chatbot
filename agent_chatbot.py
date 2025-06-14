from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
import openai
import os
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
ddg_search = DuckDuckGoSearchResults()

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)



tools = [
   Tool(
       name="DuckDuckGo Search",
       func=ddg_search.run,
       description="Useful to browse information from the Internet.",
   )
]


llm = ChatOpenAI(model_name="gpt-4.1-mini")

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Previous_conversation:
{chat_history}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)

# Create a ReAct-style agent that uses the search tool
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# Build the AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# query = "What is the process of applying for visa in Germany for Nepali citizens?"
# response = agent_executor.invoke({"input": query})
# print(response['output'])
query1 = "What is the process of applying for visa in Japan for Nepali citizens?"
response1 = agent_executor.invoke({"input": query1})
print(response1['output'])

query2 = "What documents do I need?"
response2 = agent_executor.invoke({"input": query2})
print(response2['output'])
