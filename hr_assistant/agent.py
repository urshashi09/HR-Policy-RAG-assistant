from langchain.agents import create_agent
from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def create_hr_agent(llm, tools ):
    """return a langchain agent that can call our tools to answer questions about the hr policy document"""
    logger.info("creating HR agent with %d tools(s)", len(tools))
    agent= create_agent(
        model= llm,
        tools= tools,
        system_prompt = config.SYSTEM_PROMPT
    )
    logger.info("HR agent ready")
    return agent