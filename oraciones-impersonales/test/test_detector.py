"""
Tests de integración del detector: requieren en_core_web_sm.

Si el modelo no está instalado se saltean automáticamente (ver
conftest.py). Cubren los cinco tipos impersonales, el caso de
control personal, casos de borde y trampas conocidas.
"""

import pytest
from test.conftest import requires_model


pytestmark = requires_model


def _analyze(text):
    from model.detector import analyze_text
    return analyze_text(text)


def _first(text):
    return _analyze(text)[0]


# ---------------------------------------------------------------------------
# Casos del documento de especificación (uno por tipo)
# ---------------------------------------------------------------------------
class TestCasosDelDocumento:
    def test_it_extraposition(self):
        r = _first("It is important to remember the guidelines.")
        assert r["impersonal"] is True
        assert r["type"] == "IT_EXTRAPOSITION"

    def test_there_existential(self):
        r = _first("There are many factors to consider.")
        assert r["impersonal"] is True
        assert r["type"] == "THERE_EXISTENTIAL"

    def test_weather_it(self):
        r = _first("It rains a lot.")
        assert r["impersonal"] is True
        assert r["type"] == "WEATHER_IT"

    def test_weather_adjective(self):
        r = _first("It is cold today.")
        assert r["impersonal"] is True
        assert r["type"] == "WEATHER_ADJECTIVE"

    def test_impersonal_passive(self):
        r = _first("It is said that history repeats itself.")
        assert r["impersonal"] is True
        assert r["type"] == "IMPERSONAL_PASSIVE"

    def test_caso_control_personal(self):
        results = _analyze("I bought a car. It is fast.")
        assert results[0]["impersonal"] is False
        assert results[1]["impersonal"] is False
        assert results[1]["type"] == "PERSONAL"


# ---------------------------------------------------------------------------
# Variantes adicionales por tipo
# ---------------------------------------------------------------------------
class TestVariantes:
    @pytest.mark.parametrize("text", [
        "There is a problem with the server.",
        "There were several mistakes in the report.",
        "There has been an accident.",
    ])
    def test_there_variantes(self, text):
        r = _first(text)
        assert r["type"] == "THERE_EXISTENTIAL", r

    @pytest.mark.parametrize("text", [
        "It snowed all night.",
        "It was pouring yesterday.",
        "It never rains in this city.",
    ])
    def test_clima_verbal_variantes(self, text):
        r = _first(text)
        assert r["type"] == "WEATHER_IT", r

    @pytest.mark.parametrize("text", [
        "It was very hot yesterday.",
        "It is sunny in Buenos Aires.",
        "It gets dark early in winter.",
    ])
    def test_clima_adjetival_variantes(self, text):
        r = _first(text)
        assert r["impersonal"] is True, r

    @pytest.mark.parametrize("text", [
        "It is believed that the economy will improve.",
        "It was reported that the team won.",
        "It is known that smoking causes cancer.",
    ])
    def test_pasiva_impersonal_variantes(self, text):
        r = _first(text)
        assert r["type"] == "IMPERSONAL_PASSIVE", r

    @pytest.mark.parametrize("text", [
        "It seems that the results are wrong.",
        "It is necessary to check the data.",
        "It was difficult to understand the lecture.",
        "It appears that nobody noticed.",
    ])
    def test_extraposicion_variantes(self, text):
        r = _first(text)
        assert r["type"] == "IT_EXTRAPOSITION", r


# ---------------------------------------------------------------------------
# Trampas: oraciones que DEBEN dar False (control de falsos positivos)
# ---------------------------------------------------------------------------
class TestTrampas:
    @pytest.mark.parametrize("text", [
        "It is fast.",                      # it referencial + adjetivo sin cláusula
        "She said that he was late.",       # verbo de reporte con sujeto real
        "The weather is cold in my room.",  # adjetivo de clima con sujeto real
        "I live there.",                    # there locativo, no existencial
        "It belongs to my brother.",        # it referencial con verbo común
        "It runs smoothly on my laptop.",   # it referencial (programa/auto)
    ])
    def test_oraciones_personales(self, text):
        r = _first(text)
        assert r["impersonal"] is False, r


# ---------------------------------------------------------------------------
# Casos de borde de la API del modelo
# ---------------------------------------------------------------------------
class TestBordes:
    def test_texto_vacio(self):
        assert _analyze("") == []

    def test_solo_espacios(self):
        assert _analyze("   \n  ") == []

    def test_multiples_oraciones_mixtas(self):
        text = (
            "It is raining. I bought a car. "
            "There is a meeting tomorrow. It is fast."
        )
        results = _analyze(text)
        assert len(results) == 4
        flags = [r["impersonal"] for r in results]
        assert flags == [True, False, True, False]

    def test_estructura_del_resultado(self):
        r = _first("It rains.")
        assert set(r.keys()) == {"sentence", "impersonal", "type"}
        assert isinstance(r["impersonal"], bool)
