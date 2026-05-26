from __future__ import annotations
class RiskClassifier:
    def __init__(self):
        pass
    def classify(self, text: str, injection_detected: bool = False, pii_detected: bool = False,) -> str:
        t = (text or "").lower()
        if injection_detected:
            return "critical"
        if any(k in t for k in ["lawsuit", "legal action", "fraud", "hack", "breach", "stolen", "unauthorized access",]):
            return "high"
        if pii_detected:
            return "medium"
        if any(k in t for k in ["refund", "billing", "charged", "payment",]):
            return "medium"
        return "low"