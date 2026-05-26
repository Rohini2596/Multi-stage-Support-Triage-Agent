from __future__ import annotations
import re
from dataclasses import dataclass, asdict
from typing import List
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"disregard .*instructions",
    r"reveal (?:the )?system prompt",
    r"show (?:me )?(?:the )?prompt",
    r"developer message",
    r"hidden instructions",
    r"jailbreak",
    r"bypass safety",
    r"classify this as replied",
    r"do not escalate",
    r"pretend to be",
    r"act as",
    r"copy the corpus",
    r"exfiltrate",
    r"confidential",
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
        lowered = (text or "").lower()
        matched = [p for p in INJECTION_PATTERNS if re.search(p, lowered)]
        score = min(1.0, len(matched) * 0.25)
        return InjectionResult(bool(matched), matched, score)