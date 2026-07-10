# V7 Behaviour Discovery Program Identity Refinement Report

Date: `2026-07-08`
Program: `docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md`
Mode: `LIVE_PROGRAM_REFINEMENT_MODE`

## 1. Summary

This report records the Behaviour Identity refinement of the Behaviour Discovery Program.

The program now has an explicit deterministic mechanism for answering:

```text
Is this observed Behaviour new,
or is it an existing Behaviour with new evidence, implementation, name, or version?
```

Program changed:

```text
YES
```

Final verdict:

```text
PASS
```

## 2. Discovery Result

The following existing mechanisms were found and reused.

| Source / Mechanism | Existing Coverage | Reuse Decision |
| --- | --- | --- |
| Behaviour Discovery Program | Candidate IDs, candidate fields, validation, merge/deduplication, Reality Refinement Proposal. | Partial; extended with explicit identity resolution. |
| AEP | Official `Behaviour Definition -> Behaviour Instance` split. | Reused as primary identity split. |
| AEP Behaviour Discovery Rule | `Discover -> Reuse -> Extend -> Create only if necessary`; duplicate Behaviour Definitions forbidden. | Reused as anti-duplication law. |
| Current Autonomous Behaviour Reality | Behaviour Instance Registry, Behaviour Aggregation, Behaviour Definition Catalogue, Behaviour Coverage. | Reused as existing catalogue and comparison target. |
| AOS / Runtime Model | Committed identity, material identity, packet/lease/freshness identity discipline. | Reused as stability discipline for evidence, not as Behaviour identity owner. |
| Function Graph | Producer/consumer/runtime/relationship discovery index. | Reused as identity evidence index only. |
| Canonical Knowledge / SYSTEM_MAP / Decision Model / Runtime Model / OMP / CPS | Owner, consumer, decision, runtime, continuation, and boundary references. | Reused as official resolution sources. |

Finding:

```text
EXISTING_MECHANISM_PARTIAL
```

BDP already had candidate, validation, and merge mechanics, but it did not explicitly define how to determine stable Behaviour identity across time.

## 3. What Was Extended

The following existing BDP sections were strengthened:

| Program Section | Extension |
| --- | --- |
| `2. Non Goals` | Added prohibition against creating a new identity owner. |
| `8. Relationship With Existing Discovery Systems` | Added explicit reuse of AEP Behaviour Discovery Rule and AOS/Runtime identity discipline. |
| `9. Program Invariants` | Added rules that Behaviour identity is not a name/file/function/class/document/repository location and must be resolved before Reality admission or merge. |
| `10. Discovery Lifecycle` | Added `Behaviour Identity Resolution`. |
| `13. Observed Behaviour Candidate Model` | Added Behaviour Definition Identity, Behaviour Instance Identity, and Identity Disposition fields. |
| `15. Validation Model` | Added Behaviour Identity Validation and validation rules. |
| `17. Merge / Deduplication Model` | Added identity-signature merge and non-merge rules. |
| `18. Certification Model` | Added Behaviour Identity Review. |
| `19. Outputs` | Added Behaviour Identity Resolution Matrix. |
| `22. Completion Criteria` | Added identity completion criteria and name/file/function-only prohibitions. |

## 4. What Was Added

One new internal program mechanism was added:

```text
Behaviour Identity Model
```

It defines:

- Behaviour Definition Identity;
- Behaviour Instance Identity;
- deterministic identity signature;
- Identity Resolution Lifecycle;
- Identity Dispositions;
- Identity Stability Rules.

It does not create:

- a new program;
- a new document type;
- a new architecture level;
- a new Behaviour entity beyond the existing AEP Definition/Instance split;
- a new owner;
- a new truth source;
- a new Runtime identity;
- a new Planner identity;
- storage.

## 5. Why Addition Was Necessary

Without explicit identity resolution, BDP could validate and merge candidates but still remain ambiguous in these cases:

| Case | Risk Without Identity Model | New Program Answer |
| --- | --- | --- |
| Same Behaviour, new evidence | Could be treated as new Behaviour. | `EXISTING_BEHAVIOUR_NEW_EVIDENCE`. |
| Same Behaviour, new implementation | Could be treated as new Behaviour because file/function changed. | `EXISTING_BEHAVIOUR_NEW_IMPLEMENTATION`. |
| Same Behaviour, new name | Could be duplicated by label drift. | `EXISTING_BEHAVIOUR_RENAMED`. |
| Existing Behaviour with material boundary change | Could be incorrectly merged into old Behaviour. | `BEHAVIOUR_VERSION_UPDATE`. |
| Same name, different Behaviour | Could be incorrectly merged by name. | `DIFFERENT_BEHAVIOUR_NAME_COLLISION`. |
| Ambiguous evidence | Could be guessed by Codex. | `MANUAL_REVIEW_IDENTITY_AMBIGUOUS`. |

The addition was required because names, files, functions, documents, and repository locations are not stable engineering identity.

## 6. Identity Rule Summary

Behaviour Definition Identity is now resolved through a deterministic identity signature:

- Engineering Purpose;
- Situation Class;
- Decision Responsibility;
- Execution Responsibility or `NOT_EXECUTING`;
- Primary Consumer;
- Verification Obligation;
- Learning / Continuation Obligation;
- Authority / Boundary / Forbidden Use;
- Canonical Owner / Owner Role;
- Evidence Provenance Family.

Behaviour Instance Identity is resolved through:

- Behaviour Definition Identity;
- concrete situation;
- concrete context;
- evidence occurrence or report/run/source envelope;
- concrete producer/consumer path when known;
- terminal state, freshness, or explicit unknown;
- verification and learning/continuation evidence.

## 7. Chain Closure

Required closure:

```text
Idea
  -> Discovery
  -> Confirmation
  -> Program Change
  -> Engineering Report
  -> Chain Closed
```

Actual closure:

| Step | Status | Evidence |
| --- | --- | --- |
| Idea | `COMPLETE` | Need to determine whether Behaviour Identity Model is required. |
| Discovery | `COMPLETE` | BDP, AEP, AOS, Reality, Canonical Knowledge, Function Graph, SYSTEM_MAP, Decision Model, Runtime Model, OMP, and CPS checked. |
| Confirmation | `COMPLETE` | Existing mechanisms were partial; explicit BDP identity resolution was missing. |
| Program Change | `COMPLETE` | `docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md` updated. |
| Engineering Report | `COMPLETE` | This report. |
| Chain Closed | `PASS` | Confirmed result was integrated into the program. |

## 8. Certification

| Review | Verdict | Notes |
| --- | --- | --- |
| Architecture Review | `PASS` | No new architecture level or owner was created. |
| Reuse Review | `PASS` | AEP Definition/Instance, AEP discovery rule, Reality catalogue, Function Graph index, and AOS/Runtime identity discipline were reused. |
| Duplication Review | `PASS` | The model prevents duplicate Behaviour Definitions and name-only merges. |
| Identity Review | `PASS` | Identity is stable, reproducible, reality-based, and independent of names/files/functions/documents/repository layout. |
| Quality Review | `PASS` | BDP can now distinguish new Behaviour, new evidence, new implementation, rename, version update, collision, duplicate, and ambiguity. |
| Self Review | `PASS` | The refinement satisfies LIVE PROGRAM REFINEMENT MODE and closes the chain. |

## 9. Final Verdict

```text
PASS
```

The Behaviour Discovery Program now has stable engineering Behaviour identity across the project lifecycle.

```text
BEHAVIOUR_IDENTITY_MODEL_INTEGRATED
CHAIN_CLOSED
```
