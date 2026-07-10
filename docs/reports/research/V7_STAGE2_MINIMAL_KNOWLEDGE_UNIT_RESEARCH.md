# V7 Stage 2 Minimal Knowledge Unit Research

Date: 2026-07-07

Status: `FINAL`

Scope:

```text
Independent research only.
No Stage 2 program change.
No Stage 2.2 result change.
No Stage 2.3 execution.
No new entity creation.
```

Primary evidence:

- `docs/programs/V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM.md`
- `docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION.md`

## 1. Research Question

Determine the minimum engineering unit of knowledge in Stage 2.

The research does not assume the answer in advance.

## 2. Evidence Summary

The Stage 2 program defines:

| Program mechanism | Evidence |
|---|---|
| Knowledge Object Model | A Knowledge Object is a durable engineering conclusion, rule, boundary, responsibility, relationship, lifecycle, owner mapping, or discovery. |
| Stage 2.2 Extraction Unit | The minimum Stage 2.2 input unit is one approved Knowledge Candidate. |
| Stage 2.2 Output Unit | One Knowledge Candidate may produce zero, one, or multiple Knowledge Objects. |
| Multiple Object Rule | Multiple objects are allowed when a candidate contains separable atomic knowledge units with distinct category, owner, consumer, destination, terminal state, or forbidden misuse. |
| Stage 2.3 Boundary | Deduplication collapses repeated knowledge into canonical concepts while preserving provenance. |
| Stage 2.5 Boundary | Canonical Architecture Knowledge is created only after extraction, deduplication, and graph work. |

The Stage 2.2 report shows:

| Stage 2.2 result | Count |
|---|---:|
| Queue candidates processed | 24 |
| Knowledge Objects created | 20 |
| `MULTIPLE_OBJECTS_CREATED` dispositions | 0 |
| `MANUAL_REVIEW` dispositions | 3 |
| `NO_OBJECT_CREATED` dispositions | 1 |
| Deduplication performed | 0 |
| Graph created | 0 |
| Canonical Knowledge created | 0 |

## 3. Finding: Minimum Engineering Unit

The minimum engineering unit of knowledge in Stage 2 is:

```text
Knowledge Object
```

It is not:

- a source document;
- a report;
- a Knowledge Candidate;
- a queue item;
- a future graph node;
- a canonical concept;
- a canonical prose section.

Reason:

The program treats a Knowledge Candidate as the minimum Stage 2.2 input unit, not as the minimum knowledge unit. The candidate is an extraction work package discovered during Stage 2.1. The Knowledge Object is the reusable engineering knowledge unit created by Stage 2.2 and consumed by Stage 2.3.

## 4. Research Checks

### 4.1 Can One Knowledge Candidate Legitimately Produce Multiple Independent Engineering Knowledge Units?

Verdict:

```text
YES
```

Evidence:

The Stage 2.2 program explicitly permits:

```text
Knowledge Candidate
  -> zero / one / multiple Knowledge Objects
```

Multiple Knowledge Objects are legitimate when a candidate contains separable atomic units with different category, owner, consumer, destination, terminal state, provenance, or forbidden misuse.

Conclusion:

This is already covered by the current program. No new entity is required to express this relationship.

### 4.2 Is The Current Knowledge Object The Atomic Engineering Unit?

Verdict:

```text
YES, BY PROGRAM DEFINITION
```

Evidence:

The Knowledge Object Model defines the object as one durable engineering conclusion, rule, boundary, responsibility, relationship, lifecycle, owner mapping, or discovery.

Stage 2.2 creation rules require one object only when the candidate contains one atomic knowledge unit.

Conclusion:

The program already defines Knowledge Object as the atomic engineering unit for Stage 2 extraction.

### 4.3 If Not Atomic, What Is Currently Being Prematurely Combined?

Verdict:

```text
NO PROVEN NON-ATOMIC PROGRAM DEFECT
```

Observed risk:

