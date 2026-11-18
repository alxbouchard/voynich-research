# Phase 23 — Matched label-edge structure

**French result report: [RAPPORT.md](RAPPORT.md).** Full methods: [METHODS_EN.md](METHODS_EN.md).

`NOT_TRANSLATION`. This experiment asks whether label-versus-prose edge distributions transfer across conventional quires after within-page matching. It does not assign a word meaning, recover a key, or propose a reading.

The local protocol and measurement/calibration code are committed before new calibration or manuscript results. Existing manuscript exposure is explicit; there is no untouched manuscript reserve. Read `PROTOCOL.json` for all exclusions, endpoints, gates and sensitivity analyses.

From the repository root, with Python 3 and NumPy:

```sh
python3 voynich_phase23/src/checks.py
python3 voynich_phase23/src/controls.py
python3 voynich_phase23/src/experiment.py real
python3 voynich_phase23/src/verify.py
MPLCONFIGDIR=chemin-local/voynich-phase23-mpl python3 voynich_phase23/src/report.py
python3 voynich_phase23/src/manifest.py verify
```

The manuscript command refuses to run when the frozen calibration gate fails. Outputs overwrite only this phase's derived files. Earlier phases and the atlas are read-only inputs. `SOURCES.json` identifies pinned local inputs and distinguishes articles actually consulted from experiments reproduced. Internet pages were consulted through the web reader; direct shell downloads failed, so no byte-level archive of those pages is claimed.

Here the manuscript command (`experiment.py real`) is the calibration-gated step. Matplotlib is needed only for the figure/report command; numerical checks need NumPy. `SHA256SUMS.json` checks the delivered bytes, while `FREEZE.json` checks the pre-result protocol/code. Regenerated figures may have different metadata or rendering across environments, so check the delivered inventory **before** regenerating. Do not rewrite its manifest merely to hide a reproduction difference.

The standalone bundle contains only the pinned prior-phase inputs required by this experiment; it does not claim to reproduce all earlier phases or the full atlas. Historical integrity checks were executed in the original repository and are recorded separately in `results/prior_integrity.json`.

This is a controlled extension of published label observations, not a reproduction of Landini's counts, Zandbergen's frequency study, or Sterneck–Polish–Bowern's topic models. Phase 14/15 exact/rewritten label-to-nearby-prose matching and phase 18/19 language-model edge fits are different experiments.
