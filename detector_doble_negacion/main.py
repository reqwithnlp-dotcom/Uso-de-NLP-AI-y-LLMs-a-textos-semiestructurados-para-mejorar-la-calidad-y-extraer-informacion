from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from servicio import detect_double_negation

app = FastAPI(
    title="Double Negation Detector",
    description="Recibe un string en inglés y detecta si contiene doble negación.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DetectRequest(BaseModel):
    text: str

class DetectResponse(BaseModel):
    text: str
    has_double_negation: bool

@app.post("/detect", response_model=DetectResponse)
def detect(body: DetectRequest):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacio.")
    result = detect_double_negation(body.text)
    return DetectResponse(
        text=body.text,
        has_double_negation=result,
    )

@app.get("/health")
def health():
    return {"status": "ok"}