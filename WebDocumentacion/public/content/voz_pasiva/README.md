# API de conversión de voz pasiva a activa

## Definición

La voz pasiva es una estructura gramatical utilizada para resaltar la acción y el objeto que la recibe, en lugar de quien la realiza.
En una oración pasiva, el sujeto no ejecuta la acción, sino que la recibe.

## Estructura
La voz pasiva se forma habitualmente con un auxiliar y un participio pasado. Este servicio identifica la construcción mediante las dependencias gramaticales del texto.
The letter was written by Juan:

- `was` → auxiliar de la voz pasiva
- `written` → participio del verbo write
- `by Juan` → complemento agente

## Ejemplo

| **Oración** | **Resultado** |
|-------------|---------------|
| `The letter was written by Juan.` | Voz pasiva: `True` |
| `Juan wrote the letter.` | Voz pasiva: `False` |

## Objetivo de la api
El servicio analiza una oración en inglés para identificar si contiene una construcción pasiva y localizar las posiciones de los caracteres correspondientes. Se utiliza como librería o desde la interfaz de consola; no expone un endpoint HTTP.

## Estrategia
El servicio buscará los **componentes característicos de la voz pasiva:**

1. **Análisis lingüístico:** procesa la oración con spaCy y el modelo `en_core_web_sm`.
2. **Auxiliar pasivo:** busca tokens cuya dependencia sintáctica sea `auxpass`.
3. **Participio:** extiende el rango de la construcción hasta el token con etiqueta `VBN`.
4. **Clasificación:** devuelve `True` cuando encuentra una construcción pasiva.

## Ejemplos Visuales

```text
The letter was written by Juan.
```

El análisis produce:

```text
is_passive(...) -> True
passive_positions(...) -> [(11, 22)]
```
