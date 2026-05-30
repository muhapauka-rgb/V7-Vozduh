# E32.3.A Policy Metadata Model

policy_metadata_model_defined=true

## Authoritative Policy Fields

| Field | Purpose |
| --- | --- |
| `policy_id` | Unique policy identifier. |
| `policy_type` | Type from policy taxonomy. |
| `policy_name` | Human-readable policy name. |
| `policy_version` | Version for change control. |
| `policy_status` | Lifecycle state. |
| `policy_scope` | Scope where policy applies. |
| `policy_priority` | Priority for conflict resolution. |
| `policy_owner` | Owning authority or team. |
| `created_at` | Creation timestamp. |
| `updated_at` | Last metadata update timestamp. |
| `activated_at` | Activation timestamp. |
| `expires_at` | Expiration timestamp. |
| `deprecated_at` | Deprecation timestamp. |
| `revoked_at` | Revocation timestamp. |
| `decision_mode` | Allow, deny, review, gate, or advisory. |
| `allowed_actions` | Actions this policy can allow. |
| `denied_actions` | Actions this policy can deny. |
| `required_gates` | Gates this policy requires. |
| `conflict_behavior` | Conflict handling rule. |
| `audit_lineage_id` | Audit lineage for policy changes. |

## Derived Policy Fields

| Field | Source |
| --- | --- |
| `policy_effective_status` | lifecycle state plus freshness and scope match |
| `policy_conflict_status` | priority and decision conflict evaluation |
| `policy_applicability` | scope match against action context |
| `policy_decision_preview` | dry-run decision for proposed action |
| `policy_staleness_status` | expiration and update age |

## Decision Modes

```text
ALLOW
DENY
REQUIRE_REVIEW
REQUIRE_ADDITIONAL_GATE
ADVISORY
```

## Metadata Invariants

```text
policy_id_immutable=true
policy_version_monotonic=true
active_policy_must_have_scope=true
active_policy_must_have_owner=true
active_policy_must_have_audit_lineage=true
expired_or_revoked_policy_cannot_allow=true
```

## Metadata Verdict

Policy metadata model is defined.
