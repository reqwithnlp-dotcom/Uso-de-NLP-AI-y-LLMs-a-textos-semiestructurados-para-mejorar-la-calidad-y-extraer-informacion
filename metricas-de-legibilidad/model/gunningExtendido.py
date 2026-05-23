
from spacy.tokens import Doc
from model.PenalizacionPorComa import PenalizacionPorComa


def calcularGunningExtendido (doc: Doc, penalizacion: PenalizacionPorComa)-> dict:
    sentences = list(doc.sents)
    word =[token for token in doc if token.is_alpha]
    comas =[token for token in doc if token.text == ","]

    sentencesCount = len(sentences)
    wordsCount = len(word)
    commasCount = len(comas)

    if sentencesCount == 0 or wordsCount == 0:
        return {
            "score": 0,
            "gunning_fog": 0,
            "comma_penalty": 0,
            "commas_per_sentence": 0,
            "words_per_sentence": 0,
            "alpha": penalizacion.alpha
        }

    wordsPerSentence = wordsCount / sentencesCount
    commasPerSentence = commasCount / sentencesCount

    gunning_fog = doc._.readability["gunning_fog"]
    comma_penalty = penalizacion.alpha*(commasPerSentence* wordsPerSentence)
    extended_score = gunning_fog + comma_penalty

    return {"score": round(extended_score, 2),
            "gunning_fog": round(gunning_fog, 2),
            "comma_penalty": round(comma_penalty, 2),
            "commas_per_sentence": round(commasPerSentence, 2),
            "words_per_sentence": round(wordsPerSentence, 2),
            "alpha": penalizacion.alpha}

