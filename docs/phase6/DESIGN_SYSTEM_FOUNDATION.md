# V7 Phase 6 Design System Foundation

## Purpose

Create a minimal design system foundation without overdesign.

## Tokens

Spacing:

- `space-1`: 4px;
- `space-2`: 8px;
- `space-3`: 12px;
- `space-4`: 16px;
- `space-5`: 20px.

Radius:

- small controls: 6px;
- cards/panels: 8px;
- drawers/modals: 12px.

Typography:

- body: system UI, 14px;
- compact body: 13px;
- section title: 15-18px;
- hero-scale type is not used in admin surfaces.

Status semantics:

- ok: safe/healthy;
- warning: needs attention;
- critical: unsafe/blocker;
- info: neutral context;
- muted: inactive/background.

## Component Families

- status pill;
- summary card;
- incident row;
- safe action preview;
- detail drawer;
- grouped diagnostics section;
- compact table;
- command result summary.

## Color Rule

Color must carry semantic status. It should not create decorative noise.

