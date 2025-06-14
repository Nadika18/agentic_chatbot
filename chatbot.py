from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from react_prompt_template import template  
import os
from dotenv import load_dotenv
from model import ChatRequest  


class ChatAgent:
    def __init__(self, openai_api_key=None, model_name="gpt-4.1-mini"):
        load_dotenv()
        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = openai_api_key

        self.memory_store = {}

        self.ddg_search = DuckDuckGoSearchResults()
        self.tools = [
            Tool(
                name="DuckDuckGo Search",
                func=self.ddg_search.run,
                description="Internet info search tool."
            )
        ]

        self.prompt = PromptTemplate.from_template(template)
        self.llm = ChatOpenAI(model_name=model_name)

    def get_agent_executor(self, session_id: str) -> AgentExecutor:
        if session_id not in self.memory_store:
            self.memory_store[session_id] = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )
        memory = self.memory_store[session_id]

        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)
        return AgentExecutor(agent=agent, tools=self.tools, memory=memory, verbose=False)

    def chat(self, request: ChatRequest) -> str:
        agent_executor = self.get_agent_executor(request.session_id)
        result = agent_executor.invoke({"input": request.message})
        return result["output"]
