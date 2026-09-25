from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from povshift.detector import POVShiftDetector


class TextRequest(BaseModel):
    texto: str = Field(..., description="Texto en inglés a analizar")


app = FastAPI(title="POV Shift Detector API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = POVShiftDetector()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/detect")
def detect_pov_shift(payload: TextRequest) -> list[dict[str, Any]]:
    shifts = detector.detect(payload.texto)
    result: list[dict[str, Any]] = []

    for shift in shifts:
        result.append(
            {
                "from_character": {
                    "id": shift.from_character.id,
                    "canonical_name": shift.from_character.canonical_name,
                    "mentions": shift.from_character.mentions,
                },
                "to_character": {
                    "id": shift.to_character.id,
                    "canonical_name": shift.to_character.canonical_name,
                    "mentions": shift.to_character.mentions,
                },
                "sentence_index": shift.sentence_index,
                "confidence": shift.confidence,
                "evidence": shift.evidence,
            }
        )

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8014, reload=False)
