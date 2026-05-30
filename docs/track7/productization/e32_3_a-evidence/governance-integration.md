# E32.3.A Governance Integration

governance_integration_defined=true

## Capacity Program Integration

Policy consumes capacity state and may deny or require review based on:

- capacity class;
- capacity status;
- confidence;
- effective batch cap;
- available capacity;
- policy cap;
- reservation conflict.

Policy cannot certify capacity by itself.

## Execution Batches Integration

Policy evaluates batch metadata:

- batch type;
- allowed users;
- destination target;
- rollback manifest;
- movement budget;
- blast radius;
- lifecycle state;
- failure mode.

Policy cannot mutate batch scope.

## Approval Packet Integration

Policy may require:

- packet generation;
- packet freshness;
- exact scope binding;
- dual confirmation;
- review flag.

Policy cannot consume or replay packets.

## Execution-Time Recheck Integration

Policy must be re-evaluated at execution-time recheck.

If policy changed between approval and execution:

```text
admission=DENY_OR_REQUIRE_FRESH_PACKET
```

## Operator Confirmation Integration

Policy may require:

- operator role;
- dual confirmation;
- emergency confirmation;
- human review for conflict or unknown scope.

## Audit Lineage Integration

Every policy decision must be auditable:

- policy ids;
- versions;
- decision;
- applicable scope;
- conflict state;
- gates required;
- final admission result.

## Integration Verdict

Policy Foundation integrates with governance without becoming runtime mutation.
