"""Ouvrir la prose après le gel des tables et des chaînes EVA attendues."""
from collections import Counter,defaultdict
from pathlib import Path
import csv
import hashlib
import re
import sys
sys.dont_write_bytecode = True
from ajuster import HERE, MODES, canon, corpus, load, save, sequence
from contexte import sections

SHA='11398bcb08d07827fca569014722fc487e585c4cf857ecfecced3f4983ff9401'


def folio(p):
    return re.match('f[0-9]+',p).group()


def region(p,panel):
    if p==panel:return 'panneau_source'
    return 'autre_panneau_meme_feuillet' if folio(p)==folio(panel) else 'hors_feuillet'


def confirm():
    assert hashlib.sha256((HERE/'PREDICTIONS.json.gz').read_bytes()).hexdigest()==SHA
    predictions=load('PREDICTIONS.json.gz')
    models={k:ds['tables'] for k,ds in predictions['modeles'].items() if ds['tables']}
    # La déduplication conserve toutes les tables et leurs origines dans le registre prédictif.
    types=set()
    for tables in models.values():
        for t in tables:
            for orig in t['origines']:
                for latin,ws in t['formes_predites'].items():
                    for w in ws:types.add((orig['panneau'],latin,w))
    ed,_=corpus()
    output={}; metrics=defaultdict(Counter); hits=[]
    for loc,tokens_h in ed['H'].items():
        p,kind=tokens_h[:2]
        if not kind.startswith('P') or loc not in ed['ZL'] or ed['ZL'][loc][:2]!=(p,kind):continue
        group='P0' if kind=='P0' else 'autre_'+kind
        views={e+'_'+mode:sequence(ww[loc][3],mode) for e,ww in ed.items() for mode in MODES}
        runs=sections(list(views.values()))
        modes={'commun':[(i,w) for i,w in enumerate([w for run in runs for w in run],1) if w]}
        for variant,values in views.items():
            modes[variant]=[(i,w) for i,(_,w) in enumerate(values,1) if re.fullmatch('[a-z]+',w)]
        for panel in sorted({panel for panel,_,_ in types}):
            reg=region(p,panel)
            key=(panel,group,reg)
            metrics[key]['loci']+=1
            for variant,vals in modes.items():
                metrics[key][variant]+=len(vals)
                for _,latent,eva in sorted(t for t in types if t[0]==panel):
                    for i,w in vals:
                        if w==eva:
                            hits.append({'panneau_source':panel,'region':reg,'type':kind,'locus':loc,'rang':i,
                                         'edition':variant,'mot_EVA':w,'valeur_ajustee':latent})
    for (p,kind,reg),s in metrics.items(): output.setdefault(p,{}).setdefault(kind,{})[reg]=dict(s)
    rows=load('REGISTRE.json.gz')
    around=[r for r in rows if r['page']=='f99v' and r['rang']==1]
    save('TRANSFERT.json.gz',{'reprises':hits,'denominateurs':output,'rangee_source':around,
        'informations':'Les mots nouveaux demandés ont zéro graphie EVA générable avant lecture. Aucun test positif d’une cible non représentable.'})


if __name__=='__main__':confirm()
