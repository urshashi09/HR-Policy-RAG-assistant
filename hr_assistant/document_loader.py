from langchain_community.document_loaders import TextLoader
from hr_assistant import config

def load_document(file_path:str= config.DATA_FILE_PATH):
    """load a .txt file and return it as a list of langchain documents"""
    loader = TextLoader(file_path)
    return loader.load(file_path, encoding="utf-8")
    return loader.load()
