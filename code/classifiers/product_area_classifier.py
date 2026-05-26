from __future__ import annotations
class ProductAreaClassifier:
    def __init__(self):
        pass
    def classify(self, text: str, company: str,) -> str:
        t = (text or "").lower()
        company = (company or "").lower()
        if company == "claude":
            if any(k in t for k in ["refund", "billing", "subscription", "payment", "charged", "pro", "max",]):
                return "claude_billing"
            if any(k in t for k in ["api", "console", "token", "key",]):
                return "claude_api"
            return "claude_general"
        if company == "visa":
            if any(k in t for k in ["payment", "transaction", "refund", "card",]):
                return "visa_payments"
            return "visa_general"
        if company == "devplatform":
            if any(k in t for k in ["deployment", "sdk", "api", "build",]):
                return "devplatform_developer_tools"
            return "devplatform_general"
        return "general"
_classifier = ProductAreaClassifier()
def classify_product_area(text: str, company: str,) -> str:
    return _classifier.classify(text=text,company=company,)