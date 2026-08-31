from langchain_groq import ChatGroq
from hr_assistant import config
from hr_assistant.logger import get_logger

logger= get_logger(__name__)

def get_llm():
    """return a chat model"""
    logger.info("loading llm model '%s'", config.LLM_MODEL_NAME)
    llm= ChatGroq(
    model= config.LLM_MODEL_NAME,
    temperature= 0
)
    return llm