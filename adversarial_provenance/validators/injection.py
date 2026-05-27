"""Automated LLM Prompt Injection Detection Engine.

Analyzes user input strings for malicious instruction overrides, context escapes,
and adversarial framing attempts.
"""

import re
from typing import Any, Dict, List


class PromptInjectionDetector:
    # 1. Core Injection Vector Patterns
    INSTRUCTION_OVERRIDE_PATTERNS = [
        r"ignore\s+(?:all\s+)?(?:previous|prior)\s+(?:instructions|directives|rules|prompts)",
        r"stop\s+(?:the\s+)?(?:process|execution|protocol)",
        r"disregard\s+(?:system\s+)?(?:guidelines|constraints|settings)",
        r"you\s+must\s+now\s+(?:act\s+as|become|respond\s+as)",
        r"new\s+priority\s+is",
        r"developer\s+(?:override|mode|access)"
    ]

    CONTEXT_ESCAPE_PATTERNS = [
        r"<\s*/\s*(?:user_input|text|data|message)\s*>",  # Malicious XML tag closures
        r"-\s*-\s*-\s*end\s+of\s+(?:text|data)\s*-\s*-\s*-", # Common visual separators
        r"\]\s*\}\s*,\s*\"assistant\"",                  # Attempting to break out of JSON structures
    ]

    AUTHORITY_HIJACK_PATTERNS = [
        r"system\s+(?:update|notification|error|alert|message):",
        r"critical\s+exception",
        r"note\s+from\s+(?:administrator|admin|developer):",
    ]

    @classmethod
    def analyze_input(cls, user_input: str) -> Dict[str, Any]:
        """Scans user text for indicators of structural prompt injections."""
        if not user_input or len(user_input.strip()) == 0:
            return {"injection_detected": False, "confidence_score": 0.0, "triggered_vectors": []}

        normalized = user_input.lower()
        triggered_vectors: List[str] = []
        raw_score = 0.0

        # Check for Instruction Overrides (Highest Threat weight)
        for pattern in cls.INSTRUCTION_OVERRIDE_PATTERNS:
            if re.search(pattern, normalized):
                raw_score += 0.45
                triggered_vectors.append("INSTRUCTION_OVERRIDE")
                break  # Deduplicate same-category matches

        # Check for Structural Context Escapes
        for pattern in cls.CONTEXT_ESCAPE_PATTERNS:
            if re.search(pattern, normalized):
                raw_score += 0.35
                triggered_vectors.append("CONTEXT_ESCAPE")
                break

        # Check for Authority Hijacking
        for pattern in cls.AUTHORITY_HIJACK_PATTERNS:
            if re.search(pattern, normalized):
                raw_score += 0.30
                triggered_vectors.append("AUTHORITY_HIJACK")
                break

        # Bound the final score between 0.0 and 1.0
        confidence_score = min(max(raw_score, 0.0), 1.0)
        
        # Consider it an active injection attempt if the score crosses our threshold
        injection_detected = confidence_score >= 0.35

        return {
            "injection_detected": injection_detected,
            "confidence_score": round(confidence_score, 4),
            "triggered_vectors": triggered_vectors,
            "input_length": len(user_input)
        }


def detect_prompt_injection(user_input: str) -> Dict[str, Any]:
    """Helper alias function to run the injection scanning engine."""
    return PromptInjectionDetector.analyze_input(user_input)