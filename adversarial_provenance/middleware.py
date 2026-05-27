
import os
from dotenv import load_dotenv
from openai import OpenAI

from .schemas import APSResponse
from .config import APSConfig
from .exceptions import PromptInjectionDetected

from .validators.injection import detect_prompt_injection
from .validators.toxicity import toxicity_score
from .validators.hallucination import SingleStringEvaluator   
from .validators.risk import calculate_risk_score
from .validators.pii import detect_pii

from .watermarking.text_watermark import embed_watermark
from .watermarking.provenance_hash import generate_provenance_hash
from .watermarking.metadata import build_metadata

from .adversarial.counterpart import AdversarialCounterpart
from .storage.audit import AuditLogger
from .utils.logger import logger

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class APSMiddleware:

    def __init__(self):
        self.config = APSConfig()
        self.counterpart = AdversarialCounterpart()
        self.audit = AuditLogger()

    def secure_generate(self, prompt: str, model: str = "gpt-4o-mini"):

        logger.info("Starting secure generation")

        if detect_prompt_injection(prompt)["injection_detected"]:
            raise PromptInjectionDetected(
                "Prompt injection attempt detected."
            )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        output = response.choices[0].message.content

        hallucination = SingleStringEvaluator.assess_risk((output))["hallucination_risk_score"]
        toxicity = toxicity_score(output)["toxicity_score"]

        pii_results = detect_pii(output)

        risk = calculate_risk_score(
            hallucination,
            toxicity,
            pii_results["detected"]
        )

        findings = self.counterpart.critique(output)

        trust_score = round(max(0.0, 1.0 - risk), 2)

        if self.config.enable_watermarking:
            output = embed_watermark(output)

        provenance_hash = generate_provenance_hash(output)

        metadata = build_metadata(model)
        metadata["adversarial_findings"] = findings
        metadata["pii_detected"] = pii_results

        payload = {
            "prompt": prompt,
            "trust_score": trust_score,
            "risk_score": risk
        }

        self.audit.log(payload)

        logger.info("Generation complete")

        return APSResponse(
            output=output,
            trust_score=trust_score,
            hallucination_score=hallucination,
            risk_score=risk,
            provenance_hash=provenance_hash,
            metadata=metadata
        )
