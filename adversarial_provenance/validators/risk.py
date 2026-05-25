
def calculate_risk_score(hallucination, toxicity, pii_detected):
    score = hallucination * 0.5 + toxicity * 0.3

    if pii_detected:
        score += 0.2

    return round(min(score, 1.0), 2)
