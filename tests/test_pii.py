import unittest
from adversarial_provenance.validators.pii import PIIDetector, detect_pii


class TestPIIDetector(unittest.TestCase):

    def test_empty_and_null_inputs(self):
        """Verify that empty inputs are handled gracefully and return no PII."""
        empty_scan = detect_pii("")
        self.assertEqual(empty_scan["total_count"], 0)
        self.assertFalse(empty_scan["detected"])

    def test_email_detection(self):
        """Verify RFC 5322 compliant and case-insensitive email detection."""
        text = "Contact me at alice.smith+testing@example.com or SUPPORT@DOMAIN.CO."
        result = detect_pii(text)
        
        self.assertTrue(result["detected"])
        self.assertEqual(result["total_count"], 2)
        self.assertIn("alice.smith+testing@example.com", result["emails"])
        self.assertIn("SUPPORT@DOMAIN.CO", result["emails"])
        
        # Verify invalid email structures are not flagged
        invalid_text = "invalid_email@com or @domain.com or user@.com"
        invalid_result = detect_pii(invalid_text)
        self.assertFalse(invalid_result["detected"])
        self.assertEqual(len(invalid_result["emails"]), 0)

    def test_phone_number_detection(self):
        """Verify detection of various local and international phone number formats."""
        text = "Call me at +1-555-666-7777 or (123) 456-7890 or 987-654-3210."
        result = detect_pii(text)
        
        self.assertTrue(result["detected"])
        self.assertEqual(result["total_count"], 3)
        self.assertIn("+1-555-666-7777", result["phones"])
        self.assertIn("(123) 456-7890", result["phones"])
        self.assertIn("987-654-3210", result["phones"])

    def test_ssn_detection(self):
        """Verify strict SSN validation including ignoring invalid ranges/sequences."""
        valid_ssn = "123-45-6789"
        result_valid = detect_pii(f"My SSN is {valid_ssn}")
        self.assertTrue(result_valid["detected"])
        self.assertIn(valid_ssn, result_valid["ssns"])

        # Invalid SSN prefixes
        invalid_ssns = [
            "000-45-6789",  # Invalid area prefix (000)
            "666-45-6789",  # Invalid area prefix (666)
            "900-45-6789",  # Invalid area prefix (9xx)
            "123-00-6789",  # Invalid group number (00)
            "123-45-0000",  # Invalid serial number (0000)
        ]
        for ssn in invalid_ssns:
            result = detect_pii(f"Test SSN: {ssn}")
            self.assertFalse(result["detected"], f"SSN {ssn} should have been filtered out.")

    def test_ipv4_detection(self):
        """Verify IPv4 address regex validation."""
        valid_ips = "Connection from 192.168.1.1 and 255.255.255.255 and 0.0.0.0."
        result = detect_pii(valid_ips)
        self.assertTrue(result["detected"])
        self.assertEqual(result["total_count"], 3)
        self.assertIn("192.168.1.1", result["ips"])
        self.assertIn("255.255.255.255", result["ips"])
        
        # Verify out-of-range IP is not matched
        invalid_ip = "256.100.100.1"
        result_invalid = detect_pii(f"IP: {invalid_ip}")
        self.assertFalse(result_invalid["detected"])

    def test_credit_card_luhn_validation(self):
        """Verify credit card capture and Luhn checksum validation."""
        valid_card = "4111-1111-1111-1111"
        invalid_card = "4111-1111-1111-1112"
        
        # Valid Luhn card
        result_valid = detect_pii(f"Charge it to {valid_card}")
        self.assertTrue(result_valid["detected"])
        self.assertEqual(result_valid["entities"]["CREDIT_CARD"][0]["value"], valid_card)
        
        # Invalid Luhn card
        result_invalid = detect_pii(f"Charge it to {invalid_card}")
        self.assertFalse(result_invalid["detected"])

    def test_entity_metadata(self):
        """Verify precise entity metadata including start and end positions."""
        text = "Email: a@b.co"
        result = detect_pii(text)
        
        self.assertTrue(result["detected"])
        self.assertEqual(result["total_count"], 1)
        
        email_entity = result["entities"]["EMAIL"][0]
        self.assertEqual(email_entity["value"], "a@b.co")
        self.assertEqual(email_entity["start"], 7)
        self.assertEqual(email_entity["end"], 13)


if __name__ == "__main__":
    unittest.main()
