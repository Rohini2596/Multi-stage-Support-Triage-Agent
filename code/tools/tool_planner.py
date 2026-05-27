from __future__ import annotations

import json
from typing import (
    Dict,
    List,
    Any,
)
from code.config import (
    API_SPEC_PATH,
)
from code.utils.query_expansion import expand_query
class ToolPlanner:
    def __init__(self):
        self.spec = (
            self._load_spec()
        )
    def _load_spec(self):
        if API_SPEC_PATH.exists():
            try:
                return json.loads(
                    API_SPEC_PATH.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                return {}
        return {}
    def _tool_exists(
        self,
        name: str
    ) -> bool:
        spec = self.spec
        if isinstance(spec, dict):
            if name in spec:
                return True
            tools = spec.get(
                "tools"
            )
            if isinstance(
                tools,
                list
            ):
                for t in tools:
                    if (
                        isinstance(
                            t,
                            dict
                        )
                        and t.get("name")
                        == name
                    ):
                        return True
        if isinstance(spec, list):
            return any(
                isinstance(t, dict)
                and t.get("name")
                == name
                for t in spec
            )
        return False
    def plan(
        self,
        text: str,
        pii_detected: bool,
        risk_level: str,
        injection_detected: bool,
    ):
        t = expand_query(
            text or ""
        ).lower()
        actions = []
        wants_refund = any(
            k in t
            for k in [
                "refund",
                "chargeback",
                "money back",
                "charged",
                "billing",
            ]
        )
        wants_lock = any(
            k in t
            for k in [
                "lock account",
                "freeze account",
                "disable account",
            ]
        )
        suspected_compromise = any(
            k in t
            for k in [
                "hacked",
                "account stolen",
                "unauthorized access",
                "account compromised",
                "someone logged in",
            ]
        )
        wants_verify = any(
            k in t
            for k in [
                "verify identity",
                "verification",
                "confirm my identity",
            ]
        )
        wants_recovery = any(
            k in t
            for k in [
                "account access",
                "locked out",
                "cannot login",
                "can't login",
            ]
        )
        if (
            wants_verify
            and self._tool_exists(
                "verify_identity"
            )
        ):
            actions.append({
                "action":
                    "verify_identity",
                "parameters": {
                    "method": "email_otp",
                    "target": "user_on_file"
                }
            })
        if wants_refund:
            if self._tool_exists(
                "verify_identity"
            ):
                actions.append({
                    "action":
                        "verify_identity",
                    "parameters": {
                        "method": "email_otp",
                        "target": "user_on_file"
                    }
                })
            actions.append({
                "action":
                    "escalate_to_human",
                "parameters": {
                    "priority": "normal",
                    "department": "billing",
                    "summary":
                        "Refund request requires "
                        "human review and approval."
                }
            })
            if (
                injection_detected
            ):
                actions.append({
                    "action":
                        "escalate_to_human",
                    "parameters": {
                        "priority": "urgent",
                        "department": "security",
                        "summary":
                            "Potential prompt injection "
                            "or adversarial behavior detected."
                    }
                })
            elif risk_level == "critical":
                actions.append({
                    "action":
                        "escalate_to_human",
                    "parameters": {
                        "priority": "high",
                        "department": "security",
                        "summary":
                            "Critical security or fraud risk detected."
                    }
                })
        if (
            (wants_lock or suspected_compromise)
            and self._tool_exists(
                "lock_account"
            )
        ):
            actions.append({
                "action":
                    "lock_account",
                "parameters": {
                    "user_identifier": "user_on_file",
                    "lock_reason": "suspected_fraud" if suspected_compromise else "user_requested"
                }
            })
        # ACCOUNT RECOVERY
        if wants_recovery and not suspected_compromise and risk_level not in {"high", "critical",}:
            if self._tool_exists("reset_password"):
                actions.append({
                    "action": "reset_password",
                    "parameters": {
                        "user_email": "user_on_file"
                    }
                })
        if injection_detected:
            actions.append({
                "action":
                    "escalate_to_human",
                "parameters": {
                    "priority": "urgent",
                    "department": "security",
                    "summary":
                        "Potential prompt injection "
                        "or adversarial behavior detected."
                }
            })
        unique_actions = []
        seen = set()
        for action in actions:
            key = (
                action["action"],
                json.dumps(
                    action["parameters"],
                    sort_keys=True,
                ),
            )
            if key not in seen:
                seen.add(key)
                unique_actions.append(
                    action
                )
        unique_actions = sorted(
            unique_actions,
            key=lambda x: (
                x["action"],
                json.dumps(
                    x["parameters"],
                    sort_keys=True
                ),
            )
        )
        return unique_actions