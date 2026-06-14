# UX.3 REAL WORLD OPERATOR SCENARIOS AND FINAL VISUAL MOCKUPS REPORT

Project: V7 Vozduh
Date: 2026-06-14
Branch inspected: `Updatesystem`
Mode: visual operator mockups only

No UI implementation was performed. No UI was modified. No drawer was changed. No workflow was changed. No deploy was performed.

## Truth Gate

| Gate | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED |
| `tools/v7-convergence-status --json` | PASS / ALIGNED |

Operator rule for all mockups:

- Understand situation in 5 seconds.
- Know what to do in 10 seconds.
- Screen 1 shows only the daily operator answer.
- Details and Evidence are available only after the operator asks for them.

## 1. Scenario 1 Mockup

Scenario: user is healthy. Internet works. No action required.

### Desktop - Screen 1

```text
--------------------------------------------------
USER
--------------------------------------------------
Ivan Petrov
Acme Logistics
+7 900 111-22-33
MacBook Air / 10.0.0.21

--------------------------------------------------
STATUS
--------------------------------------------------
Works
Internet is connected

--------------------------------------------------
CURRENT
--------------------------------------------------
Channel: awg3
Connection: Online
Profile: Ready
Route: OK

--------------------------------------------------
WHY
--------------------------------------------------
Reason: Current channel is working well          [Details]

--------------------------------------------------
ACTION
--------------------------------------------------
[Observe]                                        [Details]

--------------------------------------------------
```

### Mobile - Screen 1

```text
------------------------------
USER
------------------------------
Ivan Petrov
Acme Logistics
+7 900 111-22-33
10.0.0.21

------------------------------
STATUS
------------------------------
Works
Internet is connected

------------------------------
CURRENT
------------------------------
Channel: awg3
Connection: Online
Profile: Ready
Route: OK

------------------------------
WHY
------------------------------
Current channel is working well
[Details]

------------------------------
ACTION
------------------------------
[Observe]
[Details]
------------------------------
```

### Screen 2 After Details

```text
--------------------------------------------------
DETAILS
--------------------------------------------------

State
Profile: Ready
Connection: Online
Route: OK
Speed: Last check OK

Checklist
Profile          OK
Connection       OK
Route            OK
Leak             No risk
Speed            OK

Why
Current channel is working well.
No safer or better move is needed now.

Profile
Latest link: delivered
Client: Karing

Route
Expected: awg3
Actual: awg3
Leak risk: No

Speed
V7: 84 Mbps
Direct: 91 Mbps
Drop: 8%

Actions
[Refresh]  [Request Speed]  [Logs]
--------------------------------------------------
```

### Screen 3 Evidence / History

```text
--------------------------------------------------
EVIDENCE / HISTORY
--------------------------------------------------

Evidence
Last route check: OK
Last profile check: OK
Last speed check: OK

History
No recent problems
No recent switches
No failed commands

Decision
Keep current channel
Reason: working and stable
--------------------------------------------------
```

## 2. Scenario 2 Mockup

Scenario: user exists. Profile has not been issued.

### Desktop - Screen 1

```text
--------------------------------------------------
USER
--------------------------------------------------
Maria Smirnova
North Trade
+7 900 222-33-44
iPhone / 10.0.0.34

--------------------------------------------------
STATUS
--------------------------------------------------
Needs Action
Profile is missing

--------------------------------------------------
CURRENT
--------------------------------------------------
Channel: awg5
Connection: Not connected
Profile: Missing
Route: Not checked

--------------------------------------------------
WHY
--------------------------------------------------
Reason: Profile was never issued                 [Details]

--------------------------------------------------
ACTION
--------------------------------------------------
[Issue Profile]                                  [Details]

--------------------------------------------------
WARNING
--------------------------------------------------
User cannot connect until profile is issued
--------------------------------------------------
```

### Mobile - Screen 1

```text
------------------------------
USER
------------------------------
Maria Smirnova
North Trade
+7 900 222-33-44
10.0.0.34

------------------------------
STATUS
------------------------------
Needs Action
Profile is missing

------------------------------
CURRENT
------------------------------
Channel: awg5
Connection: Not connected
Profile: Missing
Route: Not checked

------------------------------
WHY
------------------------------
Profile was never issued
[Details]

------------------------------
ACTION
------------------------------
[Issue Profile]
[Details]

------------------------------
WARNING
------------------------------
Cannot connect without profile
------------------------------
```

### Screen 2 After Details

