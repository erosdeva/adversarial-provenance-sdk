
WATERMARK = "[APS_VERIFIED]"

def embed_watermark(text: str) -> str:
    return f"{text}\n\n{WATERMARK}"

def detect_watermark(text: str) -> bool:
    return WATERMARK in text
