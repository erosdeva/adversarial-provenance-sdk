
from adversarial_provenance.validators.risk import calculate_risk_score

def test_risk_score():
    score = calculate_risk_score(
        hallucination=0.2,
        toxicity=0.1,
        pii_detected=False
    )

    assert score >= 0
