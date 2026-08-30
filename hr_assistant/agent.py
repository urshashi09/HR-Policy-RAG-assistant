from langchain.agents import create_agent
from hr_assistant import config

def create_hr_agent(llm, tools ):
    """return a langchain agent that can call our tools to answer questions about the hr policy document"""
    agent= create_agent(
        model= llm,
        tools= tools,
        system_prompt = config.SYSTEM_PROMPT
    )
    return agent