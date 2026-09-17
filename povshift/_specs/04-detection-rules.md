# POV Shift Detection Rules

## Fundamental Principle

A POV shift must not be detected solely because of:

- subject change;
- character change;
- pronoun change;
- grammatical person change.

The detector must evaluate changes in narrative focus and the evidence supporting that change.

The detection rules below define the conditions and constraints used to determine whether a change in narrative focus constitutes a POV shift.

---


## RULE-01 — Subject Change Is Not a POV Shift

A change in grammatical subject does not, by itself, constitute a POV shift.

Example:

```text
John opened the door.
Mary entered.
```

There is a change of subject and character, but the sentences only describe observable actions.

Result:

```text
POV SHIFT = False
```

---


## RULE-02 — Character Change Is Not a POV Shift

A change from one character to another does not, by itself, constitute a POV shift.

A character becoming the subject, participant, or focus of an observable action is insufficient to establish a POV shift.

Example:

```text
John opened the door.
Mary entered.
```

The narrative mentions different characters, but there is no sufficient evidence of a change in internal narrative focus.

Result:

```text
POV SHIFT = False
```


---

## RULE-03 — Person Shift Is Not a POV Shift

A change in grammatical person does not, by itself, constitute a POV shift.

Example:

```text
I opened the door.
You closed it.
```

This represents a grammatical person shift, but it does not necessarily represent a POV shift.

Result:

```text
PERSON SHIFT = True
POV SHIFT = False
```

The detector must not automatically classify a grammatical person shift as a POV shift.

---

## RULE-04 — Internal State Provides Focalization Evidence

Evidence of an internal state provides evidence that the corresponding experiencer may represent the narrative focus.

Internal states may be classified as:

- cognition;
- emotion;
- perception.

Example:

```text
John wondered where Mary was.
```

The internal state `wondered` provides evidence associated with John's internal experience.

This evidence can contribute to establishing narrative focus.

The presence of an internal-state verb does not, by itself, establish a POV shift.


---

## RULE-05 — Same Experiencer Means No Shift

When consecutive narrative focus is associated with the same experiencer, there is no POV shift between those focus states.

Example:

```text
John wondered where Mary was.
He felt nervous.
```

Coreference:

```text
He -> John
```

Experiencers:

```text
John -> John
```

Focus:

```text
John -> John
```

Result:

```text
POV SHIFT = False
```


---

## RULE-06 — Different Experiencer Can Indicate a Shift

A change from one experiencer to a different experiencer can indicate a POV shift when the narrative focus was already established and the new experiencer provides sufficient evidence of internal experience.

A different experiencer alone is not sufficient to establish a POV shift.

The detector must also consider:

* whether a previous narrative focus was already established;
* whether the new experiencer provides internal-state evidence;
* whether the change occurs across distinct narrative sentences;
* whether the experiencer is reliably identified;
* whether the available evidence is sufficient to support the focus change.

Example:

```text
John wondered where Mary was.
Mary knew he was waiting.
```

Experiencers:

```text
John -> Mary
```

Both sentences provide evidence of internal states.

Focus:

```text
John -> Mary
```

The previous focus was established as John, and Mary subsequently provides sufficient evidence of a new narrative focus.

Result:

```text
POV SHIFT = True
```

Conceptually:

```text
Established previous focus
        +
Different experiencer
        +
New internal-state evidence
        +
Distinct narrative sentence
        +
Sufficient supporting evidence
        ↓
POV SHIFT
```

A different character or experiencer without sufficient evidence of a change in narrative focus must not automatically produce a POV shift.

---

## RULE-07 — Focus Establishment Is Not a Shift

The establishment of the first narrative focus must not be classified as a POV shift.

Example:

```text
John opened the door.
Mary felt afraid.
```

The first sentence does not necessarily establish an internal narrative focus.

The second sentence provides evidence associated with Mary's internal state.

Therefore, the detector should distinguish:

```text
FOCUS ESTABLISHED = Mary
```

from:

```text
POV SHIFT = John -> Mary
```

A focus establishment is not, by itself, a POV shift.


---

## RULE-08 — Coreference Must Be Resolved Before Focus Comparison

