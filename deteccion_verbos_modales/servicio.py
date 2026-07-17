"""
Modal Verb Inconsistency Detector (English)

Idea (per discussion with Giu):
Counting or judging an "excess" of modal verbs doesn't make sense on its
own -- it depends on the type of text (legal text vs. general text, etc.).
What IS a real problem is INCONSISTENCY: the same action described in one
part of the text with a modal from one category ("You can submit X" ->
possibility/permission) and in another part with a modal from a
different category for that same action ("You must submit X" ->
obligation).

This script:
1. Finds every occurrence of a modal verb/expression in the text.
2. Extracts the "action" associated with each modal (whatever follows it
   until the end of that sentence).
3. Compares actions against each other to find pairs that describe the
   same thing but were tagged with modals from different categories.
4. Reports those inconsistencies.
"""

import re
from itertools import combinations

# Modal expressions grouped by semantic category.
# Longer/more specific phrases are matched first so that, for example,
# "must not" is not wrongly classified as "must".
MODAL_CATEGORIES = {
    "prohibition": [
        "cannot", "can not", "can't", "must not", "mustn't",
        "may not", "is not allowed to", "are not allowed to",
        "is prohibited", "are prohibited", "is forbidden", "are forbidden",
    ],
    "obligation": [
        "has to", "have to", "needs to", "need to",
        "is required to", "are required to",
        "is necessary to", "is mandatory", "must",
    ],
    "recommendation": [
        "ought to", "should", "is recommended", "are recommended",
        "it is advisable to",
    ],
    "possibility/permission": [
        "is permitted to", "are permitted to", "is allowed to", "are allowed to",
        "is possible to", "are possible to",
        "could", "might", "may", "can",
    ],
}

# Simple English stopwords so actions are compared by meaningful words only.
STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "and", "or", "that", "this",
    "these", "those", "is", "are", "be", "on", "for", "with", "by",
    "its", "it", "as", "about", "at", "from", "into", "your", "their",
    "his", "her", "our", "so", "will", "shall",
}


def build_pattern_list():
    """Returns [(modal_phrase, category)] sorted longest-phrase first."""
    all_modals = []
    for category, phrases in MODAL_CATEGORIES.items():
        for phrase in phrases:
            all_modals.append((phrase, category))
    all_modals.sort(key=lambda x: -len(x[0].split()))
    return all_modals


def split_sentences(text: str):
    """Splits text into sentences, keeping their offset in the text."""
    sentences = []
    for match in re.finditer(r"[^.;\n]+[.;\n]?", text):
        sentence = match.group().strip()
        if sentence:
            sentences.append((match.start(), sentence))
    return sentences


def extract_modal_actions(text: str):
    """
    Looks for modals in each sentence and extracts the "action" (whatever
    follows the modal within that same sentence).

    Returns a list of dicts: {modal, category, action, sentence}
    """
    pattern_list = build_pattern_list()
    results = []

    for _, sentence in split_sentences(text):
        lowered = sentence.lower()
        matched_spans = []

        for phrase, category in pattern_list:
            for m in re.finditer(r"\b" + re.escape(phrase) + r"\b", lowered):
                # skip if it overlaps a previously matched (longer) phrase
                if any(m.start() < e and s < m.end() for s, e in matched_spans):
                    continue
                matched_spans.append((m.start(), m.end()))

                action = sentence[m.end():].strip(" ,:-")
                if action:
                    results.append({
                        "modal": phrase,
                        "category": category,
                        "action": action,
                        "sentence": sentence.strip(),
                    })

    return results


def normalize_action(action: str) -> set:
    """Turns the action into a set of keywords (no punctuation, no stopwords)."""
    action = action.lower()
    action = re.sub(r"[^a-z0-9\s]", " ", action)
    words = action.split()
    return {w for w in words if w not in STOPWORDS and len(w) > 2}


def find_consistencies_and_inconsistencies(
    modal_actions: list, min_shared_words: int = 2, min_overlap: float = 0.5
):
    """
    Compares every action against every other action that shares enough
    keywords (i.e. describes essentially the same action).

    - If both actions were tagged with modals from the SAME category ->
      it's a "consistency" (the text treats that action the same way
      everywhere).
    - If they were tagged with modals from DIFFERENT categories ->
      it's an "inconsistency".

    Returns a tuple: (consistencies, inconsistencies), each a list of
    dicts with {shared_action, case_1, case_2}.
    """
    for item in modal_actions:
        item["_keywords"] = normalize_action(item["action"])

    consistencies = []
    inconsistencies = []

    for a, b in combinations(modal_actions, 2):
        shared = a["_keywords"] & b["_keywords"]
        smaller = min(len(a["_keywords"]), len(b["_keywords"])) or 1
        overlap = len(shared) / smaller

        if len(shared) < min_shared_words or overlap < min_overlap:
            continue  # not the same action -> not relevant either way

        pair = {
            "shared_action": ", ".join(sorted(shared)),
            "case_1": a,
            "case_2": b,
        }

        if a["category"] == b["category"]:
            consistencies.append(pair)
        else:
            inconsistencies.append(pair)

    return consistencies, inconsistencies


def report(consistencies: list, inconsistencies: list):
    print(f"Detected {len(consistencies)} consistent pair(s):\n")
    for i, con in enumerate(consistencies, 1):
        c1, c2 = con["case_1"], con["case_2"]
        print(f"--- Consistency {i} (shared keywords: {con['shared_action']}) ---")
        print(f'  [{c1["category"]}] "{c1["modal"]}" in: "{c1["sentence"]}"')
        print(f'  [{c2["category"]}] "{c2["modal"]}" in: "{c2["sentence"]}"')
        print()

    if not inconsistencies:
        print("No modal verb inconsistencies were detected.\n")
        return

    print(f"Detected {len(inconsistencies)} possible inconsistency(ies):\n")
    for i, inc in enumerate(inconsistencies, 1):
        c1, c2 = inc["case_1"], inc["case_2"]
        print(f"--- Inconsistency {i} (shared keywords: {inc['shared_action']}) ---")
        print(f'  [{c1["category"]}] "{c1["modal"]}" in: "{c1["sentence"]}"')
        print(f'  [{c2["category"]}] "{c2["modal"]}" in: "{c2["sentence"]}"')
        print()


def analyze_text(text: str):
    """
    Runs the full pipeline and returns (consistencies, inconsistencies).
    """
    modal_actions = extract_modal_actions(text)
    consistencies, inconsistencies = find_consistencies_and_inconsistencies(modal_actions)
    report(consistencies, inconsistencies)
    return consistencies, inconsistencies


if __name__ == "__main__":
    print("=== Modal Verb Inconsistency Detector ===")
    print("Paste the text to analyze and press Enter:\n")
    text_input = input("> ")
    analyze_text(text_input)