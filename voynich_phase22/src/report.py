#!/usr/bin/env python3
"""Phase-22 results, figures and every new-boundary decision. CC BY-SA 4.0."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import phase22lib as c


def main():
    s=c.read(c.OUT/'summary.json');v=c.read(c.OUT/'verification.json');assert v['passed']
    cases=s['cases'];p=c.read(c.ROOT/'PROTOCOL.json');aggregate={};diagnostics=[];events=[]
    posthoc=c.read(c.OUT/'posthoc_diagnostic.json')['transfer_totals']['recovered']
    for mode in ('recovered','oracle'):
        aggregate[mode]={}
        for arm in ('baseline','corrected'):
            rows=[x['rows'][mode]['transfer'][arm] for x in cases]
            tp=sum(x['boundary_tp'] for x in rows);fp=sum(x['boundary_fp'] for x in rows);fn=sum(x['boundary_fn'] for x in rows)
            correct=sum(x['correct_letters'] for x in rows);total=sum(x['letters'] for x in rows)
            aggregate[mode][arm]={'correct_letters':correct,'total_letters':total,'accuracy':correct/total,
                'boundary_f1_macro':sum(x['boundary_f1'] for x in rows)/len(rows),'boundary_f1_micro':2*tp/(2*tp+fp+fn),
                'boundary_tp':tp,'boundary_fp':fp,'boundary_fn':fn,
                'passes_both':sum(x['character_accuracy']>=p['gate']['character_accuracy'] and x['boundary_f1']>=p['gate']['boundary_f1'] for x in rows)}
    for case in cases:
        name=case['case'];folder=c.DATA/'controls'/name;truth=c.read(folder/'truth.json')
        fit=(folder/'fit.txt').read_text().strip();transfer=(folder/'transfer.txt').read_text().strip()
        truekey=''.join(c.ALPHABET[truth['encryption_key'].index(x)] for x in c.ALPHABET);key=case['rows']['recovered']['key']
        wrong=[{'cipher':x,'predicted':key[ord(x)-97],'true':truekey[ord(x)-97],
            'fit_count':fit.count(x),'transfer_count':transfer.count(x)} for x in sorted(set(fit+transfer)) if key[ord(x)-97]!=truekey[ord(x)-97]]
        diagnostics.append({'case':name,'all_fit_observed_mappings_correct':all(x['fit_count']==0 for x in wrong),'wrong_mappings':wrong})
        for mode in ('recovered','oracle'):
            for split in ('fit','transfer'):
                row=case['rows'][mode][split];gold=c.cuts(truth['plaintext_'+split]);letters=row['corrected']['segmentation'].replace(' ','')
                for gap in row['added_positions']:
                    # Show the entire formerly fused token and its new pieces.
                    bounds=[0]+sorted(c.cuts(row['baseline']['segmentation']))+[len(letters)]
                    start=max(x for x in bounds if x<gap);end=min(x for x in bounds if x>gap)
                    cuts=[start]+sorted(x for x in c.cuts(row['corrected']['segmentation']) if start<x<end)+[end]
                    events.append({'case':name,'mode':mode,'split':split,'gap':gap,'correct':gap in gold,
                        'baseline_token':letters[start:end],'corrected_token':' '.join(letters[a:b] for a,b in zip(cuts,cuts[1:])),
                        'true_letters':truth['plaintext_'+split].replace(' ','')[start:end],
                        'true_boundaries_inside_token':[x-start for x in sorted(gold) if start<x<end]})
    c.save(c.OUT/'aggregate.json',{'aggregate':aggregate,'key_diagnostics':diagnostics,'added_boundary_decisions':events})
    totals=s['totals']['transfer']['recovered'];a=aggregate['recovered']['baseline'];b=aggregate['recovered']['corrected']
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'voynich-phase22-v1'})
    fig,axes=plt.subplots(2,1,figsize=(12,7.6),gridspec_kw={'height_ratios':[1,1.25]})
    by=s['by_language']['transfer']['recovered'];x=np.arange(2)
    before=[totals['baseline_fn'],totals['baseline_fp']];after=[totals['corrected_fn'],totals['corrected_fp']]
    for offset,values,color,label in ((-.18,before,'#7a8491','Avant correction'),(.18,after,'#087e77','Après correction')):
        bars=axes[0].bar(x+offset,values,.32,color=color,label=label);axes[0].bar_label(bars,padding=3)
    axes[0].set_xticks(x,['Frontières oubliées (fusions)','Fausses coupures'])
    axes[0].set(ylabel='Nombre de frontières erronées',ylim=(0,max(before+after+[1])*1.4),title='Les erreurs restent identiques sur les nouveaux passages de transfert')
    axes[0].legend(loc='upper right',frameon=False)
    x=np.arange(12)
    for arm,color,marker,label in (('baseline','#7a8491','o','Avant correction'),('corrected','#087e77','x','Après correction')):
        values=[r['rows']['recovered']['transfer'][arm]['boundary_f1'] for r in cases]
        axes[1].scatter(x,values,s=42,color=color,marker=marker,label=label,zorder=3)
    axes[1].axhline(.9,color='#c45045',linestyle='--',linewidth=1,label='Seuil : 0,90')
    axes[1].set(ylim=(0,1.04),ylabel='F1 des frontières de mots',title='Comparaison à clés identiques, sur les 12 passages de transfert')
    labels=[]
    for r in cases:
        lang,length,trial=r['case'].split('_');labels.append(('Lat.' if lang=='latin' else 'It.')+f'\n{length}/{trial}')
    axes[1].set_xticks(x,labels,fontsize=8);axes[1].axvline(5.5,color='#bbb',linewidth=.8)
    axes[1].legend(ncol=3,loc='lower center',bbox_to_anchor=(.5,-.45),frameon=False)
    for ax in axes:
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
    fig.suptitle('Phase 22 — correction conservatrice, passages et clés nouveaux',fontsize=14)
    objective='atteint' if s['strict_task_success'] else 'non atteint'
    fig.text(.5,.03,f"Objectif strict {objective} : {totals['added_correct_cuts']} fusions corrigées, {totals['added_false_cuts']} fausse(s) coupure(s) ajoutée(s).\nAucun essai sur le Voynich.",ha='center',fontsize=10)
    fig.subplots_adjust(top=.88,bottom=.23,hspace=.53,left=.09,right=.98)
    fig.savefig(c.OUT/'conservative_boundaries.png',dpi=160)
    svg=c.OUT/'conservative_boundaries.svg';fig.savefig(svg,metadata={'Date':None})
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n');plt.close(fig)
    fmt=lambda value,n=2:f'{value:.{n}f}'.replace('.',',')
    table=[]
    for case in cases:
        row=case['rows']['recovered']['transfer'];old=row['baseline'];new=row['corrected'];delta=row['changes']
        table.append(f"| {case['case']} | {fmt(new['character_accuracy']*100)} % | {fmt(old['boundary_f1'],4)} | {fmt(new['boundary_f1'],4)} | {delta['added_correct_cuts']} | {delta['added_false_cuts']} | {'Oui' if case['passes_gate'] else 'Non'} |")
    language_table=[]
    for lang,title in (('latin','Latin'),('italian','Italien')):
        d=by[lang];language_table.append(f"| {title} | {d['baseline_fn']} → {d['corrected_fn']} | {d['baseline_fp']} → {d['corrected_fp']} | {d['added_correct_cuts']} | {d['added_false_cuts']} |")
    examples=[x for x in events if x['mode']=='recovered' and x['split']=='transfer']
    example_lines=[f"- `{x['case']}`, position {x['gap']} : `{x['baseline_token']}` → `{x['corrected_token']}` ; {'séparation correcte' if x['correct'] else 'fausse coupure'} selon le texte source." for x in examples]
    seen=sum(x['all_fit_observed_mappings_correct'] for x in diagnostics);wrong=sum(len(x['wrong_mappings']) for x in diagnostics)
    oracle=s['totals']['transfer']['oracle'];o=aggregate['oracle']['corrected']
    observed_errors=sum(w['transfer_count'] for x in diagnostics for w in x['wrong_mappings'] if w['fit_count']>0)
    absent_errors=sum(w['transfer_count'] for x in diagnostics for w in x['wrong_mappings'] if w['fit_count']==0)
    dev=c.read(c.OUT/'development/verification.json');maxdev=max(x['maximum_score_error'] for x in dev['checks'])
    status='est atteint sur cette série' if s['strict_task_success'] else "n'est pas atteint sur cette série"
    fit=s['totals']['fit']['recovered']
    fit_examples=[x for x in events if x['mode']=='recovered' and x['split']=='fit']
    fit_lines=[f"- `{x['case']}`, position {x['gap']} : `{x['baseline_token']}` → `{x['corrected_token']}` ; {'séparation correcte' if x['correct'] else 'fausse coupure'}." for x in fit_examples]
    report=f'''# Phase 22 — correction prudente des fusions : aucun gain sur les nouveaux passages

**Sur douze nouveaux passages de transfert, la correction rétablit
{totals['added_correct_cuts']} séparations oubliées et ajoute {totals['added_false_cuts']}
fausse(s) coupure(s). L'objectif strict « corriger dans les deux langues sans
ajouter de coupure erronée » {status}.
{s['passed']}/12 contrôles passent les deux seuils de lettres et d'espaces,
contre {a['passes_both']}/12 avant correction. Aucun essai sur le Voynich.**

![Fusions et fausses coupures](results/conservative_boundaries.png)

## Ce qui a été modifié

Le déchiffreur de phase 21 reste identique : initialisation sur les caractères,
puis affinage avec le modèle de mots connus et inconnus. La phase 22 intervient
**après fixation des lettres**. Chaque frontière déjà proposée est conservée.
Une coupure supplémentaire doit être soutenue par le contexte de trois lettres
à gauche et trois à droite, puis améliorer le score global de segmentation.
Les comparaisons avant/après utilisent donc exactement les mêmes clés.

Le classifieur est entraîné uniquement sur César et Inferno/Purgatorio, avec
repli vers des contextes plus courts et lissage de force 20. Il n'utilise aucune
frontière de Pline ou du Paradiso pour apprendre ses tables. Son résultat est
une fréquence contextuelle lissée, pas une probabilité calibrée de lecture juste.

Le score contraint est celui de phase 21, augmenté de la somme des log-rapports
`log(p / (1-p))` aux nouvelles coupures, avec poids 1. Les nouvelles coupures
doivent avoir `p ≥ 0,90`. La programmation dynamique est exacte dans cet espace
contraint ; elle ne recherche pas toutes les segmentations possibles. Elle
préfère moins d'ajouts en cas d'égalité et conserve le résultat initial si le
gain ne dépasse pas 1e-9. Ce score pondéré n'est pas une vraisemblance normalisée.
Les termes constants omis ne le sont qu'à lettres fixées : ce score ne sert
jamais à comparer des clés différentes.

Cette contrainte empêche toute nouvelle fusion, mais empêche également de
retirer une ancienne fausse coupure. Elle limite donc le progrès possible.

## Réglage sur les anciens passages, puis gel

Les 48 passages des phases 20 et 21 ont servi au développement, à lettres et
espaces connus. Parmi 24 configurations prédéfinies, seuil 0,90 et poids 1
corrigent six fusions (quatre latines, deux italiennes) sans nouvelle fausse
coupure. Cette mesure a servi à choisir le réglage ; elle n'est pas un test réservé.

Le commit **`{v['frozen_code_and_protocol_unchanged_since'][:7]}`** fige ensuite
le protocole, le moteur, le générateur, le vérificateur et ces résultats avant
de sélectionner les nouveaux extraits ou de générer leurs clés. Aucun réglage
n'a été changé après les nouveaux résultats. Ce gel local n'est pas un
préenregistrement externe, et les œuvres étaient déjà connues de l'analyste.

Douze substitutions monoalphabétiques nouvelles sont cherchées sur environ
250, 500 ou 1 000 lettres sans espaces, puis transférées sans réajustement à
environ 500 autres lettres. Les extraits sont disjoints de ceux des phases 20
et 21 avec une marge de 50 mots ; les deux extraits de chaque contrôle sont
séparés de 50 mots. La langue est fournie au solveur. Les vérités et les passages
de transfert n'entrent pas dans la recherche de clé. Les graphies normalisées
de phase 10 et les deux œuvres de contrôle, Pline et le Paradiso, restent les mêmes.

## Résultats complets sur les passages de transfert

Le critère strict exige au moins une fusion corrigée dans chaque langue et
zéro fausse coupure ajoutée en tout. Le seuil général exige au moins 95 % de
lettres correctes et F1 des frontières au moins 0,90 dans **chacun** des douze
contrôles. Les arrondis du tableau ne modifient pas la décision.

| Contrôle | Lettres correctes | F1 avant | F1 après | Fusions corrigées | Fausses coupures ajoutées | Deux seuils |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
{chr(10).join(table)}

| Langue | Frontières oubliées avant → après | Fausses coupures avant → après | Fusions corrigées | Fausses coupures ajoutées |
| --- | ---: | ---: | ---: | ---: |
{chr(10).join(language_table)}

Les frontières oubliées passent de **{totals['baseline_fn']} à {totals['corrected_fn']}**,
et les fausses coupures de **{totals['baseline_fp']} à {totals['corrected_fp']}**.
La moyenne des F1 par passage passe de **{fmt(a['boundary_f1_macro'],4)} à
{fmt(b['boundary_f1_macro'],4)}** ; les F1 regroupés sont respectivement
{fmt(a['boundary_f1_micro'],4)} et {fmt(b['boundary_f1_micro'],4)}.
Il faut comparer les deux méthodes sur ces mêmes passages, pas directement
aux chiffres de phase 21 obtenus sur d'autres extraits.

Les six contrôles italiens passent les deux seuils et les six latins échouent,
avant comme après correction. Le passage de 5/12 en phase 21 à 6/12 ici ne
constitue donc pas un progrès de la méthode : les passages ont changé et
la correction ne modifie aucun résultat de transfert.

## Toutes les nouvelles coupures de transfert

{chr(10).join(example_lines) if example_lines else 'Aucune nouvelle coupure proposée.'}

Le [fichier des décisions](results/aggregate.json) conserve aussi tous les
ajouts sur les passages d'ajustement et avec les lettres exactes.

## Résultats sur les nouveaux passages d'ajustement des clés

Ces passages sont nouveaux pour le réglage de la correction, mais servent à
chercher les clés : ils ne sont pas des passages de transfert. La correction
y rétablit **{fit['added_correct_cuts']} frontière** et ajoute **{fit['added_false_cuts']}
fausses coupures**. Ce résultat défavorable est conservé : zéro erreur sur
le développement ne garantissait pas zéro erreur sur de nouveaux textes.

{chr(10).join(fit_lines)}

Les positions comptent les lettres sans espaces. « Fausse coupure » signifie
ici un désaccord avec les espaces de la source normalisée ; ce critère ne
tranche pas à lui seul le statut linguistique des éléments séparés.

## Diagnostic explicatif ajouté après les résultats

Sur les {posthoc['missing_boundaries']} frontières oubliées en transfert,
**{posthoc['missing_below_context_threshold']}** ont une fréquence contextuelle
inférieure au seuil figé. Les **{posthoc['missing_eligible']}** restantes franchissent
ce filtre, mais leur ajout isolé dégrade encore le score de segmentation ;
le meilleur gain vaut {fmt(posthoc['best_isolated_missing_cut_gain'],4)}.
Le calcul exact contraint confirme qu'aucune combinaison admise n'améliore
le résultat. Le filtre est donc trop restrictif pour corriger ces omissions
dans le dispositif testé ; le modèle lexical résiste aussi aux rares ajouts admis.

Ce [diagnostic postérieur](results/posthoc_diagnostic.json) explique l'absence
d'action. Il n'était pas préenregistré et ne sert pas à retoucher le seuil.
Baisser simplement le seuil ne serait pas une correction validée : la grille
de développement et les deux fausses coupures nouvelles montrent déjà le
risque de réintroduire les erreurs que l'on cherche à éviter.

## Clés et diagnostic à lettres exactes

Les deux méthodes restituent **{b['correct_letters']}/{b['total_letters']}
lettres ({fmt(b['accuracy']*100)} %)**. La correction des espaces ne peut pas
changer ce résultat. Toutes les correspondances observées pendant
l'ajustement sont exactes dans **{seen}/12 contrôles**. Les erreurs de transfert
se répartissent en {observed_errors} occurrences de signes déjà observés et
{absent_errors} occurrences de signes absents de l'ajustement. Une affectation
de clé à un signe absent ne constitue pas une correspondance identifiée.

En fournissant les lettres exactes après les recherches de clés, la correction
rétablit {oracle['added_correct_cuts']} séparations et ajoute
{oracle['added_false_cuts']} fausse(s) coupure(s). Le découpage corrigé atteint
F1 ≥0,90 dans {o['passes_both']}/12 cas à lettres exactes. Ce diagnostic ne
compte pas comme réussite de déchiffrement à clé inconnue.

## Vérification

- Les 256 contextes du classifieur vérifiés par comptage indépendant concordent.
- 48 tests courts, incluant un modèle artificiel qui force des ajouts, comparent
  le C++, le programme Python et l'énumération de 6 144 partitions candidates
  avant filtrage des contraintes ; écart maximal {maxdev:.3g}.
- Les {v['scored_outputs_checked']} sorties sont reconstruites et notées par
  un code Python distinct ; {v['exact_optima_recomputed']} optima sont recalculés
  (48 de base et 48 contraints), avec écart maximal {v['maximum_score_difference']:.3g}.
- Les frontières initiales sont préservées partout ; les ajouts, les métriques,
  les 24 extraits source, les marges d'exclusion, les douze nouvelles clés et
  l'absence des vérités dans les commandes de recherche sont vérifiés.
- Le code et le protocole figés sont inchangés depuis le commit de gel.

Le premier lancement du vérificateur a chargé par erreur un module homonyme
de phase 21 et a échoué avant l'audit. Un lanceur explicite ajouté ensuite
permet d'exécuter le vérificateur figé sans en modifier les assertions ni
les résultats de l'expérience. Cette correction d'exécution, postérieure
aux résultats, est documentée dans [l'addendum](AUDIT_ADDENDUM.md).

[Vérification](results/verification.json) · [résultats complets](results/summary.json)
· [agrégats, clés et décisions](results/aggregate.json).
Ces vérifications sont internes, avec les mêmes corpus et modèles, et ne
remplacent pas une réplication extérieure.

## Portée

Ce test mesure une correction précise sur deux œuvres, en langue connue et
sous substitution monoalphabétique. Il ne valide ni une langue, ni un procédé
de codage, ni une traduction du manuscrit. Même un bon score de lettres ne
suffit pas à certifier les mots. Les témoins sans message de phase 19 restent
nécessaires avant toute interprétation du Voynich.

Les paramètres sont conservés tels quels. Si ces erreurs guident une nouvelle
correction, ces passages devront devenir du développement et la nouvelle
méthode devra être évaluée sur d'autres données réservées.

La correction de phase 22 n'est pas retenue comme amélioration : elle ne
corrige aucune fusion en transfert et introduit deux erreurs sur les passages
d'ajustement. La prochaine piste serait de mieux distinguer un mot inconnu
entier de deux mots fusionnés, avec possibilité d'abstention, puis de mesurer
à nouveau le compromis sur de nouveaux passages. Elle reste à tester.

[Méthode et reproduction](README.md) · [protocole figé](PROTOCOL.json)
· [attribution](NOTICE.md).
'''
    (c.ROOT/'RAPPORT.md').write_text(report)
    print(json.dumps({'baseline':a,'corrected':b,'strict_task_success':s['strict_task_success'],'observed_key_successes':seen}),flush=True)


if __name__=='__main__':main()
