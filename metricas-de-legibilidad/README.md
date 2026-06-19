# Métricas de Legibilidad

Microservicio (FastAPI) que analiza la legibilidad de un texto en inglés con el
índice **Gunning Fog extendido** (con penalización por comas).

## Requisitos

- Python 3.10+
- Dependencias en `requirements.txt`

## Instalación

Parado en la carpeta del servicio (la que contiene `main.py`):

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt
```

## Levantar el servicio

Desde la misma carpeta del servicio:

```bash
uvicorn main:app --reload
```

o, equivalentemente:

```bash
python main.py
```

- Documentación interactiva: http://127.0.0.1:8000/docs
- Para usar otro puerto: `uvicorn main:app --reload --port 8001`

## Endpoint

`POST /analizar`

```json
{ "texto": "The text to analyze.", "penalizacion": "medium" }
```

`penalizacion` admite: `minimum`, `low`, `medium`, `high`.

## Tests

```bash
python -m pytest Tests -q
```
