
from datetime import datetime

def build_metadata(model: str):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "model": model,
        "verified": True,
        "watermarked": True
    }
