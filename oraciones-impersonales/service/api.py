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
from model import classifier
from model.detector import analyze_text
from service.schemas import AnalyzeRequest, AnalyzeResponse, SentenceResult

app = FastAPI(
    title="Detector de Oraciones Impersonales",
    description=(
        "Microservicio que clasifica oraciones en inglés como personales o "
        "impersonales. Capa 1: reglas sobre dependencias de spaCy, que dan "
        "dos booleanos independientes —«personal» e «impersonal»— y marcan "
        "como `ambiguous` los casos límite (ambos True o ambos False). "
        "Capa 2: un clasificador spaCy (textcat_multilabel) entrenado sobre "
        "un corpus propio desambigua solo esos casos. `final_label` y "
        "`decided_by` informan la decisión final."
    ),
    version="3.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["infra"])
def health():
    """Chequeo de vida del servicio. Informa si la capa 2 está disponible
    (carga el clasificador si existe; no carga el parser de la capa 1)."""
    return {"status": "ok", "layer2_loaded": classifier.is_loaded()}


@app.post("/analyze", response_model=AnalyzeResponse, tags=["nlp"])
def analyze(request: AnalyzeRequest):
    """Analiza un texto y devuelve el diagnóstico oración por oración."""
    try:
        raw_results = analyze_text(request.text)
    except (RuntimeError, OSError) as exc:
        # Falta el modelo de spaCy de la capa 1 o el de la capa 2 está roto
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    results = [SentenceResult(**r) for r in raw_results]
    return AnalyzeResponse(
        results=results,
        total=len(results),
        impersonal_count=sum(1 for r in results if r.impersonal),
        personal_count=sum(1 for r in results if r.personal),
        ambiguous_count=sum(1 for r in results if r.ambiguous),
        layer2_resolved_count=sum(1 for r in results if r.decided_by == "layer2"),
        undecided_count=sum(1 for r in results if r.final_label == "UNDECIDED"),
    )
