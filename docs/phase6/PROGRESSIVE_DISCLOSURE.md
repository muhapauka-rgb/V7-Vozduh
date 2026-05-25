# V7 Phase 6 Progressive Disclosure

## Purpose

Complexity should be available, not dumped.

## Layering

Layer 1: summary.

- health;
- impact;
- reason;
- next action.

Layer 2: grouped detail.

- users;
- channels;
- services;
- route classes;
- events.

Layer 3: advanced diagnostics.

- raw check output;
- JSON details;
- command results;
- logs.

## UI Rule

No raw table or metric wall should be visible before summary context exists.

## Current Compatibility

Current drawers and workspaces already provide a useful progressive-disclosure pattern. Future extraction should keep the pattern and reduce embedded JavaScript coupling.

