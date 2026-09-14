# Detector de cambio de POV

Inicio rápido para el detector y la API local.

## Ejecutar la API

```bash
cd /home/carlos/Documentos/trabajo/proyectoSpacy/Uso-de-NLP-AI-y-LLMs-a-textos-semiestructurados-para-mejorar-la-calidad-y-extraer-informacion/povshift
.venv/bin/python main.py
```

El servicio queda disponible en:

```text
http://localhost:8014
```

## Probar una frase

```bash
curl -X POST http://localhost:8014/detect \
  -H "Content-Type: application/json" \
  -d '{"texto":"John wondered where Mary was. Mary knew he was waiting."}'
```

Ejemplo de respuesta:

```json
[
  {
    "from_character": {
      "id": 1,
      "canonical_name": "John",
      "mentions": ["John"]
    },
    "to_character": {
      "id": 7,
      "canonical_name": "Mary",
      "mentions": ["Mary"]
    },
    "sentence_index": 1,
    "confidence": 0.85,
    "evidence": [
      "previous focus on John",
      "new focalization on Mary"
    ]
  }
]
```

## Uso en Python

```python
from povshift.detector import POVShiftDetector

text = "John wondered where Mary was. Mary knew he was waiting."
detector = POVShiftDetector()
shifts = detector.detect(text)
print(shifts)
```

## Notas

- El servicio espera un cuerpo JSON con el campo `texto`.
- El detector es conservador: evita falsos positivos causados por cambios de sujeto, acciones observables o pronombres ambiguos.
- El proyecto sigue siendo un MVP centrado en textos narrativos en inglés y ejemplos simples y bien formados.

Entrada:

```text
John wondered where Mary was.
Mary knew he was waiting.
```

El sistema identifica:

```text
John → internal experience
Mary → internal experience
```

Por lo tanto:

```text
Narrative Focus:
John → Mary
```

Resultado:

```text
POV Shift = True
```

Conceptualmente:

```python
POVShift(
    from_character=John,
    to_character=Mary,
    ...
)
```

---

## ¿Qué no es un cambio de POV?

### Cambio de sujeto

```text
John opened the door.
Mary entered.
```

Resultado:

```text
POV Shift = False
```

Ambas oraciones describen acciones observables.

### Coreferencia

```text
John wondered where Mary was.
He felt nervous.
```

Después de la resolución:

```text
He → John
```

Enfoque:

```text
John → John
```

Resultado:

```text
POV Shift = False
```

### Cambio de persona gramatical

```text
I opened the door.
You closed it.
```

La narración pasa de primera persona a segunda persona aquí, pero la persona
gramatical no es, por sí sola, evidencia de un cambio en el enfoque narrativo;
tampoco es un campo que el detector siga o devuelva (no existe ningún atributo
`person` o `person_shift` en el modelo de dominio). Este ejemplo es solo
descriptivo de la *entrada*, no de algo que el sistema reporte.

Resultado:

```text
POV Shift = False
```

### Cláusulas dentro de la misma oración

```text
John opened the door and Mary felt afraid.
```

La oración contiene dos cláusulas, pero la decisión sobre POV se evalúa a nivel de
**oraciones**, no simplemente entre cláusulas.

---

## Modelo de dominio

El sistema usa cuatro objetos principales del dominio:

```text
Character
Clause
FocusState
POVShift
```

### Character

Representa una entidad narrativa.

```text
Character
 ├── id
 ├── canonical_name
 └── mentions
```

### Clause

Representa información lingüística analizada.

```text
Clause
 ├── text
 ├── sentence_index
 ├── subject
 ├── verb
 ├── internal_state
 ├── state_type
 └── experiencer
```

### FocusState

Representa el enfoque narrativo asociado a una oración.

```text
FocusState
 ├── character
 ├── sentence_index
 └── reason
```

### POVShift

Representa un cambio detectado en el enfoque narrativo.

```text
POVShift
 ├── from_character
 ├── to_character
 ├── sentence_index
 ├── confidence
 └── evidence
```

