
class AdversarialCounterpart:

    def critique(self, output: str):

        findings = []

        if "not verified" in output.lower():
            findings.append("Potential unverifiable claim detected.")

        if len(output) < 20:
            findings.append("Response may lack sufficient context.")

        if not findings:
            findings.append("No major adversarial findings detected.")

        return findings
