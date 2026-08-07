# Detección de inconsistencias de verbos modales

Servicio que analiza un texto en inglés y detecta **inconsistencias** en el uso de verbos modales: cuando una misma acción es descrita en distintas partes del texto con modales de categorías semánticas diferentes (por ejemplo, en un párrafo se presenta como *posibilidad/permiso* — "you **can** submit the report" — y en otro como *obligación* — "you **must** submit the report").

La idea de fondo: contar o juzgar un "exceso" de verbos modales no tiene sentido por sí solo, ya que depende del tipo de texto (legal vs. general, etc.). Lo que sí es un problema real es la **inconsistencia**: tratar la misma acción de formas contradictorias a lo largo del texto.

## Instalación

1. Ubicate en la carpeta del servicio:
   ```bash
   cd deteccion_verbos_modales
   ```

2. (Opcional pero recomendado) Creá y activá un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Levantá el servidor con:
```bash
python main.py
```
o:
```bash
uvicorn main:app --reload
```

El servicio queda disponible en `http://localhost:8000`.

La documentación interactiva (Swagger UI), generada automáticamente por FastAPI, está disponible en:
```
http://localhost:8000/docs
```

## Uso

### Endpoint: `POST /analizar`

Analiza un texto y devuelve una única lista:

- **`inconsistencies`**: pares de menciones de una misma acción usando modales de **distinta** categoría (posible inconsistencia a revisar).

El servicio ya no devuelve una lista de "consistencias" (pares que comparten la misma categoría): esos casos simplemente no se reportan, porque no representan un problema a revisar.

**Parámetros esperados** (body, JSON):

| Campo   | Tipo   | Requerido | Descripción                |
|---------|--------|-----------|------------------------------|
| `texto` | string | Sí        | Texto en inglés a analizar   |

**Categorías de verbos modales reconocidas:**

| Categoría                | Ejemplos                                                    |
|----------------------------|-----------------------------------------------------------------|
| `prohibition`               | cannot, can't, must not, may not, is forbidden                  |
| `obligation`                 | has to, have to, needs to, must, is required to                 |
| `recommendation`             | should, ought to, is recommended, it is advisable to            |
| `possibility/permission`     | can, could, might, may, is allowed to                           |

### Ejemplo de uso: texto con inconsistencia

**Request:**
```bash
curl -X POST "http://localhost:8000/analizar" \
  -H "Content-Type: application/json" \
  -d '{"texto": "You can submit the report by Friday. However, you must submit the report before the deadline."}'
```

**Response real (verificada):**
```json
{
  "inconsistencies": [
    {
      "shared_action": "report, submit",
      "case_1": {
        "modal": "can",
        "category": "possibility/permission",
        "action": "submit the report by Friday.",
        "sentence": "You can submit the report by Friday."
      },
      "case_2": {
        "modal": "must",
        "category": "obligation",
        "action": "submit the report before the deadline.",
        "sentence": "However, you must submit the report before the deadline."
      }
    }
  ]
}
```

El servicio detecta que la acción "submit the report" se describe primero como **posible/permitida** ("can") y luego como **obligatoria** ("must") — una inconsistencia que conviene revisar en el texto original.

### Ejemplo de uso: texto consistente (sin inconsistencias)

**Request:**
```json
{
  "texto": "Employees can request time off through the online portal. Employees can also request time off through the online portal for medical reasons."
}
```

**Response esperada:**
```json
{
  "inconsistencies": []
}
```

Acá ambas menciones usan modales de la **misma** categoría (`possibility/permission`), por lo que no hay nada que reportar: no se trata como un caso a revisar.

### Ejemplo de uso: texto sin acciones relacionadas

**Request:**
```json
{
  "texto": "The dog runs in the park."
}
```

**Response esperada:**
```json
{
  "inconsistencies": []
}
```

No hay verbos modales en el texto, por lo que no hay nada para comparar.

## Cómo funciona (resumen técnico)

1. **`extract_modal_actions`**: recorre el texto oración por oración, detecta cada verbo/expresión modal presente y extrae la "acción" asociada (el resto de la oración después del modal).
2. **`normalize_action`**: convierte cada acción en un conjunto de palabras clave, descartando stopwords y palabras muy cortas.
3. **`find_inconsistencies`**: compara cada par de acciones detectadas; si comparten suficientes palabras clave (es decir, describen esencialmente la misma acción) pero fueron etiquetadas con modales de **categorías distintas**, se agrega a la lista de inconsistencias. Si son de la misma categoría, el par se descarta y no se reporta.

## Tests

El servicio incluye tests (`test.py`) que verifican: detección de modales simples y compuestos, distinción entre prohibición y obligación (ej. "must not" vs "must"), detección de inconsistencias, y manejo de textos sin modales o sin acciones relacionadas.

Ejecutalos con:
```bash
pytest test.py -v
```

## Dependencias

Ver `requirements.txt`. El servicio se expone mediante **FastAPI** y se ejecuta con **uvicorn**. La lógica de detección utiliza únicamente los módulos estándar `re` e `itertools` de Python (sin dependencias externas de NLP).