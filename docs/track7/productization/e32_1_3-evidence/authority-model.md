# E32.1.3 Authority Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

authority_model_defined=true

## Authority Alternatives

### Runtime Evidence Only

Pros:

- objective;
- automatable;
- resistant to operator optimism.

Cons:

- cannot resolve product risk choices;
- cannot approve staged proof versus exact proof;
- cannot decide production-pool policy caps.

Verdict: insufficient alone.

### Operator Only

Pros:

- fast;
- flexible for exceptional situations.

Cons:

- weakens governance;
- risks metadata-only promotion;
- contradicts E25-E31 evidence-bound pattern.

Verdict: rejected.

### Operator Plus Evidence

Pros:

- preserves evidence-bound governance;
- allows human responsibility for architecture decisions;
- fits current V7 block process.

Cons:

- needs clear artifact format;
- can be slower than automation.

Verdict: recommended current authority.

### Policy Engine

Pros:

- needed for production pool;
- can enforce TTLs, caps, and reservations.

Cons:

- not yet certified;
- must not become autonomous authority before policy is proven.

Verdict: future authority after architecture and validation.

### Governance Board

Pros:

- appropriate for large-scale production policy;
- separates operational authority from implementation.

Cons:

- not defined in current V7 process;
- may be too heavy for early architecture.

Verdict: candidate future process.

## Recommended Current Authority

```text
capacity_certification_authority=OPERATOR_PLUS_EVIDENCE
```

Meaning:

- evidence is mandatory;
- operator/governance block accepts or rejects the evidence;
- automation may validate consistency but cannot promote above proven policy alone.

## Future Authority

```text
future_capacity_authority=POLICY_ENGINE_WITH_OPERATOR_GOVERNANCE
```

Meaning:

- policy engine enforces TTL, batch caps, reservations, and state transitions;
- operator governance approves class promotions and architecture policy.

## ARCHITECTURE_DECISION_REQUIRED

decision_needed=large_scale_certification_authority_for_CLASS_50_CLASS_100_AND_PRODUCTION_POOL

Options:

1. Exact movement proof remains mandatory for every class.
2. Staged production-pool proof may certify CLASS_50/CLASS_100.
3. Policy engine may certify based on load/rollback/audit simulation plus smaller live batches.

Pros and cons:

- Option 1 is simplest and strongest, but may create unnecessary blast radius.
- Option 2 balances proof with operational safety, but needs staged certification rules.
- Option 3 is operationally efficient, but risks certifying execution without real rollback proof at scale.

Recommended option:

```text
Option 2: staged production-pool proof may certify CLASS_50/CLASS_100 only after policy-engine, rollback orchestration, audit volume, replay volume, and scheduler controls are themselves certified.
```

This decision is not required for CLASS_10 and below, which are already exact-proof certified.

