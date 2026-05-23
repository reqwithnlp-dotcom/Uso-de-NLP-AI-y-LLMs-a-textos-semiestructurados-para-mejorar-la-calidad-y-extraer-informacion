import spacy
import textdescriptives as td
from Tests.test_gunning_extendido import casosPrueba

from model.gunningExtendido import calcularGunningExtendido

nlp= spacy.load('en_core_web_sm')
nlp.add_pipe("textdescriptives/readability")

def analizar_texto(nombre: str, cuerpo: str, penalizacion):
    doc = nlp(cuerpo)

    resultado = calcularGunningExtendido(
        doc=doc,
        penalizacion=penalizacion
    )

    print("\n" + "=" * 80)
    print(nombre)
    print("=" * 80)
    print(f"Gunning Fog tradicional: {resultado['gunning_fog']}")
    print(f"Gunning Fog extendido:   {resultado['score']}")
    print(f"Penalización por comas:  {resultado['comma_penalty']}")
    print(f"Comas por oración:       {resultado['commas_per_sentence']}")
    print(f"Palabras por oración:    {resultado['words_per_sentence']}")
    print(f"Alpha usado:             {resultado['alpha']}")


def ejecutar_lote_pruebas():
    for caso in casosPrueba:
        analizar_texto(
            nombre=caso["nombre"],
            cuerpo=caso["cuerpo"],
            penalizacion=caso["penalizacion"]
        )


if __name__ == "__main__":
    ejecutar_lote_pruebas()