# Detector de puntuacion inusual

Servicio en Python para detectar signos de puntuacion potencialmente inusuales en textos en ingles.

## Explicacion amigable

Este servicio funciona como un revisor automatico de puntuacion. Le enviamos
una frase y nos responde si encontro algo que conviene revisar.

- `unusual_punctuation: false` significa que no encontro una irregularidad.
- `unusual_punctuation: true` significa que encontro una irregularidad.
- `positions` muestra los signos involucrados. Si no hay problemas, devuelve `0`.

En otras palabras: enviamos texto, el servicio lo analiza y devuelve un
resultado que otra aplicacion puede mostrar o guardar.

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

## Guia paso a paso para el video

Esta secuencia se puede seguir directamente durante la grabacion.

### Paso 1: instalar y levantar el servicio

Abrir una terminal dentro de la carpeta `deteccion_puntuacion_inusual` y
ejecutar:

```bash
python -m pip install fastapi uvicorn pytest
python -m uvicorn main:app --reload
```

En pantalla debe aparecer que Uvicorn esta ejecutandose en
`http://127.0.0.1:8000`.

### Paso 2: abrir la documentacion interactiva

Abrir en el navegador:

```text
http://127.0.0.1:8000/docs
```

Swagger muestra los endpoints disponibles. Para este video se usaran
`/health` y `/detect`.

### Paso 3: comprobar que el servicio esta vivo

1. Buscar `GET /health` y abrirlo.
2. Presionar `Try it out`.
3. Presionar `Execute`.

La respuesta esperada es:

```json
{"status": "ok"}
```

Esto demuestra que el servidor esta encendido y listo para recibir textos.

### Paso 4: enviar un texto correcto

1. Buscar `POST /detect` y abrirlo.
2. Presionar `Try it out`.
3. En el cuerpo de la solicitud escribir:

```json
{
  "text": "Hi! Nice to meet you."
}
```

4. Presionar `Execute`.

La respuesta esperada es:

```json
{
  "unusual_punctuation": false,
  "positions": 0
}
```

Explicacion para el video: la frase no presenta una irregularidad, por eso el
resultado es `false` y `positions` vale `0`.

### Paso 5: enviar un texto con puntuacion inusual

Repetir los pasos anteriores usando este texto:

```json
{
  "text": "Hi!.., Nice to meet you"
}
```

La respuesta esperada es:

```json
{
  "unusual_punctuation": true,
  "positions": ["!", ","]
}
```

Explicacion para el video: el servicio encontro signos consecutivos poco
habituales (`!..,`) y los devuelve en `positions` para que la aplicacion sepa
que debe revisar.

### Paso 6: mostrar una entrada invalida

Enviar un texto vacio o compuesto solo por espacios:

```json
{
  "text": "   "
}
```

La API responde con estado `400` y este detalle:

```json
{
  "detail": "El texto no puede estar vacio."
}
```

Explicacion para el video: el servicio valida la entrada antes de analizarla
y avisa que hace falta enviar un texto.

### Resumen para narrar

> Primero levantamos el servicio y comprobamos su estado. Luego enviamos una
> frase normal y obtenemos `false`. Despues enviamos una frase con puntuacion
> inusual y obtenemos `true`, junto con los signos detectados. Finalmente
> mostramos que una entrada vacia devuelve un error claro.

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
