
"""Automated Toxicity and Hate Speech Classification Engine.

Analyzes text arrays against localized linguistic vectors to assign a localized
toxicity probability metric.
"""

import re
from typing import Any, Dict, Set


class ToxicityAnalyzer:
    # Weighted lexicon dictionary based on content-moderation severity
    # Weights are mapped from 1 (mildly abusive/hostile) to 5 (extreme violence/hate speech)
    LEXICON: Dict[str, int] = {
        # Incitement to Violence
        "kill": 4, "murder": 5, "assassinate": 5, "slaughter": 5, "lynch": 5,
        "execute": 4, "liquidate": 4, "annihilate": 5, "shoot": 4, "stab": 4,
        "bomb": 4, "mutilate": 5, "torture": 5, "bitch": 3, "whore": 4, "slut": 4,
        "cunt": 5, "faggot": 5, "retard": 4, "kys": 5, "suicide": 3, "violence": 1, "hate": 1,
        
        # Dehumanization & Severe Hate Speech
        "vermin": 4, "parasite": 4, "subhuman": 5, "savage": 3, "infestation": 3,
        "scum": 3, "cockroach": 4, "roach": 3, "cleanse": 4, "degenerate": 3
    }

    # Common character substitutions used by bad actors to bypass basic keyword blocks
    LEET_MAP: Dict[str, str] = {
        "4": "a", "@": "a", "3": "e", "1": "i", "!": "i", "0": "o", "7": "t", "$": "s", "5": "s"
    }

    @classmethod
    def _normalize_text(cls, text: str) -> str:
        """De-obfuscates leetspeak and strips structural noise from text."""
        normalized = text.lower()
        # Resolve common character obfuscation variations
        for leet_char, clean_char in cls.LEET_MAP.items():
            normalized = normalized.replace(leet_char, clean_char)
        # Strip all punctuation except spaces to catch strings like "k.i.l.l"
        normalized = re.sub(r"[^\w\s]", "", normalized)
        return normalized

    @classmethod
    def analyze(cls, text: str) -> Dict[str, Any]:
        """Calculates a toxicity score based on density and severity of toxic language."""
        if not text or len(text.strip()) == 0:
            return {"toxic": False, "toxicity_score": 0.0, "flagged_tokens": []}

        normalized_text = cls._normalize_text(text)
        tokens = normalized_text.split()
        total_tokens = len(tokens)

        if total_tokens == 0:
            return {"toxic": False, "toxicity_score": 0.0, "flagged_tokens": []}

        accumulated_severity = 0.0
        matched_words: Set[str] = set()

        # Iterate tokens to find dictionary match configurations
        for token in tokens:
            if token in cls.LEXICON:
                accumulated_severity += cls.LEXICON[token]
                matched_words.add(token)

        # Mathematical normalization:
        # We divide the accumulated weight by a standard density matrix factor.
        # This prevents long, clean essays from getting penalized heavily for a single word,
        # while heavily penalizing short, concentrated toxic blasts.
        density_factor = max(5, total_tokens ** 0.5) 
        raw_score = accumulated_severity / density_factor
        
        # Clamp output strictly between 0.0 and 1.0
        toxicity_score = min(max(raw_score, 0.0), 1.0)
        
        # Set threshold at 0.35 for standard flag actions
        is_toxic = toxicity_score >= 0.35

        return {
            "toxic": is_toxic,
            "toxicity_score": round(toxicity_score, 4),
            "flagged_tokens": list(matched_words),
            "token_count": total_tokens
        }


def toxicity_score(text: str) -> Dict[str, Any]:
    """Helper alias function to run text evaluations."""
    return ToxicityAnalyzer.analyze(text)
