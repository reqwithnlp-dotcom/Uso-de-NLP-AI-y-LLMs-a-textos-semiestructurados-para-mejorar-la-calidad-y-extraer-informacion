from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from povshift.detector import POVShiftDetector


class TextRequest(BaseModel):
    texto: str = Field(..., description="Texto en inglés a analizar")


app = FastAPI(title="POV Shift Detector API", version="1.0.0")
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

    uvicorn.run("main:app", host="127.0.0.1", port=8014, reload=False)
