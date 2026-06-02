# Z8.13 Final Truth Check Results

## Local

Command:

```text
python3 tools/v7-truth-check --local --json
```

Result:

```text
current_commit=12dbd30e597a1dfe75028c966340e9ad515e0fbe
convergence_status=LOCAL_ALIGNED
final_verdict=PASS
blockers=[]
warnings=documentation_dirty_ignored
```

## GitHub

Command:

```text
python3 tools/v7-truth-check --github --json
```

Result:

```text
current_commit=12dbd30e597a1dfe75028c966340e9ad515e0fbe
remote_branch_commit=12dbd30e597a1dfe75028c966340e9ad515e0fbe
convergence_status=GITHUB_ALIGNED
final_verdict=PASS
blockers=[]
```

## All

Command:

```text
python3 tools/v7-truth-check --all --json
```

Result:

```text
current_commit=12dbd30e597a1dfe75028c966340e9ad515e0fbe
remote_branch_commit=12dbd30e597a1dfe75028c966340e9ad515e0fbe
runtime_access_status=READY
runtime_truth_status=KNOWN
state_truth_status=KNOWN
convergence_status=FULLY_ALIGNED
final_verdict=PASS
blockers=[]
warnings=documentation_dirty_ignored
```

