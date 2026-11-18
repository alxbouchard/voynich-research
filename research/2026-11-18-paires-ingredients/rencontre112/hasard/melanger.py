"""Post hoc, position-stratified shuffle for one prespecified pair and a family of 128."""
from collections import defaultdict
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from deux_feuilles import PAIR, overlap
from predire import word_pairs
from tester import raw_text, tokens

N = 49999
BATCH = 200
SEED = 13112026


def inputs():
    base = HERE.parents[1]
    rows = json.loads((base / "predictions_pots_elargis.json").read_text())["conditions"]["accord/joint/strict"]
    row = rows["f102v2/1"]
    assert row["objets"]["f102v2.7"] == []
    row["objets"]["f102v2.7"] = ["otol"]
    row["paires"] = sorted(word_pairs(row["objets"].values()))
    pairs = sorted({tuple(pair) for r in rows.values() for pair in r["paires"]})
    assert len(pairs) == 128 and PAIR in pairs
    source = json.loads((base / "notices/paragraphes.json").read_text())
    parts = {ed: [[x.split(",")[0] for x in b] for b in source[ed]] for ed in ("H", "ZL")}
    blocks = overlap(parts["H"], parts["ZL"])
    raw = raw_text({b[0].split(".")[0] for b in blocks})
    return pairs, blocks, raw


def layout(pairs, blocks, table, within_block):
    vocabulary = {word for pair in pairs for word in pair}
    group = defaultdict(list)
    targets = defaultdict(list)
    target_indices = defaultdict(list)
    slot_blocks, target_places = [], []
    for b, block in enumerate(blocks):
        for locus in block:
            page = locus.split(".")[0]
            words = tokens(table[locus], False)
            for i, w in enumerate(words):
                role = "solo" if len(words) == 1 else ("debut" if i == 0 else "fin" if i + 1 == len(words) else "interieur")
                stratum = (b if within_block else page, role)
                slot = len(slot_blocks)
                slot_blocks.append(b)
                group[stratum].append(slot)
                if w in vocabulary:
                    k = len(target_places)
                    target_places.append(slot)
                    target_indices[stratum].append(k)
                    targets[(page, w)].append(k)

    # A candidate is a pair of distinct occurrences on one page. Pages cannot exchange words.
    left, right, pair_ids = [], [], []
    for page in dict.fromkeys(b[0].split(".")[0] for b in blocks):
        for pair_id, (u, v) in enumerate(pairs):
            for i in targets[page, u]:
                for j in targets[page, v]:
                    left.append(i)
                    right.append(j)
                    pair_ids.append(pair_id)

    pools = [(np.array(group[k], dtype=np.int32), np.array(indices, dtype=np.int32))
             for k, indices in target_indices.items()]
    assert sum(len(indices) for _, indices in pools) == len(target_places)
    return (np.array(slot_blocks), np.array(target_places, dtype=np.int32),
            np.array(left), np.array(right), np.array(pair_ids), pools)


def run(pairs, blocks, table, within_block, seed):
    block_id, obs, left, right, labels, pools = layout(pairs, blocks, table, within_block)
    fixed = labels == pairs.index(PAIR)

    def hits(places):
        a, b = places[:, left], places[:, right]
        return (np.abs(a - b) <= 8) & (block_id[a] == block_id[b])

    observed = hits(obs[None, :])[0]
    rng = np.random.Generator(np.random.PCG64(seed))
    count_fixed = count_any = 0
    for start in range(0, N, BATCH):
        rows = min(BATCH, N - start)
        places = np.empty((rows, len(obs)), dtype=np.int32)
        for slots, indices in pools:
            # Distinct targets are assigned different positions within the same stratum.
            draws = rng.permuted(np.broadcast_to(slots, (rows, len(slots))), axis=1)
            places[:, indices] = draws[:, :len(indices)]
        result = hits(places)
        count_any += int(np.count_nonzero(result.any(axis=1)))
        count_fixed += int(np.count_nonzero(result[:, fixed].any(axis=1)))
    scores = {"fixe": count_fixed, "famille": count_any}
    return {"graine": seed, "tirages": N, "positions": len(block_id), "positions_mots_interet": len(obs),
            "troncons": len(blocks), "mots_interet_distincts_total": len({w for p in pairs for w in p}),
            "paires_testables_meme_page": len(set(labels)), "paires": len(pairs),
            "observe_occurrences_fixe": int(observed[fixed].sum()), "observe_occurrences_famille": int(observed.sum()),
            "observe_paires_distinctes": [pairs[k] for k in sorted(set(labels[observed]))],
            "tirages_positifs": scores, "fractions": {k: v / N for k,v in scores.items()},
            "erreurs_types_mc": {k: (v / N * (1-v/N) / N)**.5 for k,v in scores.items()}}


def main():
    pairs, blocks, raw = inputs()
    outputs = {}
    for index, ed in enumerate(("H", "ZL")):
        outputs[ed] = {}
        for mode_id, (name, within_block) in enumerate((("par_page", False), ("par_troncon", True))):
            outputs[ed][name] = run(pairs, blocks, raw[ed], within_block, SEED + index * 100 + mode_id)
            print(ed, name, outputs[ed][name], flush=True)
    (HERE / "resultats.json").write_text(json.dumps(outputs, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
