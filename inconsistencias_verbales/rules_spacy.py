import spacy
"""
VB	Verbo base	eat, go, study
VBD	Pasado simple	ate, went, studied
VBG	Gerundio / participio presente	eating, going, studying
VBN	Participio pasado	eaten, gone, studied
VBP	Presente (excepto 3ª persona singular)	I eat, they go
VBZ	Presente 3ª persona singular	she eats, he goes
"""


TEMP_VERB_RULES = {
    ("will","have","been","VBG"):"cont_perf_fut",
    ("will","have","VBN"):"perf_fut",
    ("will","be","VBG"):"cont_fut",
    ("will","VB"):"simp_fut",
    ("have" or "has","been","VBG"):"cont_perf_pres",
    ("have" or "has","VBN"):"perf_pres",
    ("had","been","VBG"):"cont_perf_past",
    ("had","VBN"):"perf_past",
    ("was","VBG"):"cont_past",
    ("were","VBG"):"cont_past",
    ("am" or "are" or "is", "VBG"):"cont_pres",
    ("are" , "VBG"):"cont_pres",
    ("is", "VBG"):"cont_pres",
    ("VB" or "VBP" or "VBZ",):"simp_pres",
    ("VBP",):"simp_pres",
    ("VBZ",):"simp_pres",
    ("VBD",):"simp_past",
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





"""
if token.text.lower() in AUX_RULES:
                #
                expected_tag = AUX_RULES[token.text.lower()]

                # Buscar el siguiente verbo
                for next_token in text[i+1:]:

                    if next_token.pos_ == "VERB":

                        if next_token.tag_ != expected_tag:
                            return "aux_missmatch"

                        break
"""





def detect_aux_mismatch():
    text = "By the time she arrived, I had been working for three hours, I have completed the report, and I will have been waiting for the manager for more than an hour before the meeting starts."
    doc = nlp(text)
    aux_list= []
    verb_times = []
    for token in doc:
        if token.text == "not":
            continue
        if token.pos_ == "AUX":
            aux_word = token.text.strip().lower()
            aux_list.append(aux_word)

        if token.pos_ == "VERB":
            aux_word = token.tag_
            aux_list.append(aux_word)    
            aux_tuple = tuple(aux_list)
            print(aux_tuple , type(aux_tuple))
            temp_verb = TEMP_VERB_RULES.get(aux_tuple)
            if temp_verb != None:
                verb_times.append(f"{token.text} -> {temp_verb}")
            else:
                verb_times.append(f"{token.text} -> aux_mismatch")
            
            aux_list.clear()
    for v in verb_times:
        print(v)
    return verb_times


detect_aux_mismatch()





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



