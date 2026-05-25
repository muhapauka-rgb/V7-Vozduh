# V7 Phase 4 Adaptive Stealth Foundation

## Purpose

Phase 4 only prepares hooks for adaptive stealth. It does not implement full adaptive stealth or AI-driven routing.

## Modes

Future stealth behavior should use bounded modes:

- normal fast mode;
- elevated stealth mode;
- severe blocking fallback mode.

## Escalation Rules

Stealth should escalate only when:

- blocking evidence is persistent;
- route-class policy allows it;
- target transport supports required capability;
- performance cost is acceptable;
- operator policy allows escalation.

## De-Escalation Rules

Heavy stealth should not remain active forever. Recovery windows and service quality checks should allow return to normal fast mode.

## Autoswitch Integration

Autoswitch may use stealth capability as candidate metadata, but must not:

- always prefer heavy obfuscation;
- override route classes;
- bypass kill switch;
- silently change transport behavior.

## Future Data Needed

- transport capabilities;
- regional blocking patterns;
- service-specific blocking evidence;
- historical survivability;
- performance penalty summaries.

