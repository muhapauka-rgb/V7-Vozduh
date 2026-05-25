# V7 Phase 6 Admin Platform Architecture

## Purpose

Phase 6 prepares V7 admin to evolve from one embedded executable into a professional operator platform.

This phase does not rewrite the admin runtime. It defines safe modular boundaries and creates a non-production frontend scaffold.

## Current Platform

Current admin is one runtime-critical file:

- `admin/v7-admin-api`;
- approximately 30067 lines;
- Python backend;
- embedded login page;
- embedded public connect page;
- embedded `admin-v2` HTML/CSS/JS;
- API handler and route dispatch;
- auth, RBAC, CSRF, audit;
- identity, provisioning, routing, diagnostics, policy, autoswitch, profile delivery.

## Target Shape

Backend modules:

- auth;
- state;
- identity;
- provisioning;
- routing;
- diagnostics;
- autoswitch;
- policy;
- audit;
- profile delivery.

Frontend modules:

- overview;
- users;
- channels;
- routing;
- diagnostics;
- security;
- logs;
- settings.

## Migration Rule

Extraction must be compatibility-first:

- keep existing executable path;
- keep existing endpoint paths;
- keep existing JSON response shapes until contract migration exists;
- keep legacy embedded admin as fallback;
- never change datapath as part of UI migration.

## Phase 6 Boundary

Phase 6 creates architecture contracts, frontend scaffold, design tokens, and static review tooling.

It does not introduce a production SPA, does not change routing behavior, and does not remove the old admin UI.

