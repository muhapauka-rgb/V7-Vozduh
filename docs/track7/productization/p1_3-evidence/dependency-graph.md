# P1.3 Dependency Graph

dependency_graph_defined=true

## Hard Dependencies

```text
Evidence Store
-> Evidence API
-> Evidence UI
```

```text
Evidence Store
-> Proposal Store
-> Proposal API
-> Proposal UI
```

```text
Evidence Store
-> Runtime Convergence Store
-> Runtime Trust API
-> Runtime Trust UI
```

```text
Evidence Store
-> Release Trust Store
-> Release Trust API
-> Release Trust UI
```

```text
Release Trust
-> Runtime Trust release_match meaning
```

## Soft Dependencies

| Component | Soft dependency | Why |
| --- | --- | --- |
| Proposal UI | Runtime Trust UI | Proposals can show trust blockers after runtime trust exists. |
| Runtime Trust UI | Release Trust UI | Runtime match is stronger when release identity is visible. |
| Release Trust UI | Backup/Restore surfaces | Rollback lineage becomes more useful when backup/restore is linked. |
| Evidence search | Closure workflow | Search is valuable before closure but not blocked by it. |

## Optional Dependencies

| Component | Optional dependency |
| --- | --- |
| Advanced details | Role-gated raw payload access. |
| Proposal-to-batch | Future governance implementation. |
| Drift closure | Future trust operations. |
| Release refresh | Future guarded verification action. |

## Dependency Risk

Highest-risk dependency:

```text
canonical storage backend decision
```

Mitigation:

Use one adapter interface for all Phase 1 stores and begin with SQLite if available, otherwise JSONL with migration boundaries.

## Graph Verdict

Evidence is the root dependency. Build Evidence first, then Proposal, then Runtime/Release Trust as visible status surfaces.
