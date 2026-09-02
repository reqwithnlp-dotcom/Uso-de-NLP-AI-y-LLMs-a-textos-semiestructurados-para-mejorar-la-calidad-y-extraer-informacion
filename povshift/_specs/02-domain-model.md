# POV Shift Detector — Domain Model

## 1. Overview

The domain model represents the concepts that the POV Shift Detector needs to reason about.

The main domain classes are:

* `Character`
* `Clause`
* `FocusState`
* `POVShift`

Each class has a different responsibility. The model keeps linguistic information, narrative state, and detection results separated.

The model does not introduce a separate `Sentence` domain class.

However, sentence boundaries are explicitly represented through `sentence_index`, because clauses are used for linguistic analysis while POV shift decisions are evaluated across sentences.

The fundamental distinction is:

```text
Clause
    ↓
linguistic analysis

Sentence boundary
    ↓
focus comparison

FocusState
    ↓
focus change

POVShift
```

---

## 2. Character

`Character` represents a narrative entity that can participate in the narrative and potentially become the focus of the narration.

Python representation:

```python
class Character:
    id: int
    canonical_name: str
    mentions: list[str]
```

### Attributes

#### `id`

Unique identifier for the character within the analyzed document.

Example:

```python
id = 1
```

#### `canonical_name`

Canonical name used to identify the character.

Example:

```python
canonical_name = "John"
```

#### `mentions`

List of textual mentions that refer to the same character.

Example:

```python
mentions = [
    "John",
    "he",
    "the man"
]
```

Mentions may include names, pronouns, or other textual references when they have been resolved to the same character.

Example:

```text
John entered the room.
He sat down.
```

The system should represent both mentions as referring to the same `Character`:

```text
John
 ↑
 |
He
```

### Purpose

`Character` provides a stable identity across different textual mentions.

This prevents the detector from incorrectly interpreting a change such as:

```text
John → He
```

as a change of character or narrative focus when coreference has established that both mentions refer to the same character.

An ambiguous or unresolved reference must not be arbitrarily assigned to a `Character`.

---

## 3. Clause

`Clause` represents a linguistic unit extracted and analyzed from the text.

It contains the information required by later stages of the POV detection pipeline.

Python representation:

```python
class Clause:
    text: str
    sentence_index: int
    subject: Character | None
    verb: str | None
    internal_state: bool
    state_type: str | None
    experiencer: Character | None
```

### Attributes

#### `text`

The original textual content of the clause.

Example:

```python
text = "John wondered where Mary was"
```

#### `sentence_index`

Index of the sentence containing the clause.

Example:

```python
sentence_index = 0
```

This attribute is important because clauses are used for linguistic analysis, while POV shift detection is evaluated across sentences.

For example:

```text
John opened the door and Mary felt afraid.
```

may be represented as:

```text
sentence_index = 0

Clause 0:
    sentence_index = 0

Clause 1:
    sentence_index = 0
```

Therefore, the detector can distinguish multiple clauses within the same sentence from clauses belonging to consecutive sentences.

#### `subject`

The grammatical subject of the clause when it can be identified and reliably associated with a `Character`.

Example:

```python
subject = john
```

If the subject cannot be reliably resolved to a `Character`:

```python
subject = None
```

A subject change must not automatically be interpreted as a character change or POV shift.

#### `verb`

The relevant main verb or predicate.

The preferred representation is the lemma rather than only the surface form.

Example:

```text
wondered → wonder
```

Therefore:

```python
verb = "wonder"
```

#### `internal_state`

Indicates whether the clause provides evidence of an internal state.

Possible values:

```python
True
False
```

Example:

```text
John wondered where Mary was.
```

```python
internal_state = True
```

Example:

```text
John opened the door.
```

```python
internal_state = False
```

The presence of an internal state does not automatically produce a POV shift.

#### `state_type`

Classifies the internal state when possible.

Expected categories:

```text
"cognition"
"emotion"
"perception"
None
```

Example:

```text
John wondered where Mary was.
```

```python
state_type = "cognition"
```

#### `experiencer`

The `Character` experiencing the internal state when this can be determined reliably.

Example:

```text
Mary felt afraid.
```

