# POV Shift Detector — Requirements Specification

## 1. Project Overview

### Objective

Develop a Python system capable of detecting narrative Point of View (POV) shifts in English text.

The system must identify when the narrative focus changes from one character's internal experience to another character's internal experience.

The system must distinguish a POV shift from:

- a change of grammatical subject;
- a change of character;
- a grammatical person shift;
- a simple change of observable action;
- an ambiguous or unresolved coreference;
- a change that occurs only between clauses within the same sentence.

---

## 2. Definition of POV Shift

A POV Shift occurs when the narrative focus changes from one character's internal experience to another character's internal experience across narrative sentences.

The relevant internal experiences may include:

- thoughts;
- beliefs;
- knowledge;
- memories;
- emotions;
- fears;
- desires;
- perceptions.

The detector may analyze clauses internally to determine the narrative focus, but a change between clauses within the same sentence must not, by itself, be reported as a POV shift.

### Example — POV Shift

John wondered where Mary was.
Mary knew he was waiting.

Analysis:

John → internal experience
Mary → internal experience

Narrative focus:

John → Mary

Result:

POV Shift = True

---

## 3. What Is NOT a POV Shift

### 3.1 Change of Subject

John opened the door.
Mary entered.

There are two different subjects:

John → Mary

However, both sentences describe observable actions.

Result:

POV Shift = False

### 3.2 Change of Character

A change of character alone is insufficient.

John walked into the room.
Mary sat near the window.

Result:

POV Shift = False

unless additional evidence establishes a change in narrative focus.

### 3.3 Person Shift

A grammatical person shift is not automatically a POV shift.

I opened the door.
You closed it.

This contains:

1st person → 2nd person

Therefore:

Person Shift = True

However:

POV Shift = Not necessarily

The detector must not classify every grammatical person shift as a POV shift.

### 3.4 Change Within the Same Sentence

A change of character or internal experience between clauses of the same sentence must not automatically produce a POV shift.

Example:

John opened the door and Mary felt afraid.

The sentence contains two characters and an internal state.

However, this does not by itself constitute a POV shift because the change occurs within the same sentence.

The detector may use the clauses to analyze the sentence, but the POV shift decision must operate at the sentence level.

---

## 4. Internal State

An internal state represents an experience that provides evidence about a character's internal perspective.

Examples include:

### Cognition

- think
- know
- wonder
- believe
- remember
- realize
- suspect

Example:

John wondered where Mary was.

Result:

internal_state = True
experiencer = John

### Emotion

- fear
- hope
- love
- hate
- feel

Example:

Mary felt afraid.

Result:

internal_state = True
experiencer = Mary

### Perception

Examples:

- see
- hear
- notice
- observe

Perception verbs must be treated carefully.

The presence of a perception verb alone does not necessarily prove internal focalization.

Example:

John saw Mary enter the room.

The system must consider contextual evidence before determining whether this establishes an internal narrative focus.

---

## 5. Coreference

Coreference resolution is a required component.

The system must identify when different textual mentions refer to the same entity.

Example:

John entered the room.
He sat down.

The system should resolve:

He → John

Therefore the narrative focus remains:

John → John

and there is no POV shift.

### 5.1 Coreference Must Prevent False Positives

Example:

John wondered where Mary was.
He felt nervous.
Mary knew he was waiting.

Coreference:

He → John

Focus:

John → John → Mary

Expected POV shift:

John → Mary

The system must NOT interpret:

John → He

as a POV shift.

### 5.2 Ambiguous Coreference

Example:

John met Paul.
He smiled.

The system must not arbitrarily decide:

He → John

if the available evidence is insufficient.

The system should represent the reference as:

unresolved

or:

ambiguous

This prevents incorrect POV shift detection.

---

## 6. Narrative Focus

The system must maintain a representation of the current narrative focus.

The narrative focus represents the character whose internal experience currently guides the narration.

Example:

John wondered...

Focus:

John

Then:

He remembered...

After coreference resolution:

He → John

Focus remains:

John

Then:

Mary knew...

Focus becomes:

Mary

The focus history becomes:

John → John → Mary

The transition:

John → Mary

is a candidate POV shift only when the transition occurs between distinct narrative sentences and satisfies the POV shift detection requirements.

---

## 7. Focus Establishment vs Focus Shift

The system must distinguish between establishing a narrative focus and changing an existing focus.

Example:

John opened the door.
Mary felt afraid.

The first sentence does not necessarily establish an internal narrative focus.

The second sentence provides Mary's internal experience.

Therefore the system should be able to represent:

Focus Established = Mary

rather than automatically reporting:

POV Shift = John → Mary

A POV Shift requires a previously established narrative focus.

A character becoming the first established focus is not itself a POV shift.

---

## 8. Processing Pipeline

The system must implement the following logical pipeline:

Input Text
    |
    v
analyze()
    |
    v
resolve_coreference()
    |
    v
detect_internal_states()
    |
    v
update_focus()
    |
    v
detect_shift()
    |
    v
POVShift[]

The pipeline must preserve the textual order of sentences and clauses so that narrative focus can be evaluated in sequence.

---

## 9. Main Public Interface

The system must expose a main method:

def detect(self, text: str) -> list[POVShift]:
    ...

The caller provides raw English text.

The detector performs the complete analysis internally.

Example:

detector = POVShiftDetector()

shifts = detector.detect(text)

---

## 10. Functional Requirements

### FR-01 — Text Analysis

The system must analyze English text using spaCy.

It must obtain, when available:

- tokens;
- sentences;
- clauses;
- lemmas;
- part-of-speech tags;
- dependency relations;
- subjects;
- verbs;
- entities.

The analysis must preserve the original textual order of sentences and clauses.
The analysis must preserve the relationship between sentences and their constituent clauses.

