import spacy
from src.diccionario import ADVERB_CATEGORIES
from spacy.language import Language

#fuerza a las palabras que Spacy etiqueta de otro tipo (por ej: NOUN) a ser ADV
@Language.component("custom_adverb_fixer")
def custom_adverb_fixer(doc):
    for token in doc: 
        lemma = token.lemma_.lower()
        palabra_critica = any(lemma in lista for lista in ADVERB_CATEGORIES.values())
        if  palabra_critica:
            if token.dep_ == "nsubj":
                continue
            token.pos_ = "ADV"
    return doc

class AdverbDetector:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("custom_adverb_fixer", last=True)

    def _classify_adverb(self, token) -> str:
        lemma = token.lemma_.lower()
        text = token.text.lower()

        for category, lemas in ADVERB_CATEGORIES.items():
            if lemma in lemas:
                return category

        if text.endswith("ly") and token.pos_ == "ADV":
            return "Manner"
 
        return "Other"

    def analyze_sentence(self, sentence: str) -> list:
        doc = self.nlp(sentence)
        results = []
    
        for token in doc:
            if token.pos_ == "ADV":
                category = self._classify_adverb(token)
                results.append([token.text, category])
        return results