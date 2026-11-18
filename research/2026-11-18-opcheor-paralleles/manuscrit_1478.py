"""Réexamen après transcription de la copie Wellcome de la camomille."""
from itertools import product
import json
from chercher import HERE, SHAPES, analyze, cases, sources, tokenize
from quatre import inserted

def main():
    fragment = ['herba', 'erba', 'terra', 'similis']
    records = next(iter(cases({'MS458-f14v':fragment})))[1]
    summary = {}
    for (name, edition), compound, rev, width, mute in product(
            SHAPES.items(), (True,False), (False,True), (1,2,None), (False,True)):
        words = [tokenize(w,compound,rev) for w in sources()[edition][4:8]]
        result = analyze(words,records,width,mute)
        key = '/'.join([name, 'bancs' if compound else 'separes', 'inverse' if rev else 'direct',
                        str(width or 'libre'), str(int(mute))])
        summary[key] = {'deux':result['deux_mots'], 'trois':result['trois_mots'],
                        'sorties':[p for r in result['reservations'] for p in r['sorties']]}
    out = {'mots':fragment,'insertion_entre_terra_et_similis':inserted(*fragment[2:]),
           'branches':summary}
    (HERE/'latin/camomille/NOUVEAU-CALCUL.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')

if __name__=='__main__':
    main()
