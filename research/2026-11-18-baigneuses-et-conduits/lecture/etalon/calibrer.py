"""Contrôle indépendant du modèle injectif lettre par lettre de confronter.py."""
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import random
import re
import string
import sys
import unicodedata

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
from confronter import assignments, repertories

ALPHABET = string.ascii_lowercase
SIGNES = [f's{i:02}' for i in range(26)]


def mots(vers):
    texte = ''.join(c for c in unicodedata.normalize('NFD',vers.lower()) if not unicodedata.combining(c))
    return re.findall('[a-z]+',texte)


def motif(paire):
    vus = {}
    return tuple(tuple(vus.setdefault(s,len(vus)) for s in mot) for mot in paire)


def apparier(chiffre, clair):
    return {s:c for a,b in zip(chiffre,clair,strict=True) for s,c in zip(a,b,strict=True)}


def coherent(a,b):
    union = a | b
    return len(set(union.values())) == len(union) and all(union[s] == c for s,c in a.items())


class Bibliotheque:
    def __init__(self, corpus):
        self.positions = defaultdict(list)
        self.motifs = defaultdict(list)
        self.longueurs = defaultdict(list)
        for notice,vers in enumerate(corpus):
            for numero,ligne in enumerate(vers,1):
                for debut,paire in enumerate(zip(ligne,ligne[1:]),1):
                    self.positions[paire].append((notice,numero,debut))
        for paire in self.positions:
            self.motifs[motif(paire)].append(paire)
            self.longueurs[tuple(map(len,paire))].append(paire)

    @lru_cache(maxsize=None)
    def interpretes(self,chiffre):
        clefs = {p:apparier(chiffre,p) for p in self.motifs[motif(chiffre)]}
        autre = {}
        for p in self.longueurs[tuple(map(len,chiffre))]:
            for d in assignments(chiffre,p,1):
                assert p not in autre
                autre[p] = d
        assert autre == clefs, 'Désaccord sur les amorces entre les deux implémentations'
        return clefs

    def transfert(self,source,cible):
        """L'appelant ne fournit que les signes de deux paires. Aucune vérité terrain."""
        cles = self.interpretes(source)
        valeurs = self.interpretes(cible)
        couvert = set(s for w in cible for s in w) <= set(s for w in source for s in w)
        par_extension = set()
        fixes = set()
        for amorce,cle in cles.items():
            for paire,extension in valeurs.items():
                if paire == amorce:
                    continue
                direct = coherent(cle,extension)
                production = next(assignments(cible,paire,1,cle),None)
                assert direct == (production is not None), 'Désaccord sur une extension'
                if direct:
                    par_extension.add(paire)
                    if couvert:
                        lecture = tuple(''.join(cle[s] for s in w) for w in cible)
                        assert lecture == paire
                        fixes.add(paire)
        return couvert,fixes,par_extension


def coder(paires,numero):
    noms = SIGNES.copy()
    random.Random(f'Pierre-Eboli-etalon-20261118/{numero}').shuffle(noms)
    substitution = dict(zip(ALPHABET,noms,strict=True))
    return [tuple(tuple(substitution[c] for c in w) for w in p) for p in paires]


def alterer(chiffre):
    ancien = chiffre[0][0]
    nouveau = next((s for w in chiffre for s in w if s != ancien),SIGNES[(SIGNES.index(ancien)+1)%26])
    return ((nouveau,) + chiffre[0][1:],chiffre[1])


def bilan(candidats,attendu):
    return {'candidats':len(candidats),'exact_inclus':attendu in candidats,'exact_unique':candidats=={attendu}}


