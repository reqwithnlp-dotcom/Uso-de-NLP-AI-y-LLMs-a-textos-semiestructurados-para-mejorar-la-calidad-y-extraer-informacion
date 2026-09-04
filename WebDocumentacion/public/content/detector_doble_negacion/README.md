# API de detección de doble negación

## Definición

La doble negación ocurre cuando una misma cláusula contiene dos elementos negativos.
Este servicio analiza textos en inglés e identifica si presentan este fenómeno.

## Estructura
El servicio recibe un objeto JSON:

- `text` → texto en inglés que será analizado

La respuesta contiene:

- `text` → texto original
- `has_double_negation` → valor booleano que indica si existe doble negación

## Ejemplo

| **Entrada** | **Resultado** |
|-------------|---------------|
| `It's not impossible that she will come.` | `has_double_negation: true` |
| `She did not come.` | `has_double_negation: false` |

## Objetivo de la api
El servicio recibe un texto en inglés y determina si contiene al menos dos elementos negativos en una misma cláusula u oración.

## Estrategia
La api buscará los **componentes característicos de la doble negación:**

1. **Análisis sintáctico:** procesa el texto con spaCy y `en_core_web_trf`.
2. **Dependencias negativas:** cuenta tokens con dependencia `neg`.
3. **Diccionario:** reconoce palabras negativas configuradas en el servicio.
4. **Prefijos negativos:** reconoce palabras con prefijos como `un-`, `in-`, `im-`, `dis-` y `non-`.
5. **Decisión:** devuelve positivo cuando el conteo llega a dos negaciones.

## Ejemplos Visuales

```json
{
  "text": "It's not impossible that she will come."
}
```

La respuesta contiene:

```json
{
  "text": "It's not impossible that she will come.",
  "has_double_negation": true
}
```
