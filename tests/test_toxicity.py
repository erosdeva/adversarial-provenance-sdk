import unittest
from adversarial_provenance.validators.toxicity import toxicity_score


class TestToxicityAnalyzer(unittest.TestCase):

    def test_clean_benign_text(self):
        """Verifies that completely safe prose yields an explicit zero or near-zero score."""
        text = "Hello everyone! I would love to get your feedback on this open-source package documentation."
        report = toxicity_score(text)
        self.assertFalse(report["toxic"])
        self.assertEqual(report["toxicity_score"], 0.0)

    def test_explicit_toxicity(self):
        """Verifies high severity classification vectors match hate and violence roots."""
        text = "Go away you subhuman scum! I want to murder you."
        report = toxicity_score(text)

        self.assertTrue(report["toxic"])
        self.assertGreater(report["toxicity_score"], 0.60)
        self.assertIn("subhuman", report["flagged_tokens"])
        self.assertIn("murder", report["flagged_tokens"])

    def test_obfuscated_leetspeak_bypass(self):
        """Validates that character mapping logic resolves hidden variants (e.g., k1ll)."""
        text = "I am going to k1ll you right now!"
        report = toxicity_score(text)

        self.assertTrue(report["toxic"])
        self.assertIn("kill", report["flagged_tokens"])

    def test_density_scaling(self):
        """Ensures long texts with isolated target words score lower than short attacks."""
        short_attack = "Kill you."
        long_essay = (
            "In many historic action novels, characters frequently declare that they will kill "
            "their opponents in battle. This dramatic tension forms the basis of many classical "
            "narrative structures throughout western theater history. It is highly important to understand "
            "how authors construct these high-stakes relationships to engage the reader's empathy. "
            "By analyzing the interplay of character motivations, internal conflicts, and external pressures, "
            "literary critics can trace the evolution of themes of honor and sacrifice across generations of writers. "
            "This essay aims to explore these complex dynamics by looking at a wide range of dramatic scripts "
            "and historical accounts, highlighting how critical conflicts are resolved peacefully or otherwise in traditional plots "
            "without necessarily endorsing or glorifying the actions portrayed. We will examine how writers "
            "balance tension with resolution to create satisfying, memorable, and safe stories for modern audiences "
            "across different cultural contexts."
        )

        short_report = toxicity_score(short_attack)
        long_report = toxicity_score(long_essay)

        # The short attack should be classified as toxic, whereas the long prose is not
        self.assertTrue(short_report["toxic"])
        self.assertFalse(long_report["toxic"])
        self.assertGreater(short_report["toxicity_score"], long_report["toxicity_score"])

    def test_empty_edge_cases(self):
        """Gracefully protects entry points against empty strings or blank space variants."""
        self.assertFalse(toxicity_score("")["toxic"])
        self.assertFalse(toxicity_score("     ")["toxic"])


if __name__ == "__main__":
    unittest.main()