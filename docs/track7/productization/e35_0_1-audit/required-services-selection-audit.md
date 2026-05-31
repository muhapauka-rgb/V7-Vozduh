# E35.0.1 Required Services Selection Audit

## Scope

Audit question: how required services participate in selection.

## Service Sources

required_services_selection_audited=true

Autoswitch gathers important services from:

- policy `switch.required_services`
- policy `required_services`
- org policy `required_services`
- service preferences root `required_services`
- CLI `--service`
- per-user `service-preferences.json`

If there is no per-user schema v2 service row, defaults are used:

- YouTube
- Instagram
- Telegram
- Google
- Google Auth

Admin also exposes optional groups:

- ChatGPT -> `chatgpt`, `openai_auth`
- Claude -> `claude`, `anthropic`
- WhatsApp -> `whatsapp`

## Route Class Inference

Important services affect route class:

- video services -> `VIDEO_OPTIMIZED`
- Telegram/WhatsApp/Apple -> `GLOBAL_STABLE`
- Gosuslugi/banks/tax services -> `TRUSTED_RU_SENSITIVE`
- otherwise -> `GLOBAL_FAST`

Route class then affects route-class fitness and trusted-RU hard checks.

## Hard Blocks from Services

Required services can hard-block a channel when:

- Telegram is hard blocked/down.
- route class fitness is `FAIL`.
- multiple critical services fail.
- one service failure is persistent by sample count or bad-for window.
- `TRUSTED_RU_SENSITIVE` is required and the egress is not trusted.

## Soft Effects from Services

Required services can softly affect score when:

- Telegram is degraded.
- a single non-persistent service fails.
- services are OK and add service score.
- service latency affects latency score.
- route class fitness is WARN.

The score model includes:

- `service`
- `telegram_required`
- `latency`

## Proposal Layer

`service_recommendations()` separately evaluates the current channel and candidate channels against user-required services.

It emits:

- `KEEP_CURRENT`
- `SWITCH_AVAILABLE`
- `NO_EGRESS_MATCHES_REQUIRED_SERVICES`

`generated_proposals()` turns those into movement proposals or observations, but proposals are non-authoritative and non-executing.

## Answer by Service

Telegram:

- hard down can hard-block.
- degraded is soft warning/score penalty.

Google Auth:

- participates as normal required service and route class fitness.
- persistent or multi-service failure can hard-block.

YouTube / Instagram:

- influence `VIDEO_OPTIMIZED`.
- one transient failure is soft degraded.
- persistent failure or multiple critical failures can hard-block.

ChatGPT / Claude:

- known services in service catalog.
- if selected, they participate like other non-Telegram services.
- no special hard-coded stronger rule was found.

## Audit Verdict

required_services_affect_score=true
required_services_affect_ranking=true
required_services_can_hard_block=true
required_services_also_create_proposals=true
service_selection_is_not_proposal_only=true

## Important Caveat

Required services hard-block autoswitch candidates, but E35.0 found they are not yet a universal hard contract across every possible runtime movement path. Autonomous design should not assume universal enforcement until it is centralized.
