from code.agent import (
    SupportAgent,
)

from code.ui.terminal_ui import (
    show_banner,
    show_ticket,
    show_result,
)

agent = SupportAgent()

show_banner()

while True:

    print("\n====================")
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

    show_ticket(fake_ticket)

    result = (
        agent.pipeline.process_row(
            fake_ticket
        )
    )

    show_result(result)