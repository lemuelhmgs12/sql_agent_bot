"""
Builds the ABC Grocery SQL agent: LLM + SQL tools + system prompt.
Run from the project root:  uv run python -m src.agent
"""
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src import config
from src.database import get_database


def load_system_prompt():
    """Read the system prompt from prompts/sql-agent-system-prompt.txt."""
    with open(config.PROMPT_FILE, "r", encoding="utf-8") as f:
        system_text = f.read() 
    return system_text

def build_agent():
    """Create the SQL agent: the LLM, the four SQL tools and the system prompt."""
    db = get_database()
    
    llm = ChatOpenAI(model=config.LLM_MODEL,
                     temperature=0)
    
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    agent = create_agent(model=llm,
                         tools=tools,
                         system_prompt=load_system_prompt())
    return agent


def ask(agent, question):
    """Send one question to the agent and return its final answer as text."""
    result = agent.invoke({"messages": [HumanMessage(content=question)]})

    return result["messages"][-1].content


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    agent = build_agent()
    print(ask(agent, "On average, which gender lives furthest from store?"))