import re
def normalize_whitespace(text: str):
    return re.sub(
        r"\s+",
        " ",
        text or "",
    ).strip()
def parse_issue(issue_text: str):
    if not issue_text:
        return []
    issue_text = str(issue_text)
    if issue_text.startswith("["):
        return [issue_text]
    lines = issue_text.splitlines()
    messages = []
    current = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if (
            line.lower().startswith("customer:")
            or line.lower().startswith("support:")
            or line.lower().startswith("user:")
            or line.lower().startswith("assistant:")
        ):
            if current:
                messages.append(
                    " ".join(current)
                )
                current = []
        current.append(line)
    if current:
        messages.append(
            " ".join(current)
        )
    if not messages:
        messages = [issue_text]
    return messages
def flatten_conversation(messages):
    if not messages:
        return ""
    return "\n".join(messages)
def latest_user_message(messages):
    if not messages:
        return ""
    return str(messages[-1])
def redact_sensitive_literals(text: str):
    if not text:
        return ""
    text = re.sub(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "[REDACTED_EMAIL]",
        text,
    )
    text = re.sub(
        r"\b\d{10,}\b",
        "[REDACTED_NUMBER]",
        text,
    )
    text = re.sub(
        r"\b\d{12,19}\b",
        "[REDACTED_CARD]",
        text,
    )
    return text