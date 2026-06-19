from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from service.service import ReadabilityService
from model.PenalizacionPorComa import PenalizacionPorComa


_service: ReadabilityService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _service
    _service = ReadabilityService()
    yield


app = FastAPI(
    title="Metricas de Legibilidad",
    description="API para analisis de legibilidad de textos con Gunning Fog extendido",
    version="0.1.0",
    lifespan=lifespan,
)


class AnalizarRequest(BaseModel):
    texto: str = Field(..., min_length=1, description="Texto a analizar")
    penalizacion: PenalizacionPorComa = Field(
        default=PenalizacionPorComa.MEDIUM,
        description="Nivel de penalizacion por coma: minimum, low, medium, high",
    )


class AnalizarResponse(BaseModel):
    score: float
    gunning_fog: float
    comma_penalty: float
    comma_ratio: float
    words_per_sentence: float
    alpha: float


@app.post("/analizar", response_model=AnalizarResponse)
def analizar(request: AnalizarRequest) -> dict:
    return _service.analizar(texto=request.texto, penalizacion=request.penalizacion)
