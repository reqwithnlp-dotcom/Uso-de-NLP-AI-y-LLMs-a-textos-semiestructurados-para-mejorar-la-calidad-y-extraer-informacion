import spacy
from diccionario_negacion import PALABRAS_NEGATIVAS, PREFIJOS_NEGATIVOS

nlp = spacy.load("en_core_web_trf")


def _es_semanticamente_negativo(token) -> bool:
    return (
        token.lower_ in PALABRAS_NEGATIVAS
        or token.lower_.startswith(PREFIJOS_NEGATIVOS)
    )


def _contar_negaciones(token) -> int:
  
    count = 0

    if _es_semanticamente_negativo(token):
        count += 1

    for hijo in token.children:
        if hijo.dep_ == "neg":
            count += 1
        else:
            count += _contar_negaciones(hijo)

        if count >= 2:
            return count

    return count


def detect_double_negation(text: str) -> bool:

    doc = nlp(text)

    for sent in doc.sents:
        if _contar_negaciones(sent.root) >= 2:
            return True

    return False