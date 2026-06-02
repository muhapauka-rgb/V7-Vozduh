# Z8.12 Validation Outputs

## Local JSON validation

Command:

```text
python3 tools/v7-truth-check --local --json
```

Result:

```text
final_verdict=NO-GO
blockers=dirty_workspace,runtime_critical_dirty
warnings=documentation_dirty_ignored,runtime_relevant_dirty
```

Current classification:

- `tools/v7-truth-check`: runtime critical, blocking
- `tests/unit/test_v7_truth_check.py`: runtime relevant, warning
- `PROGRAM_Z8_11_PRODUCTION_CONVERGENCE_REMEDIATION_REPORT.md`: documentation only, ignored
- `PROGRAM_Z9_ONE_USER_OPERATION_EXECUTION_CERTIFICATION_REPORT.md`: documentation only, ignored
- `z8_11-evidence/`: documentation only, ignored
- `z9-evidence/00_mandatory_discovery_gate_no_go.md`: documentation only, ignored

## Full JSON validation

Command:

```text
env V7_TRUTH_RUNTIME_SNAPSHOT=z8_11-evidence/runtime_convergence_snapshot.json python3 tools/v7-truth-check --all --json
```

Result:

```text
github.final_verdict=PASS
runtime.final_verdict=PASS
runtime_access_status=READY
runtime_truth_status=KNOWN
state_truth_status=KNOWN
final_verdict=NO-GO
blockers=dirty_workspace,runtime_critical_dirty
```

The remaining NO-GO is correct and is caused by the in-progress Z8.12 modification to the truth-check tool itself. Documentation/evidence artifacts no longer block.