```python
experiencer = mary
```

If the experiencer cannot be determined reliably:

```python
experiencer = None
```

The system must not invent an experiencer.

### Purpose

`Clause` acts as the bridge between linguistic analysis and narrative analysis.

The detector uses the information contained in `Clause` to determine:

* grammatical subject;
* relevant verb;
* whether an internal state exists;
* type of internal state;
* experiencer;
* sentence membership.

`Clause` is an analysis unit. It does not independently represent a POV shift.

---

## 4. FocusState

`FocusState` represents the narrative focus established or maintained at a particular sentence.

It represents a state, rather than a change between states.

Python representation:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class FocusState:
    character: Optional["Character"]
    sentence_index: int
    reason: Optional[str] = None
```

### Attributes

#### `character`

The character currently considered the narrative focus.

Example:

```python
character = john
```

If the system cannot establish a reliable narrative focus:

```python
character = None
```

#### `sentence_index`

Index of the sentence associated with this focus state.

Example:

```python
sentence_index = 0
```

The focus state is associated with a sentence rather than directly with a clause because POV shift detection operates across sentences.

Clauses within that sentence can provide the evidence used to establish the focus.

#### `reason`

Explanation for why the focus state was established or updated.

The reason may refer to the evidence used by the detector, such as:

```text
"internal_state"
"cognition"
"emotion"
"perception"
```

If no specific reason is available:

```python
reason = None
```

The `reason` attribute is explanatory information. It does not define an additional focus category or detection rule.

### Example

Given:

```text
John wondered where Mary was.
```

The system may produce:

```python
FocusState(
    character=john,
    sentence_index=0,
    reason="internal_state"
)
```

Then:

```text
Mary knew he was waiting.
```

The system may produce:

```python
FocusState(
    character=mary,
    sentence_index=1,
    reason="internal_state"
)
```

The focus history is therefore:

```text
John → Mary
```

### Purpose

`FocusState` allows the system to maintain the narrative focus in textual order.

The `update_focus()` processing stage creates or updates focus states.

The `detect_shift()` processing stage compares focus states associated with consecutive narrative sentences.

Focus establishment itself is not a POV shift.

---

## 5. POVShift

`POVShift` represents a detected change in narrative focus.

It is the final domain result produced by the detection process.

Python representation:

```python
class POVShift:
    from_character: Character
    to_character: Character
    sentence_index: int
    confidence: float
    evidence: list[str]
```

### Attributes

#### `from_character`

The character who previously held the narrative focus.

Example:

```python
from_character = john
```

#### `to_character`

The character who becomes the new narrative focus.

Example:

```python
to_character = mary
```

#### `sentence_index`

Index of the sentence in which the new focus is detected.

For a shift:

```text
Sentence 0 → John
Sentence 1 → Mary
```

the resulting `POVShift` is associated with:

```python
sentence_index = 1
```

This represents the destination sentence of the focus change.

The shift is therefore understood as:

```text
previous sentence focus
        ↓
new sentence focus
        ↓
POVShift at new sentence
```

#### `confidence`

Confidence score assigned by the detector.

The value must satisfy:

```text
0.0 <= confidence <= 1.0
```

The confidence value must be reproducible for the same input and configuration.

The domain model does not prescribe a specific numerical value or scoring formula.

#### `evidence`

List of evidence supporting the detected shift.

Example:

```python
evidence = [
    "focus_changed",
    "different_experiencer",
    "internal_state"
]
```

Evidence must correspond to information actually used by the detector.

Possible evidence includes:

* `focus_changed`
* `different_experiencer`
* `internal_state`
* `cognition`
* `emotion`
* `perception`
* `coreference_resolved`

### Purpose

`POVShift` represents the conclusion reached by the detector.

It contains enough information to explain:

* from whom the focus changed;
* to whom the focus changed;
* in which sentence the new focus was detected;
* with what confidence;
* based on which evidence.

---

## 6. Relationship Between the Classes

The conceptual relationship is:

```text
Clause
 |
 +---- subject ------> Character
 |
 +---- experiencer --> Character
 |
 +---- internal_state
 |
 +---- state_type
 |
 +---- sentence_index
 |
 v
