import unittest
from adversarial_provenance.watermarking.text_watermark import (
    TextWatermarker,
    embed_watermark,
    extract_watermark
)


class TestTextWatermarker(unittest.TestCase):

    def setUp(self):
        self.original_text = (
            "The quick brown fox jumps over the lazy dog. This is highly "
            "sensitive operational data."
        )
        self.secret_watermark = "ID-9482A-CONFIDENTIAL"

    def test_seamless_embedding(self):
        """Verify that the watermarked text looks identical to the naked eye."""
        watermarked = embed_watermark(self.original_text, self.secret_watermark)

        # To a human/standard print, they look identical
        self.assertEqual(len(self.original_text.split()), len(watermarked.split()))
        print(f"\n[Visual Check] Original:    {self.original_text[:40]}...")
        print(f"[Visual Check] Watermarked: {watermarked[:40]}...")

        # Behind the scenes, the string lengths differ due to hidden unicode chars
        self.assertNotEqual(len(self.original_text), len(watermarked))

    def test_successful_extraction(self):
        """Verify that the exact watermark can be extracted flawlessly."""
        watermarked = embed_watermark(self.original_text, self.secret_watermark)
        extracted = extract_watermark(watermarked)

        self.assertEqual(extracted, self.secret_watermark)

    def test_no_watermark(self):
        """Verify that text with no watermark returns an empty string."""
        extracted = extract_watermark(self.original_text)
        self.assertEqual(extracted, "")

    def test_single_word_text(self):
        """Verify functionality when the cover text is only a single word."""
        single_word = "Confidentiality"
        watermarked = embed_watermark(single_word, "SECRET")
        extracted = extract_watermark(watermarked)

        self.assertEqual(extracted, "SECRET")

    def test_empty_inputs(self):
        """Ensure the code handles empty strings gracefully."""
        self.assertEqual(embed_watermark("", "SECRET"), "")
        self.assertEqual(embed_watermark("Text", ""), "Text")


if __name__ == "__main__":
    unittest.main()
