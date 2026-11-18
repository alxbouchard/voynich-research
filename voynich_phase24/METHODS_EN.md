# Phase 24 methods and evidence boundaries

This is a locally frozen mechanism comparison, not a decoder or a claim of a language. The experimental files at commit `7fc5e24c9097bd2caf49a9b5d9375ad83280c61d` precede generation and scoring of the new controls. `FREEZE.json` pins 55 inputs, code and protocol files. Reporting and alternate verification were added afterwards. No frozen algorithm or threshold was changed after seeing results. This is not external preregistration.

## Frame and independent units

The source transcriptions are the repository's pinned ZL3b-n and IT2a-n. Only numeric folios and P0/P1 prose loci are considered. Uncertain tokens are unscored slots, not repaired words. Drawing interruptions separate segments. Metadata changes and unclassifiable metadata are excluded. A segment requires four literal `[a-z]+` tokens. The frame is selected using metadata and availability alone, before pair scoring. Tokens separated by uncertain marks are not joined in the strict primary configuration.

The partition is `floor(folio_number/5) mod 2`. Both sides of a physical folio remain in one partition. Illustration/attributed-hand/language-class strata require at least two folios in each partition. These metadata labels are not accepted as identified languages or proven authors. Whole folios are chosen by a seeded SHA-256 ordering under a 24,000-slot cap, then stratum support is rechecked. The resulting primary frame has 22,373 clean tokens, 3,063 segments, 172 pages and 85 physical folios, with 11,782/10,591 tokens in the two partitions.

All 42 controls fill exactly the same slots. Manuscript sensitivities use the same folios, but not an identical slot frame: IT contains 27,844 accepted tokens, and ZL joined-comma sensitivity contains 24,955. These variants do not constitute an equal-size replication of the primary comparison. All manuscript material was previously exposed; neither the frame nor the partitions are historically blind.

## Statistic and conditional reference

Use the 300 most frequent types; ties are broken by first occurrence. This selection is unchanged by interior shuffling or bijective type renaming. Every distinct unordered pair is included. A pair contributes at most one count per segment to its partition. There is no edit-distance or spelling mask and no pair selection based on its effect.

On each page, keep each segment's first and last slots fixed, along with unknown slots. Permute the clean interior tokens among clean interior slots on that page. This preserves page bags, segment lengths, endpoints and metadata. A rare word outside the top vocabulary remains a token in the shuffle pool, even though it does not form a scored pair.

For a segment with `m` clear interior slots, page interior pool size `N` and type count `c_i`, the probability of missing type `i` is `C(N-c_i,m)/C(N,m)`. For a pair, use inclusion–exclusion with `c_i+c_j`, suppressing the relevant absence terms when a type is fixed at an endpoint. Sum these exact presence probabilities across segments in each partition. Fixed slots can be unknown; they are not replaced with the first/last clear word.

Standardize each off-diagonal pair residual as `(observed-expected)/sqrt(expected+0.5)`. Remove its least-squares additive word effects, `mu+a_i+a_j` with `sum(a)=0`, over the complete off-diagonal matrix. The only primary endpoint is the Spearman correlation between the upper triangles of the two residual matrices. The implementation averages exact tied ranks. For 199 page-interior permutations, recompute counts, residuals and correlation with the exact expectations and vocabulary fixed. Use `p=(1+number(null >= observed-1e-12))/200`. The minimum reported p is .005.

This is a test against a conditional exchangeability reference, not a model probability, semantic test or causal conclusion. Serial dependence can violate exchangeability. Pairs sharing a word are dependent; no test treating the 44,850 pairs as independent observations is used. A nonzero baseline rho is possible and observed, which is why rho alone is not used.

## Known-message and generator controls

