# Detector de Oraciones Impersonales

Microservicio (FastAPI) que clasifica oraciones en inglés.

- **Capa 1**: reglas sobre las dependencias sintácticas de spaCy. Por oración
  da dos booleanos independientes, `personal` e `impersonal`, y marca como
  `ambiguous` los casos límite (ambos `True` o ambos `False`).
- **Capa 2**: un clasificador spaCy (`textcat_multilabel`) entrenado sobre un
  corpus propio. Solo se consulta para las oraciones `ambiguous`. Si no hay
  modelo entrenado, el servicio funciona igual, solo con la capa 1.

El entrenamiento está documentado en [`training/README.md`](training/README.md).

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

Cada oración del resultado trae:

| campo | qué es |
|---|---|
| `personal`, `impersonal`, `ambiguous`, `type`, `personal_type` | resultado de la capa 1 |
| `final_label` | `PERSONAL` / `IMPERSONAL` / `UNDECIDED` |
| `decided_by` | `layer1` / `layer2` / `none` (sin modelo o capa 2 indecisa) |
| `layer2_scores` | `{PERSONAL, IMPERSONAL}` si escaló a la capa 2; si no, `null` |

La respuesta suma los contadores `layer2_resolved_count` y `undecided_count`.
`GET /health` informa `layer2_loaded`.

## Capa 2: modelo

El modelo entrenado **no se versiona**. Se busca en `model/textcat/` o en la
ruta de `IMPERSONAL_TEXTCAT_PATH`.

| variable | default | qué hace |
|---|---|---|
| `IMPERSONAL_TEXTCAT_PATH` | `model/textcat` | carpeta del modelo |
| `IMPERSONAL_L2_THRESHOLD` | `0.5` | score mínimo de la clase ganadora |
| `IMPERSONAL_L2_MARGIN` | `0.2` | ventaja mínima sobre la otra clase |

## Tests

```bash
python -m pytest -q
```
