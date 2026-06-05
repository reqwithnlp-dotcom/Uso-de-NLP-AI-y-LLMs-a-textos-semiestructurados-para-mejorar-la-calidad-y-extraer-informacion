"""API endpoints for perception and opinion verb detection."""

from fastapi import APIRouter, HTTPException, status

from ..models.schemas import PerceptionOpinionRequest, PerceptionOpinionResponse
from ..services.service import detect_opinion_and_perception

router = APIRouter()


@router.post(
    "/perception-opinion",
    response_model=PerceptionOpinionResponse,
    status_code=status.HTTP_200_OK,
)
def detect_perception_opinion(payload: PerceptionOpinionRequest):
    """Detect perception and opinion verbs for the provided text."""
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text field is empty",
        )

    try:
        result = detect_opinion_and_perception(payload.text)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing the text",
        ) from exc

    return result