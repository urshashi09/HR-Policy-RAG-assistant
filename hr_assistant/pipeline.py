from hr_assistant import config
from hr_assistant.agent import create_hr_agent
from hr_assistant.document_loader import load_document
from hr_assistant.llm import get_llm
from hr_assistant.doc_splitter import split_into_chunks
from hr_assistant.tools import create_search_tool
from hr_assistant.vector_store import vector_store_exists, load_vector_store, build_vector_store, get_retriever  
from hr_assistant.logger import get_logger
from hr_assistant.tracing import check_langsmith_tracing
from hr_assistant.guardrails import REFUSAL_RESPONSE, check_input, check_output

logger = get_logger(__name__)


#data ingestion
def build_vector_store_for_document(file_path:str = config.DATA_FILE_PATH):
    """load + split + embed the document, 
    or reusing a qdrant store if we have one"""
    if vector_store_exists():
        logger.info("loading vector store from disk that already exists")
        vector_store= load_vector_store()
        return vector_store

    logger.info("no qdrant collection found, building one from scratch")
    documents= load_document(file_path)
    chunks= split_into_chunks(documents)
    vector_store= build_vector_store(chunks)
    return vector_store


#data retrieval

def build_hr_assistant(file_path:str= config.DATA_FILE_PATH):
    """build rag agent for the hr policy document"""

    logger.info("building HR assistant")
    config.check_api_keys()
    check_langsmith_tracing()

    vector_store= build_vector_store_for_document(file_path)
    retriever= get_retriever(vector_store)
    llm= get_llm()
    tools= [create_search_tool(retriever)]
    agent= create_hr_agent(llm, tools)
    logger.info("HR assistant ready to take questions")
    return agent


def ask(agent, question: str)->str:
    """ask the agent a question and return the response"""
    logger.info("asking question: '%s'", question)

    # input guard to make sure input is safe
    input_is_safe, _= check_input(question)
    if not input_is_safe:
        logger.warning("input guard triggered for question: '%s'", question)
        return REFUSAL_RESPONSE

    response= agent.invoke({
        "messages":[{
            "role": "user", "content": question
        }]
    })
    answer= response["messages"][-1].content
    logger.info("answer: '%s'", answer)

    # output guard to make sure output is safe
    output_is_safe, _= check_output(answer)
    if not output_is_safe:
        logger.warning("output guard triggered for answer: '%s'", answer)
        return REFUSAL_RESPONSE

    
    
    return answer