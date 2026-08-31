# Independent review record — PR #11 future studies workspace

Date: 2026-08-31

Reviewed PR: https://github.com/gharbonnier78/diderot-machine-learning-specialization/pull/11

Reviewed head at review time: `0dce8b6d18c84851c27d1de6aac3f805ddda9824`

Pinned harness: `gharbonnier78/scientific-research-harness@e80097fe8eb88c9e9340732683710ba1dc2ae008`

## Verdict

`APPROVE WITH NON-BLOCKING COMMENTS`

Scientific/pedagogical study-design assessment: approved in principle.

Merge readiness at review time: **not ready until branch reconciliation with current `main` and fresh CI**.

## Reviewer startup record

The reviewer confirmed the local harness pin from `harness-adoption.yaml` on current main and reviewed the PR body plus the two core artifacts:

- `studies/README.md`
- `studies/smets-equivariance-to-gcnn-lab.md`

The reviewer also compared the PR's original merge base with the newer `main` carrying the harness adoption.

The reviewer disclosed that the Smets PDF, `PEDAGOGICAL_CONCEPT_CONTRACT.md`, and `MATHEMATICAL_NOTATION_CAPITALIZATION.md` were not re-fetched in that pass. The mathematical fidelity of the Smets reading had already been independently reviewed in PR #9; PR #11 introduces a study design rather than a new source-attribution claim.

## Findings

### F1 — `studies/` abstraction

The workspace is considered justified and reusable. It fills a real gap between a reading note and implementation, and the four-layer distinction `SOURCE / DIDEROT / EXPERIMENT / EVIDENCE` is considered appropriate.

### F2 — lifecycle and gates

The lifecycle and gates G0-G8 are considered proportionate at this stage. The reviewer found that the study does not silently upgrade prose into evidence.

### F3 — evidence lineage

The chain from Smets source to Diderot reading, prior PR #9 independent review, study design, future chapter/lab and future evidence review is preserved. In particular, the PR #9 review is not treated as validation of the future protocol, implementation or G-CNN outcomes.

### F4 — H1-H5

H1-H5 are considered genuinely falsifiable. H4 explicitly allows augmentation to be the best practical result. H5 should be tightened before `LAB_CANDIDATE`: the expected plateau shape is currently more directional than the other hypotheses and should receive a cleaner two-sided/refutation formulation.

### F5 — baseline fairness

The listed fairness controls are appropriate for a pedagogical lab, but two items must become operational rules before `LAB_CANDIDATE`:

- what constitutes a comparable hyperparameter-search budget;
- how unavoidable parameter-count/capacity differences are handled and reported.

These are non-blocking for the current `STUDY_DESIGN` PR.

### F6 — equivariance error versus numerical error

The reviewer identified this as a particularly strong part of the design. The study separates network equivariance error from interpolation/grid/discretization effects and proposes a network-free transformation-control measurement.

### F7 — deliberately wrong symmetry

The counter-regime is scientifically important but is still only lightly specified. Before `LAB_CANDIDATE`, it should receive a mini-spec explaining exactly how absolute orientation becomes informative without making the answer trivial by construction.

### F8 — future PR separation

The planned split into pedagogical chapter, lab infrastructure/frozen protocol, experimental results/evidence review, and final book integration is considered sound and helpful against post-hoc protocol fitting.

## Branch / CI finding

At review time, the PR branch was cut from `204c90de72a426591140e34cc85108683d3c1f1d`, while current main had advanced to `0ccf7c1713fda17ded8158dbba91ea702598649d` with the reviewed harness adoption, including `AGENTS.md`, `CLAUDE.md`, `harness-adoption.yaml`, `docs/harness-meta.md` and `tests/test_harness_bootstrap.py`.

Therefore the earlier successful CI run #180 was not considered a final merge gate: it had not executed against the current-main harness bootstrap and tests.

Required merge gate from the review:

1. reconcile PR #11 branch with current `main`;
2. preserve both the harness-adoption artifacts and the studies changes;
3. run fresh CI on the reconciled head;
4. inspect the final diff and ensure no new blocker appears.

## Exact next admissible action

Reconcile the branch with current `main`, run fresh CI, and merge only if that reconciled CI succeeds and no new blocking finding appears.

## Deferred conditions before `LAB_CANDIDATE`

The following are explicitly retained as future design gates, not blockers for merging the studies workspace:

- tighten H5's outcome/refutation formulation;
- freeze a concrete fairness/hyperparameter-budget rule;
- specify the wrong-symmetry counter-regime;
- define stochastic-run seed lineage and environment capture before outcome-bearing training;
- freeze primary endpoints/statistical treatment before main experimental runs.
