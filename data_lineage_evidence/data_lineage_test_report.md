# Data Lineage Test Report

## Local Regression

Command:

`python3 -m unittest discover tests`

Result:

PASS.

Output summary:

`Ran 280 tests in 18.808s`

`OK`

## Production Dry-Run

Command:

`/usr/local/bin/v7-intelligence-snapshot-refresh --dry-run`

Result:

PASS.

Observed:

- 11 snapshots buildable
- no writes
- no user movement
- no governance behavior change
- no runtime behavior change