```text
--------------------------------------------------
DETAILS
--------------------------------------------------

State
Profile: Missing
Connection: Not connected
Route: Waiting for profile
Speed: No measurement

Checklist
Profile          Needs action
Connection       Waiting
Route            Waiting
Leak             Not checked
Speed            No measurement

Why
The user has no issued profile.
First action is profile issue, not route repair.

Profile
Generated file: No
One-time link: No
Client: Karing

Connection
Next step: send profile link to user

Actions
[Issue Profile]  [Refresh]  [Logs]
--------------------------------------------------
```

### Screen 3 Evidence / History

```text
--------------------------------------------------
EVIDENCE / HISTORY
--------------------------------------------------

Evidence
Profile file: not found
One-time link: not created
Connection events: none

History
User created
No profile issue event
No first connection

Decision
Do not check route yet
Reason: profile must be issued first
--------------------------------------------------
```

## 3. Scenario 3 Mockup

Scenario: profile exists. User never connected.

### Desktop - Screen 1

```text
--------------------------------------------------
USER
--------------------------------------------------
Alex Kim
Delta Finance
+7 900 333-44-55
Android / 10.0.0.48

--------------------------------------------------
STATUS
--------------------------------------------------
Waiting
User has not connected yet

--------------------------------------------------
CURRENT
--------------------------------------------------
Channel: awg2
Connection: Never seen
Profile: Ready
Route: Waiting

--------------------------------------------------
WHY
--------------------------------------------------
Reason: Profile exists, but user never connected [Details]

--------------------------------------------------
ACTION
--------------------------------------------------
[Send Link Again]                                [Details]

--------------------------------------------------
WARNING
--------------------------------------------------
Ask user to open the profile on the phone
--------------------------------------------------
```

### Mobile - Screen 1

```text
------------------------------
USER
------------------------------
Alex Kim
Delta Finance
+7 900 333-44-55
10.0.0.48

------------------------------
STATUS
------------------------------
Waiting
User has not connected yet

------------------------------
CURRENT
------------------------------
Channel: awg2
Connection: Never seen
Profile: Ready
Route: Waiting

------------------------------
WHY
------------------------------
Profile exists, no connection yet
[Details]

------------------------------
ACTION
------------------------------
[Send Link Again]
[Details]

------------------------------
WARNING
------------------------------
Ask user to open profile
------------------------------
```

### Screen 2 After Details

```text
--------------------------------------------------
DETAILS
--------------------------------------------------

State
Profile: Ready
Connection: Never seen
Route: Waiting for first connection
Speed: No measurement

Checklist
Profile          OK
Connection       Needs user action
Route            Waiting
Leak             Not checked
Speed            No measurement

Why
The profile is ready.
V7 has not seen the user connect yet.

Profile
Latest link: created
Downloaded: no data
Client: Karing

Connection
Next step: send the link again and ask user to open it

Actions
[Send Link Again]  [Check Connection]  [Logs]
--------------------------------------------------
```

### Screen 3 Evidence / History

```text
--------------------------------------------------
EVIDENCE / HISTORY
--------------------------------------------------

Evidence
Profile file: ready
One-time link: created
First connection: not found

History
Profile generated
Link created
No successful connection event

Decision
Do not switch channel
Reason: user has not connected yet
--------------------------------------------------
```

## 4. Scenario 4 Mockup

Scenario: user reports slow internet.

### Desktop - Screen 1

```text
--------------------------------------------------
USER
--------------------------------------------------
Olga Petrova
City Retail
+7 900 444-55-66
Windows Laptop / 10.0.0.63

--------------------------------------------------
STATUS
--------------------------------------------------
Needs Check
Speed complaint

--------------------------------------------------
CURRENT
--------------------------------------------------
Channel: awg4
Connection: Online
Profile: Ready
Route: OK

--------------------------------------------------
WHY
--------------------------------------------------
Reason: Internet works, speed needs measurement  [Details]

--------------------------------------------------
ACTION
--------------------------------------------------
[Request Speed Test]                             [Details]

--------------------------------------------------
WARNING
--------------------------------------------------
Do not move user before fresh speed check
--------------------------------------------------
```

### Mobile - Screen 1

```text
------------------------------
USER
------------------------------
Olga Petrova
City Retail
+7 900 444-55-66
10.0.0.63

------------------------------
STATUS
------------------------------
Needs Check
Speed complaint

------------------------------
CURRENT
------------------------------
Channel: awg4
Connection: Online
Profile: Ready
Route: OK

------------------------------
WHY
------------------------------
Works, but speed needs check
[Details]

------------------------------
ACTION
------------------------------
[Request Speed Test]
[Details]

------------------------------
WARNING
------------------------------
Check speed before move
------------------------------
```

### Screen 2 After Details

