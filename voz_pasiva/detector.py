import spacy

# Carga del modelo de inglés
nlp = spacy.load("en_core_web_sm")

IRREGULAR_PAST = {
    "write": "wrote", "build": "built", "make": "made", "take": "took",
    "eat": "ate", "see": "saw", "give": "gave", "break": "broke",
    "choose": "chose", "know": "knew", "grow": "grew", "draw": "drew",
    "drive": "drove", "ride": "rode", "rise": "rose", "hide": "hid",
    "bite": "bit", "forget": "forgot", "freeze": "froze", "steal": "stole",
    "shake": "shook", "fall": "fell", "begin": "began", "swim": "swam",
    "sing": "sang", "run": "ran", "come": "came", "become": "became",
    "find": "found", "keep": "kept", "leave": "left", "send": "sent",
    "spend": "spent", "feel": "felt", "meet": "met", "bring": "brought",
    "buy": "bought", "catch": "caught", "fight": "fought", "teach": "taught",
    "think": "thought", "tell": "told", "sell": "sold", "read": "read",
    "hear": "heard", "lose": "lost", "pay": "paid", "understand": "understood",
    "speak": "spoke", "wear": "wore", "win": "won", "cut": "cut", "put": "put",
    "hit": "hit", "let": "let", "set": "set", "shut": "shut", "do": "did"
}

PRONOUN_OBJ_TO_SUBJ = {
    "me": "I", "him": "he", "her": "she", "us": "we", "them": "they"
}
PRONOUN_SUBJ_TO_OBJ = {
    "i": "me", "he": "him", "she": "her", "we": "us", "they": "them"
}

def is_passive(sentence: str) -> bool:
    doc = nlp(sentence)
    return any(token.dep_ == "auxpass" for token in doc)

def passive_positions(sentence: str):
    doc = nlp(sentence)
    positions = []
    for token in doc:
        if token.dep_ == "auxpass":
            start = token.idx
            end = token.idx + len(token.text)
            head = token.head
            if head.tag_ == "VBN":
                end = max(end, head.idx + len(head.text))
            positions.append((start, end))
    return positions