Two 22,373-word windows, separated by 100 words, are taken from each source. Caesar and Dante were already used in earlier work; Austen is a new source for this phase. A new key is not a new author. Each window is independently encoded with a random bijective code of opaque ten-letter words and, separately, four disjoint alternatives per plaintext word. The scorer receives the encoded rows only. Stored codebooks are used for round-trip checks, not fitting. This assesses structural retention under word codes, not recovery of an unknown key.

Four stochastic mechanisms use each source's type frequencies and an opaque renaming:

- Page preference: choose one of 16 frequency-rank-modulo groups per page; sample from that group with probability .8, otherwise from global unigram frequencies.
- Local copy: with probability .75 copy one of the previous eight tokens on the same page; otherwise sample a unigram. Restart history on each page.
- Segment preference: the page-preference model with a new preferred group for each segment. This gives persistent associations without a target plaintext.
- First-order Markov: with probability .8 sample an empirical successor to the previous token; otherwise use unigrams. Restart each page. It inherits linguistic transition statistics, and accidental intelligible fragments are possible; it does not encode a chosen target passage.

Six actual executions of the unmodified published Java Timm generator use seeds 81–86, 6,000 native lines, and the checked-in configuration except output location/name, seed and requested line count. Skip 500 words and reflow the next 22,373 words into the common frame. Original output, effective configuration and logs are archived. The author labels in these six case filenames only identify their paired index; no Caesar, Dante or Austen text is passed to Java. The generator's native geometry is not preserved by reflow, and its seed vocabulary and rules already draw on Voynich observations. Results cover these settings, not every copy model.

Each primary case uses the same 300-type budget, frame and 199 permutations, with no optimization. Top-150 sensitivities cover the six bijective and six Java cases. On the manuscript, strict top-150 and joined-comma top-300 sensitivities are retained for both transcriptions. Six manuscript configurations include one redundant IT variant, not six independent replications.

## Gates fixed before results

Detection requires rho >= .10 AND p <= .01. This threshold is a local decision rule, not a universal linguistic boundary. Sensitivity requires >=5/6 bijective detections, >=1/2 in each author and <=1/6 page-preference detections. Copy discrimination additionally requires <=1/6 local-copy and <=1/6 Java detections. Semantic specificity additionally requires <=1/6 segment-preference and <=1/6 Markov detections. Passing any finite set would still not establish universal specificity.

Mechanical checks passed before generation. Sensitivity and copy-discrimination gates passed. Semantic specificity failed (6/6 in each challenge family). Thus manuscript scoring was permitted by the protocol, but the statistic cannot certify a target message. All manuscript configurations fail the joint rule. This neither identifies copying nor excludes other ciphers: only 3/6 four-code homophonic controls pass.

## Verification and provenance

The frozen toy checks exhaust 1,440 labeled-slot permutations, verify exact expectations and counts, compare a separate least-squares fit, and test invariance to arbitrary bijective renaming. After results, `verify.py` computes every observed count matrix through Python sets/combinations and solves complete-graph normal equations independently of the experimental residual formula. It recomputes ranks by unique-value counts, checks all reported p values and gates, and compares integer-binomial expectations on 128 partition/cell combinations per configuration (7,680 total). Sampled expectation checks are not claimed as a second full-matrix computation for every case.

Three complete 199-permutation deterministic repeats match, including primary ZL. An independently compiled Java seed-81 rerun matches bytes exactly. A post-result rank-tie diagnostic rounds residuals to 12 decimals; maximum rho difference is 1.58e-6, without replacing or tuning the frozen endpoint. All 55 frozen files and 39 third-party Git blobs match. These are same-operator technical checks, not independent scholarly or semantic confirmation.

This work adapts the cross-partition pair idea in Zhang and Sheng (2026, v1, section 5.1). It differs in exact null expectations, folio partitions, uncertainty handling and the spelling-invariant primary pair set. Their forthcoming implementation and their full experiment are not reproduced. See `SOURCES_AND_PRIOR_EVIDENCE.md` for source access and prior-evidence limits. The prior phases and atlas are preserved; no remote publication is part of this work.
