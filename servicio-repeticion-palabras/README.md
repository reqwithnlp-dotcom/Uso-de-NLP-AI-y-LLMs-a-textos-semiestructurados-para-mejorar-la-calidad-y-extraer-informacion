# Servicio de Detección de Repetición de Palabras

Servicio de NLP que analiza un texto en inglés y detecta las palabras que se repiten, indicando cuántas veces aparece cada una y en qué posición del texto original. Utiliza [spaCy](https://spacy.io/) para tokenización, lematización y filtrado de stop words.

---

## Tabla de contenidos

- [Instalación](#instalación)
- [Uso del servicio](#uso-del-servicio)
- [Parámetros](#parámetros)
- [Formato de salida](#formato-de-salida)
- [Ejemplos de uso](#ejemplos-de-uso)
- [Ejecución de tests](#ejecución-de-tests)

---

## Instalación

### 1. Clonar el repositorio y navegar a la carpeta del servicio

```bash
git clone https://github.com/tu-org/Uso-de-NLP-AI-y-LLMs-a-textos-semiestructurados-para-mejorar-la-calidad-y-extraer-informacion.git
cd Uso-de-NLP-AI-y-LLMs-a-textos-semiestructurados-para-mejorar-la-calidad-y-extraer-informacion/servicio-repeticion-palabras
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

---

## Uso del servicio

El servicio expone una única función Python que puede importarse directamente en cualquier script o aplicación:

```python
from servicio_repeticion_palabras import detectar_repeticiones

resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)
```

### Ejecución del script de ejemplo incluido

El propio archivo `servicio_repeticion_palabras.py` contiene ejemplos de prueba que se ejecutan al correrlo directamente:

```bash
python servicio_repeticion_palabras.py
```

---

## Parámetros

| Parámetro           | Tipo    | Default | Descripción |
|---------------------|---------|---------|-------------|
| `texto`             | `str`   | —       | El texto de entrada en inglés a analizar. |
| `ignorar_stopwords` | `bool`  | `True`  | Si es `True`, excluye del análisis las palabras vacías (stop words) como `"the"`, `"is"`, `"a"`, etc. Si es `False`, todas las palabras son consideradas. |
| `lematizacion`      | `bool`  | `True`  | Si es `True`, agrupa las distintas formas morfológicas de una palabra bajo su lema (forma base). Por ejemplo, `"running"`, `"runs"` y `"ran"` se agrupan como `"run"`. Si es `False`, cada forma se trata de forma independiente (comparación literal en minúsculas). |

---

## Formato de salida

La función retorna una **lista de diccionarios**, ordenada de mayor a menor por cantidad de apariciones. Cada diccionario tiene la siguiente estructura:

```json
{
  "word": "good",
  "count": 3,
  "indices": [
    { "start": 42, "end": 46 },
    { "start": 56, "end": 60 },
    { "start": 75, "end": 79 }
  ]
}
```

| Campo     | Tipo          | Descripción |
|-----------|---------------|-------------|
| `word`    | `str`         | La palabra (o lema) repetida, en minúsculas. |
| `count`   | `int`         | Número de veces que aparece en el texto. |
| `indices` | `list[dict]`  | Lista de posiciones en el string original. Cada posición tiene `start` (índice inicial, inclusive) y `end` (índice final, exclusive), equivalente al slicing `texto[start:end]`. |

Si no hay repeticiones, la función retorna una **lista vacía** `[]`.

---

## Ejemplos de uso

### Ejemplo 1 — Sin repeticiones

```python
from servicio_repeticion_palabras import detectar_repeticiones

texto = "There is no place like home."
resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)
print(resultado)
```

**Output esperado:**
```json
[]
```

---

### Ejemplo 2 — Palabra repetida 3 veces (`good`)

```python
texto = "In case we don't see each other again: good morning, good afternoon, and good night."
resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=True)
```

**Output esperado:**
```json
[
  {
    "word": "good",
    "count": 3,
    "indices": [
      { "start": 39, "end": 43 },
      { "start": 52, "end": 56 },
      { "start": 70, "end": 74 }
    ]
  }
]
```

---

### Ejemplo 3 — Sin lematización (`lematizacion=False`)

```python
texto = "No animal shall drink alcohol; no animal shall kill another animal; all animals are equal."
resultado = detectar_repeticiones(texto, ignorar_stopwords=True, lematizacion=False)
```

En este caso `"animal"` (3 apariciones) y `"animals"` (1 aparición) se tratan como palabras distintas. Solo `"animal"` supera el umbral de repetición.

**Output esperado:**
```json
[
  {
    "word": "animal",
    "count": 3,
    "indices": [
      { "start": 3,  "end": 9  },
      { "start": 34, "end": 40 },
      { "start": 55, "end": 61 }
    ]
  },
  {
    "word": "shall",
    "count": 2,
    "indices": [
      { "start": 10, "end": 15 },
      { "start": 41, "end": 46 }
    ]
  }
]
```

---

### Ejemplo 4 — Incluyendo stop words (`ignorar_stopwords=False`) y con lematización

```python
texto = "The animals observe the tree under the sun; the animal looks at the trees under the sun."
resultado = detectar_repeticiones(texto, ignorar_stopwords=False, lematizacion=True)
```

Al incluir stop words, palabras como `"the"` y `"under"` también se reportan.

**Output esperado (parcial, ordenado por count):**
```json
[
  {
    "word": "the",
    "count": 6,
    "indices": [ ... ]
  },
  {
    "word": "animal",
    "count": 2,
    "indices": [ ... ]
  },
  {
    "word": "tree",
    "count": 2,
    "indices": [ ... ]
  },
  {
    "word": "under",
    "count": 2,
    "indices": [ ... ]
  },
  {
    "word": "sun",
    "count": 2,
    "indices": [ ... ]
  }
]
```

---

## Ejecución de tests

El archivo `tests.py` contiene una suite completa de pruebas unitarias que cubre los casos principales y casos borde del servicio.

```bash
python -m pytest tests.py -v
```

O con el runner estándar de `unittest`:

```bash
python -m unittest tests -v
```

**Output esperado (todos los tests en verde):**

```
test_count_coincide_con_indices ... ok
test_estructura_output ... ok
test_indices_apuntan_a_token_correcto ... ok
test_indices_validos ... ok
test_lematizacion_false_no_agrupa ... ok
test_lematizacion_true_agrupa_formas ... ok
test_orden_descendente ... ok
test_repeticion_simple ... ok
test_sin_repeticiones ... ok
test_stopwords_false_incluye_articulos ... ok
test_stopwords_true_excluye_articulos ... ok
test_texto_solo_puntuacion ... ok
test_texto_una_palabra ... ok
test_texto_vacio ... ok

----------------------------------------------------------------------
Ran 14 tests in X.XXXs

OK
```
