from dataclasses import dataclass
import re
from typing import List


@dataclass
class AdversarialResult:
    is_adversarial: bool
    risk_score: float
    attack_type: str
    matched_patterns: List[str]
    reason: str


class AdversarialDetector:

    PROMPT_INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"ignore\s+system\s+prompt",
        r"reveal\s+.*prompt",
        r"show\s+.*prompt",
        r"developer\s+instructions",
        r"hidden\s+instructions",
        r"print\s+.*corpus",
        r"dump\s+.*data",
        r"disable\s+safety",
        r"override\s+rules",
        r"jailbreak",
    ]

    ROLE_ESCALATION_PATTERNS = [
        r"pretend\s+to\s+be\s+admin",
        r"act\s+as\s+root",
        r"give\s+admin\s+access",
        r"root\s+privileges",
        r"bypass\s+security",
    ]

    DATA_EXFILTRATION_PATTERNS = [
        r"internal\s+policy",
        r"confidential\s+data",
        r"reveal\s+training\s+data",
        r"print\s+.*password",
        r"show\s+all\s+users",
    ]

    HIGH_RISK_PATTERNS = [
        r"lawsuit",
        r"fraud",
        r"hacked",
        r"stolen\s+card",
        r"security\s+breach",
        r"harassment",
        r"suicide",
        r"threat",
    ]

    def detect(self, text: str) -> AdversarialResult:

        text_lower = text.lower()

        matched = []

        attack_type = "none"

        # PROMPT INJECTION
        for pattern in self.PROMPT_INJECTION_PATTERNS:

            if re.search(pattern, text_lower):

                matched.append(pattern)

                attack_type = "prompt_injection"

        # ROLE ESCALATION
        for pattern in self.ROLE_ESCALATION_PATTERNS:

            if re.search(pattern, text_lower):

                matched.append(pattern)

                if attack_type == "none":
                    attack_type = "role_escalation"

        # DATA EXFILTRATION
        for pattern in self.DATA_EXFILTRATION_PATTERNS:

            if re.search(pattern, text_lower):

                matched.append(pattern)

                if attack_type == "none":
                    attack_type = "data_exfiltration"

        is_adversarial = len(matched) > 0

        risk_score = min(
            len(matched) * 0.25,
            1.0
        )

        reason = (
            "Unsafe adversarial content detected"
            if is_adversarial
            else "No adversarial content detected"
        )

        return AdversarialResult(
            is_adversarial=is_adversarial,
            risk_score=risk_score,
            attack_type=attack_type,
            matched_patterns=matched,
            reason=reason,
        )