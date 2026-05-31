# E35.D Read Models

## Principle

Operator never reads raw storage.

Read models combine:

- authority state;
- authority events;
- users registry;
- egress registry;
- evidence;
- proposals;
- runtime/release trust.

## Authority Summary

Purpose:

Home and Checks summary.

Fields:

- total users with authority state;
- AUTO count;
- OPERATOR_PINNED count;
- MANUAL count;
- pending reviews;
- active emergencies;
- conflicts;
- stale/expired authority.

## Authority Timeline

Purpose:

Show history for a user/channel/action.

Fields:

- events ordered by time;
- verdicts;
- conflicts;
- reviews;
- emergencies;
- evidence/proposal links.

## Conflict Summary

Purpose:

Operator sees unresolved conflicts.

Fields:

- conflict type;
- affected user/channel;
- domains;
- current verdict;
- next safe action.

## Conflict Detail

Purpose:

Explain exact domain disagreement.

Fields:

- proposed action;
- competing domains;
- winning domain;
- rule id;
- evidence/proposal links;
- review requirement.

## Review Queue

Purpose:

Show machine decisions needing human/governance review.

Fields:

- review id;
- category;
- severity;
- created_at;
- stale age;
- suggested next action.

## Emergency Queue

Purpose:

Show active emergency authority/containment states.

Fields:

- emergency id;
- trigger;
- source target;
- temporary target;
- lease expiry;
- return status.

## Authority Health

Purpose:

Checks page health.

Fields:

- store readable;
- event log readable;
- schema version OK;
- unresolved conflicts count;
- stale authority count.

## Authority Explanation

Purpose:

User/channel drawer explanation.

Fields:

- verdict;
- authority chain;
- why allowed;
- why denied;
- next safe action.

## Verdict

```text
read_models_defined=true
```
