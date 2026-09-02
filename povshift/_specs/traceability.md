# POV Shift Detector — Traceability Matrix

## 1. Purpose

This document provides traceability between the project's:

- Functional Requirements;
- Non-Functional Requirements;
- Detection Rules;
- Domain Model;
- Architecture;
- Test Cases.

Its purpose is to ensure that every relevant requirement is represented by a detection rule, supported by the domain model and architecture, and verified by one or more tests.

The traceability relationship is:

```text
Requirement
    ↓
Detection Rule
    ↓
Domain Model
    ↓
Architecture Component
    ↓
Test Case
```

A requirement is considered adequately covered when its expected behavior is represented consistently across these artifacts.

---

# 2. Functional Requirements Traceability

| Requirement | Description | Detection Rules | Domain Model | Architecture | Tests |
|---|---|---|---|---|---|
| FR-01 | Text Analysis | RULE-10 | `Clause` | `NLPParser` / `analyze()` | TC-01, TC-02, TC-22 |
| FR-02 | Clause Extraction | RULE-10 | `Clause`, `sentence_index` | `NLPParser` / `analyze()` | TC-01, TC-02, TC-22 |
| FR-03 | Character Representation | RULE-05, RULE-06, RULE-08 | `Character` | `CoreferenceResolver` | TC-04, TC-05, TC-12, TC-13 |
| FR-04 | Coreference Resolution | RULE-08, RULE-09 | `Character` | `CoreferenceResolver` | TC-04, TC-05, TC-06, TC-11, TC-14, TC-21 |
| FR-05 | Internal State Detection | RULE-04, RULE-10 | `Clause.state_type`, `Clause.internal_state` | `InternalStateDetector` | TC-07, TC-08, TC-09, TC-23 |
| FR-06 | Experiencer Detection | RULE-04, RULE-05, RULE-06 | `Clause.experiencer` | `InternalStateDetector` | TC-07, TC-08, TC-11, TC-12, TC-13, TC-17 |
| FR-07 | Narrative Focus Tracking | RULE-05, RULE-06, RULE-07, RULE-08, RULE-10 | `FocusState` | `NarrativeFocusTracker` / `update_focus()` | TC-10, TC-11, TC-12, TC-19, TC-21, TC-22 |
| FR-08 | POV Shift Detection | RULE-01 through RULE-10 | `FocusState`, `POVShift` | `ShiftDetector` / `detect_shift()` | TC-13, TC-14, TC-15, TC-16, TC-17, TC-18, TC-19, TC-20, TC-21, TC-22 |
| FR-09 | Evidence | RULE-11 | `POVShift.evidence` | `ShiftDetector` | TC-18, TC-20, TC-24 |
| FR-10 | Confidence | RULE-11 | `POVShift.confidence` | `ShiftDetector` | TC-24 |

---

# 3. Detailed Functional Requirement Coverage

## FR-01 — Text Analysis

The system must obtain linguistic information from English text using spaCy.

Traceability:

```text
FR-01
 ↓
RULE-10
 ↓
Clause
 ↓
NLPParser / analyze()
 ↓
TC-01, TC-02, TC-22
```

Relevant tests verify:

- clause extraction;
- sentence segmentation;
- textual order;
- sentence membership;
- multiple clauses within a sentence.

---

## FR-02 — Clause Extraction

Clauses are the linguistic analysis units.

Traceability:

```text
FR-02
 ↓
RULE-10
 ↓
Clause
 ↓
sentence_index
 ↓
NLPParser
 ↓
TC-01, TC-02, TC-22
```

`TC-22` is particularly important because it verifies that multiple clauses may belong to the same sentence.

---

## FR-03 — Character Representation

Narrative entities are represented using stable `Character` objects.

Traceability:

```text
FR-03
 ↓
RULE-05 / RULE-06 / RULE-08
 ↓
Character
 ↓
CoreferenceResolver
 ↓
TC-04, TC-05, TC-12, TC-13
```

The same character must retain the same identity across textual mentions.

---

## FR-04 — Coreference Resolution

Resolvable references must be associated with the correct `Character`.

Ambiguous references must remain unresolved.

Traceability:

```text
FR-04
 ↓
RULE-08 / RULE-09
 ↓
Character
 ↓
CoreferenceResolver
 ↓
TC-04, TC-05, TC-06, TC-11, TC-14, TC-21
```

`TC-06` verifies that ambiguous references are not arbitrarily resolved.

`TC-21` is a critical regression test because incorrect coreference could create a false POV shift.

---

## FR-05 — Internal State Detection

The system must detect internal experience and classify it as cognition, emotion, or perception when possible.

Traceability:

```text
FR-05
 ↓
RULE-04
 ↓
Clause
 ↓
InternalStateDetector
 ↓
TC-07, TC-08, TC-09, TC-23
```

