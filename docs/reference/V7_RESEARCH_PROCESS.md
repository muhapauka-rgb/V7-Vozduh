# V7 Research Process

Status: canonical

Purpose:
Compact operator guide describing exactly how future research is executed.

Research uses `docs/programs/V7_RESEARCH_FRAMEWORK.md`.
Execution uses `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`.
Context is resolved before research begins.

## Start Command

Future research can start from:

`Start Research: <topic>`

## Operator Flow

1. Classify the task as research.
2. Resolve context using `docs/reference/V7_CONTEXT_RESOLVER.md`.
3. Load only the research working set:
   - `docs/reference/V7_KERNEL.md`
   - `docs/reference/V7_CONTEXT_RESOLVER.md`
   - `docs/programs/V7_RESEARCH_FRAMEWORK.md`
   - `docs/reference/V7_ENGINEERING_PRINCIPLES.md`
   - relevant ADRs
   - only target V7 documents required by the question
4. Do not load packet state, current metrics, current HLA, historical reports, or runtime execution documents unless explicitly required by the research question.
5. Collect sources from mature production systems relevant to the question.
6. Validate each source before using it:
   - mature production use is clear;
   - the source explains why the pattern exists;
   - the source explains what problem the pattern solves;
   - the pattern is not vendor-specific ceremony.
7. Extract common engineering patterns across systems.
8. Convert common patterns into universal principles.
9. Compare each principle with V7 using existing owners:
   - Canonical Reference;
   - SYSTEM_MAP;
   - Engineering Principles;
   - relevant ADRs;
   - relevant target documents.
10. Perform reuse analysis before recommending change.
11. Classify each gap:
   - ALREADY_EXISTS
   - EXISTS_BUT_UNDERUSED
   - READ_MODEL_MISSING
   - REAL_OUTCOME_REQUIRED
   - AUTHORITY_REQUIRED
   - FUTURE_SCALE_OPTIONAL
   - FUNDAMENTAL_ARCHITECTURE_GAP
12. Recommend reuse or extension before proposing new architecture.
13. Update canonical documentation only when research changes durable project meaning.
14. Create an ADR only when research changes project meaning.
15. Update SYSTEM_MAP only when ownership changes.
16. Update OMP only when scheduler or optimizer meaning changes.

## Recommendation Checklist

Every recommendation must prove:

1. used in mature production;
2. why it exists;
3. what problem it solves;
4. whether V7 already has equivalent owner;
5. reuse path;
6. extension path;
7. why new owner is or is not required.

## Completion Gate

Research is complete only when:

- universal principles are extracted;
- V7 is mapped against those principles;
- reusable owners are identified;
- recommendations are classified;
- required canonical documents are updated.

## Safety Boundary

Research never copies vendor architecture.
Research never invents architecture.
Research never changes runtime behavior.
Research never runs apply.
Research never moves users.
Research never creates synthetic evidence.
