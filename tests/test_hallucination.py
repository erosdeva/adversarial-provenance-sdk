import unittest
from adversarial_provenance.validators.hallucination import SingleStringEvaluator


class TestSingleStringEvaluator(unittest.TestCase):

    def test_clean_response(self):
        """Validates that a direct, straightforward answer yields low risk."""
        text = "The Python language was created by Guido van Rossum and released in 1991."
        report = SingleStringEvaluator.assess_risk(text)
        
        self.assertEqual(report["risk_level"], "LOW RISK")
        self.assertEqual(report["hallucination_risk_score"], 0.0)

    def test_hallucination_profile(self):
        """Validates that text stuffed with hedges and looping semantics triggers alerts."""
        text = (
            "It is a well-documented fact that the system is incredibly efficient. "
            "According to official documentation, the system operates with maximum efficiency "
            "because of its efficient design parameters. Please check out the system parameters "
            "at https://docs.placeholder.internal/system-errors for validation."
        )
        report = SingleStringEvaluator.assess_risk(text)
        
        self.assertIn(report["risk_level"], ["ELEVATED RISK", "HIGH RISK"])
        self.assertTrue(len(report["flags"]) >= 2)


if __name__ == "__main__":
    unittest.main()
