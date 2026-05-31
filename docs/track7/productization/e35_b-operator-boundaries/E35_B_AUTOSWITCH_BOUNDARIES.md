# E35.B Autoswitch Boundaries

## Product Meaning

Autoswitch is a system actor that may manage routing for users delegated to AUTO.

## Autoswitch Rights

| Question | Answer |
|---|---|
| Can autoswitch move AUTO users? | Yes, if apply authority exists and all gates pass. |
| Can autoswitch move PINNED users? | No. Emergency containment is separate and must be labeled as containment, not normal autoswitch. |
| Can autoswitch move MANUAL users? | No. |
| Can autoswitch break group restrictions? | No. |
| Can autoswitch ignore required services? | No. |
| Can autoswitch ignore capacity? | No. |
| Can autoswitch ignore safety? | No. |
| Can autoswitch ignore governance? | No. |

## Non-Negotiable Autoswitch Limits

Autoswitch cannot:

- use speed to override hard blocks;
- use score to override hard blocks;
- move execution-only target users outside governed execution;
- drain canary/execution reserved target without explicit separate approval;
- act when selected_moves/restore-settle/runtime checks are unsafe;
- mutate users outside selected approved moves.

## Admin Surface

Channels:

- autoswitch plan shows denied-by-boundary reasons.

Users:

- user drawer shows "Autoswitch allowed/blocked".

Logs:

- autoswitch boundary denial.

## Runtime Mapping

Autoswitch boundary check must happen:

- before selected moves are accepted;
- before apply path runs;
- before movement command is built.

## Storage Impact

No ownership truth in autoswitch state. Autoswitch reads authority state.

## API Impact

Autoswitch preview response should include:

- authority decision;
- boundary block reason.

## Tests

- AUTO user can move normally;
- pinned user denied;
- manual user denied;
- group excluded channel denied;
- required service hard failure denied;
- speed cannot override authority.

## Verdict

```text
autoswitch_boundaries_defined=true
```
