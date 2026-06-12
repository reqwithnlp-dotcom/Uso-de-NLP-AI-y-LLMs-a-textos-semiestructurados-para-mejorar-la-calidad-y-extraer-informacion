import spacy

AUX_RULES = {
    "did": "VB",
    "does": "VB",
    "do": "VB",
    "have": "VBN",
    "has": "VBN",
    "had": "VBN",
}



CONNECTORS = {
    "and",
    "then",
    "after"
}

PAST_MARKERS = {"yesterday", "ago"}
FUTURE_MARKERS = {"tomorrow"}


print("Loading spaCy...")

nlp = spacy.load("en_core_web_md")








def detect_aux_mismatch(text): # ESTA


    for i, token in enumerate(text):

        if token.pos_ == "AUX":

            if token.text.lower() in AUX_RULES:
                #
                expected_tag = AUX_RULES[token.text.lower()]

                # Buscar el siguiente verbo
                for next_token in text[i+1:]:

                    if next_token.pos_ == "VERB":

                        if next_token.tag_ != expected_tag:
                            return "aux_missmatch"

                        break

    return None

    




def detect_subject_verb_mismatch(text): # ESTÁ
   

    subject = None
    verb = None

    for token in text:

        if token.dep_ == "nsubj":
            subject = token

        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            verb = token

    if not subject or not verb:
        return None

    subject_text = subject.text.lower()

    if subject_text in ["he", "she", "it"]:
        if verb.tag_ == "VBP":
            return "subject_verb_mismatch"

    if subject_text in ["they", "we", "you"]:
        if verb.tag_ == "VBZ":
            return "subject_verb_mismatch"

    return None





def detect_tense_mismatch(text): # está

    past_count = 0
    present_count = 0

    for token in text:

        if token.pos_ != "VERB":
            continue

        if token.tag_ == "VBD":
            past_count += 1

        elif token.tag_ in ["VB", "VBP", "VBZ"]:
            present_count += 1

    if min(past_count, present_count) == 1 and max(past_count, present_count) >= 2:
        return "anomaly_missmatch"

    return None




def detect_connector_mismatch(text):    # está
   

    for i, token in enumerate(text):

        if token.text.lower() not in CONNECTORS:
            continue

        left_verb = None
        right_verb = None

        # buscar verbo a la izquierda
        for j in range(i - 1, -1, -1):
            if text[j].pos_ == "VERB":
                left_verb = text[j]
                break

        # buscar verbo a la derecha
        for j in range(i + 1, len(text)):
            if text[j].pos_ == "VERB":
                right_verb = text[j]
                break

        if not left_verb or not right_verb:
            continue

        left_past = left_verb.tag_ == "VBD"
        right_past = right_verb.tag_ == "VBD"

        left_present = left_verb.tag_ in ["VB", "VBP", "VBZ"]
        right_present = right_verb.tag_ in ["VB", "VBP", "VBZ"]

        if (left_past and right_present) or (left_present and right_past):
            return "connector_missmatch"

    return None





def detect_temporal_mismatch(text):
 

    has_past_marker = False
    has_future_marker = False

    root_verb = None

    for token in text:

        word = token.text.lower()

        if word in PAST_MARKERS:
            has_past_marker = True

        elif word in FUTURE_MARKERS:
            has_future_marker = True

        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            root_verb = token

    if root_verb is None:
        return None

    # yesterday / ago
    if has_past_marker:

        if root_verb.tag_ in ["VB", "VBP", "VBZ"]:
            return "temporal_missmatch"

    # tomorrow
    if has_future_marker:

        if root_verb.tag_ == "VBD":
            return "temporal_missmatch"

    return None



