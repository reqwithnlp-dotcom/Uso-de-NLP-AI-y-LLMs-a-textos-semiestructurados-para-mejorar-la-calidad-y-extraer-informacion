# Detector de doble negación

Servicio que analiza un texto en inglés y detecta si contiene **doble negación** (dos o más elementos negativos en la misma cláusula que se anulan semánticamente). Utiliza **spaCy** para el análisis de dependencias sintácticas y un diccionario extenso de palabras y prefijos negativos.

## Instalación

1. Ubicate en la carpeta del servicio:
   ```bash
   cd detector_doble_negacion
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

4. Descargá el modelo de spaCy (si aún no lo tenés):
   ```bash
   python -m spacy download en_core_web_trf
   ```

## Ejecución

Levantá el servidor con:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

El servicio queda disponible en `http://localhost:8002`.

La documentación interactiva (Swagger UI), generada automáticamente por FastAPI, está disponible en:
```
http://localhost:8002/docs
```


## Uso

### Endpoint: `POST /detect`

Detecta si un texto en inglés contiene doble negación.

**Parámetros esperados** (body, JSON):

| Campo  | Tipo   | Requerido | Descripción                 |
|--------|--------|-----------|-----------------------------|
| `text` | string | Sí        | Texto en inglés a analizar  |

### Ejemplo de uso 1: texto con doble negación

**Request:**
```bash
curl -X POST "http://localhost:8002/detect" \
  -H "Content-Type: application/json" \
  -d '{"text": "I don'\''t think she won'\''t come."}'
```

**Response esperada:**
```json
{
  "text": "I don't think she won't come.",
  "has_double_negation": true
}
```

### Ejemplo de uso 2: texto con negación simple (sin doble negación)

**Request:**
```json
{
  "text": "She never said anything."
}
```

**Response esperada:**
```json
{
  "text": "She never said anything.",
  "has_double_negation": false
}
```

### Ejemplo de uso 3: negación léxica + prefijo negativo

**Request:**
```json
{
  "text": "It's not impossible that she will come."
}
```

**Response esperada:**
```json
{
  "text": "It's not impossible that she will come.",
  "has_double_negation": true
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

- **`GET /health`**: chequeo simple de disponibilidad del servicio (`{"status": "ok"}`).

## Cómo funciona (resumen técnico)

1. **`_es_semanticamente_negativo`**: determina si un token individual es semánticamente negativo, consultando el diccionario de `PALABRAS_NEGATIVAS` y los `PREFIJOS_NEGATIVOS` (definidos en `diccionario_negacion.py`).
2. **`_contar_negaciones`**: recorre recursivamente el árbol de dependencias sintácticas desde un token raíz, sumando negaciones gramaticales (dependencia `neg`) y léxicas (palabras/prefijos negativos). Hace early return al llegar a 2.
3. **`detect_double_negation`**: procesa el texto con spaCy, itera sobre las oraciones y retorna `True` si alguna raíz acumula 2 o más negaciones.

## Tests

El servicio incluye 6 tests (`tests/test_doble_negacion.py`) que verifican: doble negación gramatical, negación léxica con pronombre, negación con prefijo, y negaciones simples que no deben dar positivo.

Ejecutalos con:
```bash
pytest tests/test_doble_negacion.py -v
```

Salida esperada: `6 passed`.

## Dependencias

Ver `requirements.txt`. El servicio se expone mediante **FastAPI** y se ejecuta con **uvicorn**. La lógica de detección utiliza **spaCy** con el modelo `en_core_web_trf` para el análisis de dependencias sintácticas.
