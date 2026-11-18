"""Dépouiller les 9 lignes de prose et la ligne décalée de f101v selon les quatre lectures."""
import json
from pathlib import Path
import re
import sys

ICI = Path(__file__).resolve().parent
RESEARCH = ICI.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RESEARCH/'2026-11-18-noms-dans-une-phrase/contexte'))
from contexte import corpus, sequence, sections, MODES

BLOCS = {'prédit_19_21':range(19,22), 'témoin_22_24':range(22,25),
         'témoin_25_27':range(25,28), 'ligne_décalée_28':[28]}


def main():
    editions,_ = corpus()
    for d in editions.values():
        for mode in MODES:
            assert sequence(d['f101v.10'][3],mode)==[(0, 'okol')]
    blocs = {}
    for groupe,numeros in BLOCS.items():
        stats = {}
        strict = 0
        stricts_par_ligne = {}
        mentions = []
        for n in numeros:
            loc=f'f101v.{n}'
            rows=[]
            for ed,d in editions.items():
                for mode in MODES:
                    words=sequence(d[loc][3],mode)
                    rows.append(words)
                    res=stats.setdefault(f'{ed}_{mode}',{'positions':0,'lisibles':0,'occurrences':0})
                    for i,(_, w) in enumerate(words,1):
                        lisible = bool(re.fullmatch('[a-z]+',w))
                        res['positions'] += 1
                        res['lisibles'] += lisible
                        res['occurrences'] += w=='okol'
                        if 'okol' in w:
                            mentions.append({'ligne': n,'rang':i,'lecture':f'{ed}_{mode}','forme':w})
            conserves=[w for span in sections(rows) for w in span if w]
            strict+=len(conserves)
            stricts_par_ligne[n]=len(conserves)
            assert 'okol' not in conserves or any(rec['forme']=='okol' for rec in mentions)
        blocs[groupe]={'positions_concordantes':strict,'concordance_par_ligne':stricts_par_ligne,
                        'lectures':stats,'formes_contenant_la_suite':mentions}
    return blocs

if __name__=='__main__':
    print(json.dumps(main(),indent=2,ensure_ascii=False))