The perception case is explicitly covered by `TC-23`.

---

## FR-06 — Experiencer Detection

The system must identify the character experiencing an internal state when this can be determined reliably.

Traceability:

```text
FR-06
 ↓
RULE-04 / RULE-05 / RULE-06
 ↓
Clause.experiencer
 ↓
InternalStateDetector
 ↓
TC-07, TC-08, TC-11, TC-12, TC-13, TC-17
```

The experiencer is more important for POV analysis than grammatical subject alone.

---

## FR-07 — Narrative Focus Tracking

The system must establish, maintain, and change narrative focus according to sufficient evidence.

Traceability:

```text
FR-07
 ↓
RULE-05 / RULE-06 / RULE-07 / RULE-08
 ↓
FocusState
 ↓
NarrativeFocusTracker
 ↓
TC-10, TC-11, TC-12, TC-19, TC-21, TC-22
```

`TC-10` verifies focus establishment.

`TC-11` verifies focus maintenance through coreference.

`TC-12` verifies focus change.

`TC-22` verifies that clauses within the same sentence do not independently generate a focus transition for POV detection.

---

## FR-08 — POV Shift Detection

A POV shift requires an established previous focus, a different subsequent focus, sufficient internal-state evidence, and a sentence-level transition.

Traceability:

```text
FR-08
 ↓
RULE-01
RULE-02
RULE-03
RULE-04
RULE-05
RULE-06
RULE-07
RULE-08
RULE-09
RULE-10
 ↓
FocusState
POVShift
 ↓
ShiftDetector
 ↓
TC-13 through TC-22
```

This is the central requirement of the system.

The tests verify both positive and negative cases.

---

## FR-09 — Evidence

Every detected POV shift must contain evidence supporting the decision.

Traceability:

```text
FR-09
 ↓
RULE-11
 ↓
POVShift.evidence
 ↓
ShiftDetector
 ↓
TC-18, TC-20, TC-24
```

Evidence must represent information actually used by the detector.

---

## FR-10 — Confidence

Every detected POV shift must contain a reproducible confidence value between `0.0` and `1.0`.

Traceability:

```text
FR-10
 ↓
RULE-11
 ↓
POVShift.confidence
 ↓
ShiftDetector
 ↓
TC-24
```

The requirements intentionally do not prescribe a specific scoring formula.

The scoring strategy is an implementation concern as long as the result is bounded and reproducible.

---

# 4. Non-Functional Requirements Traceability

| Requirement | Description | Architecture | Domain Model | Tests |
|---|---|---|---|---|
| NFR-01 | Modularity | Specialized processing components | Separated domain classes | Unit tests across processing stages |
| NFR-02 | Testability | Independent processing components | Domain objects with clear interfaces | TC-01 through TC-24 |
| NFR-03 | Explainability | `ShiftDetector` produces evidence | `POVShift.evidence` | TC-18, TC-20, TC-24 |
| NFR-04 | Robustness | Pipeline separation and specialized components | Explicit unresolved references and focus states | TC-06, TC-15, TC-16, TC-21, TC-22 |
| NFR-05 | Extensibility | Modular components and dependency direction | spaCy-independent domain model | Architectural design |

---

# 5. Detection Rule Traceability

| Rule | Principle | Requirements | Domain Model | Architecture | Tests |
|---|---|---|---|---|---|
| RULE-01 | Subject change is not sufficient | FR-08, NFR-04 | `Clause.subject`, `FocusState` | `ShiftDetector` | TC-15 |
| RULE-02 | Character change is not sufficient | FR-08, NFR-04 | `Character`, `FocusState` | `ShiftDetector` | TC-15 |
| RULE-03 | Person shift is not sufficient | FR-08, NFR-04 | `Clause`, `FocusState` | `ShiftDetector` | TC-16, TC-17 |
| RULE-04 | Internal state provides focalization evidence | FR-05, FR-06, FR-07, FR-08 | `Clause.internal_state`, `state_type`, `experiencer` | `InternalStateDetector` | TC-07, TC-08, TC-17, TC-23 |
| RULE-05 | Same experiencer means no shift | FR-07, FR-08 | `Character`, `FocusState` | `NarrativeFocusTracker`, `ShiftDetector` | TC-11, TC-14, TC-19, TC-21 |
| RULE-06 | Different experiencer can indicate shift | FR-06, FR-07, FR-08 | `Clause.experiencer`, `FocusState`, `POVShift` | `InternalStateDetector`, `ShiftDetector` | TC-12, TC-13, TC-17, TC-20 |
| RULE-07 | Focus establishment is not a shift | FR-07, FR-08 | `FocusState` | `NarrativeFocusTracker`, `ShiftDetector` | TC-10, TC-15 |
| RULE-08 | Coreference precedes focus comparison | FR-04, FR-07, FR-08 | `Character`, `Clause`, `FocusState` | `CoreferenceResolver` before `NarrativeFocusTracker` | TC-04, TC-11, TC-14, TC-21 |
| RULE-09 | Ambiguous coreference is not forced | FR-04, NFR-04 | `Character`, unresolved reference representation | `CoreferenceResolver` | TC-06 |
| RULE-10 | POV shifts are evaluated across sentences | FR-01, FR-02, FR-07, FR-08 | `Clause.sentence_index`, `FocusState.sentence_index`, `POVShift.sentence_index` | `NarrativeFocusTracker`, `ShiftDetector` | TC-02, TC-22 |
| RULE-11 | Confidence reflects evidence | FR-09, FR-10, NFR-03 | `POVShift.evidence`, `POVShift.confidence` | `ShiftDetector` | TC-18, TC-20, TC-24 |

