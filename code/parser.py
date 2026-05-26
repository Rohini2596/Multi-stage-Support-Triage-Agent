import json
def parse_issue(issue_text: str):
    try:
        return json.loads(issue_text)
    except Exception:
        return [{"role": "user", "content": issue_text}]
def latest_user_message(messages):
    user_msgs = [m["content"] for m in messages if m.get("role") == "user"]
    return user_msgs[-1] if user_msgs else ""
def flatten_conversation(messages):
    lines = []
    for m in messages:
        role = m.get("role", "unknown")
        content = m.get("content", "")
        lines.append(f"{role}: {content}")

    return "\n".join(lines)