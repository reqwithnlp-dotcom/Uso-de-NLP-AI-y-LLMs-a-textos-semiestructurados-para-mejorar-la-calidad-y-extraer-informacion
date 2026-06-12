import sys
import os
import urllib.request
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from Tests.test_gunning_extendido import casosPrueba

API_URL = "http://127.0.0.1:8000/analizar"


def analizar(texto: str, penalizacion: str) -> dict:
    payload = json.dumps({"texto": texto.strip(), "penalizacion": penalizacion}).encode()
    req = urllib.request.Request(API_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def imprimir_resultado(label: str, r: dict):
    print(f"  {label:<25} score={r['score']:>6.2f}  "
          f"gunning={r['gunning_fog']:>5.2f}  "
          f"penalizacion={r['comma_penalty']:>5.2f}  "
          f"ratio_comas={r['comma_ratio']:>6.4f}")


def main():
    print("=" * 75)
    print("LOTE DE PRUEBAS - Gunning Fog Extendido via FastAPI")
    print("=" * 75)

    for caso in casosPrueba:
        nombre = caso["nombre"]
        pen = caso["penalizacion"]
        print(f"\n[{nombre}]  penalizacion={pen}  alpha={pen.alpha}")
        print("-" * 75)

        r_sin = analizar(caso["sin_aposiciones"], pen)
        r_con = analizar(caso["con_aposiciones"], pen)

        imprimir_resultado("Sin aposiciones", r_sin)
        imprimir_resultado("Con aposiciones", r_con)

        delta = round(r_con["score"] - r_sin["score"], 2)
        signo = "+" if delta >= 0 else ""
        tendencia = "mas dificil" if delta > 0 else "mas facil" if delta < 0 else "sin cambio"
        print(f"  {'Variacion score':<25} {signo}{delta:>6.2f}  ({tendencia})")

    print("\n" + "=" * 75)
    print("Fin del lote")
    print("=" * 75)


if __name__ == "__main__":
    main()
