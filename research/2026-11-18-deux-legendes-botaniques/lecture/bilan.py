"""Dédupliquer les paires, vérifier les prédictions et tester le fragment français déjà transcrit."""
import gzip
import json
from lire import HERE, RESEARCH, indices

def load_gz(name):
    return json.loads(gzip.decompress((HERE/name).read_bytes()))

def unique_rows(models):
    return {(r['A'],r['B'],p) for rows in models.values() for r in rows if r['A']!=r['B'] for p in r['prose']}

def summarize(models):
    unique = unique_rows(models)
    brief = {(a,b,p) for a,b,p in unique if b!=p}
    return {'paires_distinctes_compatibles':len({(a,b) for a,b,p in unique}),
            'paires_avec_reduction':len({(a,b) for a,b,p in brief}),
            'nombre_projections_reduites_differentes':len({p for a,b,p in brief}),
            'nombre_triplets_A_B_et_sortie_reduite':len(brief),
            'paires_avec_valeurs_toutes_non_vides':sorted({(a,b) for a,b,p in unique_rows(
                {k:v for k,v in models.items() if k.endswith('/0')})})}

def main():
    macer = load_gz('MACER-PREDICTIONS.json.gz')
    parents = load_gz('PARENTES-PREDICTIONS.json.gz')
    verified = json.loads((HERE/'MACER-RESULTATS.json').read_text())
    hits = {(z['A'],z['B'],z['pred']) for b in verified['branches'].values() for z in b['rencontres']
            if z['A']!=z['B'] and not z['copie']}
    src = json.loads((HERE/'PARENTES-INDEX.json').read_text())
    french = {(r['A'],r['B']) for r in src if any(w['temoin']=='Wellcome-MS626' for w in r['sources'])}
    docs = json.loads((RESEARCH/'2026-11-18-opcheor-paralleles/francais/corpus.json').read_text())
    idx = indices(docs,2)
    brief = {(a,b,p) for a,b,p in unique_rows(parents) if (a,b) in french and b!=p}
    cassia = json.loads((HERE.parent/'noms/cassia/occurrences.json').read_text())['observations']
    observed = {r['lecture_developpee'].lower().replace(' ','') for r in cassia if r['categorie']!='initiale_absente'}
    expected = {(a,b,p) for a,b,p in unique_rows(parents) if (a,b) in {
        ('cassiafistula','cassialignea'), ('cassialignea','cassiafistula')} and p!=b}
    out = {'cassia_mentions_transcrites':len(cassia),'cassia_formes_entierement_lisibles':sorted(observed),
           'cassia_formes_reduites_deux_attributions_toutes_regles':len({p for a,b,p in expected}),
           'cassia_rencontres_reduites':sorted({p for a,b,p in expected}&observed),
           'macer':summarize(macer),'rubriques_apparentees':summarize(parents),
           'macer_attestations_de_formes_reduites_de_paires_distinctes':sorted(hits),
           'francais_f17_formes_raccourcies_distinctes':len({p for a,b,p in brief}),
           'francais_f17_rencontres_de_formes_raccourcies':[
               {'a':a,'b':b,'prediction':p,'positions':idx[p]} for a,b,p in sorted(brief) if p in idx]}
    (HERE/'BILAN.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')

if __name__=='__main__':
    main()
