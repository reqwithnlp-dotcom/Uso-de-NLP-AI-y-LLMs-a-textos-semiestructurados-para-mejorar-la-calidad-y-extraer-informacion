from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict

from servicio_repeticion_palabras import detectar_repeticiones

app = FastAPI(
    title="Servicio de Repetición de Palabras",
    description="API que expone el análisis de palabras repetidas en un texto.",
    version="1.0.0"
)

# Habilitar CORS para permitir peticiones desde el navegador (Django corre en puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepeticionRequest(BaseModel):
    texto: str = Field(..., description="El texto a analizar en busca de repeticiones")
    sin_palabras_frecuentes: bool = Field(True, description="Ignorar stopwords comunes")
    con_sustantivos_en_singular: bool = Field(False, description="Agrupar por lema de la palabra (lematización)")

@app.get("/health", tags=["infra"])
def health():
    return {"status": "ok"}

@app.post("/repeticiones", response_model=Dict[str, int], tags=["nlp"])
def api_detectar_repeticiones(payload: RepeticionRequest):
    try:
        # Nota:
        # - ignorar_stopwords mapea a sin_palabras_frecuentes
        # - lematizacion mapea a con_sustantivos_en_singular
        resultados_detallados = detectar_repeticiones(
            texto=payload.texto,
            ignorar_stopwords=payload.sin_palabras_frecuentes,
            lematizacion=payload.con_sustantivos_en_singular
        )
        
        # Mapeo al formato de diccionario plano {"palabra": cantidad}
        # requerido para compatibilidad directa con Object.entries(data) en aplicar_servicios.js
        retorno_plano = {item["word"]: item["count"] for item in resultados_detallados}
        return retorno_plano
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
