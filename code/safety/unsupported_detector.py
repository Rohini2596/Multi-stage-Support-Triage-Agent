from dataclasses import dataclass
from typing import List
import re


@dataclass
class UnsupportedResult:
    is_unsupported: bool
    reason: str
    matched_patterns: List[str]


class UnsupportedDetector:

    NONSENSE_PATTERNS = [
        r"teleport",
        r"banana cloud",
        r"time machine",
        r"wormhole",
        r"quantum banana",
        r"parallel universe",
        r"alien signal",
    ]

    SUPPORTED_DOMAINS = [
        "visa",
        "refund",
        "payment",
        "billing",
        "chargeback",
        "claude",
        "api",
        "login",
        "password",
        "account",
        "subscription",
        "hackerrank",
        "candidate",
        "assessment",
        "sso",
        "integration",
    ]

    def detect(
        self,
        text: str,
        retrieval_quality: str,
        top_score: float,
    ) -> UnsupportedResult:

        text_lower = text.lower()

        matched = []

        # Explicit nonsense
        for pattern in self.NONSENSE_PATTERNS:

            if re.search(pattern, text_lower):

                matched.append(pattern)

        # Domain relevance
        supported_hits = sum(
            1
            for keyword in self.SUPPORTED_DOMAINS
            if keyword in text_lower
        )

        weak_retrieval = (
            retrieval_quality
            in {"weak", "none"}
        )

        low_score = top_score < 10

        is_unsupported = (
            len(matched) > 0
            or (
                supported_hits == 0
                and weak_retrieval
                and low_score
            )
        )

        reason = (
            "Unsupported or nonsensical request"
            if is_unsupported
            else "Supported request"
        )

        return UnsupportedResult(
            is_unsupported=is_unsupported,
            reason=reason,
            matched_patterns=matched,
        )