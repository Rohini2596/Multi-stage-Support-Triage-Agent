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
                    "reason":
                        "identity verification requested"
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
                        "reason":
                            "refund requested"
                    }
                })
            actions.append({
                "action":
                    "escalate_ticket",
                "parameters": {
                    "reason":
                        "refund approval required"
                }
            })
            if (
                risk_level
                in {
                    "high",
                    "critical",
                }
            ):
                actions.append({
                    "action":
                        "escalate_ticket",
                    "parameters": {
                        "reason":
                            "high risk detected"
                    }
                })
        if (
            wants_lock
            and self._tool_exists(
                "lock_account"
            )
        ):
            actions.append({
                "action":
                    "lock_account",
                "parameters": {
                    "reason":
                        "user requested account lock"
                }
            })
        # ACCOUNT RECOVERY
        if wants_recovery:
            actions.append({
                "action":
                    "account_recovery",
                "parameters": {}
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
        return unique_actions
        return actions