```text
--------------------------------------------------
DETAILS
--------------------------------------------------

State
Profile: Ready
Connection: Online
Route: OK
Speed: Needs fresh test

Checklist
Profile          OK
Connection       OK
Route            OK
Leak             No risk
Speed            Needs action

Why
The user is connected and route is OK.
The next safe step is speed measurement.

Speed
V7: no fresh measurement
Direct: no fresh measurement
Last result: old

Route
Expected: awg4
Actual: awg4
Leak risk: No

Actions
[Request Speed Test]  [Refresh]  [Logs]
--------------------------------------------------
```

### Screen 3 Evidence / History

```text
--------------------------------------------------
EVIDENCE / HISTORY
--------------------------------------------------

Evidence
Route check: OK
Connection: online
Fresh speed result: missing

History
User reported slow internet
No recent speed test
No recent channel switch

Decision
Measure speed first
Reason: route is OK and speed data is stale
--------------------------------------------------
```

## 5. Scenario 5 Mockup

Scenario: route mismatch and leak risk.

### Desktop - Screen 1

```text
--------------------------------------------------
USER
--------------------------------------------------
Sergey Volkov
Global Sales
+7 900 555-66-77
MacBook Pro / 10.0.0.79

--------------------------------------------------
STATUS
--------------------------------------------------
Blocked
Route mismatch

--------------------------------------------------
CURRENT
--------------------------------------------------
Channel: awg1
Connection: Online
Profile: Ready
Route: Leak risk

--------------------------------------------------
WHY
--------------------------------------------------
Reason: Traffic may bypass the expected route     [Details]

--------------------------------------------------
ACTION
--------------------------------------------------
[Check Route]                                    [Details]

--------------------------------------------------
WARNING
--------------------------------------------------
Leak risk: do not switch before route check
--------------------------------------------------
```

### Mobile - Screen 1

```text
------------------------------
USER
------------------------------
Sergey Volkov
Global Sales
+7 900 555-66-77
10.0.0.79

------------------------------
STATUS
------------------------------
Blocked
Route mismatch

------------------------------
CURRENT
------------------------------
Channel: awg1
Connection: Online
Profile: Ready
Route: Leak risk

------------------------------
WHY
------------------------------
Traffic may bypass route
[Details]

------------------------------
ACTION
------------------------------
[Check Route]
[Details]

------------------------------
WARNING
------------------------------
Leak risk
Do not switch yet
------------------------------
```

### Screen 2 After Details

```text
--------------------------------------------------
DETAILS
--------------------------------------------------

State
Profile: Ready
Connection: Online
Route: Leak risk
Speed: Not important yet

Checklist
Profile          OK
Connection       OK
Route            Needs action
Leak             Risk found
Speed            Later

Why
The user is connected, but route is not safe.
Fix route check before any move.

Route
Expected: awg1
Actual: mismatch
Leak risk: Yes
Meaning: traffic may bypass the expected path

Actions
[Check Route]  [Open Logs]  [Refresh]
--------------------------------------------------
```

### Screen 3 Evidence / History

```text
--------------------------------------------------
EVIDENCE / HISTORY
--------------------------------------------------

Evidence
Expected route: awg1
Actual route: mismatch
Leak check: risk found

History
Route warning created
No approved move
No rollback needed yet

Decision
Block movement
Reason: route is unsafe until rechecked
--------------------------------------------------
```

## 6. Simplicity Audit

| Scenario | Question | Answer Visible Within 5 Seconds? |
| --- | --- | --- |
| Healthy | Who is this? | Yes |
| Healthy | Is there a problem? | Yes: Works |
| Healthy | What is the problem? | Yes: no problem |
| Healthy | What should I do? | Yes: Observe |
| Healthy | Why? | Yes: current channel is working well |
| No Profile | Who is this? | Yes |
| No Profile | Is there a problem? | Yes: Needs Action |
| No Profile | What is the problem? | Yes: Profile is missing |
| No Profile | What should I do? | Yes: Issue Profile |
| No Profile | Why? | Yes: profile was never issued |
| No Connection | Who is this? | Yes |
| No Connection | Is there a problem? | Yes: Waiting |
| No Connection | What is the problem? | Yes: user has not connected yet |
| No Connection | What should I do? | Yes: Send Link Again |
| No Connection | Why? | Yes: profile exists, no connection yet |
| Speed Complaint | Who is this? | Yes |
| Speed Complaint | Is there a problem? | Yes: Needs Check |
| Speed Complaint | What is the problem? | Yes: Speed complaint |
| Speed Complaint | What should I do? | Yes: Request Speed Test |
| Speed Complaint | Why? | Yes: works, speed needs measurement |
| Route Issue | Who is this? | Yes |
| Route Issue | Is there a problem? | Yes: Blocked |
| Route Issue | What is the problem? | Yes: Route mismatch / leak risk |
| Route Issue | What should I do? | Yes: Check Route |
| Route Issue | Why? | Yes: traffic may bypass expected route |

