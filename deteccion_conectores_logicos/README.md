# Detección de conectores lógicos

Servicio que analiza un texto en inglés y detecta los **conectores lógicos** presentes (addition, disjunction, contrast, cause-effect, sequence, exemplification, conclusion, condition), devolviendo también las palabras del texto que no forman parte de ningún conector.

## Instalación

1. Ubicate en la carpeta del servicio:
   ```bash
   cd deteccion_conectores_logicos
   ```

2. (Opcional pero recomendado) Creá y activá un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Levantá el servidor con:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

El servicio queda disponible en `http://localhost:8001`.

La documentación interactiva (Swagger UI), generada automáticamente por FastAPI, está disponible en:
```
http://localhost:8001/docs
```


## Uso

### Endpoint: `POST /detect`

Detecta los conectores lógicos presentes en un texto y clasifica cada uno por tipo.

**Parámetros esperados** (body, JSON):

| Campo  | Tipo   | Requerido | Descripción                 |
|--------|--------|-----------|--------------------------------|
| `text` | string | Sí        | Texto en inglés a analizar     |

**Categorías de conectores reconocidas:**

| Categoría          | Ejemplos                                                     |
|----------------------|-------------------------------------------------------------------|
| `addition`            | and, also, furthermore, moreover, in addition, as well as         |
| `disjunction`          | or, either, neither, nor, otherwise                                |
| `contrast`             | but, however, although, whereas, nevertheless, on the other hand   |
| `cause-effect`         | so, therefore, thus, because, since, as a result, due to           |
| `sequence`             | first, second, then, next, finally, subsequently                   |
| `exemplification`      | namely, for example, for instance, such as, that is                |
| `conclusion`           | overall, in conclusion, in summary, to sum up                      |
| `condition`            | if, unless, provided that, as long as, in case                     |

### Ejemplo de uso 1: múltiples conectores

**Request:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{"text": "Dog and cat or rabbit"}'
```

**Response real (verificada):**
```json
{
  "original_text": "Dog and cat or rabbit",
  "connectors_found": [
    {"word": "and", "type": "addition"},
    {"word": "or", "type": "disjunction"}
  ],
  "normal_words": ["dog", "cat", "rabbit"],
  "total": 2
}
```

### Ejemplo de uso 2: conector de múltiples palabras

**Request:**
```json
{
  "text": "As a result, she had to retake the exam."
}
```

**Response real (verificada):**
```json
{
  "original_text": "As a result, she had to retake the exam.",
  "connectors_found": [
    {"word": "as a result", "type": "cause-effect"}
  ],
  "normal_words": ["she", "had", "to", "retake", "the", "exam"],
  "total": 1
}
```

> Los conectores de más de una palabra (como "as a result", "on the other hand") se detectan como una sola unidad, y sus palabras individuales ("as", "result") no aparecen sueltas en `normal_words`.

### Ejemplo de uso 3: texto sin conectores

**Request:**
```json
{
  "text": "Today I went for a run."
}
```

**Response real (verificada):**
```json
{
  "original_text": "Today I went for a run.",
  "connectors_found": [],
  "normal_words": ["today", "i", "went", "for", "a", "run"],
  "total": 0
}
```

### Ejemplo de uso 4: texto vacío

**Request:**
```json
{
  "text": ""
}
```

**Response esperada:** `400 Bad Request`
```json
{
  "detail": "El texto no puede estar vacio."
}
```

### Endpoints adicionales

- **`GET /connectors`**: devuelve el diccionario completo de conectores reconocidos por el servicio y su categoría.
- **`GET /health`**: chequeo simple de disponibilidad del servicio (`{"status": "ok"}`).

## Cómo funciona (resumen técnico)

1. **`normalize`**: pasa el texto a minúsculas y elimina signos de puntuación.
2. **`detect_connectors`**: busca primero los conectores de **múltiples palabras** (más específicos, para evitar que "as" se detecte suelto cuando en realidad forma parte de "as a result"), y luego los conectores de una sola palabra, evitando solapamientos.
3. Devuelve dos listas: los conectores encontrados con su categoría, y las palabras del texto que no forman parte de ningún conector (`normal_words`).

## Tests

El servicio incluye 5 tests (`test.py`) que verifican: detección de conectores simples y compuestos, normalización de mayúsculas/puntuación, texto sin conectores y texto vacío.

Ejecutalos con:
```bash
pytest test.py -v
```
Salida esperada: `5 passed`.

## Dependencias

Ver `requirements.txt`. El servicio se expone mediante **FastAPI** y se ejecuta con **uvicorn**. La lógica de detección utiliza únicamente el módulo estándar `re` de Python (sin dependencias externas de NLP).