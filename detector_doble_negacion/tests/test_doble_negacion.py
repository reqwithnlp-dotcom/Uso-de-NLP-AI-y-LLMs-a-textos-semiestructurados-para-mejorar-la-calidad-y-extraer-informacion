import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import detect_double_negation

def test_oracion_1_dont_wont():
    resultado = detect_double_negation("I don't think she won't come.")
    assert resultado == True

def test_oracion_2_impossible_no_one():
    resultado = detect_double_negation("It's impossible that no one arrives on time.")
    assert resultado == True

def test_oracion_3_no_one_simple():
    resultado = detect_double_negation("No one said it would be easy.")
    assert resultado == False

def test_oracion_4_never_simple():
    resultado = detect_double_negation("She never said anything.")
    assert resultado == False

def test_oracion_5_didnt_simple():
    resultado = detect_double_negation("I didn't see anyone.")
    assert resultado == False

def test_oracion_6_not_impossible():
    resultado = detect_double_negation("It's not impossible that she will come.")
    assert resultado == True
