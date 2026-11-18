# Phase 23: matched label-edge transfer

## Scope and chronology

The frozen protocol is `PROTOCOL.json`, committed with the measurement and calibration code in `7b6cfdd` before the new calibration and manuscript measurements. `FREEZE.json` pins that code. There was extensive historical manuscript exposure, including all 213 atlas views and all formerly reserved views. This is a locally specified, internally cross-validated structural experiment, not an externally preregistered or blind decipherment test.

The first question extends earlier published observations of different label initials. The second asks whether final-unit distributions still differ after conditioning on the initial unit. Neither question tests a semantic interpretation. The phase-14/15 label-to-nearby-prose matching experiment and the phase-18/19 language-model fits were not rerun here.

## Data and eligibility

ZL3b-n and IT2a-n are read from the unchanged atlas sources. IVTFF label subtypes La/Lc/Lf/Ln/Lp/Ls/Lt/Lz identify a documented spatial relationship; they do not prove that the word names the object. L0 and Lx are excluded. Labels must be single clean alphabetic tokens. Prose comes only from P0/P1. The primary prose sample excludes the first and last chunks of each interruption-delimited segment. A chunk containing an uncertain space, bracket alternative, ligature, unknown sign or extended character is rejected; it is not silently repaired. Positions are assigned before rejection. Drawing interruptions remain hard barriers. Angle comments are removed, while literal raw text, IDs, positions and source lines remain in the output records.

Page metadata Q/I/H/L/C are carried through. Metadata marked `@` and lines after a changing inline tag on the page are excluded. The frozen parser is conservative; it does not claim a complete IVTFF implementation. Its exclusion audit is saved with each case. It handles the pinned input format used in this phase, not arbitrary multiline/transliteration conventions.

The main unit convention greedily groups cth, ckh, cph, cfh, ch and sh; all other lowercase letters are units. Three to twelve units are allowed. These are analytical conventions, not demonstrated glyph or phoneme boundaries. Individual EVA-character counting is a fixed sensitivity analysis.

Cells match panel/page, metadata and exact length. The final-edge endpoint also matches initial unit. Both roles must occur in a cell. A retained physical folio must contribute at least five matched labels and twenty matched prose tokens. All panels of the same physical folio remain together. At least eight folios and three conventional quires are required for inferential output. These thresholds were fixed before new measurements.

Consequently, this is **not a test of all manuscript labels**. Zodiac labels often lack a P0/P1 comparator on the same page and are outside this comparison. The astro group contributes to the initial endpoint but does not survive the final-endpoint support criteria. All support IDs and exclusions are available in the JSON results.

## Estimator and conditional randomization

For each matched cell, let d be the label mean of a one-hot edge-symbol vector minus its prose mean. Average cells within a page using matched label counts. Average pages equally within a physical folio and folios equally within a quire. This prevents a long prose page or a many-panel foldout from directly dominating the result.

For held-out quire q, set w_q to the mean d of the other quires, and compute T_q = d_q · w_q. The reported statistic T averages T_q over quires. It measures agreement of edge-distribution contrasts across quires. It is not a probability, accuracy, language-model gain or decoding score. No edge category is chosen after seeing its effect. Each held-out quire is excluded from its training-side weights; all features and weights are reported.

For each endpoint and sample, 4,999 reallocations assign the original number of label roles uniformly without replacement within each matched cell. The entire statistic, including other-quire weights, is recomputed. Random k-subsets are generated with ranks of independent continuous random values. The upper-tail Monte Carlo p-value is (1 + exceedances)/5,000, with numerical tolerance 1e-12. No result is reported as p=0. The two primary ZL/interior endpoints use Bonferroni threshold .025. Positive effects in IT and in every supported held-out quire are additional frozen consistency requirements.

This null assumes conditional token exchangeability. Real label strings and prose can be dependent or governed by different layout templates. The p-values therefore reject that particular randomized-role model; they do not establish random sampling, causal label functions, independent historical scribes, linguistic meaning or a general population effect. Conventional quire membership is a grouping variable, not a claim about the original binding or order.

## Calibration and fixed sensitivities

Twenty paired seeds generate each of four families, with four quires, three folios per quire and two pages per folio. Each page has twelve labels and sixty prose tokens, including twelve first, twelve last and thirty-six interior tokens. The known-message family preserves an explicitly documented plaintext sequence under a reversible substitution plus random role-dependent edge markers. Its keys and marked plaintext are withheld from `measure`, then disclosed in the example fixture; the test does not recover those keys. Long words can fall outside the same fixed length filter.

The other families have no encoded message: IID core strings with section-specific alphabets, role-specific edge templates, or a layout template shared by labels and prose first tokens. Seeds are shared across families for controlled comparison, so counts should not be summed as independent replications. One full example per family is archived; all twenty regenerate from source and seed. Calibration uses 199 reallocations, with the same .025 threshold and the predetermined gate. These strong constructed effects test detection and false-alert behavior, not sensitivity at the manuscript's weaker effect size or historical plausibility.

All four fixed sensitivities were run in both transcriptions: first segment word, last segment word, deduplicated page/role/surface, and individual EVA characters. Their p-values are descriptive, not extra discoveries. Deduplication precedes matching and is role-dependent; it does not make the resulting strings a random independent sample. The first/last comparisons also have less support, especially after initial-unit matching. Insufficient support is retained explicitly instead of relaxing thresholds.

## Reproduction, integrity and limits

`checks.py` verifies barriers, token positions, cipher round trips, an exact hypergeometric toy null and a separate implementation of the weighted statistic. `verify.py` independently recomputes all 20 observed results, checks bijective symbol-renaming invariance, recomputes reported p-values and repeats both primary runs including all permutations. This is a separate arithmetic implementation by the same operator, not an outside replication. The 150-file phase-22 manifest and 684-file atlas manifest were separately verified unchanged in the original repository.

`SOURCES.json` hashes local inputs. Primary web sources were inspected through the web reader. Direct shell downloads failed DNS resolution; no archived page bytes or full-paper reading is claimed where none exists. The arXiv reference uses an explicit version, while the changing author web pages are access-dated.

The final-symbol contribution inspection is descriptive and post-result. In particular, selecting final `n` now does not create a new preregistered hypothesis test. Any proposed reading based on that observation would require fresh, independently controlled predictions. The current corpus and atlas cannot be relabeled an unseen reserve. A suitable next semantic test would require independently adjudicated image/token alignments, fixed candidate mappings and negative controls, and a source or annotation set unavailable during selection. None of those semantic prerequisites is supplied by a positive T here.
