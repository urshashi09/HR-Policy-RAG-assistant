from langchain_openai import ChatOpenAI
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL
from hr_assistant import config
from hr_assistant.logger import get_logger
from hr_assistant.pipeline import ask, build_hr_assistant
from hr_assistant.vector_store import get_retriever, load_vector_store 

from langsmith import Client
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, RAG_GROUNDEDNESS_PROMPT  

client = Client()

logger = get_logger(__name__)


DATASET_NAME= "hr-policy-qa"

TEST_CASES = [
    {"question": "How many days of paid annual leave do I get per year?",
    "answer": "20 days"},
    {"question": "How many days of unused annual leave can be carried forward?", "answer": "Up to 5 days"},
    {"question": "How many paid sick days do I get per year?", "answer": "10 days"},
    {"question": "How many days per week can I work from home?", "answer": "Up to 2 days, with manager approval"},
    {"question": "How long is the probation period?",
    "answer": "3 months"},
    {"question": "What is the notice period during probation?", "answer": "15 days"},
    {"question": "What is the standard notice period for resignation?",
    "answer": "30 days"},
    {"question": "Within how many days must reimbursement claims be submitted?",
    "answer": "30 days of the expense"},
    {"question": "How many public holidays does the company observe each year?", "answer": "12"},
    {"question": "Within how many days is full and final settlement processed after the last working day?", "answer": "45 days"},
]


JUDGE_MODEL_NAME= "openai/gpt-oss-120b"


def _get_judge_llm()-> ChatOpenAI:
    """retrun a judge llm routed through portkey gateway"""
    headers= createHeaders(
        api_key=config.PORTKEY_API_KEY, 
        provider="@judgellm")
    return ChatOpenAI(
        api_key="portkey",
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=headers,
        model= JUDGE_MODEL_NAME
    )



def _ensure_dataset(client: Client):
    """create the langsmith dataset if it doesn't exist"""
    if client.has_dataset(dataset_name=DATASET_NAME):
        logger.info("Dataset '%s' already exists", DATASET_NAME)
        return client.read_dataset(dataset_name=DATASET_NAME)

    logger.info("Creating dataset '%s'", DATASET_NAME)
    dataset= client.create_dataset(dataset_name=DATASET_NAME)
    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {"inputs": {"question": case["question"]},
            "outputs": {"answer": case["answer"]}}
            for case in TEST_CASES
        ],
    )
    return dataset


def run_evaluation():
    """Upload the dataset (if needed) 
    and run the correctness evaluation."""
    client = Client()
    dataset = _ensure_dataset(client)

    agent = build_hr_assistant()
    retriever = get_retriever(load_vector_store())

    # write the answers 
    def target(inputs: dict) -> dict:
        """
        Run one test question through the real agent, 
        and also capture
        the retrieved chunks 
        so groundedness can check the answer against
        what was actually retrieved 
        (not just the reference answer).
        """
        answer = ask(agent, inputs["question"])
        chunks = retriever.invoke(inputs["question"])
        context = "\n\n".join(chunk.page_content for chunk in chunks)
        return {"answer": answer, "context": context}

    # giving marks 
    correctness_evaluator = create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        feedback_key="correctness",
        judge=_get_judge_llm(),
    )

    groundedness_judge = create_llm_as_judge(
        prompt=RAG_GROUNDEDNESS_PROMPT,
        feedback_key="groundedness",
        judge=_get_judge_llm(),
    )

    def groundedness_evaluator(outputs: dict, **kwargs) -> dict:
        """Check the answer is supported by the retrieved context, not invented."""
        return groundedness_judge(outputs={"answer": outputs["answer"]}, context=outputs["context"])

    logger.info("Running evaluation against dataset '%s'", DATASET_NAME)
    return client.evaluate(
        target,
        data=dataset.name,
        evaluators=[correctness_evaluator,
                groundedness_evaluator],
        experiment_prefix="hr-policy-eval",
        description="HR policy assistant correctness + groundedness evaluation",
    )