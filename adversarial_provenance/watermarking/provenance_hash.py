
import hashlib
import time

def generate_provenance_hash(content: str) -> str:
    payload = f"{content}:{time.time()}"
    return hashlib.sha256(payload.encode()).hexdigest()
