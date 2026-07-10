# V7 Stage 2.3 Deduplication Semantics Research

Date: 2026-07-07

Research Type: `INDEPENDENT_ARCHITECTURAL_RESEARCH`

Primary inputs:

- `docs/programs/V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM.md`
- `docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION_RERUN.md`
- `docs/reports/research/V7_STAGE2_3_KNOWLEDGE_DEDUPLICATION.md`

Restrictions:

- Stage 2 program was not changed.
- Stage 2.3 report was not changed.
- Stage 2.3 results were not changed.
- Stage 2.4 was not started.
- No Knowledge Graph, Canonical Knowledge, Acceptance, or Lock artifact was created.

## 1. Research Question

The research question is:

```text
What exactly is the result of Stage 2.3 Knowledge Deduplication?
```

This report does not assume that the Stage 2.3 result is correct. It checks whether the program requires literal duplicate-object removal, repeated-engineering-concept consolidation, thematic concept grouping, or a separate Concept Registry.

## 2. Program Evidence

The Stage 2 program defines Stage 2.3 as:

```text
Collapse repeated knowledge into single canonical concepts while preserving all provenance.
```

The program also states that deduplication must not erase meaningful differences between:

- law and implementation rule;
- architecture boundary and runtime boundary;
- current truth and history;
- owner and consumer;
- certification evidence and canonical owner;
- prohibition and recommendation;
- terminal state and superseded state.

The Stage 2 Knowledge Object Model states:

```text
A Knowledge Object is the minimum engineering knowledge unit in Stage 2.
It is not a new architecture entity, not a graph node, not a canonical concept, and not canonical prose.
It is the atomic extracted unit consumed by Stage 2.3.
```

The Stage Input / Output Contract defines Stage 2.3 outputs as:

- Deduplicated Knowledge Registry;
- Knowledge Merge Map;
- Superseded Knowledge Map;
- Stage 2.3 report.

The Stage 2.4 purpose is:

```text
Build the graph of Stage 2 knowledge objects and relationships.
```

Stage 2.4 required edge families include relationships such as:

- verifies;
- governs;
- depends_on;
- derives_from;
- supersedes;
- should_promote_to;
- should_remain_historical.

## 3. Question-by-Question Analysis

### 3.1 Literal Duplicate Objects Or Repeated Engineering Concepts

Stage 2.3 is not limited to literally identical Knowledge Object rows.

The program uses the phrase `duplicate concepts`, not `identical rows`, and requires repeated knowledge to collapse into canonical concepts. Therefore Stage 2.3 must look for repeated engineering concepts, even if titles or wording differ.

However, the same program forbids merging when meaningful differences exist. Therefore Stage 2.3 must not merge objects merely because they share:

- similar wording;
- related category;
- same source family;
- same destination;
- same broad theme.

Finding:

```text
STAGE_2_3_DEDUPLICATES_REPEATED_ENGINEERING_CONCEPTS
NOT_LITERAL_ROWS_ONLY
NOT_THEME_CLUSTERING
```

### 3.2 Meaning Of Deduplicated Knowledge Registry

The Deduplicated Knowledge Registry stores deduplicated canonical concepts for Stage 2.3 purposes.

This does not mean it stores Stage 2.5 canonical prose or final locked knowledge. It means it stores the deduplicated concept set that Stage 2.4 can consume.

If multiple extracted Knowledge Objects represent the same engineering concept, the Deduplicated Knowledge Registry should contain one retained deduplicated concept with preserved source objects and provenance.

If no duplicate concept exists, a one-to-one retained registry is valid.

Finding:

```text
DEDUPLICATED_KNOWLEDGE_REGISTRY = DEDUPLICATED_CANONICAL_CONCEPT_SET
NOT_STAGE_2_5_CANONICAL_PROSE
NOT_RAW_EXTRACTED_OBJECTS_ONLY
```

### 3.3 Can One Canonical Concept Contain Multiple Knowledge Objects Without Their Loss

Yes, but only when the multiple Knowledge Objects represent the same engineering concept.

In that case, the Deduplicated Knowledge Registry may contain one deduplicated concept with multiple source Knowledge Objects preserved as provenance and source membership. That is a true merge or consolidation.

No, if the Knowledge Objects represent related but distinct engineering concepts. Related concepts should remain separate deduplicated entries and later be connected in Stage 2.4 Knowledge Graph.

Finding:

```text
MULTI_OBJECT_CANONICAL_CONCEPT_ALLOWED_ONLY_FOR_DUPLICATE_CONCEPTS
RELATED_BUT_DISTINCT_OBJECTS_MUST_REMAIN_SEPARATE
```

### 3.4 Should Knowledge Merge Map Also Record Membership

The Knowledge Merge Map must record membership when a merge actually happens.

For example:

```text
Deduplicated Concept X
  <- Source Knowledge Object A
  <- Source Knowledge Object B
```

That membership is required to preserve provenance for merged objects.

However, the Merge Map should not become a general thematic membership map for related but non-merged concepts.

The example:

```text
Verification Concept
  -> Reality First
  -> Verification Before Promotion
  -> Evidence Before Consumption
```

is not a deduplication merge under the current program. These are distinct verification-related concepts:

