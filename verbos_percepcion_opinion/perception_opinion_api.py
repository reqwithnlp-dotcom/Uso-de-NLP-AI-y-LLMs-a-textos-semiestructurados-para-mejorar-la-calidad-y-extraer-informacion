from fastapi import FastAPI, HTTPException, status

from schemas import PerceptionOpinionRequest, PerceptionOpinionResponse
from service import detect_opinion_and_perception

app = FastAPI()


@app.post("/perception-opinion", response_model=PerceptionOpinionResponse, status_code=status.HTTP_200_OK)
def detect_perception_opinion(payload: PerceptionOpinionRequest):
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text field is empty",
        )

    try:
        result = detect_opinion_and_perception(payload.text)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing the text",
        )

    return result