
from adversarial_provenance.middleware import APSMiddleware

aps = APSMiddleware()

response = aps.secure_generate(
    prompt="Explain zero trust architecture."
)

print(response.model_dump_json(indent=2))