### FR-02 — Clause Extraction

The system must represent relevant linguistic units as Clause objects.

Clauses must preserve their original order within the text.

The clause representation must retain enough information to support subject detection, internal-state detection, experiencer identification, and narrative-focus analysis.

A clause is an analysis unit; it must not independently produce a POV shift when it occurs within the same sentence as another clause.

### FR-03 — Character Representation

The system must represent narrative entities using Character objects.

Each Character must have:

- unique identifier;
- canonical name;
- textual mentions.

Different textual mentions referring to the same entity must resolve to the same Character whenever coreference can be established reliably.

### FR-04 — Coreference Resolution

The system must associate resolvable textual mentions with their corresponding Character.

Ambiguous references must not be resolved arbitrarily.

Unresolved or ambiguous references must remain explicitly marked as such.

Coreference resolution must occur before narrative-focus comparison.

### FR-05 — Internal State Detection

The system must determine whether a clause contains evidence of an internal state.

The system must classify internal states, when possible, as:

- cognition;
- emotion;
- perception.

The presence of an internal-state verb alone must not automatically establish a POV shift.

### FR-06 — Experiencer Detection

When a clause contains an internal state, the system must identify the Character experiencing that state when this can be determined reliably.

Example:

Mary feared the storm.

Result:

experiencer = Mary

If the experiencer cannot be determined reliably, it must remain unresolved rather than being inferred arbitrarily.

### FR-07 — Narrative Focus Tracking

The system must maintain the narrative focus while processing sentences in textual order.

The focus must be updated only when sufficient evidence exists.

The system must distinguish between:

- establishing the first narrative focus;
- maintaining the current focus;
- changing an established narrative focus.

### FR-08 — POV Shift Detection

The system must compare narrative focus states across consecutive narrative sentences.

The system must detect a POV shift only when all of the following conditions are satisfied:

1. a previous narrative focus has already been established;
2. a different Character becomes the narrative focus in a subsequent sentence;
3. the new focus is supported by sufficient evidence of internal experience;
4. the focus change is not based solely on a change of grammatical subject;
5. the focus change is not based solely on a change of character;
6. the focus change is not based solely on a grammatical person shift;
7. the relevant focus change is not merely a change between clauses within the same sentence.

### FR-09 — Evidence

Every detected POV shift must contain evidence explaining the decision.

Evidence may include:

- focus_changed;
- different_experiencer;
- internal_state;
- cognition;
- emotion;
- perception;
- coreference_resolved.

The evidence must correspond to information actually used by the detector when making the decision.

### FR-10 — Confidence

Every detected POV shift must contain a confidence value between:

0.0 and 1.0

Higher confidence must indicate stronger supporting evidence according to the detector's confidence model.

The confidence value must be reproducible for the same input and configuration.

---

## 11. Non-Functional Requirements

### NFR-01 — Modularity

Each processing stage must have a single primary responsibility.

The main detector must orchestrate the components rather than implement all linguistic logic itself.

### NFR-02 — Testability

Each processing stage must be independently testable.

The project must contain:

- unit tests;
- integration tests.

The implementation must allow the behavior defined by the functional requirements and detection rules to be verified through automated tests.

### NFR-03 — Explainability

The detector must provide evidence for detected POV shifts.

A simple boolean result is insufficient for the final domain model.

### NFR-04 — Robustness

The system must avoid making unsupported assumptions.

In particular:

- do not force ambiguous coreference;
- do not treat every subject change as a POV shift;
- do not treat every character change as a POV shift;
- do not treat every grammatical person shift as a POV shift;
- do not treat every mental or perception verb as automatic proof of focalization;
- do not report a POV shift based only on a change between clauses within the same sentence.

### NFR-05 — Extensibility

The architecture should allow future improvements such as:

- better coreference resolution;
- machine-learning classifiers;
- contextual verb classification;
- discourse analysis;
- free indirect discourse detection;
- narrator detection;
- confidence-scoring improvements.

These extensions must not require rewriting the entire detector.

---

## 12. Domain Objects

The minimum domain model must contain:

- Character
- Clause
- FocusState
- POVShift

---

## 13. Expected Output

For:

John wondered where Mary was.
Mary knew he was waiting.

the system should produce conceptually:

POVShift

from_character = John
to_character = Mary
confidence = 0.xx

evidence:
    - focus_changed
    - different_experiencer
    - internal_state

The exact confidence value depends on the implemented confidence model.

---

## 14. Important Design Principles

The system must NOT use a rule such as:

if subject != previous_subject:
    pov_shift = True

Nor:

if pronoun_changed:
    pov_shift = True

Nor:

if grammatical_person_changed:
    pov_shift = True

Nor:

if character_changed:
    pov_shift = True

Instead, the system must infer a POV shift from a change in narrative focus supported by internal-state evidence and satisfying the sentence-level POV shift conditions.

The fundamental conceptual relationship is:

Character
    |
    v
Experiencer
    |
    v
Narrative Focus
    |
    v
Focus Change
    |
    v
POV Shift

---

## 15. Success Criteria

The implementation will be considered successful if it can:

1. detect clear POV shifts;
2. reject simple subject changes;
3. reject simple character changes;
4. distinguish grammatical person shifts from POV shifts;
5. correctly resolve and use coreference information when possible;
6. avoid false shifts caused by pronouns;
7. avoid false shifts caused by ambiguous coreference;
8. track narrative focus across multiple sentences;
9. distinguish focus establishment from focus shift;
10. avoid reporting a POV shift caused only by clauses within the same sentence;
11. identify multiple POV shifts in the same text;
12. explain why each shift was detected;
13. handle ambiguous coreference without inventing information;
14. pass the defined unit and integration test cases.