FocusState
 |
 | compare across sentences
 v
POVShift
```

The complete conceptual flow is:

```text
Text
 |
 v
Clause
 |
 +---- linguistic evidence
 |
 +---- experiencer
          |
          v
      Character
          |
          v
    Narrative Focus
          |
          v
     FocusState
          |
          v
    Focus Change
          |
          v
       POVShift
```

The important distinction is:

```text
CLAUSE
    ↓
linguistic analysis

SENTENCE
    ↓
unit across which focus is compared

FOCUS STATE
    ↓
narrative state

POV SHIFT
    ↓
detected focus change
```

A separate `Sentence` domain class is not required by the current specification.

The `sentence_index` on `Clause`, `FocusState`, and `POVShift` is sufficient to preserve the distinction required by the current rules.

---

## 7. Important Separation of Responsibilities

The domain classes must not contain the entire detection algorithm.

The domain model represents information and results.

The processing logic belongs to detector services or components such as:

```text
analyze()
resolve_coreference()
detect_internal_states()
update_focus()
detect_shift()
```

Responsibilities are therefore separated as follows:

### `Character`

Represents a stable narrative entity.

### `Clause`

Represents analyzed linguistic information.

### `FocusState`

Represents the narrative focus associated with a sentence.

### `POVShift`

Represents a detected change between narrative focus states.

The domain model does not determine the detection algorithm by itself.

---

## 8. Example of the Complete Model

Input:

```text
John wondered where Mary was.
Mary knew he was waiting.
```

### Linguistic analysis

```text
Sentence 0

Clause 0:
    text = "John wondered where Mary was"
    sentence_index = 0
    subject = John
    verb = "wonder"
    internal_state = True
    state_type = "cognition"
    experiencer = John
```

```text
Sentence 1

Clause 1:
    text = "Mary knew he was waiting"
    sentence_index = 1
    subject = Mary
    verb = "know"
    internal_state = True
    state_type = "cognition"
    experiencer = Mary
```

### Characters

```text
Character(1, "John")
Character(2, "Mary")
```

The mention:

```text
he
```

is resolved to John.

### Focus states

```python
FocusState(
    character=john,
    sentence_index=0,
    reason="internal_state"
)

FocusState(
    character=mary,
    sentence_index=1,
    reason="internal_state"
)
```

Focus history:

```text
John → Mary
```

### Detected result

```python
POVShift(
    from_character=john,
    to_character=mary,
    sentence_index=1,
    confidence=<reproducible value between 0.0 and 1.0>,
    evidence=[
        "focus_changed",
        "different_experiencer",
        "internal_state"
    ]
)
```

The exact confidence value and scoring method are implementation concerns governed by `FR-10` and `RULE-11`.

---

## 9. Multiple Clauses Within One Sentence

The model must preserve the distinction between clauses and sentences.

Example:

```text
John opened the door and Mary felt afraid.
```

This may be represented as:

```text
Sentence 0

Clause 0:
    sentence_index = 0
    subject = John
    internal_state = False

Clause 1:
    sentence_index = 0
    subject = Mary
    internal_state = True
    state_type = "emotion"
    experiencer = Mary
```

Both clauses belong to the same sentence:

```text
Clause 0 ─┐
          ├── Sentence 0
Clause 1 ─┘
```

Therefore, the change from John to Mary must not automatically produce:

```text
POV SHIFT = True
```

The model supports the distinction:

```text
CLAUSES
    ↓
linguistic evidence

SAME sentence_index
    ↓
no cross-sentence focus comparison
```

This is consistent with `RULE-10`.

---

## 10. Core Principle

The most important relationship in the model is:

```text
Character
    ↓
Experiencer
    ↓
Narrative Focus
    ↓
Focus Change
    ↓
POVShift
```

However:

```text
Character change
    ≠
POV shift
```

```text
Subject change
    ≠
POV shift
```

```text
Grammatical person change
    ≠
POV shift
```

A `POVShift` requires evidence that the narrative focus has moved from one character's internal experience to another character's internal experience.

Clauses provide the linguistic evidence required to establish this focus, while sentence boundaries determine where focus comparisons are evaluated.
