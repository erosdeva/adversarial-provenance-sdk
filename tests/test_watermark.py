
from adversarial_provenance.watermarking.text_watermark import (
    embed_watermark,
    detect_watermark
)

def test_watermark():
    text = "hello"
    marked = embed_watermark(text)

    assert detect_watermark(marked) is True
