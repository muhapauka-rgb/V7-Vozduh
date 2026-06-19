# CHANNEL_ATTENTION_MATRIX

Project: V7 VOZDUH
Program: UX.4_CHANNELS_ATTENTION_FIRST_PASS
Date: 2026-06-20
Branch: Updatesystem

## Scope

This matrix defines the operator attention order for the existing Channels surface.

It does not introduce a new planner, new assignment model, new signal calculation, new execution path, new storage, or new truth source. Attention is derived from existing Channel Decision V7, first-level channel signals, Overview Attention items, channel status, service matrix, capacity/load, runtime readiness, and stability.

## Priority Model

| Priority | Operator meaning | Source |
| --- | --- | --- |
| Critical | Look first. Users may need to leave or users are on a channel V7 should not use. | Existing Channel Decision V7 and channel attention items |
| Action Required | Action exists now. Operator should open the existing destination. | Existing signal/action flow and Overview Attention |
| Review | Needs fresh check or investigation, but does not outrank a V7 decision by itself. | Existing first-level signal severity |
| Information | Role or state matters, but it can wait if no users/problem are affected. | Existing assignment role and calm states |
| Healthy | Safe to ignore during triage. | Use/Keep plus no red first-level signal |

## Attention Inventory

| State | Severity | Action required? | Urgent? |
| --- | --- | --- | --- |
| Evacuate | Critical | Yes | Yes |
| Blocked with users | Critical | Yes | Yes |
| Disabled with users | Action Required | Yes | Yes |
| Channel not started with users | Action Required | Yes | Yes |
| Load hard/full/over limit | Action Required | Yes | Yes when users are assigned |
| Service degradation | Action Required or Review | Yes | Depends on affected service count |
| Runtime issue | Action Required or Review | Yes when visible as a problem | No if only stale evidence |
| Stability issue | Action Required or Review | Yes when below required level | No if only stale evidence |
| Missing service data | Review | Review existing Service Matrix | No |
| Missing readiness data | Review | Review existing drawer/diagnostics | No |
| Emergency Only | Information | No by itself | No |
| Blocked without users | Information | No by itself | No |
| Use with all first-level signals OK | Healthy | No | No |
| Keep with all first-level signals OK | Healthy | No | No |

## Sorting Rule

Attention First mode sorts:

1. Critical
2. Action Required
3. Review
4. Information
5. Healthy

Tie-breakers:

1. More assigned users first.
2. Worse first-level signal first.
3. Existing default operator order.
4. Channel name.

Default mode preserves existing table behavior, including manual table sorting.

## Visual Rule

Urgent rows receive a narrow left marker only. The table must remain calm:

- no duplicate alert system;
- no score-based attention;
- no aggregate `Signals` column sorting;
- no noisy badge multiplication;
- healthy channels stay visually quiet.

## Reuse Rule

Attention entries open existing destinations only:

- Channel Drawer
- Service Matrix
- Channel users expansion
- Logs / diagnostics
- Existing governed user/action flows when already present

No item may create a new execution path or new channel decision.
