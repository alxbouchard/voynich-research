"""Classer les étiquettes en réservant un bifeuillet entier, avec permutations sur chaque face."""
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import json
import re
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-mois-automne/cle"))
from dechiffrer import segment
from transfert import corpus, tokens, langage

N_PERM = 9999
SEED = 20261118
KINDS = ("mot", "prefixe", "suffixe")
LABELS = {"Ln", "Lt"}


def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def inventory():
    editions, _ = corpus()
    source = {ed: langage.DATA / (stem + "-n.txt") for ed,stem in langage.EDITIONS.items()}
    faces = {}
    for line in source["ZL"].read_text().splitlines():
        page = re.match(r"^<(f\d+[rv])>", line)
        if page and "$Q=M " in line:
            meta = dict(re.findall(r"\$(\w)=(\w+)", line))
            faces[page[1]] = {"bifeuillet": int(meta["B"]), "loci": {}, "main": meta["H"],
                              "currier": meta["L"]}
    assert len(faces) == 20
    sets = {}
    for ed, rows in editions.items():
        sets[ed] = set()
        for face, page in faces.items():
            page["loci"][ed] = Counter(r[1] for loc,r in rows.items() if r[0] == face)
        for loc, (face, kind, _, _) in rows.items():
            if face in faces and kind in LABELS:
                sets[ed].add(loc)
    places = {}
    for loc in sorted(set.union(*sets.values()), key=lambda s:(s.split(".")[0],int(s.split(".")[1]))):
        face, seq = loc.split(".")
        index = int(seq)
        views = {}
        kinds = set()
        for ed, rows in editions.items():
            row = rows.get(loc)
            kinds.add(row[1] if row else None)
            views[ed] = {"code":row[1],"localisateur": row[2],"original":row[3]} if row else None
        canon = (f"f75v.{index-index%2}+{index-index%2+1}"
                 if face == "f75v" and 18 <= index <= 37 else loc)
        obj = places.setdefault(canon, {"id":canon,"face":face,"bifeuillet":faces[face]["bifeuillet"],
                                        "lieux":{},"mots":set(),"codes":set()})
        obj["codes"].update(kinds)
        readings = [set(w for w in tokens(v["original"], spacing) if re.fullmatch("[a-z]+",w))
                    for v in views.values() for spacing in ("joints","separes") if v is not None]
        shared = sorted(set.intersection(*readings)) if len(readings) == 4 else []
        obj["lieux"][loc] = {"editions":views,"mots_communs":shared}
        obj["mots"].update(shared)
    for obj in places.values():
        codes = obj.pop("codes")
        obj["code"] = next(iter(codes)) if len(codes) == 1 and codes.issubset(LABELS) else None
        obj["mots"] = sorted(obj["mots"])
        obj["inclusion"] = ("codes discordants" if not obj["code"] else
                            "aucun mot concordant" if not obj["mots"] else
                            "aucun mot de deux unités" if not any(len(segment(w)) >= 2 for w in obj["mots"])
                            else "retenu")
    sources = {str(path.relative_to(RESEARCH.parent)):sha256(path.read_bytes()).hexdigest()
               for path in source.values()}
    return {"sources":sources,"faces":faces,"emplacements":list(places.values())}


def features(words, kind):
    if kind == "mot":
        return set(words)
    signs = [segment(w) for w in words]
    return {"".join(s[:2] if kind == "prefixe" else s[-2:]) for s in signs if len(s) >= 2}