Some Stage 2.2 objects are broad because Stage 1 architecture laws are broad. Examples include:

- Authority Boundary;
- Runtime Apply Boundary;
- Forbidden Stage 2 Actions;
- Program State Machine and Stage Gates;
- Producer / Consumer Model.

Analysis:

Broad is not automatically non-atomic. A boundary object may include both what the owner is allowed to own and what it must not do. A lifecycle object may include a complete sequence. A forbidden-action object may include multiple forbidden examples when all examples protect the same boundary.

The program's actual atomicity test is not sentence count. The test is whether the object merges separable units with different category, owner, consumer, destination, terminal state, provenance, or forbidden misuse.

No evidence proves that the program itself forces premature combination.

Execution note:

Stage 2.2 created no `MULTIPLE_OBJECTS_CREATED` disposition. That is an execution observation, not an architectural defect by itself. The current program already allowed multiple objects if required.

### 4.4 Did Stage 2.2 Perform Stage 2.3 Responsibilities?

Verdict:

```text
NO
```

Evidence:

Stage 2.3 responsibilities are:

- review every extracted object for duplication;
- merge duplicate concepts;
- preserve provenance;
- create Deduplicated Knowledge Registry;
- create Knowledge Merge Map;
- create Superseded Knowledge Map.

Stage 2.2 report records:

- Deduplication Performed = 0;
- Graph Nodes Created = 0;
- Graph Edges Created = 0;
- Canonical Knowledge Created = 0.

No merge map, superseded map, deduplicated registry, graph, or canonical knowledge artifact was created.

Conclusion:

Stage 2.2 did not execute Stage 2.3.

### 4.5 Did Premature Canonicalization Of Wording Occur?

Verdict:

```text
NO PROVEN CANONICALIZATION
```

Evidence:

The Stage 2.2 objects have:

```text
review_state = extracted
```

They are not:

- deduplicated;
- graph-accepted;
- canonicalized;
- accepted;
- locked.

The `destination = CANONICAL KNOWLEDGE` field is a future routing destination, not current canonical status.

Analysis:

Stage 2.2 necessarily writes extracted knowledge in readable form. That does not make the wording canonical. Canonical wording is the responsibility of Stage 2.5 after Stage 2.3 and Stage 2.4.

Conclusion:

No premature canonicalization is proven.

### 4.6 Should A New Entity Be Introduced?

Verdict:

```text
NO
```

Reason:

The program already has enough layers:

```text
Source
  -> Knowledge Candidate
  -> Knowledge Object
  -> Deduplicated Knowledge Concept
  -> Knowledge Graph Node / Edge
  -> Canonical Knowledge
```

Introducing another entity between Candidate and Knowledge Object would duplicate the existing distinction between work package and atomic extracted knowledge.

If future evidence proves that some Knowledge Objects are too coarse, the correct architectural lever is the existing Knowledge Object Creation Rules, not a new entity.

## 5. Alternative Architectures Considered

### Option A: Keep Current Program

Description:

Knowledge Candidate remains the input work unit. Knowledge Object remains the atomic extracted knowledge unit. Stage 2.3 deduplicates extracted objects into canonical concepts.

Impact:

| Area | Impact |
|---|---|
| Stage 2.2 | No change. Continue candidate -> zero/one/multiple object extraction. |
| Stage 2.3 | No change. Deduplicate objects, do not split candidates. |
| Knowledge Graph | Graph consumes deduplicated objects/concepts and preserves relationships. |
| Canonical Knowledge | Canonical wording remains Stage 2.5 responsibility. |

Pros:

- Matches current program.
- No new entity.
- Preserves stage boundaries.
- Keeps Candidate as work queue and Knowledge Object as atomic knowledge.

Cons:

- Requires disciplined extraction review so broad candidates are split when program rules require it.

### Option B: Introduce A New "Knowledge Atom" Entity

Description:

Add a new entity between Knowledge Candidate and Knowledge Object.

Impact:

