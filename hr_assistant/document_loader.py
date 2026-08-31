from langchain_community.document_loaders import TextLoader
from hr_assistant import config
from lark import logger
from hr_assistant.logger import get_logger

logger= get_logger(__name__)

def load_document(file_path:str= config.DATA_FILE_PATH):
    """load a .txt file and return it as a list of langchain documents"""
    logger.info("loading document from '%s'", file_path)
    loader = TextLoader(file_path, encoding="utf-8")
    documents= loader.load()
    logger.info("loaded %d documents", len(documents))
    return documents
