
from hr_assistant.gateway import get_gateway_llm

from hr_assistant.logger import get_logger

logger= get_logger(__name__)

def get_llm():
    """return a chat model"""
    logger.info("loading llm model via Portkey gateway")
    return get_gateway_llm()