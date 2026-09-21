from __future__ import annotations

from typing import List

from povshift.domain import POVShift, FocusState


class ShiftDetector:
    def detect_shift(self, focus_history: List[FocusState]) -> List[POVShift]:
        shifts = []
        for previous, current in zip(focus_history, focus_history[1:]):
            if previous.character is None or current.character is None:
                continue
            if previous.character == current.character:
                continue
            if previous.sentence_index == current.sentence_index:
                continue

            shifts.append(
                POVShift(
                    from_character=previous.character,
                    to_character=current.character,
                    sentence_index=current.sentence_index,
                    confidence=0.85,
                    evidence=[
                        f"previous focus on {previous.character.canonical_name}",
                        f"new focalization on {current.character.canonical_name}",
                    ],
                )
            )
        return shifts
