import unittest
from servicio_deteccion_cliches import detectar_cliches


class TestDetectarClichesFase1(unittest.TestCase):
    """Tests de la Fase 1 (filtrado_inicial=True, analisis_profundo=False)."""

    # ------------------------------------------------------------------
    # Casos base — clichés presentes literalmente en el corpus
    # ------------------------------------------------------------------

    def test_cliche_simple_en_oracion(self):
        """'back to square one' detectado dentro de una oración más larga."""
        texto = "We failed, so it's back to square one for us."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("back to square one", resultado)

    def test_cliche_al_inicio(self):
        """Cliché al comienzo del texto."""
        texto = "raining cats and dogs outside today."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("raining cats and dogs", resultado)

    def test_cliche_al_final(self):
        """Cliché al final del texto."""
        texto = "He just couldn't beat around the bush."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("beat around the bush", resultado)

    def test_multiples_cliches_sin_solapamiento(self):
        """Dos clichés distintos en el mismo texto, ambos detectados."""
        texto = "Back to square one after trying to kill two birds with one stone."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("back to square one", resultado)
        self.assertIn("kill two birds with one stone", resultado)

    def test_orden_de_aparicion(self):
        """Los clichés se devuelven en orden de aparición en el texto."""
        texto = "Back to square one after trying to kill two birds with one stone."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        idx_primero = resultado.index("back to square one")
        idx_segundo = resultado.index("kill two birds with one stone")
        self.assertLess(idx_primero, idx_segundo)

    def test_cliche_con_lematizacion(self):
        """'dogs' → lema 'dog': 'raining cats and dogs' se detecta igual."""
        texto = "It was raining cats and dogs all night."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("raining cats and dogs", resultado)

    def test_cliche_con_mayusculas(self):
        """El texto en distintas capitalizaciones se detecta igual."""
        texto = "It's always Better Late Than Never."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("better late than never", resultado)

    def test_variante_posesivo_your(self):
        """'ants in your pants' → posesivo normalizado → detectado."""
        texto = "He had ants in his pants before the exam."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("ants in his pants", resultado)

    # ------------------------------------------------------------------
    # Sin clichés
    # ------------------------------------------------------------------

    def test_sin_cliches(self):
        """Oración sin clichés → lista vacía."""
        texto = "The researchers analyzed the structural properties of the molecule."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertEqual(resultado, [])

    # ------------------------------------------------------------------
    # Casos borde
    # ------------------------------------------------------------------

    def test_texto_vacio(self):
        """Texto vacío → lista vacía."""
        resultado = detectar_cliches("", filtrado_inicial=True, analisis_profundo=False)
        self.assertEqual(resultado, [])

    def test_texto_solo_espacios(self):
        """Texto de solo espacios → lista vacía."""
        resultado = detectar_cliches("   ", filtrado_inicial=True, analisis_profundo=False)
        self.assertEqual(resultado, [])

    def test_texto_solo_puntuacion(self):
        """Solo puntuación → lista vacía."""
        resultado = detectar_cliches("... !!! ???", filtrado_inicial=True, analisis_profundo=False)
        self.assertEqual(resultado, [])

    def test_texto_una_sola_palabra(self):
        """Una sola palabra → imposible formar n-grama de 2+ tokens → lista vacía."""
        resultado = detectar_cliches("Hello", filtrado_inicial=True, analisis_profundo=False)
        self.assertEqual(resultado, [])

    # ------------------------------------------------------------------
    # Validación de estructura del output
    # ------------------------------------------------------------------

    def test_output_es_lista(self):
        """El output siempre es una lista."""
        resultado = detectar_cliches("back to square one", filtrado_inicial=True, analisis_profundo=False)
        self.assertIsInstance(resultado, list)

    def test_output_contiene_strings(self):
        """Cada elemento del output es un string."""
        resultado = detectar_cliches("back to square one", filtrado_inicial=True, analisis_profundo=False)
        for item in resultado:
            self.assertIsInstance(item, str)

    def test_output_en_minusculas(self):
        """Las frases del output están en minúsculas."""
        resultado = detectar_cliches("BACK TO SQUARE ONE", filtrado_inicial=True, analisis_profundo=False)
        for item in resultado:
            self.assertEqual(item, item.lower())

    def test_output_subcadena_del_texto(self):
        """Cada frase del output es subcadena (case-insensitive) del texto original."""
        texto = "We ended up back to square one."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        for item in resultado:
            self.assertIn(item, texto.lower())

    # ------------------------------------------------------------------
    # Parámetros booleanos
    # ------------------------------------------------------------------

    def test_ambas_fases_false(self):
        """Si ninguna fase está activa, siempre retorna lista vacía."""
        texto = "raining cats and dogs, back to square one."
        resultado = detectar_cliches(texto, filtrado_inicial=False, analisis_profundo=False)
        self.assertEqual(resultado, [])

    def test_fase1_false_no_detecta_con_corpus(self):
        """Con filtrado_inicial=False no se usa el corpus de n-gramas."""
        # Un cliché del corpus no debe ser detectado por Fase 1 si está desactivada
        # (la Fase 2 podría o no detectarlo, pero lo testeamos sin profundo tampoco)
        texto = "raining cats and dogs"
        resultado = detectar_cliches(texto, filtrado_inicial=False, analisis_profundo=False)
        self.assertEqual(resultado, [])


