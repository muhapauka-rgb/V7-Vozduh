# Z8.12 Discovery And Duplication Audit

## Existing logic

`tools/v7-truth-check` previously treated every non-empty `git status --short` output as:

```text
dirty_workspace -> NO-GO
```

There was no existing file classification logic, documentation exemption, evidence allowlist, runtime-affecting path list, or report/evidence rule to reuse.

## Existing blockers

Current local blockers before Z8.12 policy hardening:

- `workspace_mismatch`
- `branch_mismatch`
- `remote_mismatch`
- `dirty_workspace`
- `commit_unknown`

The problem was that `dirty_workspace` did not distinguish runtime-affecting changes from documentation/evidence artifacts.

## Required reuse/merge conclusion

No duplicate policy system was present. Z8.12 extends the existing `local_check` gate in `tools/v7-truth-check` instead of creating a parallel truth policy.