---

# 6. Domain Model Traceability

## Character

Responsibilities:

- stable narrative identity;
- canonical name;
- textual mentions.

Supports:

```text
FR-03
FR-04
FR-06
FR-07
FR-08
```

Verified by:

```text
TC-04
TC-05
TC-06
TC-11
TC-12
TC-13
TC-14
TC-21
```

---

## Clause

Responsibilities:

- linguistic analysis unit;
- subject;
- verb;
- internal-state information;
- state type;
- experiencer;
- sentence membership.

Supports:

```text
FR-01
FR-02
FR-05
FR-06
FR-07
FR-08
```

Verified by:

```text
TC-01
TC-02
TC-07
TC-08
TC-09
TC-22
TC-23
```

---

## FocusState

Responsibilities:

- represent narrative focus;
- associate focus with a sentence;
- distinguish focus establishment, maintenance, and change.

Supports:

```text
FR-07
FR-08
```

Verified by:

```text
TC-10
TC-11
TC-12
TC-13
TC-14
TC-19
TC-20
TC-21
TC-22
```

---

## POVShift

Responsibilities:

- represent a detected focus change;
- identify source character;
- identify destination character;
- identify sentence location;
- store confidence;
- store evidence.

Supports:

```text
FR-08
FR-09
FR-10
```

Verified by:

```text
TC-13
TC-18
TC-20
TC-24
```

---

# 7. Architecture Component Traceability

| Component | Responsibility | Requirements | Domain Objects |
|---|---|---|---|
| `POVShiftDetector` | Pipeline orchestration | FR-01 through FR-10 | All |
| `NLPParser` | Linguistic analysis and clause extraction | FR-01, FR-02 | `Clause` |
| `CoreferenceResolver` | Entity/reference resolution | FR-03, FR-04 | `Character`, `Clause` |
| `InternalStateDetector` | Internal-state and experiencer detection | FR-05, FR-06 | `Clause`, `Character` |
| `NarrativeFocusTracker` | Focus establishment and maintenance | FR-07 | `FocusState`, `Character` |
| `ShiftDetector` | POV shift classification, evidence, confidence | FR-08, FR-09, FR-10 | `FocusState`, `POVShift` |

The dependency direction remains:

```text
POVShiftDetector
        ↓
processing components
        ↓
domain model
```

The domain model remains independent of spaCy.

---

# 8. Test Coverage by Category

## Linguistic Analysis

```text
TC-01
TC-02
TC-22
```

Covers:

- clauses;
- sentences;
- order;
- sentence boundaries;
- multiple clauses.

---

## Coreference

```text
TC-04
TC-05
TC-06
TC-11
TC-14
TC-21
```

Covers:

- male pronoun resolution;
- female pronoun resolution;
- ambiguity;
- same-character focus;
- false-positive prevention.

---

## Internal States

```text
TC-07
TC-08
TC-09
TC-23
```

Covers:

- cognition;
- emotion;
- observable action;
- perception.

---

## Focus Tracking

```text
TC-10
TC-11
TC-12
TC-19
TC-21
TC-22
```

Covers:

- focus establishment;
- focus maintenance;
- focus change;
- coreference;
- sentence-level evaluation.

---

## POV Shift Detection

```text
TC-13
TC-14
TC-15
TC-16
TC-17
TC-18
TC-19
TC-20
TC-21
TC-22
```

Covers:

- clear shift;
- no shift;
- subject change;
- character change;
- grammatical person change;
- internal-state evidence;
- same-sentence clauses;
- multiple shifts;
- coreference regression.

---

## Confidence and Explainability

```text
TC-18
TC-20
TC-24
```

Covers:

- detected shift;
- evidence;
- confidence bounds;
- confidence reproducibility.

