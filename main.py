from hr_assistant.pipeline import build_hr_assistant, ask
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("---starting CLI run---")
    print("building the hr policy assistant...")
    agent = build_hr_assistant()
    print("hr assistant ready")

    demo_ques=[
        "how many paid annual leave days do i get?",
        "what is the npotice period during probation?",
        "can i work form home everyday?"
    ]

    for question in demo_ques:
        answer= ask(agent, question)
        print("Question: ", question)
        print("Answer: ", answer)
        print("="*60)

    logger.info("---ending CLI run---")


if __name__ == "__main__": main()