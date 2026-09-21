from __future__ import annotations

from typing import List

from povshift.domain import FocusState, Clause


class NarrativeFocusTracker:
    def update_focus(self, clauses: List[Clause]) -> List[FocusState]:
        focus_history = []
        current_focus = None

        for clause in clauses:
            if clause.experiencer is not None:
                if current_focus is None:
                    current_focus = clause.experiencer
                    reason = "first internal focalization"
                elif clause.experiencer == current_focus:
                    reason = "same experiencer"
                else:
                    current_focus = clause.experiencer
                    reason = "different experiencer with internal evidence"
            else:
                reason = "no internal-state evidence"

            focus_history.append(
                FocusState(
                    character=current_focus,
                    sentence_index=clause.sentence_index,
                    reason=reason,
                )
            )

        return focus_history
