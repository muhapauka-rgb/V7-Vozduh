# Block D1 Decision Tree

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Tree

```text
IF safety review critical
  IF parser sees zero enabled egress but KV parser sees enabled egress
    -> fix safety-review registry parser
    -> rerun safety review
  ELSE
    -> fix runtime registry or egress state

IF execution target count == hard limit
  -> HOLD current cohort
  -> create or certify second execution target

IF planner raw moves > approved cap
  -> do not execute
  -> build capped proposal packet

IF planner treats execution cohort as failover candidates
  -> add governance hold/exclusion semantics
  -> rerun shadow

IF safety status OK AND admin health accepted/resolved AND capped proposal valid
  -> operator approval model may proceed
ELSE
  -> shadow retry only

IF approved packet runtime hashes mismatch
  -> deny

IF approval expired or replayed
  -> deny

IF rollback manifest incomplete
  -> deny
```

## Verdict

`decision_tree_complete=true`