Coreference must be resolved before comparing narrative focus between characters.

Example:

```text
John wondered where Mary was.
He felt nervous.
```

If:

```text
He -> John
```

then the experiencer sequence is:

```text
John -> John
```

and no POV shift is detected.

Coreference information must therefore be available before the detector compares the experiencers or narrative focus of consecutive sentences.

---

## RULE-09 — Ambiguous Coreference Must Not Be Forced

When a reference cannot be resolved reliably, the detector must not arbitrarily assign it to a character.

Example:

```text
John met Paul.
He smiled.
```

The reference:

```text
He
```

must not be arbitrarily resolved as either:

```text
He -> John
```

or:

```text
He -> Paul
```

The reference must remain explicitly:

```text
ambiguous / unresolved
```

An ambiguous or unresolved reference must not be used as if it were a confidently resolved experiencer.

---

## RULE-10 — POV Shift Is Evaluated Across Sentences

POV shift detection is evaluated between narrative sentences.

Clauses are used for linguistic analysis, including the detection of internal states and experiencers, but a change between clauses within the same sentence must not automatically produce a POV shift.

Example:

```text
John opened the door and Mary felt afraid.
```

The text contains multiple clauses and may contain internal-state evidence associated with Mary.

However, the clauses belong to the same sentence.

Therefore, the detector must not automatically infer:

```text
John -> Mary
```

as a POV shift.

The distinction is:

```text
CLAUSES   -> linguistic analysis
SENTENCES -> POV shift decision
```

---

## RULE-11 — Confidence Must Reflect Supporting Evidence

Each detected POV shift must have a confidence value between:

```text
0.0 <= confidence <= 1.0
```

Confidence must reflect the supporting evidence used by the detector.

Stronger supporting evidence includes:

- previous internal state;
- new internal state;
- different experiencer;
- clear coreference;
- consecutive narrative focus.

Subject change, grammatical person shift, and observable action are not sufficient evidence by themselves to establish a POV shift.

The confidence value must be reproducible for the same input and configuration.



## Important Principles

The following principles summarize the fundamental decisions that must remain consistent across the detection rules.

### 1. Narrative focus is not the same as grammatical subject

The grammatical subject of a sentence does not necessarily represent the narrative focus.

A subject change alone must never be treated as sufficient evidence of a POV shift.

---

### 2. Character change is not necessarily focus change

The appearance of a different character does not necessarily mean that the narrative perspective has shifted to that character.

A character must have sufficient evidence of internal experience before becoming a candidate for narrative focus.

---

### 3. Internal-state evidence is central to focalization

Cognition, emotion, and perception provide evidence about a character's internal experience.

However, detecting an internal state does not automatically mean that a POV shift has occurred.

---

### 4. Experiencer identity is more important than grammatical role

The detector should compare the characters experiencing the relevant internal states rather than relying only on grammatical roles such as subject or object.

---

### 5. Coreference must precede focus comparison

Pronouns and other references must be resolved before their associated characters are used to compare narrative focus.

Ambiguous references must remain ambiguous rather than being assigned arbitrarily.

---

### 6. Focus establishment is different from focus change

The first reliably established narrative focus is not a POV shift.

A POV shift requires an already established focus and sufficient evidence that the focus subsequently changes.

---

### 7. POV shifts are evaluated between sentences

Clauses provide linguistic evidence for the analysis, but the decision about whether a POV shift occurred is made across narrative sentences.

A change of internal state between clauses belonging to the same sentence must not automatically produce a POV shift.

---

### 8. Multiple signals must be considered together

POV shift detection must not depend on a single superficial linguistic signal.

The detector should consider the combination of:

- narrative focus;
- experiencer identity;
- internal-state evidence;
- coreference resolution;
- sentence boundaries;
- supporting evidence.

---

### 9. Absence of sufficient evidence means no forced decision

When the available linguistic evidence is insufficient or ambiguous, the detector must not invent a character, experiencer, coreference, or POV shift.

---

### 10. Detection must be explainable

A detected POV shift must be supported by evidence that corresponds to information actually used by the detector.

The resulting confidence must be reproducible for the same input and configuration.