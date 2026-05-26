class SafetyGuard:
    BLOCKLIST = [
        "ignore previous instructions",
        "reveal system prompt",
        "developer message",
        "hidden instructions",
        "print prompt",
        "bypass safety",
    ]
    def check(self, text):
        lowered = text.lower()
        reasons = []
        for item in self.BLOCKLIST:
            if item in lowered:
                reasons.append(item)
        return {
            "safe": len(reasons) == 0,
            "reasons": reasons,
        }