from fastapi import FastAPI, HTTPException

from model.detector import detectar_puntuacion_inusual
from service.schemas import DetectRequest, DetectResponse


app = FastAPI(title="Unusual English Punctuation Detector", version="1.0.0")


@app.post("/detect", response_model=DetectResponse)
def detect(body: DetectRequest) -> DetectResponse:
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacio.")

    unusual, positions = detectar_puntuacion_inusual(body.text)
    return DetectResponse(unusual_punctuation=unusual, positions=positions)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}