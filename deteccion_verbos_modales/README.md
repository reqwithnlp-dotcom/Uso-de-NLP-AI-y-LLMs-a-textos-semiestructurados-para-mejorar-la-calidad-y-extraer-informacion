# Detección de inconsistencias de verbos modales

Servicio que detecta verbos modales en un texto en inglés, clasifica su tipo semántico (obligación, posibilidad, permiso, etc.) y devuelve las frases que quedan entre cada verbo modal detectado.

## Instalación

1. Cloná el repositorio y ubicate en la carpeta del servicio:
   ```bash
   cd deteccion_verbos_modales
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
python main.py
```

o alternativamente:
```bash
uvicorn main:app --reload
```

El servicio queda disponible en `http://localhost:8000`.

La documentación interactiva (Swagger UI), generada automáticamente por FastAPI, está disponible en:
```
http://localhost:8000/docs
```

## Uso

### Endpoint: `POST /detectar`

Detecta los verbos modales presentes en un texto y las frases que quedan entre ellos.

**Parámetros esperados** (body, formato JSON):

| Campo   | Tipo   | Requerido | Descripción                              |
|---------|--------|-----------|-------------------------------------------|
| `texto` | string | Sí        | Texto en inglés a analizar               |

**Verbos modales reconocidos:**

| Verbo modal | Tipo                    |
|-------------|--------------------------|
| can         | ability                  |
| could       | ability/possibility      |
| may         | permission/possibility   |
| might       | possibility              |
| must        | obligation               |
| shall       | future/obligation        |
| should      | recommendation           |
| ought to    | obligation               |
| have to     | obligation               |
| need to     | necessity                |
| will        | future                   |
| would       | conditional              |
| used to     | past habit               |

### Ejemplo de uso

**Request:**
```bash
curl -X POST "http://localhost:8000/detectar" \
  -H "Content-Type: application/json" \
  -d '{"texto": "You should call her because she might need help."}'
```

**Response esperada:**
```json
{
  "modals": [
    ["should", "recommendation"],
    ["might", "possibility"],
    ["need to", "necessity"]
  ],
  "phrases": [
    "you",
    "call her because she",
    "help"
  ]
}
```

> **Nota:** las frases devueltas se normalizan a minúsculas y sin signos de puntuación, ya que el texto pasa por una función de normalización antes de la detección.

### Ejemplo sin verbos modales

**Request:**
```json
{
  "texto": "The dog runs in the park."
}
```

**Response esperada:**
```json
{
  "modals": [],
  "phrases": ["the dog runs in the park"]
}
```

### Ejemplo con verbo modal compuesto ("have to")

**Request:**
```json
{
  "texto": "I have to finish this today."
}
```

**Response esperada:**
```json
{
  "modals": [
    ["have to", "obligation"]
  ],
  "phrases": [
    "i",
    "finish this today"
  ]
}
```

## Tests

El servicio incluye un script de tests (`test.py`) para verificar el correcto funcionamiento de la detección de verbos modales. Para ejecutarlo:

```bash
pytest test.py
```

o, si no usás pytest:

```bash
python -m unittest test.py
```

## Dependencias

Ver `requirements.txt`. El servicio se expone mediante **FastAPI** y se ejecuta con **uvicorn**. La lógica de detección utiliza únicamente el módulo estándar `re` de Python.