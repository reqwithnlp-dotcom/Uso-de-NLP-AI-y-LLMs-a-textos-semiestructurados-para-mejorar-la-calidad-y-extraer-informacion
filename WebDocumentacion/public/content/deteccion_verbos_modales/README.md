# API de detección de inconsistencias de verbos modales

## Definición

Los verbos modales expresan obligación, prohibición, recomendación, posibilidad o permiso.
Este servicio detecta acciones similares que aparecen asociadas con categorías modales diferentes.

## Estructura
El servicio recibe un objeto JSON:

- `texto` → texto en inglés que será analizado

La respuesta devuelve los pares de inconsistencias detectados, incluyendo el modal, su categoría, la acción y la oración correspondiente.

## Ejemplo

| **Entrada** | **Resultado** |
|-------------|---------------|
| `You can submit the report. You must submit the report.` | Inconsistencia entre posibilidad/permiso y obligación |
| `You must wear a helmet. You should wear a helmet.` | Inconsistencia entre obligación y recomendación |

## Objetivo de la api
El servicio recibe un texto en inglés y encuentra acciones repetidas que fueron expresadas con verbos modales de categorías semánticas diferentes.

## Estrategia
La api buscará los **componentes característicos de las inconsistencias modales:**

1. **Separación:** divide el texto en oraciones.
2. **Detección:** identifica frases modales mediante expresiones regulares.
3. **Prioridad:** procesa primero las frases modales largas y luego las formas simples.
4. **Extracción:** obtiene la acción que aparece después del modal.
5. **Comparación:** compara palabras significativas entre acciones y reporta un par cuando comparte al menos dos palabras y cubre al menos el 50 % de la acción menor.

## Ejemplos Visuales

```json
{
  "texto": "You can submit the report by Friday. However, you must submit the report before the deadline."
}
```

El resultado identifica `can` como posibilidad/permiso y `must` como obligación, con la acción compartida `report, submit`.
