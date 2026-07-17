from typing import List, Tuple

from fastapi import FastAPI
from pydantic import BaseModel

from servicio import detect_modal_verbs, MODAL_VERBS

app = FastAPI(
    title="Detección de inconsistencias de verbos modales",
    description="Servicio que detecta verbos modales en un texto y las frases entre ellos.",
    version="1.0.0",
)


class TextoRequest(BaseModel):
    texto: str


class DeteccionResponse(BaseModel):
    modals: List[Tuple[str, str]]
    phrases: List[str]


@app.get("/")
def root():
    return {"mensaje": "Servicio de detección de inconsistencias de verbos modales activo"}


@app.post("/detectar", response_model=DeteccionResponse)
def detectar_modales(request: TextoRequest):
    modals, phrases = detect_modal_verbs(request.texto, MODAL_VERBS)
    return {"modals": modals, "phrases": phrases}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)