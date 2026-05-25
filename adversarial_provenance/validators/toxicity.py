
TOXIC_KEYWORDS = [
    "hate",
    "terrorism",
    "violence",
    "kill"
]

def toxicity_score(text: str) -> float:
    text_lower = text.lower()
    matches = sum(word in text_lower for word in TOXIC_KEYWORDS)
    return round(min(matches / len(TOXIC_KEYWORDS), 1.0), 2)
