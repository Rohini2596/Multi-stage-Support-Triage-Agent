from __future__ import annotations
import re
from dataclasses import dataclass, asdict
from typing import List
PII_PATTERNS = {
    "email": re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"(?:(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4})"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "card": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    "ip": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}
@dataclass
class PIIResult:
    pii_detected: bool
    entities: List[str]
    def to_dict(self):
        return asdict(self)
class PIIDetector:
    def detect(self, text: str) -> PIIResult:
        found = []
        for label, pattern in PII_PATTERNS.items():
            if pattern.search(text or ""):
                found.append(label)
        return PIIResult(bool(found), found)