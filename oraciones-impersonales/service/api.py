"""
Capa service: expone el modelo como API HTTP con FastAPI.

Responsabilidad única: traducir HTTP <-> llamadas al modelo.
No contiene NINGUNA regla lingüística; todo lo gramatical vive
en la capa `model`. Si mañana se cambia FastAPI por Flask, solo
se reescribe este paquete.

Levantar con:
    uvicorn service.api:app --reload
Documentación interactiva automática en:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model.detector import analyze_text
from service.schemas import AnalyzeRequest, AnalyzeResponse, SentenceResult

app = FastAPI(
    title="Detector de Oraciones Impersonales",
    description=(
        "Microservicio que clasifica oraciones en inglés (capa 1 a base de "
        "reglas sobre dependencias de spaCy). Para cada oración devuelve dos "
        "booleanos independientes —«personal» e «impersonal»— y marca como "
        "`ambiguous` los casos límite (ambos True o ambos False) que deben "
        "escalar a una capa 2 basada en un modelo de lenguaje."
    ),
    version="2.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O ["*"] para desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Incluye OPTIONS
    allow_headers=["*"],
)

@app.get("/health", tags=["infra"])
def health():
    """Chequeo de vida del servicio (no carga el modelo)."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse, tags=["nlp"])
def analyze(request: AnalyzeRequest):
    """Analiza un texto y devuelve el diagnóstico oración por oración."""
    try:
        raw_results = analyze_text(request.text)
    except RuntimeError as exc:
        
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    results = [SentenceResult(**r) for r in raw_results]
    return AnalyzeResponse(
        results=results,
        total=len(results),
        impersonal_count=sum(1 for r in results if r.impersonal),
        personal_count=sum(1 for r in results if r.personal),
        ambiguous_count=sum(1 for r in results if r.ambiguous),
    )
