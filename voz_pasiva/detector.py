import spacy

# Carga del modelo de inglés
nlp = spacy.load("en_core_web_sm")

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

def to_active_voice(sentence: str) -> str:
    """
    Convierte una oración en voz pasiva en inglés a voz activa.
    Si no es pasiva o no cuenta con la estructura clara (ej. falta el sujeto 'by ...'),
    retorna la oración original o una versión adaptada.
    """
    doc = nlp(sentence)
    
    if not is_passive(sentence):
        return sentence

    passive_subj = None
    verb = None
    agent = None
    auxpass = None

    # Recorremos los tokens para identificar los componentes principales
    for token in doc:
        if token.dep_ in ("nsubjpass", "nsubj"):
            passive_subj = token
        elif token.dep_ == "auxpass":
            auxpass = token
            verb = token.head
        elif token.dep_ == "agent":
            # El agente suele ser la preposición 'by'
            for child in token.children:
                if child.dep_ == "pobj":
                    agent = child

    # Si falta el agente 'by ...' (ej. "The letter was written"), asignamos un sujeto genérico ("Someone")
    agent_text = agent.text if agent else "Someone"
    
    if verb and passive_subj:
        # Determinar el tiempo verbal básico basándonos en el auxiliar pasivo (is/was/will be, etc.)
        lemma_verb = verb.lemma_
        
        # Ajuste de conjugación según el verbo auxiliar pasivo principal
        if auxpass and auxpass.text.lower() in ["was", "were"]:
            # Pasado simple
            active_verb = verb.lemma_ + "d" if not verb.lemma_.endswith("e") else verb.lemma_ + "d"
            # Manejo básico de verbos irregulares comunes
            irregular_past = {
                "write": "wrote", "build": "built", "make": "made",
                "take": "took", "eat": "ate", "see": "saw", "give": "gave"
            }
            active_verb = irregular_past.get(lemma_verb, active_verb)
        elif auxpass and auxpass.text.lower() in ["is", "are", "am"]:
            # Presente simple
            active_verb = lemma_verb if agent_text.lower() in ["they", "we", "you"] else lemma_verb + "s"
        else:
            active_verb = lemma_verb

        # Extraer el objeto (sujeto pasivo) ajustando mayúsculas/minúsculas
        obj_text = passive_subj.text
        if obj_text.isupper() or obj_text.istitle():
            obj_text = obj_text.lower()

        # Dar formato de mayúscula inicial al nuevo sujeto
        agent_formatted = agent_text.capitalize()

        # Reconstruir la oración
        return f"{agent_formatted} {active_verb} {obj_text}."

    return sentence