def etudier(bib,nom,numero,paires,regime):
    code = coder(paires,numero)
    if regime == 'transferts_alteres':
        code = [code[0]] + [alterer(p) for p in code[1:]]
    elif regime == 'amorce_alteree':
        code[0] = alterer(code[0])
    cles = bib.interpretes(code[0])
    rapport = {'jeu':nom,'notice':numero,'regime':regime,'origine':' '.join(paires[0]),
               'chiffres':[[list(w) for w in p] for p in code], 'amorce':bilan(set(cles),paires[0]),
               'lieux_amorce_compatibles':sum(len(bib.positions[k]) for k in cles),'transferts':[]}
    for chiffre,attendu in zip(code[1:],paires[1:],strict=True):
        couvert,fixes,extensions = bib.transfert(code[0],chiffre)
        rapport['transferts'].append({'vraie_paire':' '.join(attendu),'couverture_signes':couvert,
                        'fixes':bilan(fixes,attendu),'extensions':bilan(extensions,attendu)})
        if nom=='bain_XVI':
            rapport['candidats_amorce']={' '.join(p):bib.positions[p] for p in sorted(cles)}
            rapport['candidats_fixes']=[' '.join(p) for p in sorted(fixes)]
            rapport['candidats_extensions']=[' '.join(p) for p in sorted(extensions)]
    return rapport


def resumer(lignes):
    if not lignes:return {}
    amorces = Counter()
    for d in lignes:
        for attribut in ['exact_inclus','exact_unique']:
            amorces[attribut] += d['amorce'][attribut]
        amorces['sans_solution'] += d['amorce']['candidats']==0
        amorces['lieu_exact_unique'] += d['amorce']['exact_unique'] and d['lieux_amorce_compatibles']==1
    sorties = []
    for i in range(len(lignes[0]['transferts'])):
        cases=[r['transferts'][i] for r in lignes]
        compte={'n':len(cases),'tous_signes_couverts':sum(c['couverture_signes'] for c in cases)}
        for k in ['fixes','extensions']:
            res=Counter()
            for c in cases:
                res['au_moins_une'] += bool(c[k]['candidats'])
                res['une_reponse'] += c[k]['candidats']==1
                res['exact_inclus'] += c[k]['exact_inclus']
                res['exact_unique'] += c[k]['exact_unique']
            compte[k]=res
        sorties.append(compte)
    return {'n':len(lignes),'amorces':amorces,'transferts':sorties}


def main(cache):
    source = cache/'vers.json'
    checksum = sha256(source.read_bytes()).hexdigest()
    assert checksum == json.loads((ICI.parent/'SOURCE.json').read_text())['sha256']
    texte=json.loads(source.read_text())
    corpus = [[mots(l) for l in n['vers']] for n in texte]
    bib=Bibliotheque(corpus)
    assert bib.positions == repertories(cache)["bains"], "Désaccord sur les paires ou leurs positions"
    rep = []
    jeux = ['intact','transferts_alteres','amorce_alteree']
    for numero,vers in enumerate(corpus):
        paires=[tuple(v[:2]) for v in vers[:3]]
        assert all(len(p)==2 for p in paires)
        for mode in jeux:
            rep.append(etudier(bib,'notices' if numero else 'prologue',numero,paires,mode))
        if numero:
            lettres=set(''.join(paires[0]))
            plus = [(j,k,p) for j,v in enumerate(vers[1:],2) for k,p in enumerate(zip(v,v[1:]),1)
                    if p!=paires[0] and set(''.join(p))<=lettres]
            if plus:
                j,k,cible=plus[0]
                r=etudier(bib,'couverture_construite',numero,[paires[0],cible],'intact')
                r['position_transfert']=[numero,j,k]
                rep.append(r)
    bonus=[('adibis','aquas'),('aquas','aqua')]
    assert (16,8,4) in bib.positions[bonus[0]] and (16,11,3) in bib.positions[bonus[1]]
    for mode in jeux: rep.append(etudier(bib,'bain_XVI',16,bonus,mode))
    synthese={}
    for nom in ['notices','prologue','couverture_construite','bain_XVI']:
        synthese[nom]={}
        for mode in jeux:
            selection=[r for r in rep if r['jeu']==nom and r['regime']==mode]
            if selection:synthese[nom][mode]=resumer(selection)
    exemples = [r for r in rep if r['jeu']=='bain_XVI']
    return {'sha256_source':checksum,'pieces':len(corpus),'vers':sum(map(len,corpus)),
            'paires_distinctes':len(bib.positions),'positions':sum(map(len,bib.positions.values())),
            'synthese':synthese, 'exemple_XVI':exemples, 'epreuves':rep}


if __name__ == '__main__':
    print(json.dumps(main(Path(sys.argv[1])),ensure_ascii=False,indent=1))
