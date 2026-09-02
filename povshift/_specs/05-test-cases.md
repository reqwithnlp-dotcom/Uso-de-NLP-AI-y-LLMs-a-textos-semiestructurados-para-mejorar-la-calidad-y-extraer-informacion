# POV Shift Detector — Test Cases

## Testing strategy

Tests must exist at two levels:

1. Unit tests
2. Integration tests

Unit tests verify each processing stage. Integration tests verify the complete detector.

---

## Unit Tests

### TC-01 — Simple clause

Input:

```text
John opened the door.
```

Expected:

- one clause
- subject = John
- verb = open

---

### TC-02 — Multiple Sentences

Input:

```text
John opened the door.
Mary entered.
```

Expected:

* two sentences;
* two clauses;
* Clause 1 belongs to sentence 0;
* Clause 2 belongs to sentence 1;
* the clauses preserve their original textual order.

---

### TC-03 — Empty text

Input: empty string

Expected: `ValueError`

---

### TC-04 — Coreference

Input:

```text
John entered the room.
He sat down.
```

Expected: `He -> John`

---

### TC-05 — Female coreference

Input:

```text
Mary entered the room.
She sat down.
```

Expected: `She -> Mary`

---

### TC-06 — Ambiguous coreference

Input:

```text
John met Paul.
He smiled.
```

Expected: Reference must be marked ambiguous or unresolved; do not arbitrarily choose John or Paul.
---

### TC-07 — Cognitive state

Input:

```text
John wondered where Mary was.
```

Expected:

- `internal_state = True`
- `state_type = cognition`
- `experiencer = John`

---

### TC-08 — Emotional state

Input:

```text
Mary felt afraid.
```

Expected:

- `internal_state = True`
- `state_type = emotion`
- `experiencer = Mary`

---

### TC-09 — Observable action

Input:

```text
John opened the door.
```

Expected: `internal_state = False`

---

## Focus Tests

### TC-10 — Initial focus

Input:

```text
John wondered about Mary.
```

Expected:
- FocusState.character = John
- focus establishment = True
- POV Shift = False

---

### TC-11 — Same focus through coreference

Input:

```text
John wondered about Mary.
He felt nervous.
```

Expected: Focus history `John -> John` (No POV shift).

---

### TC-12 — Focus change

Input:

```text
John wondered about Mary.
Mary knew he was waiting.
```

Expected: Focus history `John -> Mary`.

---

## POV Shift Tests

### TC-13 — Clear POV Shift

Input:

```text
John wondered where Mary was.
Mary knew he was waiting.
```

Expected: POV Shift = True (from `John` to `Mary`).

---

### TC-14 — No POV Shift

Input:

```text
John wondered where Mary was.
He knew she was coming.
```

Expected: POV Shift = False (because `He -> John`, focus `John -> John`).

---

### TC-15 — Character change without POV shift

Input:

```text
John opened the door.
Mary entered.
```

Expected: POV Shift = False (only observable actions).

---

### TC-16 — Person Shift Without Internal-State Evidence

Input:

```text
I opened the door.
You closed it.
```

Expected:

* grammatical person shift = True;
* POV Shift = False.

Reason:

The change from first person to second person is a grammatical person shift, but there is no sufficient evidence of a change in narrative focus based on internal experience.

---

### TC-17 — Person Shift With Internal-State Evidence

Input:

```text
I felt nervous.
You felt angry.
```

Expected:

* grammatical person shift = True;
* first sentence experiencer = I;
* second sentence experiencer = You;
* both sentences provide internal-state evidence;
* focus changes from `I` to `You`;
* POV Shift = True.

Reason:

The grammatical person shift alone is not sufficient. In this case, both sentences provide internal-state evidence and the experiencer changes from `I` to `You` across sentence boundaries.

---

## Integration Tests

### TC-18 — Complete pipeline (shift)

Input:

```text
John wondered where Mary was.
Mary knew he was waiting.
```

Expected output:

```python
[
    POVShift(
        from_character=John,
        to_character=Mary
    )
]
```

---

### TC-19 — Complete pipeline (no shift)

Input:

```text
John wondered where Mary was.
He felt nervous.
He remembered their conversation.
```

Expected: `[]` (no POV shifts). Focus history: `John -> John -> John`.

---

### TC-20 — Multiple shifts

Input:

```text
John wondered where Mary was.
Mary knew he was waiting.
John remembered the conversation.
```

Expected: Two POV shifts: `John -> Mary` and `Mary -> John` (total 2).

---

### TC-21 — Critical regression: coreference must prevent false POV shift

Input:

```text
John wondered where Mary was.
He felt nervous.
Mary knew he was waiting.
```

Expected focus: `John -> John -> Mary`.

Expected POV shifts: only `John -> Mary` (do NOT interpret `John -> He` as a POV shift).

This test prevents false positives caused by incorrect coreference resolution.



### TC-22 — Multiple Clauses Within the Same Sentence

Input:

```text
John opened the door and Mary felt afraid.
```

Expected:

* one sentence;
* two clauses;
* Clause 1: `subject = John`, `internal_state = False`;
* Clause 2: `subject = Mary`, `internal_state = True`, `experiencer = Mary`;
* no POV shift is detected.

Expected result:

```text
POV SHIFT = False
```

Reason:

The change from John to Mary occurs between clauses belonging to the same sentence. Clauses are used for linguistic analysis, but POV shift detection is evaluated across sentences.

---

### TC-23 — Perception State

Input:

```text
John saw Mary leaving the room.
```

Expected:

* `internal_state = True`
* `state_type = perception`
* `experiencer = John`

Reason:

The clause contains a perceptual experience associated with John. The detector must classify this evidence as `perception`.

This test verifies that perception is represented as a distinct internal-state category from cognition and emotion. It does not imply that every perception verb automatically establishes a narrative focus or produces a POV shift.

---

### TC-24 — Confidence

Input:

```text
John wondered where Mary was.
Mary knew he was waiting.
```

Expected:

* exactly one POV shift;
* `from_character = John`;
* `to_character = Mary`;
* `confidence` is between `0.0` and `1.0`;
* the same input and configuration produce the same confidence value.

Reason:

The detector must produce a bounded and reproducible confidence value for the same evidence.
