
def hallucination_score(output: str) -> float:
    output_lower = output.lower()

    suspicious_terms = [
        "possibly",
        "might",
        "could be",
        "uncertain",
        "not verified",
        "sources vary",
        "URL is",
        "well-documented fact",
        "generally understood",
        "commonly believed",
        "unverified claim",
    ]

    score = 0.0

    for term in suspicious_terms:
        if term in output_lower:
            score += 0.1

    if len(output.split()) < 10:
        score += 0.2

    return round(min(score, 1.0), 2)
