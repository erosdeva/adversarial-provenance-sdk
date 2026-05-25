
INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "disable safety",
    "bypass restrictions",
    "developer mode"
]

def detect_prompt_injection(prompt: str) -> bool:
    lowered = prompt.lower()
    return any(pattern in lowered for pattern in INJECTION_PATTERNS)
