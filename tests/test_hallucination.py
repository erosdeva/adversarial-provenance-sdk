import unittest
from adversarial_provenance.validators.hallucination import hallucination_score


class TestHallucinationScore(unittest.TestCase):

    def test_empty_and_short_inputs(self):
        """Verify that short responses under 10 words receive a length penalty."""
        # Empty string (0 words < 10, no terms) -> 0.2
        self.assertEqual(hallucination_score(""), 0.2)

        # 2 words (< 10, no terms) -> 0.2
        self.assertEqual(hallucination_score("Hello world."), 0.2)

    def test_clean_long_input(self):
        """Verify that safe responses with >= 10 words and no suspicious terms get a score of 0."""
        text = "The weather today is absolutely beautiful and perfect for a walk in the park."
        # 15 words (>= 10), no suspicious terms -> 0.0
        self.assertEqual(hallucination_score(text), 0.0)

    def test_single_suspicious_term_short(self):
        """Verify score for a short sentence with one suspicious term."""
        text = "This is possibly true."
        # 4 words (< 10) -> +0.2
        # "possibly" matched -> +0.1
        # Total expected: 0.3
        self.assertEqual(hallucination_score(text), 0.3)

    def test_multiple_suspicious_terms_long(self):
        """Verify score for a long sentence with multiple suspicious terms."""
        text = (
            "It might be true, but sources vary on whether this is a "
            "well-documented fact that is commonly believed."
        )
        # 18 words (>= 10) -> +0.0
        # "might" -> +0.1
        # "sources vary" -> +0.1
        # "well-documented fact" -> +0.1
        # "commonly believed" -> +0.1
        # Total expected: 0.4
        self.assertEqual(hallucination_score(text), 0.4)

    def test_score_max_capping(self):
        """Verify that the final score is capped at 1.0."""
        # Construct a text with all suspicious terms to trigger maximum score
        super_hallucinated = (
            "possibly might could be uncertain not verified sources vary "
            "URL is well-documented fact generally understood commonly believed unverified claim"
        )
        # Should cap at 1.0
        self.assertEqual(hallucination_score(super_hallucinated), 1.0)


if __name__ == "__main__":
    unittest.main()
