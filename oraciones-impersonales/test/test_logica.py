"""
Tests de lógica pura: NO requieren el modelo de spaCy.

Validan la integridad de los lexicones, el orden del pipeline de
reglas y el contrato de la capa model.
"""

from model import lexicons
from model.rules import RULES, DEFAULT_TYPE
from model.rules import (
    rule_there_existential,
    rule_weather_it,
    rule_weather_adjective,
    rule_impersonal_passive,
    rule_it_extraposition,
)


class TestLexicons:
    def test_weather_verbs_son_lemas_en_minuscula(self):
        assert all(v == v.lower() for v in lexicons.WEATHER_VERBS)
        assert "rain" in lexicons.WEATHER_VERBS
        assert "snow" in lexicons.WEATHER_VERBS

    def test_weather_adjectives_basicos_presentes(self):
        for adj in ("cold", "hot", "sunny", "foggy"):
            assert adj in lexicons.WEATHER_ADJECTIVES

    def test_reporting_verbs_basicos_presentes(self):
        for v in ("say", "believe", "know", "report"):
            assert v in lexicons.REPORTING_VERBS

    def test_copular_incluye_be_y_seem(self):
        assert "be" in lexicons.COPULAR_VERBS
        assert "seem" in lexicons.COPULAR_VERBS

    def test_lexicones_inmutables(self):
        # frozenset evita mutaciones accidentales desde otra capa
        assert isinstance(lexicons.WEATHER_VERBS, frozenset)
        assert isinstance(lexicons.WEATHER_ADJECTIVES, frozenset)

    def test_sin_solapamiento_verbos_clima_y_reporte(self):
        assert not lexicons.WEATHER_VERBS & lexicons.REPORTING_VERBS


class TestPipelineOrder:
    def test_orden_de_reglas_especifica_a_general(self):
        """El orden es parte del contrato: corte temprano correcto."""
        assert RULES == (
            rule_there_existential,
            rule_weather_it,
            rule_weather_adjective,
            rule_impersonal_passive,
            rule_it_extraposition,
        )

    def test_default_conservador_es_personal(self):
        assert DEFAULT_TYPE == "PERSONAL"

    def test_hay_cinco_reglas(self):
        assert len(RULES) == 5
