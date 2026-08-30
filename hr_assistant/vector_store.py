from langchain_community.vectorstores import FAISS
import os

from hr_assistant import config
from hr_assistant.embeddings import get_embedding_model

def build_vector_store(chunks):
    """embed every chunk and build
    a searchable faiss index in memory"""
    embedding_model= get_embedding_model()
    vector_store= FAISS.from_documents(
        documents= chunks,
        embedding= embedding_model
    )
    return vector_store


#save vector store

def save_vector_store(vector_store, path:str= config.VECTOR_STORE_PATH)->None:
    """save the faiss index to disk 
    so we dont have to rebuild it every time"""
    vector_store.save_local(path)


def load_vector_store(path:str= config.VECTOR_STORE_PATH)->None:
    """load the previously saved faiss index from disk"""
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
    retriever= vector_store.as_retriever(
        search_kwargs={
            "k": k
        }
    )
    return retriever