- `Reality First Law` protects reality/source-of-truth discipline;
- `Verification Before Promotion` protects promotion lifecycle;
- `Evidence Requires Verification Before Consumption` protects evidence-consumption discipline.

They are related. They are not duplicates. Their relationship belongs in Stage 2.4 Knowledge Graph, not in Stage 2.3 Merge Map.

Finding:

```text
MERGE_MAP_MEMBERSHIP_REQUIRED_FOR_ACTUAL_MERGES
THEMATIC_MEMBERSHIP_BELONGS_TO_STAGE_2_4_GRAPH
```

### 3.5 Was MERGES = 0 Correct Or Too Literal

`MERGES = 0` is correct if, after review, no two admitted Stage 2.2 Knowledge Objects represent the same engineering concept.

The Stage 2.3 report reviewed the most likely near-neighbor groups and intentionally retained them because they preserve different engineering meanings:

- chain completeness versus individual domain responsibilities;
- baseline lock versus closed-by-default law versus Stage 2 architecture-change prohibition;
- different verification surfaces;
- authority ownership versus authority misuse;
- rollback authorization versus closure evidence;
- state machine versus stage-gate law;
- different producer/consumer stage contracts;
- different forbidden-action families;
- different ADR evidence rules.

These are not literal duplicates and not repeated engineering concepts. Merging them would erase the distinctions the program explicitly protects.

Finding:

```text
MERGES_0_IS_VALID_FOR_CURRENT_INPUT_SET
NO_EVIDENCE_OF_OVER_LITERAL_DEDUPLICATION_FOUND
```

### 3.6 Should Stage 2.3 Build A Concept Registry Instead Of A Merged Registry

Stage 2.3 already produces a Deduplicated Knowledge Registry, which is a deduplicated concept registry for repeated concepts.

But Stage 2.3 should not build a broad thematic Concept Registry that groups related concepts under abstract headings such as `Verification Concept`, `Governance Concept`, or `Authority Concept`.

That broader relationship work is assigned to Stage 2.4 Knowledge Graph, whose purpose is to build the graph of knowledge objects and relationships.

If Stage 2.3 created thematic membership groups, it would risk performing Stage 2.4 work early.

Finding:

```text
STAGE_2_3_SHOULD_NOT_BUILD_THEMATIC_CONCEPT_REGISTRY
STAGE_2_3_DEDUPLICATED_REGISTRY_IS_SUFFICIENT
STAGE_2_4_OWNS_RELATIONSHIP_GRAPHING
```

## 4. Interpretation Matrix

| Interpretation | Program fit | Consequence | Verdict |
|---|---|---|---|
| Literal identical-row deduplication only | Too narrow | Would miss true duplicate concepts with different wording. | REJECTED |
| Repeated engineering concept deduplication | Best fit | Merges only same concept while preserving provenance and meaningful differences. | ACCEPTED |
| Thematic concept membership registry | Too broad for Stage 2.3 | Would move relationship graphing into Stage 2.3 and blur Stage 2.4 boundary. | REJECTED |
| Canonical prose creation | Wrong stage | Would perform Stage 2.5 early. | REJECTED |

Architecturally correct interpretation:

```text
Stage 2.3 produces a deduplicated canonical concept set by consolidating repeated engineering concepts only.
It does not cluster related concepts thematically.
It does not build the Knowledge Graph.
It does not create Stage 2.5 canonical prose.
```

## 5. Assessment Of Current Stage 2.3 Result

The current Stage 2.3 report states:

```text
EXTRACTED_KNOWLEDGE_OBJECTS_IN = 65
DEDUPLICATED_KNOWLEDGE_OBJECTS_OUT = 65
MERGES_PERFORMED = 0
DUPLICATE_RATIO = 0.00
DEDUPLICATION_COVERAGE = 100%
```

It also documents intentional non-merges for the major near-neighbor groups.

This is consistent with the program because:

- every object was reviewed;
- no repeated engineering concept was proven;
- meaningful distinctions were preserved;
- no relationship graph was built;
- no canonical prose was created;
- no object provenance was lost.

The result is not evidence that deduplication was understood too literally. It is evidence that the Stage 2.2 atomicity refinement produced already-distinct engineering units and that Stage 2.3 correctly refused to collapse related but non-duplicate concepts.

## 6. Program Sufficiency Analysis

The program is sufficient for the current question because it already defines:

- Stage 2.3 as collapse of repeated knowledge into canonical concepts;
- preservation requirements that prevent unsafe merging;
- Stage 2.4 as the relationship graph stage;
- Stage 2.5 as the canonical knowledge prose stage;
- Knowledge Object as not itself a graph node, canonical concept, or canonical prose.

Potential ambiguity:

The phrase `canonical concepts` may tempt a reader to create broad thematic concepts during Stage 2.3. However, the surrounding Stage Boundaries and Stage 2.4 relationship responsibility resolve that ambiguity sufficiently for execution.

Refinement need:

```text
NO_PROGRAM_REFINEMENT_REQUIRED
```

Reason:

The correct interpretation can be deterministically derived from existing program text. The program distinguishes deduplication, graph relationship building, and canonical knowledge creation across separate stages.

## 7. Final Architecture Verdict

```text
PROGRAM_IS_CORRECT
```
