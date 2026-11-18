"""Transmettre au prédicteur la base et la position, sans donner la réponse de réserve."""
from collections import Counter
from corpus_dam import corpus, group, h_rows, metadata, position_key, save, split_word, strict_rows


def main():
    editions,_ = corpus()
    sections = metadata()
    training, held = [], []
    coverage = Counter()
    for loc,(page,kind,_,raw) in editions["H"].items():
        lot = group(page,kind,sections)
        if not lot:
            continue
        if lot == "apprentissage":
            rows = strict_rows(editions,loc,sections[page]["I"],coverage)
        else:
            rows = h_rows(raw)
        for block,idx,word,roles in rows:
            split = split_word(word)
            if not split:
                continue
            base, tail = split
            item = [position_key(loc,block,idx),base,"fin" in roles]
            if lot == "apprentissage":
                training.append([*item,tail])
            else:
                held.append([*item,lot])
    save("APPRENTISSAGE.json.gz",training)
    save("MASQUES.json.gz",held)


if __name__ == "__main__":
    main()