class Evaluation:
    def __init__(self, rows):
        self.rows = rows
        self.y = np.array([r["code"] == "Ln" for r in rows], dtype=float)
        faces = np.array([r["face"] for r in rows])
        sheets = np.array([r["bifeuillet"] for r in rows])
        self.pools = [np.flatnonzero(faces == f) for f in sorted(set(faces))]
        self.mixed = [idx for idx in self.pools if 0 < self.y[idx].sum() < len(idx)]
        self.usable = np.concatenate(self.mixed)
        same = sheets[:,None] == sheets[None,:]
        self.sheets = sheets
        self.folds = sorted(set(sheets[self.usable]))
        self.train_n = np.stack([(~same) @ (self.y == c).astype(float) for c in (0,1)])
        assert np.all(self.train_n > 0)
        self.majority = np.sign(self.train_n[1] - self.train_n[0])
        self.weights = np.zeros((2,len(rows)))
        for idx in self.mixed:
            b = sheets[idx[0]]
            nfaces = sum(sheets[p[0]] == b for p in self.mixed)
            for c in (0,1):
                n = (self.y[idx] == c).sum()
                self.weights[c,idx] = 1 / (2 * n * nfaces * len(self.folds))
        self.kernels = {}
        for kind in KINDS:
            attrs = [features(row["mots"], kind) for row in rows]
            vocab = sorted(set.union(*attrs))
            X = np.array([[int(v in a)/len(a) for v in vocab] for a in attrs])
            similarity = X @ X.T
            similarity[same] = 0
            self.kernels[kind] = similarity

    def predict(self, y, kind):
        kernel = self.kernels[kind]
        weight_ln = y @ kernel.T
        margin = weight_ln / self.train_n[1] - (kernel.sum(1) - weight_ln) / self.train_n[0]
        return np.where(margin > 1e-12, 1, np.where(margin < -1e-12, -1, 0))

    def score(self, y, predictions):
        points = (1 + (2*y-1)*predictions) / 2
        weights = np.where(y == 1, self.weights[1], self.weights[0])
        return (points*weights).sum(axis=-1)

    def detail(self, pred):
        def counts(ix):
            good = (2*self.y[ix]-1)*pred[ix]
            return {"corrects":int((good>0).sum()),"errones":int((good<0).sum()),
                    "abstentions":int((good==0).sum())}
        by_face = {}
        for ix in self.mixed:
            by_class = [np.mean((1+(2*self.y[part]-1)*pred[part])/2)
                        for c in (0,1) for part in [ix[self.y[ix] == c]]]
            by_face[self.rows[ix[0]]["face"]] = {"score":float(np.mean(by_class)),**counts(ix)}
        by_sheet = {str(b):float(np.mean([by_face[self.rows[ix[0]]["face"]]["score"] for ix in self.mixed
                                         if self.sheets[ix[0]] == b])) for b in self.folds}
        total = float(self.score(self.y, pred))
        assert abs(total - np.mean(list(by_sheet.values()))) < 1e-12
        return {"score":total,"par_face":by_face,"par_bifeuillet":by_sheet,
                "objets_sur_faces_mixtes":counts(self.usable),"tous":counts(np.arange(len(self.y)))}

    def permute(self, by_length=False):
        pools = self.pools
        if by_length:
            sizes = np.array([min(2, len(r["mots"])) for r in self.rows])
            pools = [part for idx in pools for n in (1,2) for part in [idx[sizes[idx] == n]] if len(part)]
        rng = np.random.default_rng(SEED)
        observed = {k:self.score(self.y,self.predict(self.y,k)) for k in KINDS}
        upper = Counter()
        for start in range(0,N_PERM,256):
            n = min(256,N_PERM-start)
            Y = np.tile(self.y,(n,1))
            for idx in pools:
                ordering = rng.random((n,len(idx))).argsort(axis=1)
                Y[:,idx] = self.y[idx][ordering]
            for k in KINDS:
                scores = self.score(Y, self.predict(Y,k))
                upper[k] += int((scores >= observed[k]-1e-12).sum())
        return {k:{"superieur_ou_egal":upper[k],"tirages":N_PERM,"p":(1+upper[k])/(1+N_PERM)}
                for k in KINDS}


def main():
    inv = inventory()
    write("INVENTAIRE.json",inv)
    rows = [r for r in inv["emplacements"] if r["inclusion"] == "retenu"]
    test = Evaluation(rows)
    witnesses = [dict(r,mots=["xyx" if r["code"] == "Ln" else "aba"]) for r in rows]
    demo = Evaluation(witnesses)
    tautology = {k:float(demo.score(demo.y,demo.predict(demo.y,k))) for k in KINDS}
    assert all(abs(v-1)<1e-12 for v in tautology.values())
    decisions = {k:test.predict(test.y,k) for k in KINDS}
    results = {k:test.detail(p) for k,p in decisions.items()}
    null = test.permute()
    conditional = test.permute(True)
    running = 0.
    for i,k in enumerate(sorted(KINDS,key=lambda k:null[k]["p"])):
        running = max(running,min(1.,(len(KINDS)-i)*null[k]["p"]))
        null[k]["p_holm"] = running
    for k, r in results.items():
        r["nul_face"] = null[k]
        r["nul_face_et_nombre_mots"] = conditional[k]
        r["critere_atteint"] = bool(r["score"]>0.5 and null[k]["p_holm"]<=0.05 and
                                    sum(s>0.5 for s in r["par_bifeuillet"].values())>=2 and conditional[k]["p"]<=0.05)
    for i,r in enumerate(rows):
        r["score_sur_face_mixte"] = bool(i in test.usable)
        r["apprentissage"] = {"Ln":int(test.train_n[1,i]),"Lt":int(test.train_n[0,i])}
        r["predictions"] = {k:({-1:"Lt",1:"Ln",0:None}[int(p[i])]) for k,p in decisions.items()}
    predictions = [{k:r[k] for k in ("id","mots","code","score_sur_face_mixte","apprentissage","predictions")}
                   for r in rows]
    resources = {"python": ">=3.9", "numpy":np.__version__}
    write("RESULTATS.json",{"graine":SEED,"logiciels":resources,"test":results,"predictions":predictions,
                            "plus_frequente":test.detail(test.majority),
                            "choix_equiprobable_esperance":0.5,"temoin_artificiel":tautology})
    print("objets",len(inv["emplacements"]),len(rows),"évalués",len(test.usable))
    for k,r in results.items():
        print(k,r["score"],r["par_bifeuillet"],r["nul_face"],r["nul_face_et_nombre_mots"])


if __name__ == "__main__":
    main()
