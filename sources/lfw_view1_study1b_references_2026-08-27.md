# LFW View 1 — Study 1B trusted source references

Date: 2026-08-27, updated 2026-08-28

Purpose: capitalise the reliable references and engineering/scientific lessons used to repair and audit the non-outcome Study 1B preflight in `siamese-embedding-compression-lab`.

## 1. Dataset/protocol authority — University of Massachusetts Amherst

**Labeled Faces in the Wild (LFW)** was introduced by Gary B. Huang, Manu Ramesh, Tamara Berg and Erik Learned-Miller in *Labeled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments*, University of Massachusetts Amherst, Technical Report 07-49 (2007).

Project endpoint:

- http://vis-www.cs.umass.edu/lfw/

Author/institution publication index:

- https://people.cs.umass.edu/~elm/papers_by_type.html

The paper distinguishes two evaluation views. View 1 is intended for algorithm development/model selection before formal reporting; View 2 is reserved for final reporting. The Study 1B design does **not** claim to reproduce an official LFW benchmark leaderboard: it uses the View-1 identity boundary as a provenance/split constraint for a separate matched-compression experiment.

## 2. Independent integrity authority — torchvision

PyTorch torchvision's LFW dataset implementation points its download prefix to the original UMass LFW site and publishes checksums for the canonical metadata files:

- https://docs.pytorch.org/vision/0.25/_modules/torchvision/datasets/lfw.html

Relevant MD5 values:

| File | Published MD5 |
|---|---|
| `peopleDevTrain.txt` | `54eaac34beb6d042ed3a7d883e247a21` |
| `peopleDevTest.txt` | `e4bf5be0a43b5dcd9dc5ccfcb8fb19c5` |
| `pairsDevTrain.txt` | `4f27cbf15b2da4a85c1907eb4181ad21` |
| `pairsDevTest.txt` | `5132f7440eb68cf58910c8a45a2ac10b` |

This is useful because source availability and source integrity are different questions. A mirror can be operationally convenient, but Study 1B should not trust a file merely because it has the right filename. The bytes must match an independently published canonical digest.

## 3. Availability fallback — commit-pinned HTTPS mirror

On 2026-08-27, the original UMass hostname could not be resolved from a GitHub-hosted runner. The preflight therefore remained fail-closed rather than reconstructing the missing identities from pair files.

A fallback source was then introduced:

- repository: `charlesreid1/in-your-face`
- immutable commit: `00d3f2e4bdcc3ef8a851e5e133cde29d2f574f15`
- paths: `data/peopleDevTrain.txt`, `data/peopleDevTest.txt`

This mirror is **not treated as a scientific authority**. It is acceptable only because the downloaded bytes are checked against the canonical MD5 values independently published by torchvision. If neither UMass nor a mirror produces those canonical bytes, Study 1B remains blocked.

The next GitHub preflight provided the expected evidence: the UMass hostname remained unavailable on the runner, the commit-pinned fallback was used, and both files matched the torchvision checksums exactly. The observed identity counts were 4038 for `peopleDevTrain` and 1711 for `peopleDevTest`, so the fallback changed byte availability, not the scientific identity boundary.

## 4. Operational image mirror — Kaggle LFW v4

Study 0/Study 1A already used:

- `jessicali9530/lfw-dataset/versions/4`

For Study 1B this remains an **operational image-byte mirror**, not the authority defining the View-1 identity partition. The 2026-08-27 preflight demonstrated that this package can materialise the image archive while omitting `peopleDevTrain.txt` / `peopleDevTest.txt`. Consequently metadata sourcing and image sourcing are now explicitly decoupled.

## 5. Engineering lesson captured

A reproducible ML experiment should separate four notions that are often conflated:

1. **scientific authority** — who defines the dataset/protocol semantics;
2. **integrity authority** — how canonical bytes are independently recognised;
3. **operational mirror** — where bytes are efficiently obtained today;
4. **experimental evidence artifact** — the exact bytes/hashes actually used in one run.

This separation reduces dependency on a single hosting service and makes source replacement auditable without changing the scientific object. A fifth practical concept is useful as well: **availability fallback**, whose role is only to provide canonical bytes when the primary host is temporarily inaccessible.

