# API de detección de verbos débiles

## Definición

Los verbos débiles son verbos generales o poco expresivos que pueden reemplazarse por verbos más específicos según el contexto.
Este servicio detecta verbos como `make`, `do`, `have`, `get`, `take`, `give` y `be`.

## Estructura
El servicio recibe un objeto JSON:

- `text` → texto en inglés que será analizado

La respuesta es una lista de verbos débiles encontrados.

## Ejemplo

| **Entrada** | **Resultado** |
|-------------|---------------|
| `She made a decision.` | `["made"]` |
| `They gave up.` | No se incluye `gave` porque forma parte de un verbo frasal |

## Objetivo de la api
El servicio recibe un texto en inglés y devuelve los verbos débiles presentes, excluyendo los que forman parte de verbos frasales.

## Estrategia
La api buscará los **componentes característicos de los verbos débiles:**

1. **Análisis lingüístico:** procesa el texto con spaCy.
2. **Categoría gramatical:** identifica verbos y auxiliares.
3. **Lista de referencia:** compara el lema con `WEAK_VERBS`.
4. **Verbos frasales:** excluye los verbos que tienen un hijo con dependencia `prt`.
5. **Resultado:** devuelve las formas de los verbos débiles encontrados.

## Ejemplos Visuales

```json
{
  "text": "She made a decision."
}
```

La respuesta es:

```json
["made"]
```
