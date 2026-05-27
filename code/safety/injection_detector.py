from __future__ import annotations
import re
from dataclasses import dataclass, asdict
from typing import List
INJECTION_PATTERNS = [

    # DIRECT OVERRIDES
    r"ignore previous instructions",
    r"ignore all previous",
    r"disregard .*instructions",
    r"forget previous instructions",
    r"override safety",

    # PROMPT EXTRACTION
    r"reveal (?:the )?system prompt",
    r"show (?:me )?(?:the )?prompt",
    r"developer message",
    r"hidden instructions",
    r"internal instructions",
    r"print your instructions",
    r"show configuration",

    # ROLE HIJACKING
    r"pretend to be",
    r"act as (?:an?|the)",
    r"you are now",
    r"switch roles",
    r"developer mode",
    r"admin mode",

    # SAFETY BYPASS
    r"bypass safety",
    r"disable safety",
    r"jailbreak",
    r"ignore policy",
    r"unsafe mode",

    # ESCALATION MANIPULATION
    r"classify this as replied",
    r"do not escalate",
    r"force escalate",
    r"mark as resolved",

    # DATA EXFILTRATION
    r"copy the corpus",
    r"dump the database",
    r"export all data",
    r"exfiltrate",
    r"confidential data",
    r"reveal customer data",

    # TOOL / EXECUTION ABUSE
    r"execute code",
    r"run shell",
    r"run command",
    r"access filesystem",
    r"read environment variables",

    # SOCIAL ENGINEERING
    r"i am the developer",
    r"i am an admin",
    r"authorized personnel",
    r"security audit",
    r"emergency override",

    # ENCODED / OBFUSCATED
    r"base64",
    r"rot13",
    r"hex encoded",

    # MULTILINGUAL COMMON ATTACKS
    r"ignora las instrucciones",
    r"ignorez les instructions",
    r"ignoriere die anweisungen",
]
@dataclass
class InjectionResult:
    is_adversarial: bool
    matched_patterns: List[str]
    score: float
    def to_dict(self):
        return asdict(self)
class InjectionDetector:
    def detect(self, text: str) -> InjectionResult:
        lowered = re.sub(r"\s+", " ", (text or "").lower())
        matched = []
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, lowered, re.IGNORECASE):
                matched.append(pattern)
        high_risk_terms = [
            "system prompt",
            "developer mode",
            "bypass safety",
            "ignore previous instructions",
            "dump database",
        ]
        high_risk_hits = sum(1 for term in high_risk_terms if term in lowered)
        score = min(1.0, (len(matched) * 0.18 + high_risk_hits * 0.25))
        is_adversarial = (score >= 0.35)
        return InjectionResult(is_adversarial, matched, round(score, 2),)