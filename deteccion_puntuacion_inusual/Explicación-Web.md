# Detector de puntuacion inusual

## 1. Definicion

El detector de puntuacion inusual es un servicio que recibe un texto y revisa
si contiene signos de puntuacion que podrian necesitar una correccion.

Detecta principalmente:

- Signos de puntuacion consecutivos, excepto el caso permitido `...`.
- Signos de puntuacion pegados directamente a una palabra.
- Parentesis, corchetes o llaves sin cerrar o desbalanceados.
- Signos repetidos, como dos apostrofes consecutivos.

El servicio no corrige el texto automaticamente. Indica si encontro una
irregularidad y devuelve los signos detectados para que otra aplicacion pueda
mostrarlos o revisarlos.

## 2. Estructura del proyecto

```text
deteccion_puntuacion_inusual/
|
|-- main.py                         Punto de entrada de FastAPI.
|-- model/
|   |-- detector.py                  Reglas de deteccion.
|   `-- __init__.py
|-- service/
|   |-- api.py                      Endpoints HTTP.
|   |-- schemas.py                  Modelos de entrada y respuesta.
|   `-- __init__.py
|-- test/
|   `-- test_detector.py            Pruebas de las reglas.
|-- test_service.py                 Pruebas del servicio.
|-- README.md                       Documentacion general.
|-- README_local.md                 Este documento.
`-- explicacion_friendly_poster.txt Texto breve para el poster.
```

## 3. Objetivo de la API

El objetivo de la API es ofrecer una forma simple de consultar el detector
 desde otra aplicacion.

El flujo es:

```text
Aplicacion cliente
       |
       |  POST /detect con un texto
       v
API FastAPI
       |
       |  Ejecuta las reglas del detector
       v
Resultado JSON
       |
       v
La aplicacion muestra o guarda el resultado
```

Endpoints principales:

| Metodo | Endpoint | Funcion |
|---|---|---|
| GET | `/health` | Comprueba que el servicio este disponible. |
| POST | `/detect` | Analiza un texto y devuelve el resultado. |

## 4. Ejemplo de entrada y resultado

### Entrada sin irregularidades

Solicitud a `POST /detect`:

```json
{
  "text": "Hi! Nice to meet you."
}
```

Resultado:

```json
{
  "unusual_punctuation": false,
  "positions": 0
}
```

Interpretacion: el texto no presenta una puntuacion inusual.

### Entrada con irregularidades

Solicitud a `POST /detect`:

```json
{
  "text": "Hi!.., Nice to meet you"
}
```

Resultado:

```json
{
  "unusual_punctuation": true,
  "positions": ["!", ","]
}
```

Interpretacion: el servicio encontro una secuencia de signos que conviene
revisar.

### Entrada invalida

Solicitud:

```json
{
  "text": "   "
}
```

Resultado HTTP `400`:

```json
{
  "detail": "El texto no puede estar vacio."
}
```

## 5. Estrategia de deteccion

El detector analiza el texto mediante reglas simples y explicables:

1. Recorre los caracteres del texto.
2. Identifica signos de puntuacion y sus repeticiones.
3. Permite la secuencia `...` como una excepcion.
4. Comprueba que los delimitadores `()`, `[]` y `{}` esten balanceados.
5. Revisa si un signo aparece pegado a una palabra de forma inusual.
6. Devuelve `true` cuando encuentra una irregularidad.
7. Devuelve en `positions` los signos involucrados o `0` si no encuentra nada.

Esta estrategia permite explicar cada resultado y facilita agregar nuevas reglas
sin cambiar el contrato de la API.

## 6. Ejemplos visuales

### Flujo de una solicitud correcta

```text
+----------------------+       +------------------+       +------------------+
| Texto del usuario    | ----> | POST /detect     | ----> | Resultado JSON   |
| Hi! Nice to meet you |       | recibe text      |       | false, positions |
+----------------------+       +------------------+       +------------------+
```

### Flujo con puntuacion inusual

```text
+----------------------+       +------------------+       +------------------+
| Texto recibido       | ----> | Reglas activadas | ----> | Requiere revision|
| Hi!.., Nice...       |       | !.., detectado   |       | true: ! y ,      |
+----------------------+       +------------------+       +------------------+
```

### Significado visual del resultado

```text
unusual_punctuation = false  -->  Texto normal
unusual_punctuation = true   -->  Revisar puntuacion
positions = 0                -->  No se detectaron signos problematicos
positions = ["!", ","]      -->  Signos involucrados en la alerta
```

## 7. Como levantar el servicio

Desde esta carpeta:

```bash
python -m pip install fastapi uvicorn pytest
python -m uvicorn main:app --reload
```

Abrir la documentacion interactiva en:

```text
http://127.0.0.1:8000/docs
```

Desde Swagger se puede seleccionar `POST /detect`, presionar `Try it out`,
escribir un JSON de ejemplo y presionar `Execute`.

## 8. Mensaje breve para una presentacion

Este servicio recibe un texto, analiza sus signos de puntuacion y avisa si
encuentra una combinacion inusual. La API devuelve un resultado simple para
que cualquier aplicacion pueda mostrarlo, guardarlo o solicitar una revision.
