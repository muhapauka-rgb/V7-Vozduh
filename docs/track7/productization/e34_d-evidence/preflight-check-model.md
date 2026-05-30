# E34.D Preflight Check Model

preflight_check_model_defined=true

## Mandatory Checks

| Check | Severity | Fail Behavior |
| --- | --- | --- |
| disk space | BLOCKING for TEST/PRODUCTION | Stop until sufficient disk exists. |
| memory | BLOCKING for TEST/PRODUCTION | Stop or select smaller profile. |
| cpu | WARN/BLOCKING by profile | Warn in LAB; block production below floor. |
| network | BLOCKING | Stop if outbound/inbound assumptions fail. |
| public ip | BLOCKING for public deployment | Stop or select private/lab profile. |
| dns | BLOCKING when domain required | Stop until DNS resolves as expected. |
| time sync | BLOCKING | Stop because certificates, audits, and lineage depend on time. |
| wireguard requirements | BLOCKING if WG target required | Stop until kernel/tools available. |
| amneziawg requirements | BLOCKING if AWG target required | Stop until AWG runtime available. |
| reality requirements | BLOCKING if Reality/VLESS profile required | Stop until dependencies/config are valid. |
| tun availability | BLOCKING | Stop until TUN/TAP support exists. |
| permissions | BLOCKING | Stop until installer has required privileges. |
| required services | BLOCKING for PRODUCTION | Stop if service catalog/probe requirements are missing. |
| release availability | BLOCKING | Stop if certified release object is unavailable. |
| backup readiness | BLOCKING for PRODUCTION | Stop if verified backup/rollback plan unavailable. |

## Check Output

Each preflight check returns:

```text
check_id
status=PASS|WARN|FAIL|SKIP
severity
evidence
operator_message
recovery_hint
profile_applicability
```

## Fail-Closed Rule

Any BLOCKING preflight failure prevents INSTALLATION and READY states.

preflight_check_model_defined=true
