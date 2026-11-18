"""Isoler quatre positions anonymes ; réserver les trois autres et tous les noms d'image."""
import json
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = {'voynich':'voynich/f68r3-centres.json','bayer':'etalons/bayer1603_UMA_points.json'}


def main():
    fit, reserved = {},{}
    for tag,source in SOURCES.items():
        data = (HERE.parent/source).read_bytes()
        points = sorted(json.loads(data)['points'],key=lambda p:(p['x'],p['y']))
        assert len(points)==7
        fit[tag] = {'empreinte':sha256(data).hexdigest(), 'xy':[[p['x'],p['y']] for p in points[::2]]}
        reserved[tag] = {'empreinte':sha256(data).hexdigest(),'reserve':points[1::2], 'calage':points[::2]}
    for fname,obj in [('apprentissage',fit),('reserve',reserved)]:
        (HERE/(fname+'.json')).write_text(json.dumps(obj,indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
