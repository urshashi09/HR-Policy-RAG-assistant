from langchain_community.embeddings import JinaEmbeddings
from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def get_embedding_model():
    """return jina embedding model"""
    logger.info("loading embedding model '%s", config.EMBEDDING_MODEL_NAME)
    embedding_model = JinaEmbeddings(
        model_name=config.EMBEDDING_MODEL_NAME, 
        jina_api_key=config.JINA_API_KEY
        )
    return embedding_model
