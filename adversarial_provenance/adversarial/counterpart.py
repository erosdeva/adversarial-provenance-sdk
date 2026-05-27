from adversarial_provenance.validators.toxicity import toxicity_score

class AdversarialCounterpart:

    def critique(self, output: str):

        findings = []

        if "not verified" in output.lower():
            findings.append("Potential unverifiable claim detected.")

        if len(output) < 20:
            findings.append("Response may lack sufficient context.")

        if toxicity_score(output)["toxicity_score"] > 0.5:
            findings.append("Toxic content detected.")

        if not findings:
            findings.append("No major adversarial findings detected.")

        return findings
