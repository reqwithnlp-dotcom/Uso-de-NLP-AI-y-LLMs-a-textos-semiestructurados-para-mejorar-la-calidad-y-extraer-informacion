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

## API HTTP

La aplicacion FastAPI se importa como `main:app` y escucha, por defecto, en el
puerto `8000`.

### `GET /health`

Comprueba que el servicio este disponible.

Respuesta:

```json
{"status": "ok"}
```

### `POST /detect`

Analiza un texto recibido en formato JSON. El campo `text` debe ser una cadena
no vacia.

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

Para verificar el contrato completo de la API se pueden usar los siguientes
endpoints de documentacion:

- `GET /docs`: Swagger UI interactiva.
- `GET /redoc`: documentacion ReDoc.
- `GET /openapi.json`: especificacion OpenAPI en JSON.

## Ejecucion local

Desde la carpeta `deteccion_puntuacion_inusual`:

```bash
python -m pip install fastapi uvicorn pytest
python -m uvicorn main:app --reload
```

El servidor queda disponible en `http://127.0.0.1:8000`. La documentacion
interactiva queda disponible en:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Ejecucion en servidor

Instalar las dependencias en el entorno del servidor y ejecutar Uvicorn
escuchando en todas las interfaces de red:

```bash
python -m pip install fastapi uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Para una ejecucion administrada por un proceso de servicio, se recomienda
usar un supervisor como systemd, Docker o el administrador de procesos de la
plataforma donde se publique. El puerto externo y HTTPS deben configurarse en
el proxy inverso o balanceador del servidor.

## Ejemplos de uso

### Comprobar disponibilidad

```bash
curl http://127.0.0.1:8000/health
```

Respuesta:

```json
{"status":"ok"}
```

### Texto sin irregularidades

```bash
curl -X POST http://127.0.0.1:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"Hi! Nice to meet you."}'
```

Respuesta:

```json
{
  "unusual_punctuation": false,
  "positions": 0
}
```

### Texto con puntuacion inusual

```bash
curl -X POST http://127.0.0.1:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"Hi!.., Nice to meet you"}'
```

Respuesta:

```json
{
  "unusual_punctuation": true,
  "positions": ["!", ","]
}
```

### Solicitud invalida

```bash
curl -i -X POST http://127.0.0.1:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"   "}'
```

Respuesta HTTP `400`:

```json
{
  "detail": "El texto no puede estar vacio."
}
```

## Pruebas

```bash
python -m pytest -q
```

Los casos incluidos cubren puntuacion normal, signos consecutivos, apostrofes repetidos y delimitadores desbalanceados.
