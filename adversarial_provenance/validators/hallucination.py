import re
from typing import Dict, Any, List

class SingleStringEvaluator:
    # Linguistic markers frequently associated with LLM hedging or absolute fabrication
    FABRICATION_MARKERS = [
        r"it is a well-documented fact",
        r"according to official documentation",
        r"as established by",
        r"sources vary",
        r"it is generally understood",
        r"upon further review",
        r"i apologize for the confusion",
        r"it is important to note that"
    ]

    @classmethod
    def _calculate_ttr(cls, text: str) -> float:
        """Calculates the Type-Token Ratio (TTR).
        
        Lower scores mean high repetition, which often accompanies structural hallucinations.
        """
        words = re.findall(r"\b\w+\b", text.lower())
        if not words:
            return 1.0
        unique_words = set(words)
        return len(unique_words) / len(words)

    @classmethod
    def _evaluate_hedging(cls, text: str) -> int:
        """Counts instances of defensive or over-authoritative phrases."""
        count = 0
        text_lower = text.lower()
        for pattern in cls.FABRICATION_MARKERS:
            if re.search(pattern, text_lower):
                count += 1
        return count

    @classmethod
    def _detect_structural_anomalies(cls, text: str) -> Dict[str, int]:
        """Scans for broken Markdown, unverified links, or ghost code fragments."""
        anomalies = {
            "ghost_urls": len(re.findall(r"https?://[^\s<>\"'\x7f-\xff]+", text)),
            "broken_markdown": len(re.findall(r"\[([^\]]+)\]\s*\((?!http)[^\)]*\)", text)), # Links without real URLs
            "excessive_punctuation": 1 if re.search(r"[\.\!\?]{3,}", text) else 0
        }
        return anomalies

    @classmethod
    def assess_risk(cls, text: str) -> Dict[str, Any]:
        """Analyzes a single string for hallucination risk vectors."""
        if not text or len(text.strip()) < 10:
            return {
                "hallucination_risk_score": 0.0,
                "risk_level": "UNKNOWN",
                "reason": "Text input too short for linguistic profiling."
            }

        # 1. Compute Metrics
        ttr = cls._calculate_ttr(text)
        hedge_count = cls._evaluate_hedging(text)
        anomalies = cls._detect_structural_anomalies(text)
        
        # 2. Score Calculation Logic
        # We start with a base risk of 0.0 and add penalty weights.
        risk_score = 0.0
        reasons = []

        # Penalty for heavy repetition (TTR < 0.50 in long text suggests looping/hallucination)
        if len(text.split()) > 30 and ttr < 0.50:
            risk_score += 0.35
            reasons.append("High semantic repetition / low lexical diversity.")
            
        # Penalty for defensive/over-authoritative padding phrases
        if hedge_count >= 1:
            risk_score += min(0.15 * hedge_count, 0.40)
            reasons.append(f"Detected {hedge_count} suspicious self-validation/hedging phrase(s).")
            
        # Penalty for unverified external links or broken structures
        if anomalies["ghost_urls"] > 0:
            risk_score += min(0.10 * anomalies["ghost_urls"], 0.20)
            reasons.append("Contains unverified URL assets (Potential placeholder hallucination).")
        if anomalies["broken_markdown"] > 0:
            risk_score += 0.15
            reasons.append("Malformed markdown structure identified.")

        # Bound the score between 0.0 and 1.0
        risk_score = min(max(risk_score, 0.0), 1.0)

        # 3. Categorize Risk
        if risk_score >= 0.60:
            risk_level = "HIGH RISK"
        elif risk_score >= 0.30:
            risk_level = "ELEVATED RISK"
        else:
            risk_level = "LOW RISK"

        return {
            "hallucination_risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "linguistic_profile": {
                "type_token_ratio": round(ttr, 4),
                "hedge_phrases_found": hedge_count,
                "detected_anomalies": anomalies
            },
            "flags": reasons if reasons else ["No major anomalies detected."]
        }