---

# 9. Integration Coverage

The integration tests verify the complete pipeline:

```text
Input Text
    ↓
analyze()
    ↓
resolve_coreference()
    ↓
detect_internal_states()
    ↓
update_focus()
    ↓
detect_shift()
    ↓
POVShift[]
```

Integration coverage:

| Test | Purpose |
|---|---|
| TC-18 | Complete pipeline with one POV shift |
| TC-19 | Complete pipeline without a POV shift |
| TC-20 | Complete pipeline with multiple POV shifts |
| TC-21 | Coreference regression through the complete pipeline |
| TC-22 | Sentence/clause boundary regression |
| TC-24 | Complete shift result with confidence validation |

---

# 10. Critical Regression Requirements

The following behaviors are considered critical and must remain protected by automated tests.

### Coreference

```text
John wondered where Mary was.
He felt nervous.
```

must not produce:

```text
John → He
```

as a POV shift.

Covered by:

```text
TC-11
TC-14
TC-21
```

---

### Subject Change

```text
John opened the door.
Mary entered.
```

must not produce a POV shift.

Covered by:

```text
TC-15
```

---

### Grammatical Person Change

```text
I opened the door.
You closed it.
```

must not automatically produce a POV shift.

Covered by:

```text
TC-16
```

---

### Same-Sentence Clause Change

```text
John opened the door and Mary felt afraid.
```

must not automatically produce a POV shift.

Covered by:

```text
TC-22
```

---

### Ambiguous Coreference

```text
John met Paul.
He smiled.
```

must not force a coreference decision.

Covered by:

```text
TC-06
```

---

# 11. Traceability Completeness

The current specification provides coverage for all defined functional requirements:

```text
FR-01 ✓
FR-02 ✓
FR-03 ✓
FR-04 ✓
FR-05 ✓
FR-06 ✓
FR-07 ✓
FR-08 ✓
FR-09 ✓
FR-10 ✓
```

The current specification also provides architectural support for all defined non-functional requirements:

```text
NFR-01 ✓
NFR-02 ✓
NFR-03 ✓
NFR-04 ✓
NFR-05 ✓
```

The detection rules are covered by requirements, domain concepts, architecture components, and tests.

---

# 12. Consistency Constraints

The following constraints must remain true across all project artifacts.

### Constraint 1 — Subject is not focus

```text
subject change
    ≠
POV shift
```

---

### Constraint 2 — Character change is not focus change

```text
character change
    ≠
POV shift
```

---

### Constraint 3 — Person change is not sufficient

```text
grammatical person change
    ≠
POV shift
```

---

### Constraint 4 — Internal state is evidence, not conclusion

```text
internal state
    →
possible focus evidence

internal state
    ≠
automatic POV shift
```

---

### Constraint 5 — Coreference precedes focus comparison

```text
coreference
    ↓
experiencer identity
    ↓
focus comparison
```

---

### Constraint 6 — Focus establishment is not a shift

```text
None → John
```

means:

```text
focus established
```

not:

```text
POV shift
```

---

### Constraint 7 — POV decisions are sentence-level

```text
Clause
    ↓
linguistic evidence

Sentence
    ↓
focus comparison boundary
```

A change between clauses sharing the same `sentence_index` must not automatically produce a POV shift.

---

### Constraint 8 — Ambiguity must not be converted into certainty

```text
unresolved reference
    ≠
known Character
```

The detector must not create a POV shift from unsupported identity assumptions.

---

# 13. Final Traceability Model

The complete project can be represented as:

```text
                    REQUIREMENTS
                         │
                         ▼
                 DETECTION RULES
                         │
                         ▼
                   DOMAIN MODEL
                         │
                         ▼
                    ARCHITECTURE
                         │
                         ▼
                   IMPLEMENTATION
                         │
                         ▼
                      TESTS
```

For the POV Shift Detector, the central traceability chain is:

```text
FR-08 — POV Shift Detection
          │
          ├── RULE-01 — Subject change is not enough
          ├── RULE-02 — Character change is not enough
          ├── RULE-03 — Person change is not enough
          ├── RULE-04 — Internal state provides evidence
          ├── RULE-05 — Same experiencer means no shift
          ├── RULE-06 — Different experiencer can indicate shift
          ├── RULE-07 — Focus establishment is not a shift
          ├── RULE-08 — Coreference precedes comparison
          ├── RULE-09 — Ambiguity is not forced
          └── RULE-10 — Comparison occurs across sentences
                         │
                         ▼
                 FocusState + POVShift
                         │
                         ▼
                    ShiftDetector
                         │
                         ▼
              TC-13 through TC-22
```

This traceability structure ensures that the implementation can be evaluated against explicit requirements rather than against undocumented assumptions.