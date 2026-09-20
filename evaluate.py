from hr_assistant.evaluation import run_evaluation


def main():
    print("Running HR policy evaluation...")
    result= run_evaluation()
    print("evaluation result: ", result)


if __name__ == "__main__":
    main()