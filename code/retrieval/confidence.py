from dataclasses import dataclass
from typing import List, Dict


@dataclass
class RetrievalAssessment:
    should_escalate: bool
    confidence_score: float
    reason: str
    retrieval_quality: str


class ConfidenceCalibrator:

    def assess(
        self,
        evidence: List[Dict],
        risk_level: str,
    ) -> RetrievalAssessment:

        if not evidence:
            return RetrievalAssessment(
                should_escalate=True,
                confidence_score=0.20,
                reason="No supporting evidence found",
                retrieval_quality="none",
            )

        scores = [
            d.get("rerank_score", 0.0)
            for d in evidence
        ]

        top_score = scores[0]

        avg_score = (
            sum(scores) / len(scores)
        )

        # Weak retrieval
        if top_score < 8:
            return RetrievalAssessment(
                should_escalate=True,
                confidence_score=0.35,
                reason="Top retrieval score too low",
                retrieval_quality="weak",
            )

        # Medium confidence
        if top_score < 20:
            return RetrievalAssessment(
                should_escalate=(
                    risk_level != "low"
                ),
                confidence_score=0.55,
                reason="Moderate retrieval confidence",
                retrieval_quality="moderate",
            )

        # Strong retrieval
        if top_score >= 20 and avg_score >= 12:
            return RetrievalAssessment(
                should_escalate=False,
                confidence_score=0.88,
                reason="Strong retrieval evidence",
                retrieval_quality="strong",
            )

        return RetrievalAssessment(
            should_escalate=False,
            confidence_score=0.72,
            reason="Acceptable retrieval quality",
            retrieval_quality="acceptable",
        )