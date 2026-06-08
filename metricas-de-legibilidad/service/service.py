import spacy
import textdescriptives as td

from model.gunningExtendido import calcularGunningExtendido
from model.PenalizacionPorComa import PenalizacionPorComa


class ReadabilityService:

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")
        self._nlp.add_pipe("textdescriptives/readability")

    def analizar(self, texto: str, penalizacion: PenalizacionPorComa) -> dict:
        doc = self._nlp(texto)
        return calcularGunningExtendido(doc=doc, penalizacion=penalizacion)
