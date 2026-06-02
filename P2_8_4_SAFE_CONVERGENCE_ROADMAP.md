# P2.8.4 Safe Convergence Roadmap

Project: V7 Vozduh
Block: P2.8.4

## Roadmap

1. Complete planning package.
   - P2.8.4 only creates documentation.
   - No branch creation.

2. Future branch preparation block.
   - Confirm branch base `origin/Updatesystem`.
   - Create branch only after explicit approval.

3. Baseline inventory.
   - Capture source hash, runtime hash, route inventory, function inventory.

4. Wave 1 runtime read APIs.
   - Preserve runtime-only execution read APIs.
   - Add tests and non-executable guarantees.

5. Wave 2 draft + validation preview.
   - Apply local candidate package.
   - Verify fail-closed behavior.

6. Wave 3 simulation + rollback.
   - Apply local candidate package.
   - Verify preview-only outputs.

7. Wave 4 candidate workflow.
   - Apply candidate approval/governance/rehearsal/workflow package.
   - Verify retention and archive behavior.

8. Wave 5 UI integration.
   - Integrate with `/admin-v2`.
   - Verify no dead hooks or missing routes.

9. Wave 6 tests and documentation.
   - Run unit/static tests.
   - Generate report and deploy manifest draft.

10. Review and release decision.
   - No deploy in convergence branch preparation.
   - Separate deploy block required.

safe_convergence_roadmap_defined=true
