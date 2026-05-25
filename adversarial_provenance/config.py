
from pydantic import BaseModel

class APSConfig(BaseModel):
    enable_watermarking: bool = True
    enable_adversarial_validation: bool = True
    enable_pii_detection: bool = True
    trust_threshold: float = 0.70
