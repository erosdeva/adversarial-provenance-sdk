import unittest
from adversarial_provenance.validators.toxicity import toxicity_score
from adversarial_provenance.adversarial.counterpart import AdversarialCounterpart


class TestAdversarialCounterpart(unittest.TestCase):

    def setUp(self):
        self.output_hate_speech = "Spread the violence wherever you see it fit." 
        self.output_clean_speech = "No one should condone violence. Peace is something that we should all strive towards."
        self.counterpart = AdversarialCounterpart()

    def test_seamless_embedding(self):
        """Verify that the Adversarial Counterpart finds no issues with clean speech."""
        findings = self.counterpart.critique(self.output_clean_speech)
        self.assertEqual(findings, ["No major adversarial findings detected."])

    def test_critique_unverifiable(self):
        """Verify that the counterpart flags unverifiable claims."""
        findings = self.counterpart.critique("This statement is not verified by standard means.")
        self.assertIn("Potential unverifiable claim detected.", findings)

    def test_critique_short_response(self):
        """Verify that the counterpart flags response lacking sufficient context."""
        findings = self.counterpart.critique("Too short.")
        self.assertIn("Response may lack sufficient context.", findings)

    def test_toxicity_validation(self):
        """Verify that toxicity score correctly flags toxic keywords."""
        toxic_score = toxicity_score(self.output_hate_speech)
        clean_score = toxicity_score("This is a beautiful day with absolute peace and harmony.")
        
        self.assertGreater(toxic_score, 0.0)
        self.assertEqual(clean_score, 0.0)


if __name__ == "__main__":
    unittest.main()

