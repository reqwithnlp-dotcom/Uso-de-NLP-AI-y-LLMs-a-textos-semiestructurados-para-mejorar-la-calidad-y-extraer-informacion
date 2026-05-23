from enum import StrEnum


class PenalizacionPorComa(StrEnum):

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def alpha(self) -> float:
        match self:
            case PenalizacionPorComa.LOW:
                return 0.05
            case PenalizacionPorComa.MEDIUM:
                return 0.10
            case PenalizacionPorComa.HIGH:
                return 0.20

