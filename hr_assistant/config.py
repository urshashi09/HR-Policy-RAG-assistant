import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")

GUARD_MODEL_NAME= "openai/gpt-oss-safeguard-20b"

LANGSMITH_TRACING= os.getenv("LANGSMITH_TRACING", "false") 
LANGSMITH_ENDPOINT= os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_PROJECT= os.getenv("LANGSMITH_PROJECT")
LANGSMITH_API_KEY= os.getenv("LANGSMITH_API_KEY")


DATA_FILE_PATH= os.path.join( "data", "hr.txt")

VECTOR_STORE_PATH= os.path.join( "data", "faiss_index")
QDRANT_URL= os.getenv("QDRANT_URL")
QDRANT_API_KEY= os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME  = os.getenv("QDRANT_COLLECTION_NAME", "hr_policy")

LLM_MODEL_NAME= "openai/gpt-oss-120b"

EMBEDDING_MODEL_NAME= "jina-embeddings-v5-omni-small"

CHUNK_SIZE= 500
CHUNK_OVERLAP= 100

TOP_K__RESULTS= 3

SYSTEM_PROMPT = """
You are a friendly HR Policy Assistant.

For greetings or questions about who you are, introduce yourself as an assistant
that helps employees understand the company HR policy document. You may answer
these conversational questions without using a tool.

For questions about HR policy, always use the search_hr_policy tool to look up
facts before answering. If the answer is not in the search results, say you do
not know instead of guessing.
"""


def check_api_keys()->None:
    """stop  early with a clear message if a required API key is missing"""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please set it in the .env file.")
    if not JINA_API_KEY:
        raise ValueError("JINA_API_KEY is not set. Please set it in the .env file.")
