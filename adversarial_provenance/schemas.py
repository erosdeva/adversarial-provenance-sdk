
from pydantic import BaseModel
from typing import Dict, Any

class APSResponse(BaseModel):
    output: str
    trust_score: float
    hallucination_score: float
    risk_score: float
    provenance_hash: str
    metadata: Dict[str, Any]