There is a second operational lesson: preflight dependencies should be proportional to the task. Metadata/hash/image-manifest validation does not require PyTorch/CUDA merely because later model extraction might. Splitting these environments reduced a large, unnecessary dependency download without changing the experiment.

## 6. From perceptual screening to deterministic second-stage review

The source preflight found no exact cross-role byte duplicate, but a deliberately sensitive dHash64 filter (`Hamming <= 4`) produced 18 **quasi-doublons candidats**. This is a useful distinction: a perceptual hash is a triage mechanism, not proof of leakage.

A second-stage rule was frozen before reading the candidate metrics. It compares the central 80% grayscale image, resized to 128x128, through three model-free quantities: normalized root-mean-square error (NRMSE), pixel correlation and gradient-magnitude correlation. The frozen rule is:

- NRMSE <= 0.08;
- pixel correlation >= 0.985;
- gradient correlation >= 0.97;
- 3/3 => blocking duplicate-like case;
- 2/3 => explicit review required;
- 0-1/3 => candidate cleared by this rule.

On the 18 candidates the result was 16 cleared, 1 ambiguous and 1 blocking. The blocking SCREEN/TRAIN pair had dHash distance 1, NRMSE about 0.01694, pixel correlation about 0.99680 and gradient correlation about 0.97033. The ambiguous TEST/TRAIN pair passed two criteria but not the gradient threshold. Because these thresholds were frozen before the observations, the correct response is **not to retune the thresholds until the blocker disappears**; it is to keep the preflight blocked and explicitly amend the data boundary if a conservative quarantine is selected.

This illustrates a general reproducibility principle: a preflight can legitimately discover a reason not to launch an experiment. A failed preflight is useful evidence, not a failed research programme.

## 7. Accélérer le rééchantillonnage sans changer l'estimateur

The initial scalar subject-slot bootstrap cost pilot took about 5.4 s per synthetic dataset for only 100 bootstrap replications. The statistical design, however, freezes 10,000 bootstrap replications and thousands of simulated datasets. Reducing those counts because execution is expensive would change the experiment.

Instead, the implementation was accelerated while preserving the statistical object:

- the subject multiplicity draw remains one multinomial draw per replication and in the same RNG order;
- genuine edges keep weight `m_i`, impostor edges keep `m_i*m_j`;
- candidate and reference routes receive the same subject draw;
- the whole-tie-block threshold rule at target FMR is unchanged;
- no degenerate replication is silently redrawn;
- no unobserved pair edge is synthesized.

An exact oracle test compares the accelerated path with the scalar reference on 257 replications including distance ties and potential degenerate draws. The summary quantities must match exactly before the accelerated path is admitted.

Three engineering iterations are informative. A first vectorized implementation reduced the 100-replication pilot to roughly 0.45 s/dataset. A broader batch-vectorization attempt regressed to about 0.72 s/dataset, and was therefore not retained as an improvement. A low-FMR prefix strategy then reduced the same pilot to about 0.22-0.23 s/dataset while keeping the exact oracle green. At a 1% target FMR, the threshold search usually needs only the beginning of the sorted impostor distances; the implementation therefore computes the full impostor total weight once, scans a deterministic prefix, preserves whole tie blocks, and expands that prefix without approximation only if necessary.

The lesson is broader than this experiment: **vectorization is not automatically faster**. Performance changes should themselves be treated as experiments with a correctness oracle, a cost measurement and a reversible decision.

## 8. Current boundary

The complete coverage and power simulation lots have **not** been launched. The deterministic quasi-duplicate review currently blocks the data preflight. A draft conservative amendment proposes identity-level quarantine of the four pseudonymous identities involved in the blocking and ambiguous pairs, with no replacement identities and unchanged requested pair counts; it is deliberately non-active until reviewed and explicitly authorized.

No biometric/compression Study 1B SCREEN or TEST outcome is contained in this entry.

## 9. Study 1B specific rule

Do not reconstruct `peopleDevTrain` / `peopleDevTest` identity membership from pair files. Pair files are task samples and need not enumerate every identity. Missing metadata is therefore a fail-closed provenance blocker, not permission to infer a replacement split.