| Area | Impact |
|---|---|
| Stage 2.2 | Would require new extraction output and new schema. |
| Stage 2.3 | Would need to deduplicate atoms or objects, creating ambiguity. |
| Knowledge Graph | Would need to decide whether graph nodes are atoms, objects, or concepts. |
| Canonical Knowledge | Would add another pre-canonical layer. |

Pros:

- Could make atomicity explicit by name.

Cons:

- Duplicates the current Knowledge Object role.
- Creates schema and lifecycle ambiguity.
- Risks alternate extraction lifecycle.
- Requires program refinement without proven necessity.

Conclusion:

Not justified by current evidence.

### Option C: Treat Knowledge Candidate As The Atomic Unit

Description:

Force one candidate to equal one knowledge unit.

Impact:

| Area | Impact |
|---|---|
| Stage 2.2 | Would remove legitimate one-to-many extraction. |
| Stage 2.3 | Would receive coarser objects and need to split, which is not its defined role. |
| Knowledge Graph | Graph would inherit over-broad nodes. |
| Canonical Knowledge | Canonicalization would carry candidate-level grouping errors. |

Pros:

- Simpler queue accounting.

Cons:

- Contradicts current program.
- Makes Stage 2.2 less precise.
- Pushes extraction work into Stage 2.3.

Conclusion:

Rejected.

### Option D: Move Object Splitting To Stage 2.3

Description:

Stage 2.2 extracts coarse objects; Stage 2.3 splits and deduplicates them.

Impact:

| Area | Impact |
|---|---|
| Stage 2.2 | Simpler extraction but lower object quality. |
| Stage 2.3 | Would combine splitting and deduplication responsibilities. |
| Knowledge Graph | Could receive cleaner concepts only if Stage 2.3 also performs extraction correction. |
| Canonical Knowledge | More dependent on Stage 2.3 interpretation. |

Pros:

- Lets Stage 2.2 avoid hard boundary decisions.

Cons:

- Violates current Stage 2.3 purpose.
- Blurs extraction and deduplication.
- Risks losing provenance during late splitting.

Conclusion:

Rejected.

## 6. Boundary Assessment

| Boundary question | Result | Reason |
|---|---|---|
| Is Candidate the minimal knowledge unit? | NO | Candidate is the Stage 2.2 input work unit. |
| Is Knowledge Object the minimal knowledge unit? | YES | Program defines it as the atomic reusable engineering conclusion/rule/boundary/responsibility/etc. |
| Can Candidate produce multiple objects? | YES | Program explicitly permits this. |
| Does current program require one object per candidate? | NO | It allows zero, one, or multiple objects. |
| Does current program require a new entity? | NO | Existing Candidate -> Object -> Deduplicated Concept chain is sufficient. |
| Did Stage 2.2 run Stage 2.3? | NO | No deduplication artifacts or merge outputs were created. |
| Did Stage 2.2 canonicalize wording? | NO | Objects remain `review_state = extracted`. |

## 7. Research Conclusion

The observation is useful, but it does not prove an architectural defect in the Stage 2 program.

The current program already answers the central question:

```text
Minimum extraction input unit = Knowledge Candidate
Minimum engineering knowledge unit = Knowledge Object
Minimum deduplicated canonical concept unit = Stage 2.3 output
Minimum canonical prose unit = Stage 2.5 output
```

The current program is therefore architecturally correct.

No new entity should be introduced based on the current evidence.

## 8. Architecture Verdict

```text
PROGRAM_IS_CORRECT
```

Engineering basis:

- one Knowledge Candidate can legitimately produce multiple Knowledge Objects;
- Knowledge Object is already the atomic engineering unit by program definition;
- the program already contains rules for splitting candidates into multiple objects;
- Stage 2.2 did not perform Deduplication;
- Stage 2.2 did not build a graph;
- Stage 2.2 did not create Canonical Knowledge;
- no premature canonicalization is proven;
- no new entity is justified.

