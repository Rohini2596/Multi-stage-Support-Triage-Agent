from code.agent import (
    SupportAgent,
)
agent = SupportAgent()
while True:
    print("====================")
    print("ENTER TEST TICKET")
    print("====================")
    text = input("Ticket: ")
    if text.lower() == "exit":
        break
    fake_ticket = {
        "subject": "Manual Test",
        "company": "OpenAI",
        "issue": text,
    }
    result = (
        agent.pipeline.process_row(
            fake_ticket
        )
    )
    print("RESULT:")
    print("=" * 40)
    for k, v in result.items():
        print(f"{k}:")
        print(v)
        print("-" * 40)