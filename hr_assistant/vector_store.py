from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os

from hr_assistant import config
from hr_assistant.embeddings import get_embedding_model
from hr_assistant.logger import get_logger

logger= get_logger(__name__)

def build_vector_store(chunks):
    """embed every chunk and upload it into
    qdrant cloud colllection"""
    logger.info("embedding %d chunk(s) and iploading to qdrant collection '%s'.", 
                len(chunks), config.QDRANT_COLLECTION_NAME)
    embedding_model= get_embedding_model()
    vector_store= QdrantVectorStore.from_documents(
        chunks,
        embedding= embedding_model,
        url= config.QDRANT_URL,
        api_key= config.QDRANT_API_KEY,
        collection_name= config.QDRANT_COLLECTION_NAME
    )
    logger.info("uploaded to qdrant collection '%s'", config.QDRANT_COLLECTION_NAME)
    return vector_store


#save vector store
# def save_vector_store(vector_store, path:str= config.VECTOR_STORE_PATH)->None:
#     """save the faiss index to disk 
#     so we dont have to rebuild it every time"""
#     vector_store.save_local(path)
#     logger.info("vector store saved to '%s'", path)


def load_vector_store():
    """connect to a qdrant cloud
    collection that was already created"""
    logger.info("connecting to qdrant cloud")
    embeddings_model= get_embedding_model()
    vector_store= QdrantVectorStore.from_documents(
        embedding= embeddings_model,
        url= config.QDRANT_URL,
        api_key= config.QDRANT_API_KEY,
        collection_name= config.QDRANT_COLLECTION_NAME
    )
    return vector_store


def vector_store_exists()->bool:
    """check if qdrant store already exists """
    client= QdrantClient(
        url= config.QDRANT_URL,
        api_key= config.QDRANT_API_KEY
    )
    return client.collection_exists(config.QDRANT_COLLECTION_NAME)


def get_retriever(vector_store, k:int= config.TOP_K__RESULTS):
    """turn vector store into a retriever
    that returns k most similar chunks"""
    logger.info("turning vector store into retriever with top k=%d results", k)
    retriever= vector_store.as_retriever(
        search_kwargs={
            "k": k
        }
    )
    return retriever