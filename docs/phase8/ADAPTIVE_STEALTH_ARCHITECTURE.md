# V7 Phase 8 Adaptive Stealth Architecture

## Purpose

Stealth should be adaptive, situational, and bounded.

It must not become always-on heavy obfuscation.

## Modes

normal_fast:

- preferred default;
- lowest performance overhead;
- used when no persistent blocking evidence exists.

elevated_stealth:

- temporary response to persistent service or regional blocking evidence;
- requires route-class policy compatibility;
- requires performance cost awareness.

severe_blocking_fallback:

- emergency fallback under strong blocking evidence;
- no automatic broad rollout;
- operator-visible, bounded, and reversible.

## Escalation Gates

Escalate only when:

- blocking evidence is persistent;
- service impact is real;
- target transport supports required capability;
- route class allows it;
- kill switch and policy remain valid;
- performance penalty is acceptable;
- confidence is medium or high.

## De-Escalation Gates

Return toward normal when:

- service health recovers;
- blocking evidence disappears;
- performance penalty remains high;
- recovery window passes;
- operator policy requests normal mode.

## Forbidden Behavior

- permanent heavy stealth by default;
- stealth escalation for tiny latency gains;
- stealth escalation that bypasses route classes;
- hidden transport changes.

