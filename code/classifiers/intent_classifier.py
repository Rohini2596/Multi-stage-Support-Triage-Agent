from __future__ import annotations
class IntentClassifier:
    def __init__(self):
        pass
    def classify(self, text: str) -> str:
        t = (text or "").lower()
        if any(k in t for k in ["refund", "cancel subscription", "charged", "billing", "payment",]):
            return "product_issue"
        if any(k in t for k in ["feature request", "add feature", "new feature", "improvement",]):
            return "feature_request"
        if any(k in t for k in ["bug", "error", "crash", "not working", "issue", "failed",]):
            return "bug"
        return "product_issue"