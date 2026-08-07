from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from servicio import extract_modal_actions, find_inconsistencies

app = FastAPI(
    title="Deteccion de inconsistencias de verbos modales",
    description=(
        "Servicio que detecta si una misma accion es descrita en el texto "
        "con verbos modales de categorias semanticas distintas (por ejemplo, "
        "obligacion en un lugar y posibilidad/permiso en otro)."
    ),
    version="1.0.0",
)


class TextoRequest(BaseModel):
    texto: str


class Caso(BaseModel):
    modal: str
    category: str
    action: str
    sentence: str


class Par(BaseModel):
    shared_action: str
    case_1: Caso
    case_2: Caso


class AnalisisResponse(BaseModel):
    inconsistencies: List[Par]


@app.get("/")
def root():
    return {"mensaje": "Servicio de deteccion de inconsistencias de verbos modales activo"}


@app.post("/analizar", response_model=AnalisisResponse)
def analizar_texto(request: TextoRequest):
    modal_actions = extract_modal_actions(request.texto)
    inconsistencies = find_inconsistencies(modal_actions)
    return {"inconsistencies": inconsistencies}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)