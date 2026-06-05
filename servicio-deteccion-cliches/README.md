# Servicio de Detección de Clichés (en inglés) v2.0

Servicio de NLP que analiza un texto en inglés para detectar la presencia de **clichés** (frases sobreutilizadas que restan originalidad al escrito). Combina dos estrategias complementarias:

- **Fase 1 — Filtrado inicial**: normalización con [spaCy](https://spacy.io/) (lowercase + lematización + sustitución de posesivos) y comparación por n-gramas contra el corpus `cliche500`.
- **Fase 2 — Análisis semántico profundo**: similitud semántica con [SBERT](https://www.sbert.net/) (`paraphrase-MiniLM-L6-v2`) para capturar variaciones y paráfrasis no detectadas por coincidencia exacta.

---

## Tabla de contenidos

- [Instalación](#instalación)
- [Uso del servicio](#uso-del-servicio)
- [Parámetros](#parámetros)
- [Formato de salida](#formato-de-salida)
- [Ejemplos de uso](#ejemplos-de-uso)
- [Ejecución de tests](#ejecución-de-tests)
- [Notas de diseño](#notas-de-diseño)

---

## Instalación

### 1. Navegar a la carpeta del servicio

```bash
cd servicio-deteccion-cliches
```

### 2. Crear y activar un entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Descargar el modelo de idioma de spaCy

```bash
python -m spacy download en_core_web_sm
```

### 5. (Opcional) Modelo SBERT

El modelo `paraphrase-MiniLM-L6-v2` (~80 MB) se descarga automáticamente de HuggingFace en la **primera ejecución** que use `analisis_profundo=True`. No requiere acción manual.

> Si solo se va a usar `analisis_profundo=False`, no es necesario instalar `sentence-transformers` ni `torch`.

---

## Uso del servicio

```python
from servicio_deteccion_cliches import detectar_cliches

resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=True)
```

---

## Parámetros

| Parámetro            | Tipo    | Default | Descripción |
|----------------------|---------|---------|-------------|
| `texto`              | `str`   | —       | La oración o párrafo a analizar en inglés. |
| `filtrado_inicial`   | `bool`  | `True`  | Activa la Fase 1: n-gramas normalizados contra el corpus `cliche500`. Rápido y preciso para coincidencias exactas o morfológicas. |
| `analisis_profundo`  | `bool`  | `True`  | Activa la Fase 2: ventana deslizante con SBERT. Captura variaciones, posesivos distintos y paráfrasis semánticas. Requiere `sentence-transformers`. |
| `umbral_semantico`   | `float` | `0.75`  | Umbral de similitud coseno para la Fase 2 (rango 0–1). Valores más altos = mayor precisión, menor recall. |

---

## Formato de salida

La función retorna una **lista de strings** ordenada por posición de aparición en el texto. Cada string es la frase detectada **en minúsculas**, tal como aparece en el input (sin signos de puntuación circundantes).

```python
["back to square one", "raining cats and dogs"]
```

Si no se detectan clichés, retorna una **lista vacía** `[]`.

---

## Ejemplos de uso

### Ejemplo 1 — Cliché exacto del corpus

```python
from servicio_deteccion_cliches import detectar_cliches

texto = "We failed, so it's back to square one for us."
resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
print(resultado)
# → ["back to square one"]
```

### Ejemplo 2 — Múltiples clichés en el mismo texto

```python
texto = "Back to square one after trying to kill two birds with one stone."
resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
print(resultado)
# → ["back to square one", "kill two birds with one stone"]
```

### Ejemplo 3 — Variante posesiva (normalización)

El corpus contiene `"ants in your pants"`. El servicio normaliza los pronombres posesivos (`his`, `her`, `my`, etc.) a `one's` en ambos lados, por lo que variantes como `"ants in his pants"` también son detectadas:

```python
texto = "He had ants in his pants before the presentation."
resultado = detectar_cliches(texto, filtrado_inicial=True, analisis_profundo=False)
print(resultado)
# → ["ants in his pants"]
```

### Ejemplo 4 — Solo análisis semántico (sin Fase 1)

```python
# Con analisis_profundo=True el sistema detecta por proximidad semántica
# variantes no presentes literalmente en el corpus.
texto = "Maria gets butterflies in her stomach because of Juan."
resultado = detectar_cliches(texto, filtrado_inicial=False, analisis_profundo=True)
print(resultado)
# → ["butterflies in her stomach"]  (si el umbral lo permite)
```

### Ejemplo 5 — Sin clichés

```python
texto = "The researchers analyzed the structural properties of the molecule."
resultado = detectar_cliches(texto)
print(resultado)
# → []
```

---

## Ejecución de tests

```bash
python -m unittest tests -v
```

**Output esperado (todos los tests en verde):**

```
test_cliche_con_contexto_antes_y_despues ... ok
test_cliche_con_puntuacion_interna ... ok
test_cliche_exacto_unico_token ... ok
test_no_duplicados ... ok
test_ambas_fases_false ... ok
test_cliche_al_final ... ok
test_cliche_al_inicio ... ok
test_cliche_con_lematizacion ... ok
test_cliche_con_mayusculas ... ok
test_cliche_simple_en_oracion ... ok
test_fase1_false_no_detecta_con_corpus ... ok
test_multiples_cliches_sin_solapamiento ... ok
test_orden_de_aparicion ... ok
test_output_contiene_strings ... ok
test_output_en_minusculas ... ok
test_output_es_lista ... ok
test_output_subcadena_del_texto ... ok
test_sin_cliches ... ok
test_texto_solo_espacios ... ok
test_texto_solo_puntuacion ... ok
test_texto_una_sola_palabra ... ok
test_texto_vacio ... ok
test_variante_posesivo_your ... ok

----------------------------------------------------------------------
Ran 23 tests in X.XXXs

OK
```
