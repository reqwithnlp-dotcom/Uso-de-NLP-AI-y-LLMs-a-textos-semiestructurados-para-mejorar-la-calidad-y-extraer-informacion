"""
Tests para el detector de doble negación.

Utiliza pytest con parametrize para cubrir los ejemplos de la tabla
de casos de prueba definidos en la investigación.
"""

import sys
import os
import pytest

# Agregar el directorio padre al path para importar main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from servicio import detect_double_negation



# Casos de prueba parametrizados
# Cada tupla contiene: (id, oración, resultado_esperado)

CASOS_DOBLE_NEGACION = [
    # --- Casos que SÍ son doble negación (True) ---
    pytest.param(
        "I don't think she won't come.",
        True,
        id="01_dont_wont_doble_neg_gramatical",
    ),
    pytest.param(
        "It's impossible that no one arrives on time.",
        True,
        id="02_impossible_no_one_neg_lexica_y_pronombre",
    ),
    pytest.param(
        "It's not impossible that she will come.",
        True,
        id="06_not_impossible_neg_con_prefijo",
    ),
    # --- Casos que NO son doble negación (False) ---
    pytest.param(
        "No one said it would be easy.",
        False,
        id="03_no_one_negacion_simple",
    ),
    pytest.param(
        "She never said anything.",
        False,
        id="04_never_negacion_simple",
    ),
    pytest.param(
        "I didn't see anyone.",
        False,
        id="05_didnt_negacion_simple",
    ),
]


# =============================================================================
# Test parametrizado principal
# =============================================================================

@pytest.mark.parametrize("oracion, esperado", CASOS_DOBLE_NEGACION)
def test_detect_double_negation(oracion: str, esperado: bool):
    """Verifica que detect_double_negation retorne el resultado esperado."""
    resultado = detect_double_negation(oracion)
    assert resultado == esperado, (
        f"\nOración:   '{oracion}'"
        f"\nEsperado:  {esperado}"
        f"\nObtenido:  {resultado}"
    )
