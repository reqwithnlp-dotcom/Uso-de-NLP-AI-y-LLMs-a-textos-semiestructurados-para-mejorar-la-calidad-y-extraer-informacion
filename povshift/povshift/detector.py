from __future__ import annotations

import spacy

from povshift.domain import Character, Clause


class POVShiftDetector:
    def __init__(self, model: str = "en_core_web_sm"):
        self.model = model
        try:
            self._nlp = spacy.load(model)
        except OSError as exc:
            raise OSError(f"spaCy English model '{model}' is required for analyze().") from exc

    @staticmethod
    def _is_pronoun_name(name: str | None) -> bool:
        if not name:
            return False
        return name.lower() in {"i", "you", "he", "she", "it", "we", "they", "him", "her", "me", "us", "them"}

    @staticmethod
    def _is_deictic_pronoun(name: str | None) -> bool:
        if not name:
            return False
        return name.lower() in {"i", "you"}

    def resolve_coreference(self, clauses: list[Clause]) -> list[Clause]:
        resolved: list[Clause] = []

        for clause in clauses:
            subject = clause.subject
            if subject is not None and self._is_deictic_pronoun(subject.canonical_name):
                subject.mentions = list(dict.fromkeys(subject.mentions + [subject.canonical_name]))
                resolved.append(clause)
                continue

            if subject is not None and self._is_pronoun_name(subject.canonical_name):
                candidates: list[Character] = []
                seen_names: set[str] = set()

                for previous in resolved:
                    previous_subject = previous.subject
                    if previous_subject is not None and not self._is_pronoun_name(previous_subject.canonical_name):
                        if previous_subject.canonical_name not in seen_names:
                            candidates.append(previous_subject)
                            seen_names.add(previous_subject.canonical_name)

                    if previous.text:
                        for entity in self._nlp(previous.text).ents:
                            if entity.label_ == "PERSON" and entity.text.strip():
                                name = entity.text.strip()
                                if not self._is_pronoun_name(name) and name not in seen_names:
                                    candidates.append(Character(id=len(candidates) + 1, canonical_name=name, mentions=[name]))
                                    seen_names.add(name)

                unique: list[Character] = []
                for candidate in candidates:
                    if candidate.canonical_name not in {item.canonical_name for item in unique}:
                        unique.append(candidate)

                if len(unique) == 1:
                    candidate = unique[0]
                    candidate.mentions = list(dict.fromkeys(candidate.mentions + [subject.canonical_name]))
                    clause.subject = candidate
                    resolved.append(clause)
                    continue

                clause.subject = None
                resolved.append(clause)
                continue

            if subject is not None:
                subject.mentions = list(dict.fromkeys(subject.mentions + [subject.canonical_name]))

            resolved.append(clause)

        return resolved

    def detect_internal_states(self, clauses: list[Clause]) -> list[Clause]:
        cognitive_verbs = {"wonder", "know", "believe", "remember", "realize", "think", "suspect", "decide"}
        emotional_verbs = {"feel", "fear", "hope", "love", "hate", "worry", "regret"}

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
            else:
                clause.internal_state = False
                clause.state_type = None
                clause.experiencer = None
            enriched.append(clause)

        return enriched

    def update_focus(self, clauses: list[Clause]):
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
                __import__("povshift.domain").domain.FocusState(
                    character=current_focus,
                    sentence_index=clause.sentence_index,
                    reason=reason,
                )
            )

        return focus_history

    def detect_shift(self, focus_history):
        shifts = []
        for previous, current in zip(focus_history, focus_history[1:]):
            if previous.character is None or current.character is None:
                continue
            if previous.character == current.character:
                continue
            if previous.sentence_index == current.sentence_index:
                continue

            shifts.append(
                __import__("povshift.domain").domain.POVShift(
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

    def detect(self, text: str):
        clauses = self.analyze(text)
        clauses = self.resolve_coreference(clauses)
        clauses = self.detect_internal_states(clauses)
        focus_history = self.update_focus(clauses)
        return self.detect_shift(focus_history)

    def analyze(self, text: str) -> list[Clause]:
        if text is None or not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")

        doc = self._nlp(text)
        clauses: list[Clause] = []

        for sentence_index, sentence in enumerate(doc.sents):
            clause_roots = self._extract_clause_roots(sentence)
            for root in clause_roots:
                subject_token = self._find_subject_token(root)
                subject = self._build_subject(subject_token)
                clause_text = self._build_clause_text(sentence, root)
                clauses.append(
                    Clause(
                        text=clause_text,
                        sentence_index=sentence_index,
                        subject=subject,
                        verb=root.lemma_.lower(),
                        internal_state=False,
                        state_type=None,
                        experiencer=None,
                    )
                )

        return clauses

    def _extract_clause_roots(self, sentence):
        roots = []
        for token in sentence:
            if token.pos_ in {"VERB", "AUX"} and token.dep_ in {"ROOT", "conj"}:
                roots.append(token)
        return roots

    def _find_subject_token(self, root):
        for child in root.children:
            if child.dep_ in {"nsubj", "nsubjpass", "agent"}:
                return child
        return None

    def _build_subject(self, subject_token):
        if subject_token is None:
            return None
        return Character(
            id=subject_token.i + 1,
            canonical_name=subject_token.text,
            mentions=[subject_token.text],
        )

    def _build_clause_text(self, sentence, root):
        if len(self._extract_clause_roots(sentence)) == 1:
            return sentence.text.strip()

        clause_tokens = []
        for token in sentence:
            if token in root.subtree:
                clause_tokens.append(token)
        if not clause_tokens:
            return sentence.text.strip()
        start = min(token.i for token in clause_tokens)
        end = max(token.i for token in clause_tokens)
        return sentence[start:end + 1].text.strip()
