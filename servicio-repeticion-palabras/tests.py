import unittest
from servicio_repeticion_palabras import detectar_repeticiones


class TestDetectarRepeticiones(unittest.TestCase):

    # ------------------------------------------------------------------
    # Casos base
    # ------------------------------------------------------------------

    def test_sin_repeticiones(self):
        """Sin palabras repetidas → lista vacía."""
        texto = "There is no place like home."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)
        self.assertEqual(resultado, [])

    def test_repeticion_simple(self):
        """'good' aparece 3 veces → una entrada con count=3."""
        texto = "In case we don't see each other again: good morning, good afternoon, and good night."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)

        palabras = {r["word"]: r for r in resultado}
        self.assertIn("good", palabras)
        self.assertEqual(palabras["good"]["count"], 3)
        self.assertEqual(len(palabras["good"]["indices"]), 3)

    def test_lematizacion_true_agrupa_formas(self):
        """Con lematización, 'animal' y 'animals' se agrupan bajo el mismo lema."""
        texto = "No animal shall drink alcohol; no animal shall kill another animal; all animals are equal."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)

        palabras = {r["word"]: r for r in resultado}
        # Con lematización, 'animal' y 'animals' deben agruparse
        self.assertIn("animal", palabras)
        self.assertGreaterEqual(palabras["animal"]["count"], 3)

    def test_lematizacion_false_no_agrupa(self):
        """Sin lematización, 'animal' y 'animals' se cuentan por separado."""
        texto = "No animal shall drink alcohol; no animal shall kill another animal; all animals are equal."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=False)

        palabras = {r["word"]: r for r in resultado}
        # Sin lematización, 'animal' aparece 3 veces y 'animals' 1 vez (no se repite)
        self.assertIn("animal", palabras)
        self.assertEqual(palabras["animal"]["count"], 3)
        self.assertNotIn("animals", palabras)  # solo 1 ocurrencia → no se reporta

    def test_stopwords_false_incluye_articulos(self):
        """Con ignorar_stopwords=False, palabras como 'the' y 'under' se detectan."""
        texto = "The animals observe the tree under the sun; the animal looks at the trees under the sun."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=False, lematizacion=True)

        palabras = {r["word"]: r for r in resultado}
        self.assertIn("the", palabras)
        self.assertGreaterEqual(palabras["the"]["count"], 2)

    def test_stopwords_true_excluye_articulos(self):
        """Con ignorar_stopwords=True, palabras vacías como 'the' no se reportan."""
        texto = "The animals observe the tree under the sun; the animal looks at the trees under the sun."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)

        palabras = {r["word"]: r for r in resultado}
        self.assertNotIn("the", palabras)

    # ------------------------------------------------------------------
    # Validación de estructura del output
    # ------------------------------------------------------------------

    def test_estructura_output(self):
        """Cada elemento del resultado debe tener 'word', 'count' e 'indices'."""
        texto = "good morning, good afternoon, and good night."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)

        self.assertTrue(len(resultado) > 0)
        for item in resultado:
            self.assertIn("word", item)
            self.assertIn("count", item)
            self.assertIn("indices", item)
            self.assertIsInstance(item["word"], str)
            self.assertIsInstance(item["count"], int)
            self.assertIsInstance(item["indices"], list)

    def test_indices_validos(self):
        """Los índices start/end deben ser enteros no negativos y start < end."""
        texto = "The cat sat on the mat. The cat sat."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=False, lematizacion=True)

        for item in resultado:
            for idx in item["indices"]:
                self.assertIn("start", idx)
                self.assertIn("end", idx)
                self.assertGreaterEqual(idx["start"], 0)
                self.assertGreater(idx["end"], idx["start"])

    def test_orden_descendente(self):
        """El resultado debe estar ordenado de mayor a menor por 'count'."""
        texto = "The cat sat on the mat. The cat sat on the mat. The cat."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=False, lematizacion=True)

        counts = [r["count"] for r in resultado]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_indices_apuntan_a_token_correcto(self):
        """Los índices deben apuntar exactamente a la posición del token en el texto."""
        texto = "good morning, good afternoon, and good night."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)

        palabras = {r["word"]: r for r in resultado}
        self.assertIn("good", palabras)

        for idx in palabras["good"]["indices"]:
            token_en_texto = texto[idx["start"]:idx["end"]].lower()
            self.assertEqual(token_en_texto, "good")

    # ------------------------------------------------------------------
    # Casos borde
    # ------------------------------------------------------------------

    def test_texto_vacio(self):
        """Texto vacío → lista vacía sin errores."""
        resultado = detectar_repeticiones("", ignorar_stopwords=True, lematizacion=True)
        self.assertEqual(resultado, [])

    def test_texto_solo_puntuacion(self):
        """Solo puntuación → lista vacía."""
        resultado = detectar_repeticiones("... !!! ???", ignorar_stopwords=True, lematizacion=True)
        self.assertEqual(resultado, [])

    def test_texto_una_palabra(self):
        """Una sola palabra → lista vacía (no hay repeticiones)."""
        resultado = detectar_repeticiones("Hello", ignorar_stopwords=True, lematizacion=True)
        self.assertEqual(resultado, [])

    def test_count_coincide_con_indices(self):
        """El campo 'count' debe coincidir con la longitud de 'indices'."""
        texto = "good morning, good afternoon, and good night."
        resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)

        for item in resultado:
            self.assertEqual(item["count"], len(item["indices"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
