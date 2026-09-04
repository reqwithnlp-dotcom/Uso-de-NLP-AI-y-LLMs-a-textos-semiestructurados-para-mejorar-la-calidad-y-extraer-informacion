# API de detección de oraciones impersonales

## Definición

Una oración impersonal no presenta un sujeto que realice la acción de forma explícita.
Este servicio clasifica cada oración en inglés como personal, impersonal o ambigua.

## Estructura
El servicio recibe un objeto JSON:

- `text` → texto en inglés que será separado y analizado por oraciones

La respuesta clasifica cada oración según las reglas del detector.

## Ejemplo

| **Entrada** | **Resultado** |
|-------------|---------------|
| `It rains.` | Impersonal meteorológica |
| `I bought a car.` | Personal |
| `It is fast.` | Personal o ambigua según el análisis de reglas |

## Objetivo de la api
El servicio recibe un texto en inglés, analiza sus oraciones y determina si cada una es personal, impersonal o ambigua.

## Estrategia
La api buscará los **componentes característicos de las oraciones impersonales:**

1. **Separación:** divide el texto en oraciones.
2. **Existencial:** busca construcciones con `there`.
3. **Meteorológica:** busca el sujeto `it` y adjetivos o verbos meteorológicos.
4. **Pasiva impersonal:** identifica construcciones pasivas sin agente personal.
5. **Extraposition:** reconoce construcciones con `it` anticipatorio.
6. **Comparación:** combina estas reglas con las de sujetos pronominales, nominales e imperativos para clasificar la oración.

## Ejemplos Visuales

```json
{
  "text": "It rains. I bought a car. It is fast."
}
```

El análisis identifica `It rains.` como impersonal meteorológica y `I bought a car.` como personal.
