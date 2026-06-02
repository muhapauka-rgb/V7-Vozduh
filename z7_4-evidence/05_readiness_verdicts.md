# Z7.4 Readiness Verdicts

## Critical Questions

Q: What can break if operation wiring is added to `tools/v7-users-autoswitch`?  
A: Admin JSON parse, Admin UI plan rendering, guarded apply status extraction, selected-move adapters, operator runtime recheck hashes, historical report generation, and autoswitch tests can break if existing fields move/change type or stdout stops being one JSON object.

Q: Can new fields be safely added?  
A: Yes, if additive and if current root/nested contracts remain stable.

Q: Are consumers strict?  
A: Admin stdout parsing is strict about valid JSON. Admin/UI are tolerant of extra fields. Guarded apply is strict about `apply_result.applied`. Runtime recheck is strict about selected move hash/count semantics.

Q: Would operation envelope duplicate existing structures?  
A: Not if it is lineage-only. Yes if it becomes a store, audit sink, closure store, selected-move writer, or replacement for `apply_result`.

Q: Would `operation_id` duplicate existing identifiers?  
A: It can collide semantically with Admin/operator candidate `operation_id` unless explicitly scoped as `operation_type=runtime_autoswitch` and `operation_owner=tools/v7-users-autoswitch`.

Q: What is the safest first change?  
A: Add an internal operation context and additive root `operation` envelope in dry-run/no-op output, with no apply behavior change.

Q: What is the safest implementation order?  
A: Root envelope -> selected move hash reference -> operation refs in move rows -> derived terminal fields -> apply result lineage refs -> audit metadata -> closure target refs -> tests.

Q: What is the rollback strategy?  
A: Revert the bounded autoswitch/test change. Because no new store or schema migration should be created, rollback is a simple code revert if the boundary is obeyed.

## Final Verdicts

```text
consumer_inventory_complete=true
json_contracts_understood=true
test_coverage_understood=true
runtime_contracts_understood=true
operation_id_conflicts_understood=true
change_impact_understood=true
implementation_conflicts_understood=true
safe_to_begin_bounded_implementation=true
```

## Conditions For Z7.5

Z7.5 can begin only as bounded implementation if it obeys:

- additive output only,
- no new stores,
- no scheduler/systemd changes,
- no move-selection behavior change,
- no selected-move state writer unless separately approved,
- preserve stdout JSON root,
- preserve `apply_result`,
- extend `tests/unit/test_v7_users_autoswitch_policy.py`.
