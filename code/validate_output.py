from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
REQUIRED_COLUMNS = [
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
ALLOWED_STATUS = {"replied", "escalated"}
ALLOWED_REQUEST_TYPES = {"product_issue", "feature_request", "bug", "invalid"}
ALLOWED_RISK = {"low", "medium", "high", "critical"}
def main():
    root = Path(__file__).resolve().parents[1]
    output_path = root / "support_tickets" / "output.csv"
    if not output_path.exists():
        raise SystemExit(f"Missing output.csv: {output_path}")
    df = pd.read_csv(output_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing columns: {missing}")
    for idx, row in df.iterrows():
        if row["status"] not in ALLOWED_STATUS:
            raise SystemExit(f"Invalid status in row {idx}: {row['status']}")
        if row["request_type"] not in ALLOWED_REQUEST_TYPES:
            raise SystemExit(f"Invalid request_type in row {idx}: {row['request_type']}")
        if row["risk_level"] not in ALLOWED_RISK:
            raise SystemExit(f"Invalid risk_level in row {idx}: {row['risk_level']}")
        try:
            conf = float(row["confidence_score"])
        except Exception:
            raise SystemExit(f"Invalid confidence_score in row {idx}: {row['confidence_score']}")
        if not (0.0 <= conf <= 1.0):
            raise SystemExit(f"confidence_score out of range in row {idx}: {conf}")
        try:
            parsed = json.loads(row["actions_taken"]) if str(row["actions_taken"]).strip() else []
            if not isinstance(parsed, list):
                raise ValueError
        except Exception:
            raise SystemExit(f"actions_taken must be valid JSON array in row {idx}")
    print("Validation passed.")
if __name__ == "__main__":
    main()
