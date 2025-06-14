import streamlit as st
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Define the DuckDuckGo search tool
ddg_search = DuckDuckGoSearchResults()
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=ddg_search.run,
        description="Useful to browse information from the Internet.",
    )
]

# ReAct prompt
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

# LLM
llm = ChatOpenAI(model_name="gpt-4.1-mini")

# Streamlit app
st.set_page_config(page_title="Visa Assistant", page_icon="🛂")
st.title("🛂 Visa Processing Assistant")



# Initialize chat history and memory only once
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)# Memory
    
memory = st.session_state.memory

# Agent & executor
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=False)


# Display past messages
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)

# Input from chat box
user_input = st.chat_input("Ask me anything about visa application...")

if user_input:
    st.chat_message("user").markdown(user_input)
    with st.spinner("Thinking..."):
        response = agent_executor.invoke({"input": user_input})
        final_answer = response["output"]
    st.chat_message("assistant").markdown(final_answer)

    # Save to chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", final_answer))
