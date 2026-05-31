# E35.B Operator Boundaries

## Product Meaning

Operator is the human routing authority for explicit manual intent.

## Operator Rights

| Question | Answer |
|---|---|
| Can operator pin user? | Yes, with reason/audit. |
| Can operator unpin user? | Yes, with audit. |
| Can operator place MANUAL mode? | Yes, if product policy enables it; model supports it now. |
| Can operator bypass autoswitch? | Yes. Pins/manual block autoswitch. |
| Can operator bypass suitability? | No for unsafe forward movement. Review-only exceptions require governance and audit. |
| Can operator bypass required services? | Not silently. Must require explicit override/review and cannot bypass safety-critical service failure for autonomous movement. |
| Can operator bypass safety? | No. |
| Can operator bypass governance? | No. |
| Can operator force movement? | Only through explicit manual/governed path that passes safety and runtime gates. |
| Can operator force unsafe movement? | No. |

## Non-Negotiable Operator Limits

Operator cannot:

- bypass kill switch;
- bypass runtime trust blocking forward movement;
- bypass execution-time recheck;
- bypass replay denial;
- silently override group regulated restrictions;
- make autoswitch ignore pins/manual mode.

## Admin Surface

Users drawer:

- pin/unpin;
- set AUTO;
- set MANUAL;
- reason;
- expiry;
- authority chain;
- blocked reason.

Logs:

- operator authority changes;
- denied override attempts.

## Runtime Mapping

Operator authority maps to:

- authority store;
- authority event log;
- admin manual switch path;
- governed execution packet override metadata.

## Storage Impact

Requires actor, reason, timestamp, expiry, evidence/proposal link.

## API Impact

Future write APIs must change authority state only unless they are explicit manual movement endpoints.

## Tests

- operator pin blocks autoswitch;
- operator cannot bypass safety;
- operator override of group requires audit;
- manual mode blocks autonomous movement;
- pin removal restores group/default authority.

## Verdict

```text
operator_boundaries_defined=true
```
