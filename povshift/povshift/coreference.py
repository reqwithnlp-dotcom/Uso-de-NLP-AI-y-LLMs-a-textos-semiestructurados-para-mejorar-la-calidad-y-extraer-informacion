from __future__ import annotations

from typing import List

import spacy

from povshift.domain import Character, Clause


class CoreferenceResolver:
    def __init__(self, nlp: spacy.language.Language):
        # accept an initialized spaCy Language object to reuse model loading
        self._nlp = nlp

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

    def resolve_coreference(self, clauses: List[Clause]) -> List[Clause]:
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
