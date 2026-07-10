# V7 BDP Engineering Reality Instance Output Refinement Report

Status: `PASS`
Date: `2026-07-09`
Updated Artifact: `docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md`
Scope: BDP output contract refinement only

## 1. Summary

BDP was refined so its final OMP-facing output is no longer an abstract `Implementation Candidate`.

The final OMP-facing output is now:

```text
Implementation Candidate Instance
```

This is a real engineering situation in current Reality, anchored in:

- Engineering Chain;
- Behaviour Instance;
- Engineering Intent;
- Current Reality;
- Expected Reality;
- Current Outcome;
- Expected Outcome;
- Intent Closure State;
- affected Owner;
- affected Consumer;
- Verification Context;
- Authority Context;
- Terminal Path.

No new architecture, program, owner, Runtime, Planner, truth source, OMP, or entity was created.

## 2. Real Problem

Execution Certification failed semantically because the BDP output contract allowed downstream consumers to treat abstract objects as candidates.

Those abstract objects included:

- documents;
- owners;
- models;
- reports;
- rules;
- validations;
- canonical sources;
- STOP conditions;
- context artifacts;
- abstract improvements.

OMP needs a concrete engineering situation it can:

```text
Admit
Reject
Hold
Mission
Implement
Verify
Learn
Close
```

An abstract improvement cannot complete that path.

## 3. Discover / Reuse Result

No new concept was required.

Existing reusable mechanisms already cover the needed meaning:

| Existing mechanism | Reuse decision |
| --- | --- |
| Engineering Chain | Reused as the relationship path from Intent to Closure. |
| Behaviour Instance | Reused as the concrete occurrence in current Reality. |
| Engineering Intent | Reused as the purpose that must close or fail to close. |
| Automation Break | Reused as stopping point evidence, not as the candidate itself. |
| Implementation Candidate Instance | Reused as the OMP admission unit and final BDP output. |
| Outcome / Learning | Reused as expected downstream closure requirements. |
| Reality | Reused as current observed state anchor. |
| Owner / Consumer | Reused as producer-consumer chain requirements. |
| Mission | Reused as OMP-admitted execution identity after admission. |

New entity decision:

```text
NEW_ENTITY_REQUIRED = FALSE
```

BDP may use `Engineering Reality Instance` only as an explanatory description of the output shape. It is not a new entity.

## 4. What Changed In BDP

Updated:

```text
docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md
```

Changes:

| Section | Change |
| --- | --- |
| Purpose / official order | Replaced abstract `Implementation Candidate` wording with `Implementation Candidate Instance` where BDP hands work toward OMP. |
| Relationship With OMP | Clarified that OMP receives concrete engineering situations, not abstract candidates. |
| Discovery Lifecycle | Added `Candidate Reality Gate` before candidate packaging. |
| Implementation Candidate schema | Replaced / strengthened schema as `Implementation Candidate Instance Schema`. |
| Candidate Reality Gate | Added. Requires current/expected reality, outcome, owner, consumer, verification, authority, terminal path. |
| Negative Candidate Semantics | Added. Documents, owners, models, reports, rules, validations, STOP conditions, and context artifacts cannot be emitted as Candidate Instances. |
| Source paths | Updated readiness-derived and intent-derived paths to pass through Candidate Reality Gate. |

## 5. Final Object Passed To OMP

The final object is:

```text
Implementation Candidate Instance
```

Required fields:

- Candidate Instance ID;
- Engineering Intent;
- Current Reality;
- Expected Reality;
- Engineering Chain;
- Engineering Chain Segment;
- Behaviour Instance;
- Automation Break or no-break reason;
- Current Outcome;
- Expected Outcome;
- Intent Closure State;
- Affected Owner;
- Affected Consumer;
- Evidence;
- Verification Context;
- Authority Context;
- Terminal Path;
- Implementation Readiness.

This object is admissible by OMP because it is one concrete engineering situation, not a document or idea.

## 6. Why Execution Certification Could Not Complete Before

Execution Certification needed valid BDP-derived Candidate Instances.

Before this refinement, BDP could produce outputs described as:

- Behaviour;
- Automation Break;
- Implementation Candidate;
- OMP-ready input.

But the final schema did not strictly force:

- current Reality;
- expected Reality;
- current Outcome;
- expected Outcome;
- affected Engineering Chain segment;
- affected Owner and Consumer;
- Terminal Path.

That allowed context artifacts to be counted as candidates. OMP then had to reject them under the new eligibility gate.

## 7. Why Execution Certification Can Now Work

Execution Certification can now consume only real Candidate Instances because:

- BDP final output is instance-level;
- Candidate Reality Gate blocks abstract records;
- Negative Candidate Semantics forbids documents/owners/models/reports as candidates;
- Implementation Candidate Instance schema matches OMP eligibility;
- OMP can admit, hold, reject, or mark the output not applicable;
- every candidate has a terminal path before being counted.

Expected route:

```text
BDP
  -> Implementation Candidate Instance
  -> OMP Admission
  -> Mission or legal terminal alternative
  -> Codex / existing owner when admitted
  -> Implementation / no-change / hold
  -> Verification
  -> Outcome
  -> Learning
  -> Closure
  -> Reality
  -> AEP
```

## 8. Compatibility

| Area | Result |
| --- | --- |
| AEP | `PASS` - AEP still consumes Behaviour Reality / Reality refinement outputs; no phase change. |
| OMP | `PASS` - BDP output now aligns with OMP Implementation Candidate Instance admission. |
| Engineering Chain | `PASS` - reused, not redefined. |
| Engineering Entity | `PASS` - reused existing entities; no new entity created. |
| Mission | `PASS` - Mission remains OMP-admitted identity after candidate admission. |
| Implementation Candidate Identity | `PASS` - stricter instance identity improves compatibility. |
| Cohort | `PASS` - Cohort can still group compatible Candidate Instances after OMP safety review. |
| Merge | `PASS` - merge still depends on deterministic same Candidate Instance identity. |
| CPS | `PASS` - no volatile state change required by this refinement alone. |
| LOCKED_KNOWLEDGE | `PASS` - consumed, not modified. |

## 9. Review

Architecture Review: `PASS`.
Reuse Review: `PASS`.
BDP Output Contract Review: `PASS`.
OMP Compatibility Review: `PASS`.
Execution Certification Compatibility Review: `PASS`.
Candidate Semantics Review: `PASS`.
No New Entity Review: `PASS`.
Quality Review: `PASS`.
Self Review: `PASS`.

## 10. PASS / HOLD

```text
PASS
```

Reason:

- the real problem was corrected at the BDP output contract;
- no architecture or owner was changed;
- no new entity was introduced;
- BDP now ends OMP-facing work by producing a real Implementation Candidate Instance or a legal non-candidate result;
- Execution Certification can now rerun against real engineering situations.

Final status:

```text
BDP_ENGINEERING_REALITY_INSTANCE_OUTPUT_REFINED
```
