# V7 Vozduh - Master Roadmap / Phases Overview

## Project Identity

V7 Vozduh is not a VPN service.

V7 is:

- an internet access routing platform;
- a self-healing routing system;
- an anti-blocking internet access orchestrator.

VPN, WireGuard, AmneziaWG, VLESS, OpenVPN, and similar protocols are transport layer components only.

The main goal of the platform is to:

- preserve stable internet access;
- hide routing complexity;
- adapt automatically to degradations;
- minimize operator firefighting.

The main priorities are:

1. stability;
2. speed;
3. datapath safety;
4. explainability;
5. observability;
6. adaptive stealth.

## Phase 0 - Freeze / Archive / Baseline

### Main Goal

Freeze the current project state and prepare the foundation for safe platform-grade development.

### Main Tasks

- repository cleanup;
- baseline freeze;
- runtime inventory;
- contracts discovery;
- legacy separation;
- risk map;
- runtime dependency mapping;
- admin monolith analysis.

### Main Result

V7 stops being live change chaos and gains:

- a clear baseline;
- documented runtime;
- architecture boundaries;
- a safe migration foundation.

## Phase 1 - Core Routing And Safety Stabilization

### Main Goal

Make datapath:

- deterministic;
- verifiable;
- observable;
- reconciliation-first;
- safe.

### Main Tasks

- kill switch hardening;
- routing reconciliation;
- route verification;
- runtime repair layer;
- route class formalization;
- direct/RU safety;
- health model foundation.

### Main Result

V7 becomes a safe routing platform, not a collection of VPN tunnels.

## Phase 2 - Provisioning And Egress Lifecycle

### Main Goal

Build a production-grade channel lifecycle management layer.

### Main Tasks

- staged provisioning;
- unified egress lifecycle;
- quarantine model;
- rollback and recovery;
- driver architecture;
- maintenance and drain mode;
- runtime verification before enable.

### Main Result

Adding new channels becomes:

- predictable;
- staged;
- safe;
- reversible.

## Phase 3 - Observability And Diagnostics Platform

### Main Goal

Make V7 a self-observable platform.

### Main Tasks

- unified health model;
- service matrix maturity;
- incident timeline;
- route diagnostics;
- datapath visibility;
- autoswitch explainability;
- compact diagnostics UX.

### Main Result

The system:

- understands its own state;
- explains problems;
- helps the operator;
- does not overload the interface.

## Phase 4 - Autoswitch Intelligence And Self-Healing

### Main Goal

Build a stable self-healing routing layer.

### Main Tasks

- anti-flapping;
- degradation persistence logic;
- service-aware switching;
- confidence-based switching;
- bounded migrations;
- graceful recovery;
- adaptive stealth hooks.

### Main Result

Autoswitch:

- preserves stability;
- hides problems from the user;
- does not create routing chaos.

## Phase 5 - Identity, Users And Commercial Multi-Tenant

### Main Goal

Prepare the platform for real users and organizations.

### Main Tasks

- organization isolation;
- user lifecycle;
- device lifecycle;
- onboarding maturity;
- safe profile delivery;
- reconnect and recovery UX;
- commercial readiness foundation.

### Main Result

V7 becomes a multi-tenant routing platform suitable for commercial operation.

## Phase 6 - New Admin Platform And Operator Experience

### Main Goal

Build a professional operator platform.

### Main Tasks

- split admin monolith;
- modular frontend/backend;
- workflow-oriented UI;
- operator-first UX;
- diagnostics grouping;
- routing visualization;
- scalable frontend architecture.

### Main Result

The admin platform becomes:

- modular;
- professional;
- scalable;
- calm;
- operator-oriented.

## Phase 6A - Minimal Operator UX Integration

### Main Goal

Integrate observability and platform diagnostics without breaking the minimalist interface philosophy.

### Main Tasks

- information hierarchy;
- progressive disclosure;
- summary-first UX;
- grouped diagnostics;
- diagnostic compression;
- cognitive load reduction;
- calm dashboard architecture.

### Main Result

Platform complexity is hidden inside the system instead of being transferred into the operator's head.

## Phase 7 - Scaling, Reliability And Infrastructure Maturity

### Main Goal

Prepare V7 for long-term production operation and growth.

### Main Tasks

- multi-egress scaling;
- resource management;
- backup/restore maturity;
- upgrade safety;
- disaster recovery;
- runtime persistence;
- graceful degradation;
- infrastructure reliability.

### Main Result

V7 becomes a durable infrastructure platform capable of long-term production operation.

## Phase 8 - Advanced Intelligence And Adaptive Stealth

### Main Goal

Add adaptive intelligence without breaking stability or explainability.

### Main Tasks

- adaptive stealth;
- predictive degradation;
- transport intelligence;
- operator assistance;
- route forecasting foundation;
- bounded adaptive routing;
- explainable intelligence.

### Main Result

V7 becomes an adaptive self-healing internet access platform while preserving a deterministic routing core.

## Global Development Principles

All phases must comply with:

- `V7_NON_NEGOTIABLES.md`;
- `V7_GOVERNANCE.md`.

## General Development Rules

It is forbidden to introduce:

- rewrite-from-scratch behavior;
- giant unsafe changes;
- hidden routing changes;
- overengineering;
- noisy UI growth;
- uncontrolled complexity;
- black-box AI routing.

All changes must be:

- bounded;
- reversible;
- observable;
- auditable;
- explainable;
- minimally invasive.

## Main V7 Principle

V7 must:

- hide complexity;
- preserve stable internet;
- reduce operator burden;
- adapt automatically;
- preserve predictability;
- preserve calm UX.

V7 must not become a chaotic VPN machine.

