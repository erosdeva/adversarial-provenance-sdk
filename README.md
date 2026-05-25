
# Adversarial Provenance SDK

Enterprise-grade adversarial provenance middleware SDK for validating, watermarking, auditing, and securing AI-generated outputs.

---

# Features

- Prompt injection detection
- Hallucination scoring
- Risk scoring
- Trust scoring
- PII detection
- Ethical policy enforcement
- Adversarial validation
- Provenance hashing
- Watermarking
- Audit logging
- FastAPI integration
- Docker deployment

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/adversarial-provenance-sdk.git
cd adversarial-provenance-sdk
```

## Create Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
.\venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

The editable install (`-e .`) puts `adversarial_provenance` on your Python path for imports and tests.

---

# Environment Variables

Create a `.env` file in the root directory.

```env
OPENAI_API_KEY=YOUR_API_KEY
APS_LOG_LEVEL=INFO
APS_ENV=development
```

---

# Quick Start

```python
from adversarial_provenance.middleware import APSMiddleware

aps = APSMiddleware()

response = aps.secure_generate(
    prompt="Explain zero trust architecture",
    model="gpt-4o-mini"
)

print(response.output)
print(response.trust_score)
print(response.provenance_hash)
```

---

# Run FastAPI Server

```bash
uvicorn adversarial_provenance.api.server:app --reload
```

Visit:

```text
http://127.0.0.1:8000/docs
```

---

# Run Tests

```bash
pytest tests/
```

---

# Docker

## Build

```bash
docker build -t aps-sdk .
```

## Run

```bash
docker run -p 8000:8000 aps-sdk
```

---

# Example Output

```json
{
  "output": "Zero trust architecture assumes no implicit trust...",
  "trust_score": 0.91,
  "hallucination_score": 0.08,
  "risk_score": 0.09,
  "provenance_hash": "2f3c...",
  "metadata": {
    "verified": true,
    "watermarked": true
  }
}
```

---

# Architecture

```text
User
  ↓
Enterprise Application
  ↓
APS Middleware
  ↓
Primary LLM
  ↓
Adversarial Validator
  ↓
Trust Scoring + Watermarking
  ↓
Verified Output
```

---

# Future Roadmap

- Semantic watermarking
- Redis support
- PostgreSQL persistence
- C2PA integration
- Kubernetes deployment
- Multi-modal provenance
- Enterprise dashboard

---

# License

MIT
