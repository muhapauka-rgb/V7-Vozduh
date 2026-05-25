# V7 Phase 5 Identity Runtime Consistency

## Purpose

Identity state and runtime state must not silently diverge.

## Critical Checks

The platform should detect:

- active device with no runtime registry row;
- runtime registry row with no known active device;
- revoked device still active in runtime;
- duplicate active devices sharing one VPN IP;
- pending profile expired but still pending;
- active delivery link for revoked/missing device;
- identity user references missing organization/group;
- allowed user references missing organization/group;
- org policy unreadable or invalid.

## Severity Model

critical:

- revoked device still active;
- duplicate active device IP;
- active device with missing assigned IP;
- corrupt identity DB.

warning:

- registry row has no active identity device;
- pending profile expiration stale;
- active delivery link cannot be mapped to active device;
- missing organization/group reference.

info:

- local/sandbox identity DB missing;
- optional delivery token file missing;
- no org policy configured.

## Required Tool Behavior

Identity consistency review must be:

- read-only;
- non-mutating;
- no shell execution;
- no profile generation;
- no registry writes;
- no route/nft/systemd changes.

## Operator Output

Output should group issues by:

- organizations;
- users;
- devices;
- pending profiles;
- delivery links;
- runtime registry.

