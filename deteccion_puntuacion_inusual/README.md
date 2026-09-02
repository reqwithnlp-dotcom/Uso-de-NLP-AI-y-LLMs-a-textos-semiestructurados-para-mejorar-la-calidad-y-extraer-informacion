# Detector de puntuacion inusual

Servicio en Python para detectar signos de puntuacion potencialmente inusuales en textos en ingles.

## Que detecta

- Secuencias de signos consecutivos, excepto `...`.
- Signos de puntuacion pegados directamente a una palabra.
- Parentesis, corchetes o llaves desbalanceados.
- Signos repetidos, como dos apostrofes consecutivos.

La funcion principal devuelve una tupla con:

```text
(bool, list[str] | int)
```

El primer valor indica si se detecto una irregularidad. El segundo contiene los signos encontrados o `0` cuando el texto es normal.

## Estructura y rutas

```text
deteccion_puntuacion_inusual/
|-- __init__.py                 Exporta la aplicacion.
|-- main.py                     Punto de entrada de FastAPI.
|-- model/
|   |-- __init__.py             Exporta las funciones del detector.
|   `-- detector.py             Implementa el analisis de puntuacion.
|-- service/
|   |-- __init__.py             Exporta la funcion para el servicio.
|   |-- api.py                  Define la API HTTP.
|   `-- schemas.py              Define los modelos de solicitud y respuesta.
|-- test/
|   `-- test_detector.py        Pruebas del detector.
|-- test_service.py             Pruebas mediante la interfaz del servicio.
`-- README.md                   Esta documentacion.
```

## API

### `GET /health`

Comprueba que el servicio este disponible.

Respuesta:

```json
{"status": "ok"}
```

### `POST /detect`

Analiza un texto recibido en formato JSON.

Solicitud:

```json
{"text": "Hi!.., Nice to meet you"}
```

Respuesta:

```json
{
  "unusual_punctuation": true,
  "positions": ["!", ","]
}
```

El servicio responde con estado `400` si el campo `text` esta vacio o contiene solo espacios.

## Ejecucion

Desde la carpeta `deteccion_puntuacion_inusual`:

```bash
pip install fastapi uvicorn pytest
uvicorn main:app --reload
```

La documentacion interactiva queda disponible en:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Pruebas

```bash
python -m pytest -q
```

Los casos incluidos cubren puntuacion normal, signos consecutivos, apostrofes repetidos y delimitadores desbalanceados.
