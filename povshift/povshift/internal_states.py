from __future__ import annotations

from typing import List

from povshift.domain import Clause


class InternalStateDetector:
    def detect_internal_states(self, clauses: List[Clause]) -> List[Clause]:
        cognitive_verbs = {"wonder", "know", "believe", "remember", "realize", "think", "suspect", "decide"}
        emotional_verbs = {"feel", "fear", "hope", "love", "hate", "worry", "regret"}
        perception_verbs = {"see", "hear", "notice", "observe", "watch", "look", "smell", "taste"}

        enriched: list[Clause] = []
        for clause in clauses:
            verb = (clause.verb or "").lower()
            subject = clause.subject
            if verb in cognitive_verbs:
                clause.internal_state = True
                clause.state_type = "cognition"
                clause.experiencer = subject
            elif verb in emotional_verbs:
                clause.internal_state = True
                clause.state_type = "emotion"
                clause.experiencer = subject
            elif verb in perception_verbs:
                clause.internal_state = True
                clause.state_type = "perception"
                clause.experiencer = subject
            else:
                clause.internal_state = False
                clause.state_type = None
                clause.experiencer = None
            enriched.append(clause)

        return enriched
