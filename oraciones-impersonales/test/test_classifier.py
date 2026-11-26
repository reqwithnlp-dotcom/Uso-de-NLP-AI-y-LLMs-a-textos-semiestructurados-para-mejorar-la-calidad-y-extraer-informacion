"""
Tests de la capa 2 (model/classifier.py) y de su integración con el detector.

- decide(): lógica pura, sin modelo.
- Carga: sin modelo en disco, classify() devuelve None.
- Integración: con classify() mockeado, se verifica que la capa 2 SOLO se
  consulta para las oraciones ambiguas de la capa 1.
- Sanity check con el modelo real: se saltea si no hay uno entrenado.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from model import classifier
from test.conftest import requires_model


# ---------------------------------------------------------------------------
# decide()
# ---------------------------------------------------------------------------
class TestDecide:
    def test_impersonal_claro(self):
        assert classifier.decide({"PERSONAL": 0.1, "IMPERSONAL": 0.9}, 0.5, 0.2) == "IMPERSONAL"

    def test_personal_claro(self):
        assert classifier.decide({"PERSONAL": 0.8, "IMPERSONAL": 0.3}, 0.5, 0.2) == "PERSONAL"

    def test_ambos_altos_es_undecided(self):
        # Contradictorio: los dos superan el umbral pero sin margen
        assert classifier.decide({"PERSONAL": 0.85, "IMPERSONAL": 0.8}, 0.5, 0.2) == "UNDECIDED"

    def test_ambos_bajos_es_undecided(self):
        # Sin evidencia: ninguno llega al umbral
        assert classifier.decide({"PERSONAL": 0.3, "IMPERSONAL": 0.1}, 0.5, 0.1) == "UNDECIDED"

    def test_margen_justo_alcanza(self):
        assert classifier.decide({"PERSONAL": 0.4, "IMPERSONAL": 0.6}, 0.5, 0.2) == "IMPERSONAL"

    def test_scores_none_es_undecided(self):
        assert classifier.decide(None) == "UNDECIDED"

    def test_umbral_por_variable_de_entorno(self, monkeypatch):
        monkeypatch.setenv("IMPERSONAL_L2_THRESHOLD", "0.95")
        monkeypatch.setenv("IMPERSONAL_L2_MARGIN", "0.0")
        assert classifier.decide({"PERSONAL": 0.1, "IMPERSONAL": 0.9}) == "UNDECIDED"

    def test_variable_de_entorno_invalida_usa_default(self, monkeypatch):
        monkeypatch.setenv("IMPERSONAL_L2_THRESHOLD", "abc")
        assert classifier.decide({"PERSONAL": 0.1, "IMPERSONAL": 0.9}) == "IMPERSONAL"


# ---------------------------------------------------------------------------
# Carga del modelo
# ---------------------------------------------------------------------------
class TestCarga:
    def test_sin_modelo_classify_devuelve_none(self):
        # conftest apunta IMPERSONAL_TEXTCAT_PATH a una carpeta inexistente
        assert classifier.is_loaded() is False
        assert classifier.classify("It is fast.") is None

    def test_no_reintenta_cargar_en_cada_llamada(self):
        with patch.object(classifier, "model_path") as mp:
            mp.return_value = Path("no/existe")
            classifier.classify("a")
            classifier.classify("b")
            assert mp.call_count == 1


# ---------------------------------------------------------------------------
# Integración con el detector (capa 1 -> capa 2)
# ---------------------------------------------------------------------------
@requires_model
class TestIntegracionDetector:
    def _first(self, text):
        from model.detector import analyze_text
        return analyze_text(text)[0]

    def test_caso_claro_no_consulta_capa2(self):
        with patch.object(classifier, "classify") as cl:
            r = self._first("There are many factors to consider.")
        cl.assert_not_called()
        assert r["ambiguous"] is False
        assert r["final_label"] == "IMPERSONAL"
        assert r["decided_by"] == "layer1"
        assert r["layer2_scores"] is None

    def test_caso_personal_claro(self):
        r = self._first("I bought a car.")
        assert r["final_label"] == "PERSONAL"
        assert r["decided_by"] == "layer1"

    def test_ambigua_consulta_capa2(self):
        scores = {"PERSONAL": 0.9, "IMPERSONAL": 0.05}
        with patch.object(classifier, "classify", return_value=scores) as cl:
            r = self._first("It is fast.")
        assert r["ambiguous"] is True
        cl.assert_called_once_with("It is fast.")
        assert r["final_label"] == "PERSONAL"
        assert r["decided_by"] == "layer2"
        assert r["layer2_scores"] == scores

    def test_ambigua_capa2_indecisa(self):
        with patch.object(classifier, "classify",
                          return_value={"PERSONAL": 0.55, "IMPERSONAL": 0.5}):
            r = self._first("It is fast.")
        assert r["final_label"] == "UNDECIDED"
        assert r["decided_by"] == "none"

    def test_ambigua_sin_modelo(self):
        r = self._first("It is fast.")
        assert r["ambiguous"] is True
        assert r["final_label"] == "UNDECIDED"
        assert r["decided_by"] == "none"
        assert r["layer2_scores"] is None

    def test_campos_capa1_intactos(self):
        r = self._first("It rains a lot.")
        assert r["type"] == "WEATHER_IT"
        assert r["impersonal"] is True


# ---------------------------------------------------------------------------
# Sanity check con el modelo entrenado real (si existe)
# ---------------------------------------------------------------------------
_REAL_MODEL = Path(os.environ.get("IMPERSONAL_TEXTCAT_REAL",
                                  Path(classifier.__file__).parent / "textcat"))


@pytest.mark.skipif(not (_REAL_MODEL / "config.cfg").exists(),
                    reason=f"No hay modelo de capa 2 entrenado en {_REAL_MODEL}")
class TestModeloReal:
    @pytest.fixture(autouse=True)
    def _usar_modelo_real(self, monkeypatch):
        monkeypatch.setenv("IMPERSONAL_TEXTCAT_PATH", str(_REAL_MODEL))
        classifier.reset()

    def test_scores_bien_formados(self):
        s = classifier.classify("It is important to remember the guidelines.")
        assert set(s) == {"PERSONAL", "IMPERSONAL"}
        assert all(0.0 <= v <= 1.0 for v in s.values())

    def test_extraposicion_mas_impersonal_que_referencial(self):
        imp = classifier.classify("It is important to remember the guidelines.")
        per = classifier.classify("I bought a car yesterday.")
        assert imp["IMPERSONAL"] > per["IMPERSONAL"]
        assert per["PERSONAL"] > imp["PERSONAL"]