class TestDetectarClichesCasosEspeciales(unittest.TestCase):
    """Tests de casos especiales del corpus."""

    def test_cliche_con_puntuacion_interna(self):
        """Clichés con comas o apóstrofes en el corpus se detectan igual."""
        # "all's fair in love and war" → el apóstrofe se descarta como puntuación
        texto = "All's fair in love and war, they say."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("all's fair in love and war", resultado)

    def test_no_duplicados(self):
        """Un cliché detectado una sola vez no se duplica en el output."""
        # Nota: algunos clichés con adjetivos comparativos (ej. 'easier') cambian
        # su lema según el contexto sintáctico. Se usa un cliché estable.
        texto = "He always seems to go back to square one with everything."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("back to square one", resultado)
        self.assertEqual(resultado.count("back to square one"), 1)

    def test_cliche_exacto_unico_token(self):
        """Texto que ES exactamente un cliché del corpus."""
        texto = "tip of the iceberg"
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("tip of the iceberg", resultado)

    def test_cliche_con_contexto_antes_y_despues(self):
        """El cliché embebido en texto largo se detecta y extrae correctamente."""
        texto = "Politicians often talk about the tip of the iceberg when it comes to corruption."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
        self.assertIn("tip of the iceberg", resultado)


class TestDetectarClichesFase2(unittest.TestCase):
    """Tests de la Fase 2 (filtrado_inicial=False, analisis_profundo=True)."""

    def test_variacion_semantica_butterflies(self):
        """'butterflies in her stomach' detectado como variación semántica."""
        texto = "Maria gets butterflies in her stomach because of Juan."
        resultado = detectar_cliches(texto, filtrado_inicial=False, analisis_profundo=True)
        self.assertIn("butterflies in her stomach", resultado)

    def test_variacion_semantica_ants(self):
        """'ants in his pants' detectado como variación de 'ants in your pants'."""
        texto = "He got ants in his pants before the final game."
        resultado = detectar_cliches(texto, filtrado_inicial=False, analisis_profundo=True)
        self.assertIn("ants in his pants", resultado)

    def test_variacion_semantica_barking(self):
        """Variación de 'bark up the wrong tree' detectada semánticamente."""
        texto = "I think they are barking up the wrong trees."
        resultado = detectar_cliches(texto, filtrado_inicial=False, analisis_profundo=True)
        # SBERT puede detectar una subventana (ej. 'up the wrong trees')
        # que tenga mayor similitud coseno con el cliché del corpus.
        self.assertTrue(
            len(resultado) > 0,
            "Fase 2 debería detectar una variación del cliché 'bark up the wrong tree'"
        )
        # Verificar que la frase detectada contiene las palabras clave
        frase_detectada = resultado[0]
        self.assertIn("wrong", frase_detectada)
        self.assertIn("tree", frase_detectada)

    def test_fase2_vacio(self):
        """Fase 2 con texto vacío retorna vacío."""
        resultado = detectar_cliches("", filtrado_inicial=False, analisis_profundo=True)
        self.assertEqual(resultado, [])

    def test_fase2_sin_cliches(self):
        """Fase 2 con texto sin clichés retorna vacío."""
        texto = "The researchers analyzed the structural properties of the molecule."
        resultado = detectar_cliches(texto, filtrado_inicial=False, analisis_profundo=True)
        self.assertEqual(resultado, [])


