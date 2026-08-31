# Independent review record — PR #9 / Smets *Mathematics of Neural Networks*

Date: 2026-08-31

Repository: `gharbonnier78/diderot-machine-learning-specialization`

Pull request: `#9 — Document Smets Mathematics of Neural Networks in Diderot ML`

## Reviewer verdict

`APPROVE WITH NON-BLOCKING COMMENTS`

Final recommendation from the independent review: `MERGE AFTER MINOR FIXES`.

The reviewer reported **no blocking findings**.

## Scope actually audited by the independent reviewer

The reviewer:

- read the four PR files at head commit `1248dc6`;
- checked the arXiv v1 source for chapters 1–3.2.3;
- checked the remaining equivariance material through §3.5.1 against an earlier TU/e-hosted copy of the same lecture notes;
- confirmed the mathematical treatment of invariance/equivariance, `SE(2)`, homogeneous spaces, stabilizers, Theorem 3.32, group convolution, lifting, projection and discretization;
- confirmed that the note distinguishes continuous theoretical equivariance from discretized numerical equivariance;
- confirmed that the experimental proposal is falsifiable rather than written so that a G-CNN must win;
- confirmed that the repository status does not overstate the reading as a completed or experimentally validated chapter.

The reviewer could not independently recompute the local PDF SHA-256/byte size and did not fully audit §§3.5.2–3.5.3 in the exact local PDF copy.

## Review findings

### N1 — Internal traceability

The 517-line reading note had too few local source anchors. Recommendation: add lightweight section/theorem/equation references to Smets, approximately one anchor per substantive section rather than one citation per sentence.

**Resolution:** addressed in commit `7a0f75342c425c99a54b63936eaff84c05530e5b` by adding primary-source anchors throughout the note, including `Eq. (3.5)`, `Thm. 3.32`, `Ex. 3.33`, `§3.4.1–§3.4.4`, `Eq. (3.22)`, `Eq. (3.23)`, `Remark 3.37` and `Thm. 3.54`.

### N2 — Attribution of CNN weight sharing / translation equivariance

The statement that weight sharing gives a standard CNN translation equivariance is mathematically standard, but the review found the attribution to Smets too implicit.

**Resolution:** addressed in commit `7a0f75342c425c99a54b63936eaff84c05530e5b`. The note now labels this explicitly as **“Lecture Diderot — CNN classique et translation”**, distinguishes the property from a textual claim by Smets, and notes that padding/boundaries, subsampling, interpolation and other numerical details may break exact equivariance.

### N3 — Tropical section not fully independently audited

The independent reviewer could not fully access the exact source text for §§3.5.2–3.5.3.

**Resolution by source check after review:** the exact local PDF available to the authoring workflow confirms that Smets develops equivariant tropical operators through Theorem 3.54 and concludes that operators used in neural networks, particularly ReLU and max pooling, are special cases of tropical or tropically affine operators in the equivariant semimodule-homomorphism framework. The note now anchors this claim to `§3.5.1–§3.5.3` and `Thm. 3.54`.

### N4 — Source-date caution

The reviewer noted that older course copies may carry an earlier internal date, while the arXiv v1 PDF under review carries `12 November 2022`.

**Resolution:** no change required. The manifest and reading note identify the exact arXiv version and local copy.

## Provenance closure

The local source used for the Diderot analysis is recorded as:

- filename: `1786122202337.pdf`;
- bytes: `2,025,085`;
- SHA-256: `4f4900e1c7dfe4036cb01b459ecee2e6fcac042fd79bb4cf54304fc7ae652a75`.

The repository wording intentionally scopes this hash to the exact local bytes used for analysis and does not present it as an official checksum published by arXiv.

## Experimental follow-up retained

The future lab remains out of scope for PR #9. Its required comparison is:

1. standard CNN;
2. standard CNN + rotation augmentation;
3. rotation/translation G-CNN.

The review recommends fixing train/validation/test splits, repeated seeds and optimization budgets in advance, and distinguishing network equivariance error from interpolation/discretization error. These requirements have been incorporated into the proposed protocol in the reading note.

## Merge gate

PR #9 may be merged when:

- N1 and N2 are present in the final diff;
- CI passes on the amended head commit;
- no new review or CI blocker appears.

No second full independent review is required unless the corrective diff introduces a new mathematical or provenance change beyond the review findings above.
