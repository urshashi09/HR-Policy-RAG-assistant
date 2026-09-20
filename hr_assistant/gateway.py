
from langchain_openai import ChatOpenAI
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL
from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)





def get_gateway_llm() -> ChatOpenAI:
    """Return a chat model routed through Portkey with automatic fallback."""

    logger.info("Routing LLM calls through Portkey")

    headers = createHeaders(
        api_key=config.PORTKEY_API_KEY,
        config=config.PORTKEY_CONFIG_ID
    )

    return ChatOpenAI(
        api_key=config.PORTKEY_API_KEY,
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=headers
    )

