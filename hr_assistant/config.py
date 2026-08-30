import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")


DATA_FILE_PATH= os.path.join( "data", "hr.txt")

VECTOR_STORE_PATH= os.path.join( "data", "faiss_index")

LLM_MODEL_NAME= "openai/gpt-oss-120b"

EMBEDDING_MODEL_NAME= "jina-embeddings-v5-omni-small"

CHUNK_SIZE= 500
CHUNK_OVERLAP= 100

TOP_K__RESULTS= 3

SYSTEM_PROMPT= ("you are a friendly hr assistant."
    "always use the search_hr_policy tool to look up facts before answering."
    "if answer isn't in the search results, say you don't know. instead of guessing.")


def check_api_keys()->None:
    """stop  early with a clear message if a required API key is missing"""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please set it in the .env file.")
    if not JINA_API_KEY:
        raise ValueError("JINA_API_KEY is not set. Please set it in the .env file.")