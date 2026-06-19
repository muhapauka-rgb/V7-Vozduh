# PROBLEM_INVENTORY

Project: V7 VOZDUH  
Program: UX.3_CHANNELS_ACTION_FLOW_PASS  
Date: 2026-06-20  
Branch: Updatesystem

## Scope

Inventory covers operator-visible channel drawer problems and signal details.

No planner, routing, governance, database, storage, signal calculation, or score formula changes were made.

## Inventory

| Problem | Cause | Severity | Affects decision? | Operator action required? | Existing action handler | Target destination |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram unavailable | Service Matrix marks Telegram unavailable or not OK | Red | Y | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| Google unavailable | Service Matrix marks Google unavailable or not OK | Red | Y | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| Google Auth unavailable | Supporting service check unavailable | Red / diagnostics | Y when promoted to visible service issue | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| YouTube unavailable | Service Matrix marks YouTube unavailable or not OK | Red | Y | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| Instagram unavailable | Service Matrix marks Instagram unavailable or not OK | Red | Y | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| WhatsApp unavailable | Service Matrix marks WhatsApp unavailable or not OK | Red | Y | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| ChatGPT unavailable | Service Matrix marks ChatGPT unavailable or not OK | Red | Y | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| Claude unavailable | Service Matrix marks Claude unavailable or not OK | Red | Y | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| Services not measured | No recent Service Matrix data exists | Yellow / Red | Y when V7 cannot confirm service readiness | Y | `openChannelServicesPanel(id)` | Service Matrix for the channel |
| Assignment limit reached | Users assigned exceed soft/hard assignment limit | Red | Y | Y | `showChannelWorkspace('overview'); toggleChannelUsers(id); closeDrawer()` | Channel users expansion |
| Capacity warning | Users near preferred assignment limit | Yellow | N by itself, Y when planner/load gate restricts assignments | Y before adding users | `showChannelWorkspace('overview'); toggleChannelUsers(id); closeDrawer()` | Channel users expansion |
| Route not confirmed | Route/topology readiness is incomplete | Yellow / Red | Y when planner exposes route blocker; otherwise confidence only | N if no safe handler exists | Disabled safe action | Inline reason, engineering diagnostics |
| Route issue | Route/topology evidence reports a real issue | Red | Y | N if no safe handler exists | Disabled safe action | Inline reason, engineering diagnostics |
| No fresh data | Current signal evidence is stale or incomplete | Yellow | N by itself; lowers confidence | Optional | Existing signal destination if one exists | Service Matrix, users, logs, or disabled safe action |
| Runtime issue | Runtime readiness is partial or not measured | Yellow / Red | Y when readiness prevents confidence | Y | `openV2ChannelLogs(id)` | Channel logs |
| Runtime not measured | No readiness snapshot exists | Yellow | N by itself; lowers confidence | Y if operator needs source | `openV2ChannelLogs(id)` | Channel logs |
| Stability issue | Channel/interface/stability evidence is below threshold | Red | Y | Y | `openV2ChannelLogs(id)` | Channel logs |
| Interface down / not started | Runtime reports channel interface not up | Red | Y | Y through existing lifecycle controls/logs | `openV2ChannelLogs(id)` or existing channel lifecycle action where surfaced | Channel logs / existing channel controls |
| Channel disabled | Registry marks channel disabled | Red | Y | N in drawer unless existing lifecycle control is available | Disabled safe action in operator detail | Existing maintenance path outside first-screen action flow |
| History incomplete | Recent channel history is partial | Yellow | N by itself; lowers confidence | N | Disabled safe action | Automatic history refresh |
| Bad recent history | Planner/history signal reports recent negative state | Red | Y when promoted to decision problem | N | Disabled safe action | Automatic history/evidence |
| OK signal | Signal supports current V7 decision | Green | N | N | None | Stay in drawer |

## Action Categories

| Category | Meaning | Existing examples |
| --- | --- | --- |
| Observe | Read source or acknowledge no action is needed | Open logs, automatic history, no action required |
| Review | Open existing evidence/workspace before deciding | Open Service Matrix, open users |
| Execute | Prepare or open an existing governed action flow | Prepare governed user move after evacuation decision |

## No Dead-End Rule

Every expanded issue now contains:

1. Status
2. Reason
3. Decision impact
4. Action category, destination, and expected result
5. Existing action button or explicit unavailable/automatic explanation
