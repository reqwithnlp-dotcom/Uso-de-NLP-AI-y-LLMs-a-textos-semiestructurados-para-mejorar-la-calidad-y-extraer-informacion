from __future__ import annotations

import spacy

from povshift.domain import Character, Clause
from povshift.parser import NLPParser
from povshift.coreference import CoreferenceResolver


class POVShiftDetector:
    def __init__(self, model: str = "en_core_web_sm"):
        self.model = model
        try:
            # delegate spaCy initialization and linguistic analysis to NLPParser
            self._parser = NLPParser(model=model)
            self._nlp = self._parser._nlp
            # coreference resolver reuses the initialized spaCy Language
            self._coref = CoreferenceResolver(self._nlp)
            # internal state detector
            from povshift.internal_states import InternalStateDetector
            self._internal = InternalStateDetector()
            # narrative focus tracker
            from povshift.focus_tracker import NarrativeFocusTracker
            self._focus_tracker = NarrativeFocusTracker()
            # shift detector
            from povshift.shift_detector import ShiftDetector
            self._shift_detector = ShiftDetector()
        except OSError as exc:
            raise OSError(f"spaCy English model '{model}' is required for analyze().") from exc

    def detect(self, text: str):
        clauses = self.analyze(text)
        clauses = self.resolve_coreference(clauses)
        clauses = self.detect_internal_states(clauses)
        focus_history = self.update_focus(clauses)
        return self.detect_shift(focus_history)

    def analyze(self, text: str) -> list[Clause]:
        # delegate linguistic analysis to NLPParser to preserve modularity
        return self._parser.analyze(text)

    def resolve_coreference(self, clauses: list[Clause]) -> list[Clause]:
        return self._coref.resolve_coreference(clauses)


    def detect_internal_states(self, clauses: list[Clause]) -> list[Clause]:
        return self._internal.detect_internal_states(clauses)

    def update_focus(self, clauses: list[Clause]):
        return self._focus_tracker.update_focus(clauses)

    def detect_shift(self, focus_history):
        return self._shift_detector.detect_shift(focus_history)


