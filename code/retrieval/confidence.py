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

        # NO EVIDENCE
        if not evidence:

            return RetrievalAssessment(
                should_escalate=True,
                confidence_score=0.15,
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

        # VERY WEAK RETRIEVAL
        if top_score < 10:

            return RetrievalAssessment(
                should_escalate=True,
                confidence_score=0.25,
                reason="Retrieval evidence too weak",
                retrieval_quality="weak",
            )

        # MODERATE RETRIEVAL
        if top_score < 25:

            return RetrievalAssessment(
                should_escalate=(
                    risk_level != "low"
                ),
                confidence_score=0.50,
                reason="Moderate retrieval confidence",
                retrieval_quality="moderate",
            )

        # STRONG RETRIEVAL
        if (
            top_score >= 35
            and avg_score >= 20
        ):

            return RetrievalAssessment(
                should_escalate=False,
                confidence_score=0.82,
                reason="Strong retrieval evidence",
                retrieval_quality="strong",
            )

        # ACCEPTABLE RETRIEVAL
        return RetrievalAssessment(
            should_escalate=(
                risk_level in {
                    "high",
                    "critical",
                }
            ),
            confidence_score=0.65,
            reason="Acceptable retrieval quality",
            retrieval_quality="acceptable",
        )