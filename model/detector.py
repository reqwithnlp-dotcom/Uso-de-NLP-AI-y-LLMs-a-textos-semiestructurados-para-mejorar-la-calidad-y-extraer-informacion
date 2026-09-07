"""Detection of unusual punctuation in English text."""

from __future__ import annotations

import re


PUNCTUATION = r".,;:!?\"'()[]{}"


def _add_issue(issues: list[dict], text: str, start: int, end: int) -> None:
    issue = {"text": text[start:end], "start": start, "end": end}
    if issue not in issues:
        issues.append(issue)


def _find_issues(text: str) -> list[dict]:
    issues: list[dict] = []

    for match in re.finditer(rf"[{re.escape(PUNCTUATION)}]{{2,}}", text):
        run = match.group()
        if run == "...":
            continue
        for offset, character in enumerate(run):
            if character != ".":
                _add_issue(issues, text, match.start() + offset, match.start() + offset + 1)

    for match in re.finditer(r"[.,;:!?](?=[A-Za-z])", text):
        _add_issue(issues, text, match.start(), match.end())

    stack: list[tuple[str, int]] = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for index, character in enumerate(text):
        if character in "([{":
            stack.append((character, index))
        elif character in pairs:
            if not stack or stack[-1][0] != pairs[character]:
                _add_issue(issues, text, index, index + 1)
            else:
                stack.pop()

    for _, index in stack:
        _add_issue(issues, text, index, index + 1)

    issues.sort(key=lambda issue: issue["start"])
    return issues


def detectar_puntuacion_inusual(texto: str) -> tuple[bool, list[str] | int]:
    """Return whether punctuation is unusual and the affected marks."""
    if not isinstance(texto, str):
        raise TypeError("texto debe ser un string")

    issues = _find_issues(texto)
    return bool(issues), [issue["text"] for issue in issues] or 0


def analyze_punctuation(text: str) -> tuple[bool, list[str] | int]:
    return detectar_puntuacion_inusual(text)