# P2.6 Candidate Model

## Result

candidate_model_implemented=true

## Definition

An Execution Candidate is a proposed future execution object.

It is:

- not a contract;
- not execution;
- not authority;
- not a runtime action.

## Schema

Candidate includes:

- candidate id;
- proposal references;
- evidence references;
- authority references;
- target references;
- validation state;
- simulation state;
- readiness state;
- review state;
- risk state;
- lifecycle state;
- lineage.

## Implementation

Implemented in `admin/v7-admin-api` as a derived read model over proposal-derived contract drafts.
