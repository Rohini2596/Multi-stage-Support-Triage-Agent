import json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


console = Console()


def show_banner():

    console.print(
        Panel.fit(
            "[bold cyan]SUPPORT TRIAGE AGENT[/bold cyan]\n"
            "[green]MLE Hiring Challenge[/green]",
            border_style="blue",
        )
    )


def show_ticket(ticket):

    table = Table(
        title="Incoming Ticket",
        box=box.ROUNDED,
    )

    table.add_column(
        "Field",
        style="cyan",
        width=15,
    )

    table.add_column(
        "Value",
        style="white",
        overflow="fold",
    )

    table.add_row(
        "Subject",
        str(ticket.get("subject", "")),
    )

    table.add_row(
        "Company",
        str(ticket.get("company", "")),
    )

    table.add_row(
        "Language",
        str(ticket.get("language", "")),
    )

    console.print(table)


def show_result(result):

    risk = result.get(
        "risk_level",
        "unknown",
    )

    confidence = result.get(
        "confidence_score",
        0,
    )

    status = result.get(
        "status",
        "unknown",
    )

    response = result.get(
        "response",
        "",
    )

    table = Table(
        title="Pipeline Result",
        box=box.ROUNDED,
    )

    table.add_column(
        "Field",
        style="magenta",
        width=18,
    )

    table.add_column(
        "Value",
        style="white",
        overflow="fold",
    )

    table.add_row(
        "Status",
        str(status),
    )

    table.add_row(
        "Risk",
        str(risk),
    )

    table.add_row(
        "Confidence",
        str(confidence),
    )

    table.add_row(
        "Product Area",
        str(
            result.get(
                "product_area",
                "",
            )
        ),
    )

    table.add_row(
        "Request Type",
        str(
            result.get(
                "request_type",
                "",
            )
        ),
    )

    console.print(table)

    console.print(
        Panel(
            response,
            title="Generated Response",
            border_style="green",
        )
    )

    actions = result.get(
        "actions_taken",
        [],
    )

    # HANDLE JSON STRING

    if isinstance(actions, str):

        try:

            actions = json.loads(actions)

        except Exception:

            actions = []

    # HANDLE NONE

    if actions is None:
        actions = []

    # SHOW ACTION TABLE

    if actions:

        action_table = Table(
            title="Planned Actions",
            box=box.ROUNDED,
        )

        action_table.add_column(
            "Action",
            style="yellow",
            width=25,
        )

        action_table.add_column(
            "Parameters",
            style="white",
            overflow="fold",
        )

        for a in actions:

            # DICT FORMAT

            if isinstance(a, dict):

                action_table.add_row(

                    str(
                        a.get(
                            "action",
                            "-",
                        )
                    ),

                    str(
                        a.get(
                            "parameters",
                            {},
                        )
                    ),
                )

            # STRING FORMAT

            else:

                action_table.add_row(
                    str(a),
                    "-",
                )

        console.print(action_table)