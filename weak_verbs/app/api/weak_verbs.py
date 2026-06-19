"""API endpoints for weak verb detection."""

from fastapi import APIRouter, HTTPException, status

from ..models.schemas import WeakVerbsRequest
from ..services.service import detect_weak_verbs

router = APIRouter()


@router.post(
    "/weak_verbs",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
)
def detect_weak_verbs_endpoint(payload: WeakVerbsRequest):
    """Detect weak verbs for the provided text."""
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text field is empty",
        )

    try:
        result = detect_weak_verbs(payload.text)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing the text",
        ) from exc

    return result