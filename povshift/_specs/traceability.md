# POV Shift Detector — Traceability Matrix

## 1. Purpose

This document reflects the *actual* relationships between the elements
already defined in the other specification documents:

```text
Requirement (FR / NFR)
    ↓
Rule (RULE)
    ↓
Test Case (TC)
    ↓
Implementation Component
```

No new requirements, rules, or test cases are introduced here. Every
relationship below already existed implicitly across `requirements.md`,
`detection-rules.md`, `test-cases.md`, `domain-model.md`, and
`architecture.md` — this document only consolidates them in one place.

---

## 2. Functional Requirements → Rules → Test Cases → Component

| FR | Title | Related RULE(s) | Related TC(s) | Implementing Component |
|----|-------|------------------|----------------|--------------------------|
| FR-01 | Text Analysis | — | TC-01, TC-02 | `NLPParser` (`analyze()`) |
| FR-02 | Clause Extraction | RULE-10 | TC-01, TC-02, TC-22 | `NLPParser` (`analyze()`) |
| FR-03 | Character Representation | — | TC-04, TC-05, TC-06 | domain model (`Character`) / `CoreferenceResolver` |
| FR-04 | Coreference Resolution | RULE-08, RULE-09 | TC-04, TC-05, TC-06, TC-11, TC-14, TC-21 | `CoreferenceResolver` (`resolve_coreference()`) |
| FR-05 | Internal State Detection | RULE-04 | TC-07, TC-08, TC-09, TC-23 | `InternalStateDetector` (`detect_internal_states()`) |
| FR-06 | Experiencer Detection | RULE-05, RULE-06 | TC-07, TC-08, TC-17, TC-23 | `InternalStateDetector` (`detect_internal_states()`) |
| FR-07 | Narrative Focus Tracking | RULE-07 | TC-10, TC-11, TC-12 | `NarrativeFocusTracker` (`update_focus()`) |
| FR-08 | POV Shift Detection | RULE-01, RULE-02, RULE-03, RULE-05, RULE-06, RULE-07, RULE-08, RULE-09, RULE-10 | TC-13, TC-14, TC-15, TC-16, TC-17, TC-18, TC-19, TC-20, TC-21, TC-22 | `ShiftDetector` (`detect_shift()`) |
| FR-09 | Evidence | RULE-11 (indirectly, via confidence/evidence coupling) | TC-18, TC-20, TC-21, TC-24 | `ShiftDetector` (`detect_shift()`) |
| FR-10 | Confidence | RULE-11 | TC-24 | `ShiftDetector` (`detect_shift()`) |
| FR-11 | Input Validation | — (not a detection rule; input-level concern) | TC-03 | `POVShiftDetector` (`detect()`) |

**Note on FR-03 / FR-04 overlap:** as decided during the `requirements.md`
review, FR-03 and FR-04 intentionally share responsibility over
resolving mentions to the same `Character`. This redundancy was accepted
explicitly and is reflected here rather than resolved.

---

## 3. Non-Functional Requirements → Test Cases / Architecture

| NFR | Title | How it's addressed |
|-----|-------|----------------------|
| NFR-01 | Modularity | `architecture.md` §11 (component separation: `NLPParser`, `CoreferenceResolver`, `InternalStateDetector`, `NarrativeFocusTracker`, `ShiftDetector`, `POVShiftDetector`). Not directly tied to a specific TC — verified structurally, not behaviorally. |
| NFR-02 | Testability | All 24 TCs, split into unit (TC-01–TC-09), focus (TC-10–TC-12), POV shift (TC-13–TC-17), and integration (TC-18–TC-24) tests, per `test-cases.md` §"Testing strategy". |
| NFR-03 | Explainability | FR-09 (`POVShift.evidence`) and `FocusState.reason` (`domain-model.md` §4) → TC-18, TC-20, TC-21, TC-24. |
| NFR-04 | Robustness | RULE-01, RULE-02, RULE-03, RULE-09, RULE-10 → TC-06, TC-15, TC-16, TC-21, TC-22. |
| NFR-05 | Extensibility | `architecture.md` §13 (component boundaries allow independent replacement, e.g. of `CoreferenceResolver`). Architectural quality, not covered by a specific TC. |

---

## 4. Detection Rules → Test Cases

| RULE | Title | Related TC(s) |
|------|-------|----------------|
| RULE-01 | Subject Change Is Not a POV Shift | TC-15 |
| RULE-02 | Character Change Is Not a POV Shift | TC-15 |
| RULE-03 | Person Shift Is Not a POV Shift | TC-16 |
| RULE-04 | Internal State Provides Focalization Evidence | TC-07, TC-08, TC-09, TC-23 |
| RULE-05 | Same Experiencer Means No Shift | TC-11, TC-14 |
| RULE-06 | Different Experiencer Can Indicate a Shift | TC-12, TC-13, TC-17, TC-20 |
| RULE-07 | Focus Establishment Is Not a Shift | TC-10 |
| RULE-08 | Coreference Must Be Resolved Before Focus Comparison | TC-04, TC-05, TC-11, TC-14, TC-21 |
| RULE-09 | Ambiguous Coreference Must Not Be Forced | TC-06 |
| RULE-10 | POV Shift Is Evaluated Across Sentences | TC-22 |
| RULE-11 | Confidence Must Reflect Supporting Evidence | TC-24 |

---

## 5. Coverage Check

- Every FR (FR-01 → FR-11) has at least one associated TC. No orphan FRs.
- Every RULE (RULE-01 → RULE-11) has at least one associated TC. No orphan RULEs.
- Every NFR is addressed either by TCs or by an architectural mechanism.
- Every TC (TC-01 → TC-24) traces back to at least one FR.
- No new FR, NFR, RULE, or TC was created to fill a gap; where a gap was
  found (see §6), it was resolved by adjusting scope/wording of an
  existing document, not by inventing a new ID.

---

## 6. Open Decisions / Known Limitations Carried Forward

These were raised and explicitly decided during the review process. They
are not defects — they are documented trade-offs that a future
implementer should be aware of:

1. **Deictic pronouns ("I" / "You") as `Character`** — `domain-model.md`
   §2. Accepted simplification for `TC-17`; does not generalize to
   multi-speaker dialogue. Revisit if multi-speaker text is ever in
   scope.
2. **`None` overloaded for "no evidence" vs. "ambiguous/unresolved"** —
   `domain-model.md` §3, on `Clause.subject` / `Clause.experiencer`.
   Accepted simplification; reduces explainability detail in ambiguous
   cases.
3. **Grammatical person is not a tracked domain field** — `FR-08`
   condition 6 and `RULE-03` are satisfied by the overall focus/evidence
   logic, not by an explicit "person" attribute. `TC-16` / `TC-17` no
   longer assert a `grammatical person shift` field; it remains only as
   narrative context in `test-cases.md`.
4. **Component responsible for creating `Character` objects for "I"/"You"**
   is left unspecified in `architecture.md` (§13) — deferred as a minor
   implementation detail, to be resolved during implementation rather
   than in the specification.

---

## 7. Status

All specification documents (`requirements.md`, `detection-rules.md`,
`test-cases.md`, `domain-model.md`, `architecture.md`) are stable and
mutually consistent as of this traceability matrix. This set is ready to
be used as the anchor for implementation.
