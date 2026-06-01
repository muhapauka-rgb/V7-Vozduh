# Block C Runtime Audit

Project: V7 Vozduh

Block: C - Blast Radius Expansion Program

Date: 2026-06-01

## Target

- `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`
- Initial target count: `2`
- Stage 5 target count: `5`
- Stage 10 final target count: `10`
- Hard limit: `10`

## Runtime Hashes

Initial:

- `users_hash=0c8a625da1e572f49247b87c95d1188a98f02fb079be01f0a7ef6ad599ed3d4d`
- `egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

Final:

- `final_ten_users_hash=600ca744661e76ddb4d77098b7faedb333b4cd3f6daa2027de104939a88e165b`
- `final_ten_outside_scope_hash=f06aedcc6e8459553f14c2e110409e36cb4bc50c60979968de9649b78c0647cb`
- `final_ten_egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `final_ten_selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `final_ten_routes_outside_scope_hash=0c7a2021bf63faff31ff6970fa72c2ad2ef776ca6a4c7f9510df81e01417b12a`
- `final_ten_rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

## Health

Runtime checkers passed after Stage 5 and Stage 10:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Admin API health remained unavailable with curl rc `7`.

## Verdict

Runtime audit completed. The final target is at hard limit, so further expansion requires a new capacity decision.