## 7. Noise Audit

| Scenario | Item | Why It Is Noise |
| --- | --- | --- |
| Healthy | Speed details on Screen 1 | The user is healthy; detailed numbers belong in Details. |
| Healthy | History on Screen 1 | No problem, no action needed. |
| No Profile | Route/speed details on Screen 1 | Route and speed cannot be meaningful before profile issue. |
| No Profile | Multiple profile actions on Screen 1 | One primary action is enough. |
| No Connection | Route repair on Screen 1 | Route cannot be verified until first connection. |
| No Connection | Speed action on Screen 1 | Speed cannot be measured before connection. |
| Speed Complaint | Raw route/evidence on Screen 1 | Operator first needs a speed test, not audit detail. |
| Speed Complaint | Channel switch on Screen 1 | Moving before fresh speed check increases stress and risk. |
| Route Issue | Speed details on Screen 1 | Leak risk has priority over speed. |
| Route Issue | Move/approval controls on Screen 1 | Movement should be blocked until route is checked. |

## 8. Commercial Review

Score scale: 10 is best. For Operator Stress, 10 means lowest stress.

| Scenario | Metric | Score |
| --- | --- | ---: |
| Healthy | Understandability | 10 |
| Healthy | Speed | 10 |
| Healthy | Clarity | 10 |
| Healthy | Operator Stress | 10 |
| Healthy | Information Density | 9 |
| No Profile | Understandability | 10 |
| No Profile | Speed | 10 |
| No Profile | Clarity | 10 |
| No Profile | Operator Stress | 9 |
| No Profile | Information Density | 9 |
| No Connection | Understandability | 10 |
| No Connection | Speed | 10 |
| No Connection | Clarity | 9 |
| No Connection | Operator Stress | 9 |
| No Connection | Information Density | 9 |
| Speed Complaint | Understandability | 9 |
| Speed Complaint | Speed | 9 |
| Speed Complaint | Clarity | 9 |
| Speed Complaint | Operator Stress | 8 |
| Speed Complaint | Information Density | 8 |
| Route Issue | Understandability | 10 |
| Route Issue | Speed | 9 |
| Route Issue | Clarity | 10 |
| Route Issue | Operator Stress | 8 |
| Route Issue | Information Density | 9 |

## 9. Current vs Future

| Metric | Current | Future |
| --- | --- | --- |
| Visible buttons | 12-16 in quick drawer; 25+ in live drawer | 2 on Screen 1 |
| Visible sections | 6-7 in quick drawer; 20+ in live drawer | 5-6 compact rows on Screen 1 |
| Visible screens | 1.4-8.1 scroll screens depending drawer | 0.8-1.1 phone screens for Screen 1 |
| Time to understand | 30-90 seconds, often requires scanning forms/tables | 5 seconds |
| Time to first action | 30-120 seconds, many competing buttons | 10 seconds |
| Why visibility | Large card mixed with tables and metadata | One-line reason before action |
| Warning visibility | Mixed with detail and empty states | Only actionable warnings on Screen 1 |
| Operator stress | Higher: many choices and technical terms | Lower: one problem, one action |
| Evidence access | Mixed into daily drawer | Available after Details / Evidence |
| Mobile usability | Heavy tables and dense controls | Screen 1 stacked and table-free |

## 10. Final Recommendation

Proceed to UI implementation only after approving these visual mockups.

Recommended future default:

```text
--------------------------------------------------
USER
STATUS
CURRENT
WHY
ACTION
WARNING
--------------------------------------------------
```

The first screen should always answer:

```text
Who is this?
Is there a problem?
What is the problem?
What should I do?
Why?
```

Do not put detailed traffic, raw reasons, full metrics, logs, route tables, profile tables, history, or approval chains on Screen 1.

## 11. Verdict

Final verdict: READY_FOR_UI_IMPLEMENTATION.

Reason:

- All five real operator scenarios show a clear Screen 1.
- Desktop and mobile views are understandable without technical detail.
- Details and Evidence screens remain available for deeper work.
- Operator can understand the situation in 5 seconds.
- Operator can choose the next action in 10 seconds.
- No implementation, UI modification, deploy, or runtime change was performed.

Final alignment status at report creation:

| Check | Status |
| --- | --- |
| Local | PASS / ALIGNED |
| GitHub | PASS / ALIGNED |
| Runtime | PASS / ALIGNED with docs-only mismatch ignored |
| Overall | PASS / FULLY_ALIGNED before this docs-only report |

Post-commit and post-push alignment must be verified by the required after-report commands.
