from typing import List, Tuple
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from detector import is_passive, passive_positions

app = FastAPI(
    title="Servicio de Detección de Voz Pasiva",
    description="Microservicio NLP para analizar oraciones en inglés y detectar estructuras de voz pasiva."
)

# Permitir peticiones desde cualquier origen (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic (Esquema de entrada y salida)
class PassiveRequest(BaseModel):
    texto: str = Field(..., description="El texto en inglés a analizar en busca de voz pasiva")

class PassiveResponse(BaseModel):
    is_passive: bool = Field(..., description="Indica si la oración está en voz pasiva")
    positions: List[Tuple[int, int]] = Field(..., description="Lista de tuplas con las posiciones (inicio, fin) detectadas")

# Endpoint de comprobación de salud del servicio (Health Check)
@app.get("/health", tags=["infra"])
def health():
    return {"status": "ok"}

# Endpoint principal de análisis
@app.post("/detectar_voz_pasiva", response_model=PassiveResponse, tags=["nlp"])
def api_detectar_voz_pasiva(payload: PassiveRequest):
    try:
        texto = payload.texto
        es_pasiva = is_passive(texto)
        posiciones = passive_positions(texto)
        
        return PassiveResponse(
            is_passive=es_pasiva,
            positions=posiciones
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))