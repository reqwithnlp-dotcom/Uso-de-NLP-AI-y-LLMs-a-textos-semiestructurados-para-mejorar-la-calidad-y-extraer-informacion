# POV Shift Detector

A Python system for detecting **narrative Point of View (POV) shifts** in English text.

The system identifies when the narrative focus changes from one character's **internal experience** to another character's internal experience.

## Objective

The detector distinguishes a real POV shift from changes that may look similar but do not necessarily represent a change in narrative perspective:

- grammatical subject changes;
- character changes;
- grammatical person changes;
- pronoun changes;
- observable actions;
- ambiguous coreference;
- changes between clauses within the same sentence.

The central principle is:

```text
Internal Experience
        ↓
Narrative Focus
        ↓
Focus Change
        ↓
POV Shift
```

A change of subject or character alone is **not** considered a POV shift.

---

## How It Works

The detector processes text through a modular pipeline:

```text
Raw Text
   ↓
Linguistic Analysis
   ↓
Coreference Resolution
   ↓
Internal-State Detection
   ↓
Narrative Focus Tracking
   ↓
POV Shift Detection
   ↓
POVShift[]
```

The public interface is:

```python
detector = POVShiftDetector()

shifts = detector.detect(text)
```

The caller only needs to provide the text. The internal processing stages are handled by the detector.

---

## Example

Input:

```text
John wondered where Mary was.
Mary knew he was waiting.
```

The system identifies:

```text
John → internal experience
Mary → internal experience
```

Therefore:

```text
Narrative Focus:
John → Mary
```

Result:

```text
POV Shift = True
```

Conceptually:

```python
POVShift(
    from_character=John,
    to_character=Mary,
    ...
)
```

---

## What Is Not a POV Shift?

### Subject change

```text
John opened the door.
Mary entered.
```

Result:

```text
POV Shift = False
```

Both sentences describe observable actions.

### Coreference

```text
John wondered where Mary was.
He felt nervous.
```

After resolution:

```text
He → John
```

Focus:

```text
John → John
```

Result:

```text
POV Shift = False
```

### Grammatical person change

```text
I opened the door.
You closed it.
```

The grammatical person changes, but this alone does not establish a POV shift.

```text
Person Shift = True
POV Shift = False
```

### Clauses within the same sentence

```text
John opened the door and Mary felt afraid.
```

The sentence contains two clauses, but the POV decision is evaluated across **sentences**, not simply between clauses.

---

## Domain Model

The system uses four main domain objects:

```text
Character
Clause
FocusState
POVShift
```

### Character

Represents a narrative entity.

```text
Character
 ├── id
 ├── canonical_name
 └── mentions
```

### Clause

Represents analyzed linguistic information.

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

Represents the narrative focus associated with a sentence.

```text
FocusState
 ├── character
 ├── sentence_index
 └── reason
```

### POVShift

Represents a detected change in narrative focus.

```text
POVShift
 ├── from_character
 ├── to_character
 ├── sentence_index
 ├── confidence
 └── evidence
```

---

## Internal States

Internal-state evidence is classified into three categories:

```text
cognition
emotion
perception
```

Examples:

```text
John wondered where Mary was.
→ cognition

Mary felt afraid.
→ emotion

John saw Mary leaving.
→ perception
```

Internal-state detection provides evidence for narrative focus, but an internal state alone does not automatically constitute a POV shift.

---

## Coreference

Coreference resolution is used to maintain character identity across different textual mentions.

Example:

```text
John entered the room.
He sat down.
```

The system resolves:

```text
He → John
```

Ambiguous references are not forced.

Example:

```text
John met Paul.
He smiled.
```

If the system cannot reliably determine the referent, the reference remains:

```text
ambiguous / unresolved
```

This prevents unsupported POV-shift decisions.

---

## Architecture

The project follows a modular architecture:

```text
POVShiftDetector
        ↓
Processing Components
        ↓
Domain Model
```

Recommended components:

```text
NLPParser
CoreferenceResolver
InternalStateDetector
NarrativeFocusTracker
ShiftDetector
POVShiftDetector
```

Each component has a specific responsibility.

The domain model remains independent from spaCy.

---

## Project Structure

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

## Testing

Testing is divided into two levels:

### Unit tests

Verify individual processing stages:

- linguistic analysis;
- coreference resolution;
- internal-state detection;
- focus tracking;
- shift detection.

### Integration tests

Verify the complete pipeline:

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