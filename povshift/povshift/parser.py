from __future__ import annotations

import spacy

from povshift.domain import Clause, Character


class NLPParser:
    def __init__(self, model: str = "en_core_web_sm"):
        self.model = model
        try:
            self._nlp = spacy.load(model)
        except OSError as exc:
            raise OSError(f"spaCy English model '{model}' is required for analyze().") from exc

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
