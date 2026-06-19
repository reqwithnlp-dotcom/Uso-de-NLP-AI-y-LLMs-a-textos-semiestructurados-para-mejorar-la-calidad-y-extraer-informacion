

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Body del POST /analyze."""
    text: str = Field(
        ...,
        min_length=1,
        description="Texto en inglés con una o más oraciones a evaluar.",
        examples=["It is important to remember the guidelines. I bought a car."],
    )


class SentenceResult(BaseModel):
    """Diagnóstico de una oración individual."""
    sentence: str = Field(description="La oración analizada.")
    impersonal: bool = Field(description="True si la oración es impersonal.")
    type: str = Field(
        description=(
            "Tipo detectado: THERE_EXISTENTIAL, WEATHER_IT, "
            "WEATHER_ADJECTIVE, IMPERSONAL_PASSIVE, IT_EXTRAPOSITION "
            "o PERSONAL."
        )
    )


class AnalyzeResponse(BaseModel):
    """Respuesta del POST /analyze."""
    results: list[SentenceResult]
    total: int = Field(description="Cantidad de oraciones procesadas.")
    impersonal_count: int = Field(description="Cuántas resultaron impersonales.")
