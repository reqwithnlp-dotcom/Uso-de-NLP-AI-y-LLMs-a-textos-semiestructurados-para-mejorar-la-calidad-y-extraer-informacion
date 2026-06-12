import spacy
import textdescriptives as td

from Tests.test_gunning_extendido import casosPrueba
from model.gunningExtendido import calcularGunningExtendido


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textdescriptives/readability")


def analizar_texto(cuerpo: str, penalizacion):
    doc = nlp(cuerpo)

    return calcularGunningExtendido(
        doc=doc,
        penalizacion=penalizacion
    )


def imprimir_comparacion(nombre: str, resultado_sin: dict, resultado_con: dict):
    print("\n" + "=" * 80)
    print(nombre)
    print("=" * 80)

    print("\n--- Texto sin aposiciones ---")
    print(f"Gunning Fog tradicional: {resultado_sin['gunning_fog']}")
    print(f"Gunning Fog extendido:   {resultado_sin['score']}")
    print(f"Penalización por comas:  {resultado_sin['comma_penalty']}")
    print(f"Comas por oración:       {resultado_sin['commas_per_sentence']}")
    print(f"Palabras por oración:    {resultado_sin['words_per_sentence']}")

    print("\n--- Texto con aposiciones ---")
    print(f"Gunning Fog tradicional: {resultado_con['gunning_fog']}")
    print(f"Gunning Fog extendido:   {resultado_con['score']}")
    print(f"Penalización por comas:  {resultado_con['comma_penalty']}")
    print(f"Comas por oración:       {resultado_con['commas_per_sentence']}")
    print(f"Palabras por oración:    {resultado_con['words_per_sentence']}")

    print("\n--- Diferencias ---")
    print(f"Diferencia Gunning Fog tradicional: {round(resultado_con['gunning_fog'] - resultado_sin['gunning_fog'], 2)}")
    print(f"Diferencia Gunning Fog extendido:   {round(resultado_con['score'] - resultado_sin['score'], 2)}")
    print(f"Alpha usado:                        {resultado_con['alpha']}")


def ejecutar_lote_pruebas():
    for caso in casosPrueba:
        resultado_sin = analizar_texto(
            cuerpo=caso["sin_aposiciones"],
            penalizacion=caso["penalizacion"]
        )

        resultado_con = analizar_texto(
            cuerpo=caso["con_aposiciones"],
            penalizacion=caso["penalizacion"]
        )

        imprimir_comparacion(
            nombre=caso["nombre"],
            resultado_sin=resultado_sin,
            resultado_con=resultado_con
        )


if __name__ == "__main__":
    ejecutar_lote_pruebas()