# E33.A Required Services Model

required_services_model_defined=true
required_services_integrated=true

## Purpose

Each user may have a list of required services from the admin panel.

Routing Intelligence must treat this as a first-class input. A target must be evaluated against the services that matter to the specific user.

## Required Service Record

```text
user_id
required_services[]
service_id
service_name
service_category
criticality
operator_source
created_at
updated_at
freshness
evidence_id
```

## Service Identifier Rules

Service identifiers must be stable and canonical.

Examples:

```text
youtube
telegram
instagram
whatsapp
google
openai
banking_ru
```

Display names may vary, but routing logic must use canonical service_id.

## Criticality

Supported criticality levels:

```text
REQUIRED
IMPORTANT
OPTIONAL
```

REQUIRED service failure blocks USER_TARGET_OK.

IMPORTANT service degradation lowers confidence and may produce REVIEW_REQUIRED.

OPTIONAL service degradation does not block recommendation but must be visible.

## Missing Required Services

If required_services are missing:

- do not assume all services are OK;
- output USER_TARGET_UNKNOWN for service-fit dimension;
- prefer observation recommendation or operator review;
- do not generate high-confidence movement proposal based only on global target health.

## Decision

required_services_model_defined=true
required_services_integrated=true
