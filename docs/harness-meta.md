# Harness meta-documentation

This repository is a **consumer** of the versioned
`gharbonnier78/scientific-research-harness`. The harness constrains method; it does not
replace the course material, mathematical sources, code, experiments or human judgment.

## Startup chain

```text
AGENTS.md / CLAUDE.md
        |
        v
harness-adoption.yaml
        |
        v
immutable scientific-research-harness ref
        |
        +-- HARNESS.md
        +-- task-relevant companion contracts
```

The short root files are deliberately maps rather than duplicated mega-prompts. The exact
harness commit is pinned in `harness-adoption.yaml` so a future harness change is an explicit
dependency upgrade rather than silent drift.

The current provisional pin is
`2d1cefe42676fafde9b4a2fa5bc6d300abdcfb4f`, the current head of upstream harness PR #18.
After review/merge, this repository should explicitly upgrade to the reviewed immutable
commit or tag.

## Mathematical notation

The book already has a publication-specific notation appendix at
`book/chapters/appendix-notation.tex`. That appendix is useful to a reader of this particular
book, but it should not become a second cross-domain learning registry.

The canonical Diderot notation-learning registry is maintained in:

`gharbonnier78/mmals-ml-wiki/mathematics/notation/registry.json`

Its interactive and printable views are:

- `mathematics/notation/index.html` — searchable/filterable atlas;
- `mathematics/notation/poster.html` — A2 landscape learning map.

When this specialization introduces a durable non-trivial notation, an agent should check
that canonical registry. If the concept already exists, append a meaningful encounter,
alias, domain or new disambiguation. If it does not, propose a draft entry containing at
least a spoken reading, formal/plain-language meaning, example, prerequisites, provenance,
connections and a relevant misconception.

A local book table may select a small subset of notation for publication, but it should be
regarded as a **derived publication view**, not the knowledge source.

## What can be automatic

Repository-agent runtimes that discover `AGENTS.md` or `CLAUDE.md` can be wired to load the
harness without requiring the human to restate that instruction in each task. Generic chat
surfaces that do not inspect repository instructions cannot be forced by a GitHub file
alone; their Project/workspace/agent configuration must load the same bootstrap separately.

Therefore the compliance question is not only “does the repo declare the harness?” but also
“did this runtime actually load the pinned dependency?”

## Authority boundary

- `sources/source_manifest.yaml` records the specialization's declared sources.
- Diderot explanations are pedagogical synthesis.
- The harness records method and review obligations.
- The canonical notation atlas records the learner-facing mathematical language and its
  provenance.

None of these layers should silently impersonate another.
