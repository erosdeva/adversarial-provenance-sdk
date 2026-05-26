"""
Invisible Text Watermarking Engine using Zero-Width Unicode Characters.
Transforms a watermark string into binary, then maps bits to invisible spaces.
"""

import binascii

WATERMARK = "[APS_VERIFIED]"


class TextWatermarker:
    # Use zero-width space (ZWSP) for '0' and zero-width non-joiner (ZWNJ) for '1'
    ZERO_WIDTH_0 = "\u200b"
    ZERO_WIDTH_1 = "\u200c"

    @classmethod
    def _str_to_bin(cls, text: str) -> str:
        """Converts a UTF-8 string into a string of binary digits."""
        hidden_bytes = text.encode("utf-8")
        return bin(int(binascii.hexlify(hidden_bytes), 16))[2:].zfill(
            len(hidden_bytes) * 8
        )

    @classmethod
    def _bin_to_str(cls, binary_str: str) -> str:
        """Converts a string of binary digits back into a UTF-8 string."""
        try:
            # Ensure proper padding for byte conversion
            num_bits = len(binary_str)
            num_bytes = (num_bits + 7) // 8
            binary_str = binary_str.zfill(num_bytes * 8)

            n = int(binary_str, 2)
            hex_data = "%x" % n
            # Handle edge case for odd-length hex strings
            if len(hex_data) % 2 != 0:
                hex_data = "0" + hex_data
            return binascii.unhexlify(hex_data).decode("utf-8")
        except Exception:
            raise ValueError(
                "Failed to decode binary data. The payload may be corrupted."
            )

    @classmethod
    def embed(cls, cover_text: str, watermark: str) -> str:
        """Embeds an invisible watermark string into the cover text.

        The watermark is injected seamlessly after the first word.
        """
        if not cover_text or not watermark:
            return cover_text

        # 1. Convert watermark to binary
        binary_watermark = cls._str_to_bin(watermark)

        # 2. Map binary to invisible characters
        invisible_payload = "".join(
            cls.ZERO_WIDTH_1 if bit == "1" else cls.ZERO_WIDTH_0
            for bit in binary_watermark
        )

        # 3. Inject seamlessly into the text (e.g., right after the first word)
        words = cover_text.split(" ", 1)
        if len(words) > 1:
            return f"{words[0]}{invisible_payload} {words[1]}"
        else:
            # Fallback if it's a single-word string
            return f"{cover_text}{invisible_payload}"

    @classmethod
    def extract(cls, watermarked_text: str) -> str:
        """Extracts and decodes the invisible watermark from the text.

        Returns an empty string if no watermark is found.
        """
        binary_bits = []

        # Scan text for the target hidden characters
        for char in watermarked_text:
            if char == cls.ZERO_WIDTH_0:
                binary_bits.append("0")
            elif char == cls.ZERO_WIDTH_1:
                binary_bits.append("1")

        if not binary_bits:
            return ""

        binary_str = "".join(binary_bits)
        return cls._bin_to_str(binary_str)


# Quick functional aliases for ease of use
def embed_watermark(text: str, watermark: str = WATERMARK) -> str:
    return TextWatermarker.embed(text, watermark)


def extract_watermark(text: str) -> str:
    return TextWatermarker.extract(text)