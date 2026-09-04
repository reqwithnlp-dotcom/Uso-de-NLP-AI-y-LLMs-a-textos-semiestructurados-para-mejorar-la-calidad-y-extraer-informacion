# API de detección y clasificación de adverbios

## Definición

Un adverbio es una palabra que modifica un verbo, un adjetivo u otro adverbio.
Este servicio analiza textos en inglés, identifica adverbios y los clasifica según su función.

## Estructura
El servicio recibe un objeto JSON:

- `texto` → texto en inglés que será analizado

La respuesta contiene una lista de adverbios clasificados:

- `adverbs` → palabras detectadas con su categoría
- `word` → adverbio encontrado
- `category` → categoría gramatical del adverbio

## Ejemplo

| **Entrada** | **Resultado** |
|-------------|---------------|
| `The dog is here.` | `here` → `Place` |
| `She quickly finished the task.` | `quickly` → `Manner` |

## Objetivo de la api
El servicio recibe un texto en inglés y devuelve los adverbios encontrados junto con su categoría, sin modificar el texto original.

## Estrategia
La api buscará los **componentes característicos de los adverbios:**

1. **Análisis lingüístico:** procesa el texto con spaCy y el modelo `en_core_web_trf`.
2. **Diccionario:** fuerza la etiqueta `ADV` para ciertos lemas definidos en el diccionario del servicio.
3. **Clasificación:** consulta las categorías configuradas para cada adverbio.
4. **Regla de terminación:** clasifica como `Manner` los adverbios que terminan en `ly` cuando no tienen otra categoría definida.

## Ejemplos Visuales

```json
{
  "texto": "The dog is here."
}
```

La respuesta contiene:

```json
{
  "adverbs": [{"word": "here", "category": "Place"}]
}
```
