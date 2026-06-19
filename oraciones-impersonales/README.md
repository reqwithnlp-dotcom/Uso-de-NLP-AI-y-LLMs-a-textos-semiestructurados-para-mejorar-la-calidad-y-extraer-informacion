# Detector de Oraciones Impersonales

Microservicio (FastAPI) que clasifica oraciones en inglés.

La **capa 1** aplica reglas sobre las dependencias sintácticas de spaCy y
devuelve, por oración, dos booleanos independientes —`personal` e
`impersonal`— y marca como `ambiguous` los casos límite (ambos `True` o
ambos `False`) que deben escalar a una **capa 2** basada en un modelo de
lenguaje.

## Requisitos

- Python 3.10+
- Dependencias en `requirements.txt`
- Modelo de spaCy `en_core_web_sm`

## Instalación

Parado en la carpeta del servicio (la que contiene `main.py`):

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt
python -m spacy download en_core_web_sm
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
- Para usar otro puerto: `uvicorn main:app --reload --port 8002`

## Endpoint

`POST /analyze`

```json
{ "text": "It rains. I bought a car. It is fast." }
```

Cada oración del resultado trae `personal`, `impersonal`, `ambiguous`, `type`
y `personal_type`.

## Tests

```bash
python -m pytest -q
```
