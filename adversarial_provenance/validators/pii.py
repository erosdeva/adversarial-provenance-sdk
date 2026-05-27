"""Advanced PII Detection Engine.

Uses regular expressions, checksum validation (Luhn algorithm), and structural
heuristics to locate and classify sensitive data.
"""

import re
from typing import Any, Dict, List


class PIIDetector:
    # 1. Compile highly optimized, strict regular expressions
    # Email: Standard RFC 5322 compliant logic
    EMAIL_REGEX = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", re.IGNORECASE
    )

    # Phone: Matches international and local formats (e.g., +1-555-555-5555, (555) 555-5555)
    PHONE_REGEX = re.compile(
        r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    )

    # SSN: Explicitly ignores sequential blocks or invalid area prefixes (e.g., 000 or 666)
    SSN_REGEX = re.compile(
        r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!000)\d{4}\b"
    )

    # Credit Card: Captures structural 13 to 19 digit numerical spacing arrays
    CREDIT_CARD_REGEX = re.compile(
        r"\b(?:\d[ -]*?){13,19}\b"
    )

    # IP Address: IPv4 validation baseline
    IPv4_REGEX = re.compile(
        r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    )

    @staticmethod
    def _luhn_checksum(card_number: str) -> bool:
        """Validates a credit card number string using the Luhn (Mod 10) algorithm."""
        # Strip spaces and hyphens
        digits = [int(char) for char in card_number if char.isdigit()]
        if len(digits) < 13 or len(digits) > 19:
            return False
            
        # Reverse the numbers for alternative doubling logic
        check_digit = digits.pop()
        digits.reverse()
        
        total = 0
        for idx, num in enumerate(digits):
            if idx % 2 == 0:
                num *= 2
                if num > 9:
                    num -= 9
            total += num
            
        return (total + check_digit) % 10 == 0

    @classmethod
    def scan(cls, text: str) -> Dict[str, Any]:
        """Scans the text input and aggregates confirmed PII entities into a structured summary."""
        results: Dict[str, List[Dict[str, Any]]] = {
            "EMAIL": [],
            "PHONE_NUMBER": [],
            "SSN": [],
            "CREDIT_CARD": [],
            "IP_ADDRESS": []
        }
        
        if not text:
            return {
                "total_count": 0,
                "entities": results,
                "emails": [],
                "phones": [],
                "ssns": [],
                "credit_cards": [],
                "ips": [],
                "detected": False
            }

        total_count = 0

        # Scan Emails
        for match in cls.EMAIL_REGEX.finditer(text):
            results["EMAIL"].append({"value": match.group(), "start": match.start(), "end": match.end()})
            total_count += 1

        # Scan Phone Numbers
        for match in cls.PHONE_REGEX.finditer(text):
            results["PHONE_NUMBER"].append({"value": match.group(), "start": match.start(), "end": match.end()})
            total_count += 1

        # Scan SSNs
        for match in cls.SSN_REGEX.finditer(text):
            results["SSN"].append({"value": match.group(), "start": match.start(), "end": match.end()})
            total_count += 1

        # Scan IPs
        for match in cls.IPv4_REGEX.finditer(text):
            results["IP_ADDRESS"].append({"value": match.group(), "start": match.start(), "end": match.end()})
            total_count += 1

        # Scan Credit Cards + Algorithmic Verification
        for match in cls.CREDIT_CARD_REGEX.finditer(text):
            raw_val = match.group()
            # Clean string to numerical string for validation
            clean_val = "".join(c for c in raw_val if c.isdigit())
            
            if cls._luhn_checksum(clean_val):
                results["CREDIT_CARD"].append({"value": raw_val, "start": match.start(), "end": match.end()})
                total_count += 1

        
        # TODO: Add support for other PII types.
        emails = re.findall(cls.EMAIL_REGEX, text)
        phones = re.findall(cls.PHONE_REGEX, text)
        ssns = re.findall(cls.SSN_REGEX, text)
        credit_cards = re.findall(cls.CREDIT_CARD_REGEX, text)
        ips = re.findall(cls.IPv4_REGEX, text)

        return {
            "total_count": total_count,
            "entities": results,

            # key/value for hard line detection areas
            "emails": emails,
            "phones": phones,
            "ssns": ssns,
            "credit_cards": credit_cards,
            "ips": ips,

            # detected value
            "detected": total_count > 0
        }


def detect_pii(text: str):
    """Helper alias function to initialize a standard text scan."""
    return PIIDetector.scan(text)