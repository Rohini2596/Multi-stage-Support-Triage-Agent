from __future__ import annotations
import re
from dataclasses import dataclass, asdict
from typing import List
PII_PATTERNS = {
    "email": re.compile(
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"
    ),
    "phone": re.compile(
        r"(?:(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4})"
    ),
    "ssn": re.compile(
        r"\b\d{3}-\d{2}-\d{4}\b"
    ),
    "card": re.compile(
        r"\b(?:\d[ -]*?){13,19}\b"
    ),
    "ip": re.compile(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ),
    "api_key": re.compile(
        r"(sk-[A-Za-z0-9]{20,})"
    ),
    "passport": re.compile(
        r"\b[A-Z]{1,2}[0-9]{6,8}\b"
    ),
    "address": re.compile(
        r"\d{1,5}\s+\w+\s+(street|st|road|rd|avenue|ave|lane|ln|drive|dr)\b",
        re.IGNORECASE
    ),
    "cvv": re.compile(
        r"\bcvv[:\s-]?\d{3,4}\b",
        re.IGNORECASE
    ),
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
            normalized = re.sub(
                r"\s+",
                " ",
                text or ""
            )
            if pattern.search(normalized):
                found.append(label)
        found = sorted(list(set(found)))
        return PIIResult(bool(found), found)