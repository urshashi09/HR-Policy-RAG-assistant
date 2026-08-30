from langchain_community.embeddings import JinaEmbeddings
from hr_assistant import config

def get_embedding_model():
    """return jina embedding model"""
    llm= JinaEmbeddings(
        model_name=config.EMBEDDING_MODEL_NAME, 
        jina_api_key=config.JINA_API_KEY
        )