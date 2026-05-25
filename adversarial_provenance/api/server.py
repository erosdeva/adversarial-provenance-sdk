
from fastapi import FastAPI
from pydantic import BaseModel

from adversarial_provenance.middleware import APSMiddleware

app = FastAPI(title="Adversarial Provenance SDK")

aps = APSMiddleware()

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/generate")
def generate(request: GenerateRequest):
    return aps.secure_generate(
        prompt=request.prompt,
        model=request.model
    )
