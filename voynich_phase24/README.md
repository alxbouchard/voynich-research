# Phase 24 — Persistent word pairs

`NOT_TRANSLATION`. This tests whether a specified cross-folio word-pair criterion distinguishes six stable word-code controls from specified copying mechanisms, then challenges semantic specificity with persistent stochastic preferences. It is not a decoder.

**Completed result:** 6/6 bijective controls pass, 0/6 local-copy and 0/6 published Java-generator controls pass, but 6/6 segment-preference and 6/6 Markov controls also pass. The criterion is not specific to a target message. No manuscript variant passes the frozen joint threshold. Read the [French report](RAPPORT.md), [methods](METHODS_EN.md), [source audit](../docs/PIECES_REFERENCES.md#piece-a991c27a91dc2d) and [complete table](results/table.csv).

Read `PROTOCOL.json` before running. The source and experimental code are frozen locally before new generation and scoring. All manuscript views were previously exposed. No external preregistration or independent manuscript confirmation is claimed.

Python 3, NumPy, and a JDK are needed; Matplotlib is used only for the figure. Exact recorded versions are in `data/environment.json`. Java sources compile directly with `javac` without Maven or downloaded dependencies. The original Timm sources and license are preserved byte-for-byte at the recorded Git blobs. From the repository root, first verify the delivered results without regenerating them:

```sh
python3 voynich_phase24/src/manifest.py verify
python3 voynich_phase24/src/checks.py
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 voynich_phase24/src/verify.py
```

`verify.py` checks all stored cases and repeats three entire permutation experiments plus one Java generation in a temporary directory. It updates its own verification record, never the original control or manuscript results. These are same-operator arithmetic checks. For full regeneration, create a separate copy that retains frozen source files, protocol, frame and `FREEZE.json`, but omits generated `data/cases.json`, `data/cases/`, `data/truth/`, `data/timm_native/` and `results/`. Do not remove these from the evidence copy. Then run:

```sh
python3 voynich_phase24/src/checks.py
python3 voynich_phase24/src/study.py prepare
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 voynich_phase24/src/study.py controls
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 voynich_phase24/src/study.py real
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 voynich_phase24/src/verify.py
```

`prepare` refuses to replace completed controls. Scoring commands verify the frozen sources first. If sensitivity calibration fails, `real` writes a nonexecution status instead of scoring the manuscript. A failed copying-discrimination gate prevents mechanism claims even if a structural manuscript measurement is allowed. The semantic-specificity gate never supplies a translation.

The common frame contains 22,373 clean token slots in 3,063 segments on 172 pages / 85 physical folios. Natural controls fill exactly these slots; unknown slots and line-end positions remain fixed. Other counts and exclusions are in `data/frame.json`. Two disjoint stretches per author are used, with a 100-word gap. New random seeds do not create new independent authors.

The recent Zhang–Sheng method is adapted, not reproduced: their implementation is stated as forthcoming; this phase uses exact conditional expectations, different physical-folio partitions, explicit uncertainty barriers and a primary measure independent of spelling. Their published values must not be compared numerically as if they came from this implementation.

`report.py` renders stored results only. `manifest.py write` creates a post-experiment integrity inventory; it is not the prospective protocol freeze. The phase folder depends on the pinned repository-relative files listed in `FREEZE.json`; the delivery bundle includes those inputs. Earlier phase manifests are supplied as historical evidence, not as a claim that all earlier artifacts are present in that smaller bundle.
