# API de detección de clichés

## Definición

Un cliché es una expresión sobreutilizada que ha perdido parte de su fuerza expresiva por repetirse con frecuencia.
Este servicio detecta clichés en textos en inglés.

## Estructura
El servicio recibe un texto y opciones para activar sus fases de análisis:

- `texto` → texto en inglés
- `filtrado_inicial` → activa la búsqueda directa de frases
- `analisis_profundo` → activa la búsqueda por similitud semántica
- `umbral_similitud` → umbral utilizado por el análisis semántico

La respuesta devuelve una lista de clichés detectados.

## Ejemplo

| **Entrada** | **Resultado** |
|-------------|---------------|
| `We failed, so it's back to square one for us.` | `back to square one` |
| `This phrase does not match the configured list.` | Lista vacía |

## Objetivo de la api
El servicio recibe un texto en inglés y devuelve las expresiones configuradas como clichés o las expresiones semánticamente similares a ellas.

## Estrategia
La api buscará los **componentes característicos de los clichés:**

1. **Coincidencia directa:** compara n-gramas con el archivo `cliches.txt`.
2. **Normalización lingüística:** usa minúsculas, lematización y normalización de posesivos mediante spaCy.
3. **Análisis semántico:** utiliza SBERT `paraphrase-MiniLM-L6-v2` y similitud coseno.
4. **Ventanas de texto:** compara ventanas deslizantes cuando se activa el análisis profundo.
5. **Filtrado:** aplica el umbral de similitud configurado.

## Ejemplos Visuales

```python
detectar_cliches(
    "We failed, so it's back to square one for us.",
    filtrado_inicial=True,
    analisis_profundo=False
)
```

El resultado es:

```python
["back to square one"]
```
