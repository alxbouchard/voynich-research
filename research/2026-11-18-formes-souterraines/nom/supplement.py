"""Sensibilité aux cibles secondaires trouvées dans les carnets et contrôle de daiin."""
from pathlib import Path
import json
from lire import ALL, FACES, fits, langage, windows

HERE=Path(__file__).resolve().parent
EXTRA=('f66v','f96r','f38r')

def main():
    baseline=langage.eligible()
    result={}
    for split in langage.SPLITS:
        for ed,pages in langage.tokens(set(baseline)|set(EXTRA),split).items():
            controls=sorted(set(baseline)-set(FACES))
            frequent=[f for f in controls if any(w=='daiin' for _,w in pages[f][:16])]
            sub={}
            for f in EXTRA:
                sub[f]={'positions_P0':len(pages[f])}
                for kind in ('unites','caracteres'):
                    samples=list(windows(pages[f],16,kind))
                    sub[f][kind]={'fenetres_lisibles':len(samples),'simple':fits(samples,ALL,True),'homophones':fits(samples,ALL,False)}
            result[ed+'_'+split]={'autres_faces':len(controls),'avec_daiin':frequent,'cibles_secondaires':sub}
    (HERE/'supplement.json').write_text(json.dumps(result,ensure_ascii=False,indent=1,sort_keys=True)+'\n')

if __name__=='__main__':
    main()
