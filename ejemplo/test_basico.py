import unittest

def resta(a, b):
    return a - b

class TestResta(unittest.TestCase):

    def test_numeros_positivos(self):
        self.assertEqual(resta(5, 3), 2)

    def test_con_cero(self):
        self.assertEqual(resta(5, 0), 5)

    def test_negativos(self):
        self.assertEqual(resta(-2, -3), 1)

if __name__ == "__main__":
    unittest.main()