from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

from servicio_deteccion_cliches import detectar_cliches, _get_sbert

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-cargar el modelo SBERT y vectorizar el corpus de clichés al iniciar
    print("Pre-cargando modelo SBERT y corpus para detección de clichés...")
    try:
        _get_sbert()
        print("Modelo SBERT cargado correctamente.")
    except Exception as e:
        print(f"Error al precargar el modelo SBERT: {e}")
    yield

app = FastAPI(
    title="Servicio de Detección de Clichés",
    description="API que expone la detección de clichés utilizando spaCy y Sentence Transformers (SBERT).",
    version="1.0.0",
    lifespan=lifespan
)

# Habilitar CORS para permitir peticiones desde el navegador (Django corre en puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClicheRequest(BaseModel):
    texto: str = Field(..., description="El texto a analizar en busca de clichés")
    filtrado_inicial: bool = Field(True, description="Ejecutar fase 1 de n-gramas exactos")
    analisis_profundo: bool = Field(True, description="Ejecutar fase 2 de similitud semántica con SBERT")
    umbral_semantico: float = Field(0.75, ge=0.0, le=1.0, description="Umbral de similitud para SBERT")

class ClicheResponse(BaseModel):
    cliches_encontrados: List[str] = Field(..., description="Lista de clichés detectados en minúsculas")

@app.get("/health", tags=["infra"])
def health():
    return {"status": "ok"}

@app.post("/detectar_cliches/", response_model=ClicheResponse, tags=["nlp"])
def api_detectar_cliches(payload: ClicheRequest):
    try:
        resultados = detectar_cliches(
            texto=payload.texto,
            filtrado_inicial=payload.filtrado_inicial,
            analisis_profundo=payload.analisis_profundo,
            umbral_semantico=payload.umbral_semantico
        )
        return ClicheResponse(cliches_encontrados=resultados)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
