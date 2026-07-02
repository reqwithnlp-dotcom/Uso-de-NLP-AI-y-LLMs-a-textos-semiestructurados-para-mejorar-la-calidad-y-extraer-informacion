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
    ("will","have","been","VBG"):"cont_perf_fut-fut",
    ("will","have","VBN"):"perf_fut-fut",
    ("will","be","VBG"):"cont_fut-fut",
    ("will","VB"):"simp_fut-fut",
    ("has","been","VBG"):"cont_perf_pres-pres",
    ("have","been","VBG"):"cont_perf_pres-pres",
    ("have","VBN"):"perf_pres-pres",
    ("has","VBN"):"perf_pres-pres",
    ("had","been","VBG"):"cont_perf_past-past",
    ("had","VBN"):"perf_past-past",
    ("was","VBG"):"cont_past-past",
    ("were","VBG"):"cont_past-past",
    ("am", "VBG"):"cont_pres-pres",
    ("are" , "VBG"):"cont_pres-pres",
    ("is", "VBG"):"cont_pres-pres",
    ("VBP",):"simp_pres-pres",
    ("VBZ",):"simp_pres-pres",
    ("VBD",):"simp_past-past",
}
REFERENCE_PAST_POINT =["yesterday","previous","last","former","past","preceding","prior"] 
REFERENCE_FUTURE_POINT = ["tomorrow","next","following","upcoming","coming","future","subsequent"]



CONNECTORS = {
    "and",
    "then",
    "after"
}


print("Loading spaCy...")

nlp = spacy.load("en_core_web_md")

def detect_aux_mismatch(text):
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
            temp_verb = TEMP_VERB_RULES.get(aux_tuple)
            if temp_verb != None:
                verb_times.append(f"{token.i}, {token.text}, {temp_verb}")
            else:
                verb_times.append(f"{token.i}, {token.text}, aux_mismatch")
            
            aux_list.clear()
    return verb_times

def detect_advb_mismatch():
    text = nlp("She has been studying a lot over the last week.") # sacar y colocar el text en parametro para prod
    all_temporality_list = detect_aux_mismatch(text) # sacar y colocar el temp_list en parametro para prod
    mismatch_list = []
    
    for i in range(len(text) - 1):  
        actual_word = text[i].text.strip().lower()
        is_adverb_past = actual_word in REFERENCE_PAST_POINT
        is_adverb_future = actual_word in REFERENCE_FUTURE_POINT
        if is_adverb_future or is_adverb_past:
            temporality = ""
            specific_temporality = ""
            head = text[i].head #obtenemos la dependencia padre.
            if head.pos_ != "VERB": #si el padre no es un verbo, 
                head = head.head    
            if head.pos_ == "VERB": #entonces buscamos al padre del padre ej: the last week was ....
                index_head = head.i # last pertenece a week y week a was
            else:
                continue

            for v in all_temporality_list:
                index_list = int(v[0])
                if index_list == index_head:#si coincide el indice del padre con el de la lista de temporalidades
                    temporality = v.split("-")[1] #obtenemos la temporalidad general que esta despues del guion
                    specific_temporality =  v.split(",")[2].strip().split("-")[0] # obtenemos de paso la especifica para casos de futuro

            past_not_ok = is_adverb_past and temporality != "past"
            future_not_ok = is_adverb_future and (specific_temporality == "cont_pres" or temporality != "fut") 
            if (past_not_ok) or (future_not_ok) :
                mismatch_list.append(f"{head.text} with {actual_word} -> advb_mismatch")
                continue
    print(mismatch_list)


detect_advb_mismatch()


def test_tokenization():
    text = nlp("She has been studying a lot over the last week")
    for token in text:
        print(f"{token.i} {token.text} {token.pos_} {token.tag_} {token.dep_} -HEAD- {token.head}")


#test_tokenization()

















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



