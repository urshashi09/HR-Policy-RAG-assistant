from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def check_langsmith_tracing()->None:
    """log whether langsmith tracing is enaabled or not"""
    tracing_on= config.LANGSMITH_TRACING.lower() == "true"

    if tracing_on and config.LANGSMITH_API_KEY:
        logger.info("langsmith tracing is enabled- project '%s', traces at '%s'", 
                    config.LANGSMITH_PROJECT, 
                    "https://smith.langchain.com")
        
    else:
        logger.info("langsmith tracing is disabled")