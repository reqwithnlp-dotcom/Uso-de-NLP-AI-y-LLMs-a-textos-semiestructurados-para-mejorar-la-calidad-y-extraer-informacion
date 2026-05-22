import pytest
from src.detector import AdverbDetector

@pytest.fixture
def detector():
    """Fixture para inicializar el servicio antes de cada test."""
    return AdverbDetector()

def test_oracion_1_tomorrow(detector):
    resultado = detector.analyze_sentence("See you tomorrow at the library.")
    assert resultado == [["tomorrow", "Time"]] 

def test_oracion_2_usually(detector):
    resultado = detector.analyze_sentence("Juana usually goes running in the park in the morning.")
    assert resultado == [["usually", "Frequency"]]

def test_oracion_3_sin_adverbios(detector):
    resultado = detector.analyze_sentence("The girl draws flowers in her notebook.")
    assert resultado == []  

def test_oracion_4_ambiguedad_yesterday(detector):
    resultado = detector.analyze_sentence("Yesterday was unforgettable yesterday.")
    assert resultado == [["yesterday", "Time"]]

def test_oracion_5_multiples_adverbios(detector):
    resultado = detector.analyze_sentence("He was happily inside the house")
    assert resultado == [
        ["happily", "Manner"],
        ["inside", "Place"]
    ]