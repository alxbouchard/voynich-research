"""Voisinages r/l, avec espérance exacte sous deux permutations dans chaque tronçon."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import groupby, permutations
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / '2026-11-18-mois-automne' / 'cle'))
from dechiffrer import segment
from transfert import corpus, tokens, langage

GAP = re.compile(r'<[-~]>|<![^>]*(?:gap|space|jump)[^>]*>', re.I)
SIMPLE = re.compile(r'[a-z]+')
TAILS = ('rl', 'lr')
LEVELS = ('min2', 'exact5', 'min5')


def classes(length):
    return [level for level, yes in zip(LEVELS,(length>=2,length==5,length>=5)) if yes]


@lru_cache(None)
def size(word):
    return len(segment(word))


def stratum(page, section, quires):
    if quires[page]=='T':
        return 'cahier_final'
    return {'H':'plantes_entieres','P':'pharmaceutique','Z':'zodiaque'}.get(section,'autres')


def runs(raw, cut):
    # Les interruptions physiques coupent le tronçon mais ne comptent pas comme mots.
    rank = 0
    for piece in GAP.split(raw):
        items = []
        for word in tokens(piece,cut):
            rank += 1
            items.append((rank,word))
        for valid, group in groupby(items,lambda pair:bool(SIMPLE.fullmatch(pair[1]))):
            fields = list(group)
            if valid:
                yield fields


def analyze(words):
    n=len(words)
    sizes = Counter(map(size,words))
    adjacent_sizes = Counter(size(a) for a,b in zip(words,words[1:]) if size(a)==size(b))
    counts = Counter(words)
    stats = Counter(voisins=n-1,mots=n,troncons=1)
    events = []
    for a, count in counts.items():
        if not a.endswith('r'):
            continue
        b = a[:-1]+'l'
        if b not in counts:
            continue
        length = size(a)
        for level in classes(length-1):
            product = count * counts[b]
            stats['melange_'+level] += Fraction(product,n)
            stats['longueurs_fixes_'+level] += Fraction(adjacent_sizes[length]*product, sizes[length]*(sizes[length]-1))
    for k,(a,b) in enumerate(zip(words,words[1:])):
        if size(a)==size(b):
            for level in classes(size(a)-1):
                stats['voisins_meme_longueur_'+level] += 1
                if a[-1]+b[-1] in TAILS:
                    stats['voisins_finales_'+a[-1]+b[-1]+'_'+level] += 1
        if a[:-1] != b[:-1]:
            continue
        order = a[-1]+b[-1]
        if order not in TAILS:
            continue
        for level in classes(size(a)-1):
            stats[order+'_'+level] += 1
        if size(a)>=3:
            events.append((k,a,b))
    return stats,events


def verify():
    for words in [('dar','dal','dar','k'),('ar','ar','al'),('dar','dal','dor','dol','x'),('opcheor','opcheol')]:
        stats,_ = analyze(words)
        all_perms = list(permutations(words))
        same_lengths = [p for p in all_perms if list(map(size,p))==list(map(size,words))]
        for level in LEVELS:
            for direction in TAILS:
                def count(order):
                    return sum(a[:-1]==b[:-1] and a[-1]+b[-1]==direction and level in classes(size(a)-1)
                               for a,b in zip(order,order[1:]))
                for prefix,perms in [('melange_',all_perms),('longueurs_fixes_',same_lengths)]:
                    assert stats[prefix+level] == Fraction(sum(map(count,perms)),len(perms))
    assert [rs for rs in runs('a.dar<??>.dal<!gap>dar<->dal.dar,dal','separes')] == [[(1,'a')],[(3,'dal')],[(4,'dar')],[(5,'dal'),(6,'dar'),(7,'dal')]]
    assert size('opcheor')==6


def inventory(editions, sections, quires):
    aggregates = defaultdict(Counter)
    events = defaultdict(list)
    focal = {}
    for ed,rows in editions.items():
        for cut in ('joints','separes'):
            version = ed+'/'+cut
            for loc,(page,kind,_,raw) in rows.items():
                focus = re.match(r'^f89[rv]',page) is not None
                if focus and loc!='f89r2.22':
                    continue
                section = stratum(page,sections.get(page,''),quires)
                kind_group = 'prose' if kind=='P0' else ('anneaux' if kind=='Cc' else 'autres_lieux')
                table = aggregates[version,kind_group,section]
                if not focus:
                    table['loci'] += 1
                for span in runs(raw,cut):
                    first = span[0][0]
                    stats, found = analyze([word for _,word in span])
                    if not focus:
                        table.update(stats)
                    for k,a,b in found:
                        event = {'locus':loc,'type':kind,'section':section,'rang':first+k,
                                 'mots':[a,b],'prefixe_unites':size(a)-1}
                        if focus:
                            if (a,b)==('opcheor','opcheol'):
                                focal[version] = event
                        else:
                            events[version].append(event)
    rows = {'/'.join(key):{k:(round(float(v),8) if isinstance(v,Fraction) else v)
                            for k,v in sorted(stats.items())} for key,stats in sorted(aggregates.items())}
    return rows,events,focal


def confirmed(events):
    def event_key(e):
        return e['locus'],e['type'],e['section'],*e['mots'],e['prefixe_unites']
    by_version = {version:Counter(map(event_key,found)) for version,found in events.items()}
    intersection = by_version['H/joints'].copy()
    for counter in by_version.values():
        intersection &= counter
    result = []
    for (loc,kind,sec,a,b,length),n in sorted(intersection.items()):
        ranks = {v:[e['rang'] for e in found if e['locus']==loc and e['mots']==[a,b]] for v,found in events.items()}
        result.append({'locus':loc,'type':kind,'section':sec,'mots':[a,b],
                       'prefixe_unites':length,'occurrences_min':n,'rangs':ranks})
    return result


def main():
    verify()
    editions, sections = corpus()
    heads = re.compile(r'^<([^.,>]+)>\s+<![^>]*\$Q=(\w)',re.M)
    quires = dict(heads.findall((langage.DATA/'ZL3b-n.txt').read_text()))
    counts,events,focal = inventory(editions,sections,quires)
    assert set(focal)==set(events)=={'H/joints','H/separes','ZL/joints','ZL/separes'}
    assert {e['rang'] for e in focal.values()}=={5}
    obj = {'f89r2.22':focal,'comptes_hors_f89':counts,
           'couples_observes':dict(events),'confirmes_quatre_lectures':confirmed(events)}
    (HERE/'resultats.json').write_text(json.dumps(obj,ensure_ascii=False,indent=1)+'\n')


if __name__=='__main__':
    main()
