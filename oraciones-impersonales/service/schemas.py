

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
    """Diagnóstico de una oración individual (capa 1)."""
    sentence: str = Field(description="La oración analizada.")
    personal: bool = Field(
        description="«Es personal»: hay evidencia de sujeto referencial."
    )
    impersonal: bool = Field(
        description="«Es impersonal»: matchea alguna regla impersonal."
    )
    ambiguous: bool = Field(
        description=(
            "True si personal == impersonal (ambos True o ambos False). "
            "Caso límite: la oración debe escalar a la capa 2 (LLM)."
        )
    )
    type: str = Field(
        description=(
            "Subtipo impersonal: THERE_EXISTENTIAL, WEATHER_IT, "
            "WEATHER_ADJECTIVE, IMPERSONAL_PASSIVE, IT_EXTRAPOSITION "
            "o PERSONAL (por defecto, si no hay match impersonal)."
        )
    )
    personal_type: str | None = Field(
        default=None,
        description=(
            "Subtipo de evidencia personal: PRONOUN_SUBJECT, "
            "NOMINAL_SUBJECT, IMPERATIVE; o None si no hubo match."
        ),
    )


class AnalyzeResponse(BaseModel):
    """Respuesta del POST /analyze."""
    results: list[SentenceResult]
    total: int = Field(description="Cantidad de oraciones procesadas.")
    impersonal_count: int = Field(description="Cuántas resultaron impersonales.")
    personal_count: int = Field(description="Cuántas resultaron personales.")
    ambiguous_count: int = Field(
        description="Cuántas quedaron como caso límite (a escalar a capa 2)."
    )