class TestDetectarClichesIntegracionFases(unittest.TestCase):
    """Tests de integración que combinan Fase 1 y Fase 2 en distintos escenarios."""

    def test_integracion_ambas_fases_solapamiento(self):
        """Ambas fases activas: no debe devolver 'it time and time again' si ya coincide 'time and time again'."""
        texto = "He tried to explain it time and time again."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=True)
        self.assertIn("time and time again", resultado)
        self.assertNotIn("it time and time again", resultado)

    def test_exacto_y_semantico_mezclados(self):
        """Detección combinada de clichés exactos (Fase 1) y semánticos (Fase 2) en el mismo texto."""
        # 'better late than never' -> exacto (Fase 1)
        # 'butterflies in her stomach' -> semántico (Fase 2)
        texto = "It is better late than never to admit that she gets butterflies in her stomach."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=True)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0], "better late than never")
        self.assertEqual(resultado[1], "butterflies in her stomach")

    def test_multiples_exactos_y_semanticos(self):
        """Múltiples clichés de ambas fases intercalados, respetando orden de aparición."""
        # 'back to square one' -> exacto (Fase 1)
        # 'butterflies in her stomach' -> semántico (Fase 2)
        # 'blood is thicker than water' -> exacto (Fase 1)
        texto = "We had to go back to square one because she got butterflies in her stomach, but blood is thicker than water."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=True)
        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado[0], "back to square one")
        self.assertEqual(resultado[1], "butterflies in her stomach")
        self.assertEqual(resultado[2], "blood is thicker than water")

    def test_preencion_fase2_por_exacto_fase1(self):
        """La coincidencia exacta en Fase 1 debe evitar que Fase 2 evalúe esa misma ventana u otras solapadas."""
        # 'spitting image' -> exacto. 'the spitting image' o 'spitting image of' no deben ser evaluados por Fase 2.
        texto = "He is the spitting image of his grandfather."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=True)
        self.assertEqual(resultado, ["spitting image"])

    def test_cambio_umbral_semantico_con_ambas_fases(self):
        """El umbral semántico debe controlar la Fase 2 sin alterar las detecciones de Fase 1."""
        texto = "We must go back to square one and she gets butterflies in her stomach."
        
        # Con umbral muy alto (0.99), la variación semántica no se detecta, pero el exacto de Fase 1 sí.
        resultado_alto = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=True, umbral_semantico=0.99)
        self.assertEqual(resultado_alto, ["back to square one"])
        
        # Con umbral estándar (0.75), ambos se detectan.
        resultado_estandar = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=True, umbral_semantico=0.75)
        self.assertEqual(resultado_estandar, ["back to square one", "butterflies in her stomach"])

    def test_sin_cliches_ambas_fases(self):
        """Texto limpio sin clichés con ambas fases activas retorna vacío."""
        texto = "The researchers analyzed the structural properties of the molecule."
        resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=True)
        self.assertEqual(resultado, [])

    def test_casos_borde_ambas_fases(self):
        """Casos límite (vacío, solo espacios, solo puntuación) con ambas fases activas."""
        self.assertEqual(detectar_cliches("", filtrado_inicial=True, analisis_profundo=True), [])
        self.assertEqual(detectar_cliches("   ", filtrado_inicial=True, analisis_profundo=True), [])
        self.assertEqual(detectar_cliches("...,,, ???", filtrado_inicial=True, analisis_profundo=True), [])
        self.assertEqual(detectar_cliches("hello", filtrado_inicial=True, analisis_profundo=True), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)