def _convert_single_sentence(sent) -> str:
    passive_subj = None
    verb = None
    agent = None
    agent_by = None
    auxpass = None
    aux_modal = None

    for token in sent:
        if token.dep_ == "auxpass":
            auxpass = token
            verb = token.head
        elif token.dep_ == "aux" and token.tag_ == "MD":
            aux_modal = token

    if not auxpass or not verb:
        return sent.text.strip()

    for token in sent:
        if token.dep_ in ("nsubjpass", "nsubj") and token.head == verb:
            passive_subj = token
        elif token.dep_ == "agent" and token.head == verb:
            agent_by = token
            for child in token.children:
                if child.dep_ == "pobj":
                    agent = child

    # Determinar agente (nuevo sujeto)
    if agent:
        agent_tokens = [t for t in agent.subtree if t.pos_ != "PUNCT"]
        agent_tokens.sort(key=lambda t: t.i)
        agent_text = " ".join(t.text for t in agent_tokens)
        agent_words = agent_text.split()
        if len(agent_words) == 1 and agent_words[0].lower() in PRONOUN_OBJ_TO_SUBJ:
            agent_text = PRONOUN_OBJ_TO_SUBJ[agent_words[0].lower()]
    else:
        agent_text = "Someone"

    # Determinar objeto (sujeto pasivo previo)
    if passive_subj:
        subj_tokens = [t for t in passive_subj.subtree if t.pos_ != "PUNCT"]
        subj_tokens.sort(key=lambda t: t.i)
        obj_text = " ".join(t.text for t in subj_tokens)
        obj_words = obj_text.split()
        if len(obj_words) == 1 and obj_words[0].lower() in PRONOUN_SUBJ_TO_OBJ:
            obj_text = PRONOUN_SUBJ_TO_OBJ[obj_words[0].lower()]
        elif obj_words and obj_words[0].lower() in ("the", "a", "an", "this", "that", "these", "those", "my", "your", "his", "her", "our", "their"):
            obj_words[0] = obj_words[0].lower()
            obj_text = " ".join(obj_words)
    else:
        obj_text = ""

    # Determinar conjugación verbal activa
    lemma = verb.lemma_.lower()
    aux_text = auxpass.text.lower()
    
    if aux_modal:
        active_verb = f"{aux_modal.text.lower()} {lemma}"
    elif aux_text in ("was", "were"):
        if lemma in IRREGULAR_PAST:
            active_verb = IRREGULAR_PAST[lemma]
        elif verb.tag_ == "VBN" and verb.text.lower().endswith(("ed", "d")):
            active_verb = verb.text.lower()
        else:
            active_verb = lemma + ("d" if lemma.endswith("e") else "ed")
    elif aux_text in ("is", "are", "am"):
        is_plural = any(w.lower() in ("they", "we", "you", "people", "children") for w in agent_text.split()) or (agent and agent.tag_ in ("NNS", "NNPS"))
        if agent_text.lower() == "someone" or not is_plural:
            if lemma.endswith(("s", "sh", "ch", "x", "z", "o")):
                active_verb = lemma + "es"
            elif lemma.endswith("y") and len(lemma) > 1 and lemma[-2] not in "aeiou":
                active_verb = lemma[:-1] + "ies"
            else:
                active_verb = lemma + "s"
        else:
            active_verb = lemma
    else:
        active_verb = lemma

    # Tokens excluidos de la cláusula
    excluded = {verb, auxpass}
    if aux_modal:
        excluded.add(aux_modal)
    if passive_subj:
        excluded.update(passive_subj.subtree)
    if agent_by:
        excluded.update(agent_by.subtree)

    # Identificar modificadores introductorios vs posteriores
    subj_start_i = min(t.i for t in passive_subj.subtree) if passive_subj else verb.i
    lead_tokens = [t for t in sent if t.i < subj_start_i and t not in excluded and (t.pos_ != "PUNCT" or t.text == ",")]
    trail_tokens = [t for t in sent if t.i >= subj_start_i and t not in excluded and t.pos_ != "PUNCT"]

    lead_text = ""
    if lead_tokens:
        lead_str = ""
        for t in lead_tokens:
            if t.text == ",":
                lead_str = lead_str.rstrip() + ", "
            else:
                lead_str += t.text + " "
        lead_text = lead_str.strip()

    trail_tokens.sort(key=lambda t: t.i)
    trail_text = " ".join(t.text for t in trail_tokens)

    # Ajustar mayúscula inicial del nuevo sujeto
    if lead_text:
        if agent_text and agent_text[0].isupper() and agent and agent.tag_ not in ("NNP", "NNPS"):
            agent_text = agent_text[0].lower() + agent_text[1:]
    else:
        if agent_text:
            agent_text = agent_text[0].upper() + agent_text[1:]

    # Reconstruir la oración
    parts = []
    if lead_text:
        parts.append(lead_text)
    parts.append(agent_text)
    parts.append(active_verb)
    if obj_text:
        parts.append(obj_text)
    if trail_text:
        parts.append(trail_text)

    punct = "."
    for t in reversed(list(sent)):
        if t.pos_ == "PUNCT" and t.text in (".", "!", "?"):
            punct = t.text
            break

    result = " ".join(parts).strip().replace(" ,", ",")
    if not result.endswith(punct):
        result += punct
    return result

def to_active_voice(sentence: str) -> str:
    """
    Convierte una oración o texto con oraciones en voz pasiva en inglés a voz activa.
    Si no es pasiva o no cuenta con la estructura clara, retorna la oración original.
    """
    if not is_passive(sentence):
        return sentence

    doc = nlp(sentence)
    converted_sents = []
    for sent in doc.sents:
        if any(t.dep_ == "auxpass" for t in sent):
            converted_sents.append(_convert_single_sentence(sent))
        else:
            converted_sents.append(sent.text.strip())

    return " ".join(converted_sents)

