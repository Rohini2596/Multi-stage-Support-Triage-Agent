from __future__ import annotations

import pandas as pd

from code.agent import (
    SupportAgent,
)
from code.config import (
    INPUT_CSV,
    OUTPUT_CSV,
)
from code.ui.terminal_ui import (
    show_banner,
    show_ticket,
    show_result,
)
def main():
    print("STARTING SUPPORT TRIAGE AGENT...")
    if not INPUT_CSV.exists():

        raise SystemExit(
            f"Input CSV not found: "
            f"{INPUT_CSV}"
        )
    print(
        f"Reading tickets from:"
        f"{INPUT_CSV}"
    )
    df = pd.read_csv(
        INPUT_CSV
    )

    print(
        f"Loaded {len(df)} tickets\n"
    )
    agent = SupportAgent()
    show_banner()
    # RUN PIPELINE
    outputs = []
    for _, row in df.iterrows():

        ticket = row.to_dict()

        show_ticket(ticket)

        result = agent.pipeline.process_row(ticket)

        show_result(result)

        outputs.append(result)
    out_df = pd.DataFrame(
        outputs
    )
    ordered_cols = [

        "status",

        "product_area",

        "response",

        "justification",

        "request_type",

        "confidence_score",

        "source_documents",

        "risk_level",

        "pii_detected",

        "language",

        "actions_taken",
    ]
    for col in ordered_cols:
        if col not in out_df.columns:
            out_df[col] = ""
    out_df = out_df[
        ordered_cols
    ]
    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    out_df.to_csv(
        OUTPUT_CSV,
        index=False,
    )
    print(
        "PROCESSING COMPLETE"
    )
    print(
        f"Wrote "
        f"{len(out_df)} rows "
        f"to:\n{OUTPUT_CSV}\n"
    )
    print(
        "Logs available at:"
        "logs/log.txt"
    )
if __name__ == "__main__":
    main()