"""Rendre les flexions prédites et vérifier les contraintes sur les mots de réserve."""
from collections import Counter
from pathlib import Path
import gzip,json,re,sys
from emboiter import HERE,RESEARCH,LATIN,MODES,corpus,sequence,units,read,save,encode,held_words,corpora,sha256
sys.path.insert(0,str(RESEARCH/'2026-11-18-carte-sept-etoiles/lecture'))
from essai import tables


def frozen():
    return json.loads(gzip.decompress((HERE/'MODELES.json.gz').read_bytes()))


def flexions():
    models=[m for m in frozen() if m['largeur']==2 and m['injective']];result={}
    for mdl in models:
        ws=mdl['mots'];actions={}
        for w in ws:
            suffixes=['i','ae','o'] if ws[0]=='ducenda' else ['o','i','a'];stem=w[:-1] if ws[0]=='ducenda' else w[:-2]
            for suffix in suffixes:actions[stem+suffix]=encode(stem+suffix,mdl['cle'])
        result[ws[0]]=actions
    save('FLEXIONS-ANNONCES.json',result)


def verify(xml):
    learned=frozen(); pred=read(HERE/'FLEXIONS-ANNONCES.json'); c=corpora(xml)['Celse']; vocab={w for ws in c.values() for w in ws};types={w for fam in pred.values() for w,encs in fam.items() if encs};
    eva={sig for fam in pred.values() for w,encs in fam.items() if w in vocab for sig in encs}
    extrap={sig for fam in pred.values() for encs in fam.values() for sig in encs}
    meta={}
    for line in (RESEARCH.parent/'voynich_phase17/data/ZL3b-n.txt').read_text().splitlines():
        m=re.match(r'^<(f[\drv]+)>',line)
        if m:meta[m[1]]=dict(re.findall(r'\$(\w)=(\w+)',line))
    ref=meta['f55r']; ed,_=corpus(); result={k:{'positions':0,'occurrences':[]} for k in ('f55r','f56r','f56v','autres_comparables')}
    for loc in sorted(set.intersection(*(set(rows) for rows in ed.values()))):
        views=[r[loc] for r in ed.values()];p,t=views[0][:2]; mm=meta.get(p,{})
        if not t.startswith('P') or any(r[:2]!=(p,t) for r in views):continue
        grp=p if p in result else 'autres_comparables' if all(mm.get(k)==ref.get(k) for k in ('I','H','L')) and p!='f55v' else None
        if not grp:continue
        seqs=[sequence(r[3],cut) for r in views for cut in MODES]
        for i in range(min(map(len,seqs))):
            spell={x[i][1] for x in seqs}; w=next(iter(spell))
            if len(spell)!=1 or not re.fullmatch('[a-z]+',w):continue
            result[grp]['positions']+=1
            if w in extrap:result[grp]['occurrences'].append(dict(loc=loc,rang=i+1,mot=w,atteste_dans_Celse=w in eva))
    near=[]
    for site in read(HERE/'VERIFICATION.json')['voisins_de_reserve']:
        if not site['avant']:continue
        w=site['avant'];seq=units(w,False)
        for m in learned:
            proposal=m['annonces'][site['ancre']]
            if not proposal:continue
            goal=proposal['mot']; exact=w in proposal['annonces']; compatible=False
            for k in tables(seq,goal,m['largeur'],m['cle']):
                if not m['injective'] or len(set(k.values()))==len(k):compatible=True;break
            near.append(dict(loc=site['loc'],rang=site['rang'],ancre=site['ancre'],observe=w,
             candidat=goal,triple=m['mots'],largeur=m['largeur'],injective=m['injective'],exact=exact,compatible_meme_avec_nouveaux_signes=compatible))
    allkeys=[]
    for m in learned:
        keys=m['cle'];ws=held_words(vocab,keys,m['largeur'],False) if m['corpus']=='Celse' else []
        if ws:allkeys.append(dict(mots=m['mots'],mode='homophones admis aussi pour k et r',largeur=m['largeur'],formes=ws))
    # The test cipher is manufactured separately by a permutation of six opaque symbols.
    from random import Random
    k=next(m['cle'] for m in learned if m['mots'][0]=='ducenda' and m['largeur']==2); scrambled=list('UVWXYZ');Random(806).shuffle(scrambled)
    trans=dict(zip('oldams',scrambled)); genuine={trans[e]:p for e,p in k.items()};words=['oldam','saldam','doldam'];opaque=[''.join(trans[e] for e in w) for w in words]
    recovered=[{}]
    for a,w in zip(opaque,['ducenda','inducenda','educenda']):recovered=[k for prior in recovered for k in tables(tuple(a),w,2,prior) if len(set(k.values()))==len(k)]
    out=sorted({s for key in recovered for s in encode('die',key)});secret=encode('die',genuine);assert out==secret and len(out)==1
    mac=read(LATIN);att=[n for n,ws in mac.items() if 'die' in ws];assert att
    save('FLEXIONS-RESULTATS.json',dict(propositions=pred,formes_attestees=sorted(types&vocab),attestations_celse={w:[(loc,ws.index(w)+1) for loc,ws in c.items() if w in ws] for w in sorted(types)},
      reserves=result,voisins=near,projection_homophones=allkeys,temoin_exact=dict(mots_chiffres=opaque,cles_compatibles_avec_clair=len(recovered),mot='die',annonce=out,observe=secret,notices_Macer=att)))


if __name__=='__main__':
    if sys.argv[1]=='annoncer':flexions()
    else:verify(Path(sys.argv[2]))
