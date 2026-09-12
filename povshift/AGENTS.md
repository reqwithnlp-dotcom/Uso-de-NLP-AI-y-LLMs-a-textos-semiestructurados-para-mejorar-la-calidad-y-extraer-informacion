# AGENTS.md — Instructions for AI Coding Agents

This project follows a **spec-anchored / spec-driven design** approach.
The specification in `_specs/` is the source of truth. It was built
iteratively and reviewed for internal consistency — treat it as
authoritative, not as a rough draft to improve on.

## Before writing any code

Read, in this order:

1. `_specs/requirements.md` — FR-01 to FR-11, NFR-01 to NFR-05
2. `_specs/detection-rules.md` — RULE-01 to RULE-11
3. `_specs/test-cases.md` — TC-01 to TC-24
4. `_specs/domain-model.md` — `Character`, `Clause`, `FocusState`, `POVShift`
5. `_specs/architecture.md` — pipeline, components, responsibilities
6. `_specs/traceability.md` — how everything above maps together, and
   known open decisions/limitations

## Hard rules

- **Do not invent new requirements, rules, or test cases.** If the spec
  seems to be missing something needed to implement a feature, stop and
  flag the gap instead of silently adding an ID or behavior.
- **Do not rename or renumber IDs** (`FR-xx`, `NFR-xx`, `RULE-xx`,
  `TC-xx`). They are referenced across multiple documents.
- **Do not merge responsibilities across documents.** Requirements,
  rules, domain model, architecture, and test cases each live in their
  own file for a reason — don't fold rule logic into the domain model,
  or test expectations into requirements.
- **Implement exactly the pipeline in `architecture.md`:**
  `analyze() → resolve_coreference() → detect_internal_states() →
  update_focus() → detect_shift()`, orchestrated by `detect()`. Don't
  collapse stages into one function, even if it seems simpler.
- **Domain objects must match `domain-model.md` field-for-field.** Don't
  add convenience fields without checking the spec first.
- **Clause is a unit of linguistic analysis; the sentence is the unit for
  POV shift decisions.** This distinction (via `sentence_index`) is
  foundational — never let two clauses in the same sentence produce a
  shift on their own (see `RULE-10`, `TC-22`).
- **Every `POVShift` needs real `evidence` and a reproducible
  `confidence`** (`FR-09`, `FR-10`, `RULE-11`) — don't return a shift
  without evidence that was actually used, and don't hardcode confidence.

## Known open decisions (see `traceability.md` §6)

These were deliberate, documented trade-offs — don't try to "fix" them
without raising it first:

- `"I"` / `"You"` are each modeled as their own `Character` with a
  literal `canonical_name`. This does **not** generalize to
  multi-speaker dialogue; that's accepted for now.
- `Clause.subject` / `Clause.experiencer` use `None` for both "no
  evidence" and "ambiguous/unresolved." There is no separate explicit
  ambiguity state.
- Grammatical person (1st/2nd/3rd) is **not** a tracked field anywhere
  in the domain model. Don't add a `person` or `person_shift` attribute
  — `RULE-03` is satisfied through the focus/evidence logic, not through
  an explicit person field.
- Which component creates `Character` objects for `"I"`/`"You"`
  (`NLPParser` vs `CoreferenceResolver`) is intentionally left
  unspecified — use your judgment, but keep it inside one of those two
  components, not spread across both.

## Coding conventions

- Python, using spaCy's English model for `analyze()`.
- The domain model must not depend on spaCy — no `Doc`, `Token`, or
  other spaCy objects should leak out of `analyze()`/`NLPParser`.
- `domain-model.md` shows `FocusState` explicitly as a `@dataclass`.
  Apply the same pattern consistently to `Character`, `Clause`, and
  `POVShift` unless you have a concrete reason not to.
- Match the project structure in `specs/architecture.md` §14 /
  `README.md` exactly (`src/pov_detector/...`, `tests/unit/...`,
  `tests/integration/...`).

## When implementing test cases

Every test in `specs/test-cases.md` should become an actual automated
test (`pytest`), placed under `tests/unit/` or `tests/integration/`
according to which section of `test-cases.md` it comes from. Keep the
`TC-xx` ID in the test name or docstring so it stays traceable back to
the spec.

## If you find a genuine inconsistency

Don't silently resolve it. Point it out — which documents disagree, and
why — before changing behavior or adding to the spec. This mirrors how
the specification itself was built.
