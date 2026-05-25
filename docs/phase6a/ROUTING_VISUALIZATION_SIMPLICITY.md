# V7 Phase 6A Routing Visualization Simplicity

## Purpose

Routing visualization should explain policy and impact without creating topology chaos.

## Show

- route class;
- assigned egress;
- effective path;
- trusted RU status;
- direct/RU exception state;
- degradation or mismatch;
- affected users.

## Hide Until Detail

- raw Linux route tables;
- nftables internals;
- every interface;
- every probe;
- every hop;
- every policy domain.

## Forbidden

- giant network graphs;
- animated topology;
- spaghetti diagrams;
- protocol-centered visual maps;
- visualizations that require networking expertise.

## Preferred Pattern

Use a simplified path:

user -> V7 policy -> egress/direct exception -> service

Then expose evidence through detail drawers.

