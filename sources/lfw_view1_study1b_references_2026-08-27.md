# LFW View 1 — Study 1B trusted source references

Date: 2026-08-27

Purpose: capitalise the reliable references used to repair and audit the non-outcome Study 1B preflight in `siamese-embedding-compression-lab`.

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

## 6. Study 1B specific rule

Do not reconstruct `peopleDevTrain` / `peopleDevTest` identity membership from pair files. Pair files are task samples and need not enumerate every identity. Missing metadata is therefore a fail-closed provenance blocker, not permission to infer a replacement split.

No biometric/compression Study 1B SCREEN or TEST outcome is contained in this entry.
