from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from servicio import detect_connectors, CONNECTORS

app = FastAPI(
    title="Logical Connector Detector",
    description="Recibe un string en ingles y devuelve los conectores logicos encontrados.",
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

class ConnectorResult(BaseModel):
    word: str
    type: str

class DetectResponse(BaseModel):
    original_text: str
    connectors_found: list[ConnectorResult]
    normal_words: list[str]
    total: int

@app.post("/detect", response_model=DetectResponse)
def detect(body: DetectRequest):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacio.")
    connectors, normal_words = detect_connectors(body.text)
    return DetectResponse(
        original_text=body.text,
        connectors_found=[ConnectorResult(word=w, type=t) for w, t in connectors],
        normal_words=normal_words,
        total=len(connectors),
    )

@app.get("/connectors")
def list_connectors():
    return {"connectors": CONNECTORS}

@app.get("/health")
def health():
    return {"status": "ok"}


