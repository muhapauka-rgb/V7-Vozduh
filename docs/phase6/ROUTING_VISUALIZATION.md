# V7 Phase 6 Routing Visualization

## Purpose

Routing visualization must explain policy and impact without becoming topology spaghetti.

## Allowed Visual Concepts

- user -> route class -> assigned egress;
- degraded path highlight;
- trusted RU status;
- direct routing exception status;
- service-specific degradation;
- autoswitch decision reason.

## Forbidden Visual Concepts

- giant network graph;
- all interfaces and route tables at once;
- animated engineering topology;
- raw nftables/rule dump as primary UI.

## Required Explanation

Each route visual must include:

- route class;
- effective egress;
- policy reason;
- health state;
- safety blocker if present.

