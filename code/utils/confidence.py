def compute_confidence(
    retrieval_score,
    injection_detected,
    risk_level,
):

    confidence = retrieval_score

    if injection_detected:
        confidence -= 0.3

    if risk_level == "critical":
        confidence -= 0.2

    confidence = max(0.1, min(confidence, 0.99))

    return round(confidence, 2)