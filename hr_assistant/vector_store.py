from langchain_community.vectorstores import FAISS
import os

from hr_assistant import config
from hr_assistant.embeddings import get_embedding_model
from hr_assistant.logger import get_logger

logger= get_logger(__name__)

def build_vector_store(chunks):
    """embed every chunk and build
    a searchable faiss index in memory"""
    logger.info("embedding %d chunk(s) and building vector store", len(chunks))
    embedding_model= get_embedding_model()
    vector_store= FAISS.from_documents(
        documents= chunks,
        embedding= embedding_model
    )
    logger.info("faiss index built in memory")
    return vector_store


#save vector store

def save_vector_store(vector_store, path:str= config.VECTOR_STORE_PATH)->None:
    """save the faiss index to disk 
    so we dont have to rebuild it every time"""
    vector_store.save_local(path)
    logger.info("vector store saved to '%s'", path)


def load_vector_store(path:str= config.VECTOR_STORE_PATH)->None:
    """load the previously saved faiss index from disk"""
    logger.info("loading vector store from '%s'", path)
    embeddings_model= get_embedding_model()
    vector_store= FAISS.load_local(
        path, 
        embeddings_model, 
        allow_dangerous_deserialization=True
    )
    return vector_store


def vector_store_exists(path:str= config.VECTOR_STORE_PATH)->bool:
    index_path= os.path.join(path, "index.faiss")
    return os.path.exists(index_path)


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