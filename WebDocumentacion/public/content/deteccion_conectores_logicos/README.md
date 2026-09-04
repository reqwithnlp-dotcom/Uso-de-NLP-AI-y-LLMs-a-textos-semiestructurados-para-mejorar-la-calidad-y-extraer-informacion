# API de detección de conectores lógicos

## Definición

Los conectores lógicos relacionan ideas dentro de un texto y expresan relaciones como adición, contraste, causa o conclusión.
Este servicio detecta conectores lógicos en textos en inglés y los clasifica por tipo.

## Estructura
El servicio recibe un objeto JSON:

- `text` → texto en inglés que será analizado

La respuesta contiene:

- `original_text` → texto original
- `connectors_found` → conectores encontrados y su tipo
- `normal_words` → palabras que no fueron identificadas como conectores
- `total` → cantidad total de conectores

## Ejemplo

| **Entrada** | **Resultado** |
|-------------|---------------|
| `Dog and cat or rabbit` | `and` → `addition`, `or` → `disjunction` |
| `It rained, therefore we stayed home.` | `therefore` → `conclusion` |

## Objetivo de la api
El servicio recibe un texto en inglés, detecta los conectores lógicos presentes y devuelve su clasificación junto con las palabras normales y el total encontrado.

## Estrategia
La api buscará los **componentes característicos de los conectores lógicos:**

1. **Normalización:** convierte el texto a minúsculas y elimina la puntuación.
2. **Frases compuestas:** busca primero conectores formados por varias palabras.
3. **Palabras individuales:** busca después los conectores de una sola palabra.
4. **Control de coincidencias:** evita solapamientos entre resultados.
5. **Clasificación:** asigna categorías como `addition`, `disjunction`, `contrast`, `cause-effect`, `sequence`, `exemplification`, `conclusion` y `condition`.

## Ejemplos Visuales

```json
{
  "text": "Dog and cat or rabbit"
}
```

La respuesta contiene:

```json
{
  "connectors_found": [
    {"word": "and", "type": "addition"},
    {"word": "or", "type": "disjunction"}
  ],
  "normal_words": ["dog", "cat", "rabbit"],
  "total": 2
}
```
