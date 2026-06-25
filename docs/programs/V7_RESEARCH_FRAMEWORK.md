# V7 Research Framework

Status: ACTIVE

Purpose:
Continuously improve V7 using proven engineering knowledge from mature production systems.
Research never invents architecture.
Research discovers reusable engineering patterns.

Research Framework is the research analogue of OMP.
OMP optimizes implementation.
Research Framework optimizes knowledge acquisition.

Research Framework is documentation-only.
It does not create a planner, governance layer, execution path, truth source, runtime owner, runtime behavior, apply behavior, floor change, or user movement path.

Need New Owner: FALSE

## Research Loop

Question
→ Resolve Context
→ Collect Sources
→ Validate Sources
→ Extract Patterns
→ Cross-System Comparison
→ Universal Principle
→ Compare With V7
→ Reuse Analysis
→ Gap Classification
→ Recommendation
→ Canonical Update

## Research Sources

- Cisco
- Juniper
- Arista
- Cloudflare
- Google SRE
- Kubernetes
- Envoy
- Istio
- Fastly
- Other mature production systems when relevant.

## Research Rules

Never copy vendor architecture.
Search only for common engineering principles.

Every recommendation must prove:

1. used in mature production;
2. why it exists;
3. what problem it solves;
4. whether V7 already has equivalent owner;
5. reuse path;
6. extension path;
7. why new owner is or is not required.

Never recommend new architecture before proving extension is impossible.

## Research Output

Every completed research produces:

- Universal Engineering Laws;
- Cross-System Comparison Matrix;
- V7 Mapping;
- Gap Classification;
- Reuse Analysis;
- Canonical Recommendations;
- canonical document;
- report;
- ADR if project meaning changes;
- Canonical Reference update if system truth changes;
- SYSTEM_MAP update if ownership changes;
- OMP update only if scheduler/optimizer meaning changes.

Future research must ALWAYS produce:

A. Universal Engineering Laws

B. Cross-System Comparison Matrix

C. V7 Mapping

D. Gap Classification

E. Reuse Analysis

F. Canonical Recommendations

Research is NOT complete until all six sections exist.

## Required Research Sections

### A. Universal Engineering Laws

Extract engineering laws common across mature production systems.

Each law must include:

- Law;
- why it exists;
- which systems use it;
- how V7 implements it today;
- gap classification;
- reuse path.

Do not invent laws.
Include only principles observed across multiple mature systems.

### B. Cross-System Comparison Matrix

Create a comparison table across relevant mature systems.

The matrix must show:

- how each system family solves the problem;
- what common engineering pattern exists;
- where V7 already matches;
- where V7 differs.

For decision-model research, the required columns are:

- Cisco;
- Juniper;
- Cloudflare;
- Kubernetes;
- Google SRE;
- Envoy/Istio;
- V7.

For other research, choose comparable mature production families and document why they are relevant.

### C. V7 Mapping

Map each universal principle and engineering law to existing V7 owners before recommending change.

### D. Gap Classification

Classify every gap using the canonical gap classes in this document.

### E. Reuse Analysis

Prove the reuse path and extension path before proposing new architecture.

### F. Canonical Recommendations

Recommendations must state which canonical document, report, ADR, SYSTEM_MAP row, or OMP section changes.
OMP changes are allowed only when scheduler or optimizer meaning changes.

## Gap Classification

- ALREADY_EXISTS
- EXISTS_BUT_UNDERUSED
- READ_MODEL_MISSING
- REAL_OUTCOME_REQUIRED
- AUTHORITY_REQUIRED
- FUTURE_SCALE_OPTIONAL
- FUNDAMENTAL_ARCHITECTURE_GAP

### ALREADY_EXISTS

The researched principle already has a V7 owner and an equivalent path.
Recommendation must reuse the existing owner.
Need New Owner remains FALSE.

### EXISTS_BUT_UNDERUSED

The principle exists in V7 but is not consistently used, referenced, or enforced.
Recommendation must improve use of the existing owner before proposing new structure.
Need New Owner remains FALSE.

### READ_MODEL_MISSING

V7 has the authority or execution path, but operators lack a stable read model, map, or report to use it safely.
Recommendation must prefer a read model or documentation extension.
Need New Owner remains FALSE unless no existing owner can expose the read model.

### REAL_OUTCOME_REQUIRED

The principle cannot be validated by design language alone.
Recommendation must require observed outcomes, evidence, or post-run comparison before changing system meaning.
Need New Owner remains FALSE until evidence proves otherwise.

### AUTHORITY_REQUIRED

The gap is not a missing tool but a missing authorized decision point.
Recommendation must identify whether an existing authority can absorb it.
Need New Owner remains FALSE unless existing authority cannot be extended.

### FUTURE_SCALE_OPTIONAL

The principle matters at larger scale but is not required for current V7 operation.
Recommendation must preserve it as an option without creating immediate ownership or runtime complexity.
Need New Owner remains FALSE.

### FUNDAMENTAL_ARCHITECTURE_GAP

No existing V7 owner, authority, read model, or extension path can satisfy the principle.
Recommendation may propose new architecture only after proving extension is impossible.
This is the only classification that can raise Need New Owner above FALSE.

## Research Completion Rule

Research ends only when:

- universal principles extracted;
- engineering laws extracted;
- comparison matrix completed;
- V7 mapped;
- gaps classified;
- reuse path defined;
- canonical docs updated.

## Semantic Reuse Audit

Existing V7 documents already contain partial research behavior:

- `docs/reference/V7_CONTEXT_RESOLVER.md` defines research-task loading rules and prevents packet, metrics, and runtime context from entering research by default.
- `docs/reference/V7_ENGINEERING_PRINCIPLES.md` records industry-inspired engineering principles and explicitly rejects vendor copying.
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md` and `docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md` contain cross-system comparisons and reusable architectural ideas.
- `docs/reference/V7_CANONICAL_REFERENCE.md` preserves durable system truth.
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` defines semantic reuse gates and prevents unnecessary new owners during implementation.

Semantic reuse result:
Existing coverage is partial.
V7 had research principles and research examples, but no permanent research workflow owner.
This framework extends existing documentation only.

Need New Owner: FALSE

## Duplicate Detector

Research Framework does not duplicate:

- OMP, because OMP optimizes implementation while Research Framework optimizes knowledge acquisition;
- Context Resolver, because Context Resolver selects the working document set while Research Framework defines research methodology;
- Canonical Reference, because Canonical Reference stores durable truth while Research Framework governs how research produces or updates truth;
- SYSTEM_MAP, because SYSTEM_MAP maps ownership while Research Framework compares researched principles to existing ownership;
- ADRs, because ADRs record decisions while Research Framework determines when research changes project meaning;
- runtime tools, because Research Framework has no execution behavior.

Duplicate detector result:
No equivalent permanent research workflow owner exists.
Create documentation-only framework.

## Safety Boundary

Research Framework must not:

- create runtime behavior;
- create execution behavior;
- create a new planner;
- create new governance;
- create a new truth source;
- create synthetic evidence;
- lower floors;
- run apply;
- move users.

Research recommendations remain proposals until accepted through the existing V7 decision and documentation paths.
