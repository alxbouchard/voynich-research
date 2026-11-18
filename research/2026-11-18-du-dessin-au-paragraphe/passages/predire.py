"""Classer les paragraphes à partir des seules boîtes et des graphies des légendes."""
from itertools import combinations
from statistics import median
from preparer import load, save


RULES = ["colonne", "vertical", "premier", "dernier", "longueur"]


def center(box):
    x,y,w,h = box
    return x+w/2, y+h/2


def inclination(lines):
    all_x=[center(box)[0] for boxes in lines.values() for box in boxes]
    if not all_x:
        return 0
    extent=max(all_x)-min(all_x)
    slopes=[]
    for boxes in lines.values():
        if len(boxes)<4:
            continue
        row=[(y2-y1)/(x2-x1) for (x1,y1),(x2,y2) in combinations(map(center,boxes),2)
             if x2-x1 > extent/5]
        if row:
            slopes.append(median(row))
    return median(slopes) if slopes else 0


def winners(values):
    best = min(values)
    return [i for i,v in enumerate(values) if abs(v-best)<1e-7]


def measure(label, para, lines, slope):
    a,b = center(label)
    horizontal=[]
    vertical=[]
    slots={}
    total=0
    for loc in para:
        coords=[center(box) for box in lines[loc]]
        total+=len(coords)
        deltas=[abs(x-a+slope*(y-b)) for x,y in coords]
        ids=winners(deltas)
        slots[loc]=ids[0]+1 if len(ids)==1 else None
        horizontal.append(min(deltas))
        vertical.append(abs(median(y-slope*x for x,y in coords)-(b-slope*a)))
    first=center(lines[para[0]][0]); last=center(lines[para[-1]][-1])
    return [median(horizontal),min(vertical),abs(first[0]-a+slope*(first[1]-b)),
            abs(last[0]-a+slope*(last[1]-b)),-total],slots


def predict(data):
    result={}
    for page,item in data.items():
        slope=inclination(item["lignes"])
        sets={}
        for mode,paras in item["paragraphes"].items():
            labels={}
            for loc,label in item["legendes"].items():
                if not paras:
                    continue
                readings=[measure(label["boite"],para,item["lignes"],slope) for para in paras]
                scores=[m[0] for m in readings]
                calls={}
                for k,rule in enumerate(RULES):
                    ids=winners([row[k] for row in scores])
                    calls[rule]=ids[0] if len(ids)==1 else None
                labels[loc]=dict(mot=label["mot"],annonces=calls,
                                 scores=[[round(x,6) for x in row] for row in scores],
                                 rangs_par_ligne=[r[1] for r in readings])
            sets[mode]={"paragraphes":paras,"legendes":labels}
        result[page]={"pente":slope,"decoupages":sets}
    return result


def checks():
    lines={"1":[[0,0,2,2],[8,0,2,2]], "2":[[0,8,2,2],[8,8,2,2]],
           "3":[[20,40,2,2],[40,40,2,2]]}
    data={"demo":{"lignes":lines,"paragraphes":{"strict":[["1","2"],["3"]]},
                  "legendes":{"a":{"mot":"demo","boite":[8,-3,2,2]}}}}
    p=predict(data)["demo"]["decoupages"]["strict"]["legendes"]["a"]
    assert p["annonces"]["colonne"]==0 and p["rangs_par_ligne"][0]=={"1":2,"2":2}
    assert winners([1,1,3])==[0,1]


if __name__=="__main__":
    checks()
    save("PREDICTIONS.json.gz", predict(load("CARTE-MASQUEE.json.gz")))
