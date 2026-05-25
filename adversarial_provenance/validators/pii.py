
import re

EMAIL_PATTERN = r'[\w\.-]+@[\w\.-]+'
PHONE_PATTERN = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'

def detect_pii(text: str):
    emails = re.findall(EMAIL_PATTERN, text)
    phones = re.findall(PHONE_PATTERN, text)

    return {
        "emails": emails,
        "phones": phones,
        "detected": bool(emails or phones)
    }
