"""Former les mots promis à partir des deux seuls fichiers de préparation."""
from collections import Counter, defaultdict
from corpus_dam import read, save


def most(counts):
    return min(counts,key=lambda value:(-counts[value],value))


def frequencies(examples, single):
    counts = defaultdict(Counter)
    for _,base,end,tail in examples:
        if base == "da" or (single and tail == "iin"):
            continue
        for key in ((base,end),(None,end),(base,None),(None,None)):
            counts[key][tail] += 1
    return counts


def main():
    train = read("APPRENTISSAGE.json.gz")
    model = frequencies(train,single=True)
    announcements = []
    for pos,base,end,lot in read("MASQUES.json.gz"):
        base_guess = most(model[base,None] or model[None,None])
        trained = most(model[base,end] or model[None,end])
        endings = {"r_constant":"r","r_m":"m" if end else "r",
                   "l_m":"m" if end else "l","iin_m":"m" if end else "iin",
                   "base":base_guess,"base_et_position":trained}
        announcements.append({"lieu":pos,"base":base,"fin":end,"lot":lot,
                              "mots":{rule:base+tail for rule,tail in endings.items()}})
    save("ANNONCES.json.gz",announcements)


if __name__ == "__main__":
    main()
