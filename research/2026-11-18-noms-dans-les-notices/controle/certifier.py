"""Vérifie toutes les cellules de la sortie publiée contre le second calcul."""
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
from verifier import BUNDLED, HIST, INPUT, REG, WORK, analyse, choose, parse

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def enumeration_active(data):
    active=[]
    for id in data['groups']['A']:
        row=data['details'][id]
        scores={page:max((h[-1] for h in hits),default=0) for page,hits in row.items()}
        if len(set(scores.values()))>1:
            win_tallies={}
            for page,score in scores.items():
                win_tallies[page]=sum(2*(score>other)+(score==other) for peer,other in scores.items() if peer!=page)
            active.append((id,win_tallies))
    obs=sum(w[data['ranks'][id]['page']] for id,w in active)
    choices=list(permutations(active[0][1],len(active)))
    count=sum(sum(w[p] for (_,w),p in zip(active,ps))>=obs for ps in choices)
    return dict(labels=[id for id,_ in active],at_least_as_good=count,assignments=len(choices),fraction=str(Fraction(count,len(choices))))

def main():
    out=json.loads((BUNDLED/'RESULTATS.json').read_text())
    a=json.loads((WORK/'audit_independant.json').read_text())
    versions={e+'_'+m:parse(INPUT/f,m) for e,f in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')] for m in ['separe','joint']}
    ledger=json.loads(REG.read_text())
    cohort,_=choose(ledger,versions)
    expected=[(d['id'],d['label'],d['page'],d['split'],d['strict']) for d in out['couples']]
    assert cohort==expected
    counts={}
    scores={}
    for name,secondary,main in [('latin',a['latin'],out['latin']),*((k,v,out['voynich'][k]) for k,v in a['voynich'].items())]:
        cells=hits=0
        for subset,nom in [('train','apprentissage'),('validation','validation')]:
            u,v=secondary[subset],main[nom]
            assert u['score_value']==v['permutation']['score'] and u['p']==v['permutation']['p'] and u['p_tail']==v['permutation']['au_moins_aussi_bon']
            for id,pages in u['details'].items():
                for page,ij in pages.items():
                    h=v['comparaisons'][id][page]
                    assert ij==[[x['rang'],x['mot'],x['locus'],x['score']] for x in h['lectures']]
                    assert max((x[-1] for x in ij),default=0)==h['score']
                    cells+=1
                    hits+=len(ij)
                assert u['ranks'][id]['own']==v['rangs'][id]['exact_ou_partiel']
                assert u['ranks'][id]['n']==v['rangs'][id]['positions']
            scores[name+'_'+subset]={'frac':u['score'],'queue':u['p_tail'],'permutations':u['p_count'],'scores_cibles':u['own']}
        assert secondary['train']['chosen']==main['choix_terminaison']['regle']
        counts[name]={'cellules':cells,'occurrences':hits}
    sourcehash={p.name:digest(p) for p in [HIST/'source.wiki.gz',HIST/'corpus.jsonl',REG,INPUT/'IT2a-n.txt',INPUT/'ZL3b-n.txt',BUNDLED/'comparer.py',BUNDLED/'RESULTATS.json']}
    subset,_=choose(ledger,versions,True)
    reduced={}
    for edition in ('H_separe','ZL_separe'):
        p,_,c=versions[edition]
        res=analyse(subset,p,c,False)
        reduced[edition]={'apprentissage':res['train']['score'],'validation':res['validation']['score'],'regle':res['train']['chosen']}
    audit=dict(empreintes_sha256=sourcehash,extraits_latins_entierement_reproduits=40,calculs_concordants=counts,classements=scores,
               distribution_exacte_supplementaire={k:enumeration_active(a['voynich'][k]['validation']) for k in versions},
               sensibilite_exclusion_des_fragments_attribues_possiblement_aux_montages_ambigus={'fragments_ecartes':[r[0] for r in cohort if r not in subset],'resultats':reduced})
    (WORK/'CONTRE_VERIFICATION.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(audit,ensure_ascii=False))
if __name__=='__main__':main()