---

## Estados internos

La evidencia de estado interno se clasifica en tres categorías:

```text
cognition
emotion
perception
```

Ejemplos:

```text
John wondered where Mary was.
→ cognition

Mary felt afraid.
→ emotion

John saw Mary leaving.
→ perception
```

La detección de estados internos aporta evidencia sobre el enfoque narrativo, pero un estado interno por sí solo no constituye automáticamente un cambio de POV.

---

## Coreferencia

La resolución de coreferencia se usa para mantener la identidad del personaje a lo largo de diferentes menciones textuales.

Ejemplo:

```text
John entered the room.
He sat down.
```

El sistema resuelve:

```text
He → John
```

Las referencias ambiguas no se fuerzan.

Ejemplo:

```text
John met Paul.
He smiled.
```

Si el sistema no puede determinar de forma fiable el referente, la referencia permanece:

```text
ambiguous / unresolved
```

Esto evita decisiones de cambio de POV sin respaldo.

---

## Arquitectura

El proyecto sigue una arquitectura modular:

```text
POVShiftDetector
        ↓
Processing Components
        ↓
Domain Model
```

Componentes recomendados:

```text
NLPParser
CoreferenceResolver
InternalStateDetector
NarrativeFocusTracker
ShiftDetector
POVShiftDetector
```

Cada componente tiene una responsabilidad específica.

El modelo de dominio sigue siendo independiente de spaCy.

---

## Estructura del proyecto

```text
pov-shift-detector/

├── README.md
│
├── specs/
│   ├── requirements.md
│   ├── detection-rules.md
│   ├── test-cases.md
│   ├── domain-model.md
│   ├── architecture.md
│   └── traceability.md
│
├── src/
│   └── pov_detector/
│       ├── __init__.py
│       ├── detector.py
│       ├── models.py
│       ├── parser.py
│       ├── coreference.py
│       ├── internal_states.py
│       ├── focus_tracker.py
│       └── shift_detector.py
│
├── tests/
│   ├── unit/
│   │   ├── test_parser.py
│   │   ├── test_coreference.py
│   │   ├── test_internal_states.py
│   │   ├── test_focus_tracker.py
│   │   └── test_shift_detector.py
│   │
│   └── integration/
│       └── test_pov_detector.py
│
└── pyproject.toml
```

---

## Pruebas

Las pruebas se dividen en dos niveles:

### Pruebas unitarias

Verifican etapas individuales del procesamiento:

- análisis lingüístico;
- resolución de coreferencia;
- detección de estados internos;
- seguimiento del enfoque narrativo;
- detección de cambios.

### Pruebas de integración

Verifican la tubería completa:

```text
Raw Text
   ↓
POVShiftDetector
   ↓
POVShift[]
```

The expected behavior is defined in:

```text
specs/test-cases.md
```

---

## Specification

The project follows a specification-driven approach.

The specifications define:

| Document | Purpose |
|---|---|
| `requirements.md` | Functional and non-functional requirements |
| `detection-rules.md` | Rules used to classify POV shifts |
| `test-cases.md` | Expected system behavior |
| `domain-model.md` | Domain objects and relationships |
| `architecture.md` | Components and processing pipeline |
| `traceability.md` | Relationship between requirements, rules, tests, and implementation |

The implementation should remain consistent with these specifications.

---

## Main Design Principle

The detector must not use simplistic rules such as:

```python
if subject != previous_subject:
    pov_shift = True
```

or:

```python
if character != previous_character:
    pov_shift = True
```

Instead, POV detection is based on:

```text
Character
    ↓
Experiencer
    ↓
Internal Experience
    ↓
Narrative Focus
    ↓
Focus Change
    ↓
POV Shift
```

This separation is the central design principle of the project.

---

## Status

The project specification defines the architecture, domain model, detection rules, and test cases.

Implementation should proceed incrementally, validating each component against the corresponding specifications and tests.
