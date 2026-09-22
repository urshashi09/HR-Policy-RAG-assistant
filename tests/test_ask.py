from hr_assistant.pipeline import ask, build_hr_assistant


def test_ask_returns_a_real_answer():
    agent = build_hr_assistant()
    answer = ask(agent, "How many days of paid annual leave do I get per year?")

    assert isinstance(answer, str)
    assert answer.strip() != ""