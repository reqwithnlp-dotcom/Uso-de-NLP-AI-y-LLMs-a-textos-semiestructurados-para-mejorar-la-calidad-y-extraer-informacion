from enum import StrEnum


class PenalizacionPorComa(StrEnum):
    MINIMUM="minimum"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def alpha(self) -> float:
        match self:
            case PenalizacionPorComa.MINIMUM:
                return 0.025
            case PenalizacionPorComa.LOW:
                return 0.05
            case PenalizacionPorComa.MEDIUM:
                return 0.10
            case PenalizacionPorComa.HIGH:
                return 0.20

