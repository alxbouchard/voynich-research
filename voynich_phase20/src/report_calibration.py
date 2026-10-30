#!/usr/bin/env python3
"""Report frozen calibration outcomes without changing a key or threshold.

CC BY-SA 4.0. See phase README for attribution.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import calibration as study

ROOT=study.ROOT


def main():
    p=study.protocol();summary=study.read(study.OUT/'summary.json');cases=summary['cases']
    verification=study.read(study.OUT/'verification.json')
    assert verification['passed']
    aggregate={}
    for mode in ('initializer','greedy','exact','oracle_correct_letters'):
        rows=[x['rows'][mode]['transfer'] for x in cases]
        correct=sum(x['correct_letters'] for x in rows);n=sum(x['letters'] for x in rows)
        tp=sum(x['boundary_tp'] for x in rows);fp=sum(x['boundary_fp'] for x in rows);fn=sum(x['boundary_fn'] for x in rows)
        aggregate[mode]={'correct_letters':correct,'letters':n,'character_accuracy':correct/n,
            'boundary_f1_micro':2*tp/(2*tp+fp+fn),'boundary_f1_macro':sum(x['boundary_f1'] for x in rows)/len(rows),
            'perfect_letter_cases':sum(x['correct_letters']==x['letters'] for x in rows),
            'letter_threshold_cases':sum(x['character_accuracy']>=p['gate']['character_accuracy'] for x in rows),
            'boundary_threshold_cases':sum(x['boundary_f1']>=p['gate']['boundary_f1'] for x in rows)}
    errors=[]
    for case in cases:
        name=case['case'];truth=study.read(study.DATA/name/'truth.json')
        fit=(study.DATA/name/'fit.txt').read_text().strip();transfer=(study.DATA/name/'transfer.txt').read_text().strip()
        key=case['rows']['exact']['key']
        true_key=''.join(study.ALPHABET[truth['encryption_key'].index(c)] for c in study.ALPHABET)
        wrong=[{'cipher':c,'predicted':key[ord(c)-97],'true':true_key[ord(c)-97],
                'transfer_count':transfer.count(c),'observed_during_fit':c in fit}
               for c in sorted(set(transfer)) if key[ord(c)-97]!=true_key[ord(c)-97]]
        errors.append({'case':name,'wrong_mappings':wrong,'oracle_fit_score_gap':
                      case['rows']['exact']['fit']['score']-case['rows']['oracle_correct_letters']['fit']['score']})
    comparisons={'higher_boundary_f1':sum(x['rows']['exact']['transfer']['boundary_f1']>x['rows']['greedy']['transfer']['boundary_f1'] for x in cases),
                 'same_letter_accuracy_as_greedy':all(x['rows']['exact']['transfer']['character_accuracy']==x['rows']['greedy']['transfer']['character_accuracy'] for x in cases)}
    study.save(study.OUT/'aggregate.json',{'aggregates':aggregate,'comparisons':comparisons,'error_diagnostics':errors})
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'voynich-phase20-calibration-v1'})
    x=np.arange(len(cases));fig,axes=plt.subplots(2,1,figsize=(12,7.3),sharex=True,gridspec_kw={'height_ratios':[1,1.6]})
    exact=np.array([c['rows']['exact']['transfer']['character_accuracy'] for c in cases])*100
    axes[0].scatter(x,exact,color='#086a87',s=42,zorder=3)
    axes[0].axhline(95,color='#ad3c3c',linestyle='--',linewidth=1,label='Seuil : 95 %')
    for i,y in enumerate(exact):axes[0].text(i,y+.45,f'{y:.1f}',ha='center',fontsize=8)
    axes[0].set(ylim=(92,102.4),ylabel='Lettres correctes (%)',title='Clé appliquée sans réajustement au second passage')
    axes[0].legend(loc='lower right',frameon=False)
    g=[c['rows']['greedy']['transfer']['boundary_f1'] for c in cases]
    e=[c['rows']['exact']['transfer']['boundary_f1'] for c in cases]
    axes[1].bar(x-.18,g,.34,color='#a1a8b0',label='Découpage glouton')
    axes[1].bar(x+.18,e,.34,color='#086a87',label='Découpage exact')
    axes[1].axhline(.90,color='#ad3c3c',linestyle='--',linewidth=1,label='Seuil : 0,90')
    axes[1].set(ylim=(0,1.04),ylabel='F1 des limites de mots',title='Limites de mots : un seul contrôle atteint le seuil')
    axes[1].legend(ncol=3,loc='lower center',bbox_to_anchor=(.5,-.37),frameon=False)
    labels=[]
    for c in cases:
        lang,length,trial=c['case'].split('_');labels.append(('Lat.' if lang=='latin' else 'It.')+f'\n{length}/{trial}')
    axes[1].set_xticks(x,labels,fontsize=8)
    for ax in axes:
        ax.axvline(5.5,color='#b8b8b8',linewidth=.8);ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
    fig.suptitle('Phase 20 — douze contrôles avec clés inconnues du solveur',fontsize=14)
    fig.text(.5,.035,'250, 500 ou 1 000 lettres pour chercher la clé ; environ 500 autres pour la vérifier.\nUn seul contrôle sur douze satisfait les deux seuils. Aucun essai sur le Voynich.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.89,bottom=.23,hspace=.43,left=.085,right=.98)
    fig.savefig(study.OUT/'unknown_key_controls.png',dpi=160)
    fig.savefig(study.OUT/'unknown_key_controls.svg',metadata={'Date':None})
    svg=study.OUT/'unknown_key_controls.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)
    fmt=lambda n:f'{n:.2f}'.replace('.',',')
    rows=[]
    for c in cases:
        r=c['rows'];v=r['exact']['transfer']
        rows.append(f"| {c['case']} | {fmt(v['character_accuracy']*100)} % | {fmt(r['greedy']['transfer']['boundary_f1'])} | {fmt(v['boundary_f1'])} | {fmt(r['oracle_correct_letters']['transfer']['boundary_f1'])} | {'Oui' if c['passes_gate'] else 'Non'} |")
    a=aggregate['exact'];i=aggregate['initializer'];g=aggregate['greedy']
    report=f'''# Phase 20 — clés inconnues et espaces supprimés

**La configuration ne passe pas la calibration : {summary['passed']}/{summary['total']} contrôle satisfait les deux critères fixés. Aucun essai sur le Voynich n'a été exécuté.**

Les clés sont cherchées sur un premier passage chiffré, sans connaître le
texte clair ni ses espaces. Elles sont ensuite appliquées sans changement
à un second passage. Les critères fixés exigent au moins 95 % de lettres
correctes et un F1 des limites de mots d'au moins 0,90 pour **chacun** des
douze passages réservés. Le seuil global est fermé.

![Comparaison sur les passages réservés](results/calibration/unknown_key_controls.png)

## Dispositif et portée

Six contrôles latins (Pline) et six italiens (*Paradiso*) utilisent chacun
une nouvelle permutation de 26 lettres, avec espaces supprimés. La langue
est fournie. Les modèles sont appris sur César et *Inferno/Purgatorio*.
Les textes sont normalisés selon les conventions historiques du projet.
Les modèles de langue ne voient pas les passages de contrôle ; l'analyste
connaît toutefois les œuvres par les phases précédentes.

Le protocole, le moteur et le vérificateur sont figés dans **`be58b42`**
avant génération ou ajustement des douze chiffrés. Les tailles prévues
d'apprentissage sont 250, 500 et 1 000 lettres, deux passages par taille
et langue. Chaque transfert porte sur environ 500 autres lettres. Les
passages sont distincts, avec un intervalle de 50 mots entre ajustement et
transfert. Les graines ne sont pas sélectionnées selon le résultat.

Le moteur est une adaptation, pas une réplication du MCTS de Hauer,
Hayward et Kondrak. Une initialisation par quatre caractères propose des
clés ; le score combiné affine ensuite ces clés avec découpage glouton ou
exact. Les deux bras ont les mêmes points de départ et limites de recherche.
Voir [le protocole détaillé](CALIBRATION.md) et
[les paramètres figés](CALIBRATION_PROTOCOL.json).

## Résultats de transfert complets

Le F1 compare les positions des espaces proposés aux espaces réels : ce
n'est pas un pourcentage de mots traduits. « Lettres correctes connues »
est un diagnostic calculé après l'expérience, sans recherche de clé.

| Contrôle | Lettres correctes, exact | F1 glouton | F1 exact | F1 avec lettres correctes connues | Deux seuils atteints |
| --- | ---: | ---: | ---: | ---: | --- |
{chr(10).join(rows)}

Le bras exact restitue **{a['correct_letters']}/{a['letters']} lettres
({fmt(a['character_accuracy']*100)} %)** sur les passages réservés, dont
{a['perfect_letter_cases']}/12 entièrement corrects. {a['letter_threshold_cases']}/12
franchissent le seuil des lettres, mais seulement
{a['boundary_threshold_cases']}/12 celui des espaces.

Le découpage exact améliore le F1 dans **{comparisons['higher_boundary_f1']}/12**
contrôles et l'égale dans le dernier. Les moyennes des F1 par passage sont
{fmt(g['boundary_f1_macro'])} (glouton) et {fmt(a['boundary_f1_macro'])} (exact).
Les F1 regroupant tous les espaces sont respectivement
{fmt(g['boundary_f1_micro'])} et {fmt(a['boundary_f1_micro'])}.
Ce petit jeu de contrôles ne mesure pas un taux général de réussite.

**La récupération des lettres vient surtout de l'initialisation** : elle
en restituait déjà {i['correct_letters']}/{i['letters']}. Les deux bras
finissent à {a['correct_letters']}/{a['letters']}. Le découpage exact ne
donne donc ici aucun gain supplémentaire de lettres par rapport au bras
glouton. Améliorer la segmentation n'équivaut pas à une nouvelle capacité
générale de déchiffrement.

## Diagnostic des échecs

Le dictionnaire contient les mots d'apprentissage et des lettres isolées.
Sur les passages réservés, environ **38 à 55 % des mots latins** et
**6 à 15 % des mots italiens** sont absents. Le moteur doit les couper en
fragments qu'il connaît. Même avec les lettres correctes imposées après
coup, le découpage reste sous le seuil dans onze contrôles sur douze.
Le calcul exact optimise correctement cet objectif limité ; il ne corrige
pas à lui seul la couverture lexicale et les probabilités du modèle.

Deux contrôles italiens perdent des lettres au transfert parce que les
signes correspondants n'apparaissaient jamais dans le passage d'ajustement :
12 lettres dans `italian_250_1`, sept dans `italian_500_2`.
Une correspondance non observée ne peut pas être déclarée retrouvée.

Dans `latin_250_2`, trois correspondances observées sont erronées et
produisent 26 erreurs au transfert. Le score d'ajustement de cette sortie
reste supérieur de **45,97847** unités de log naturel à celui des lettres
correctes découpées de manière optimale. Ce cas révèle une préférence
erronée du modèle ; augmenter seulement le budget ne suffirait pas à
faire du meilleur score une preuve de texte correct.

Tous les diagnostics, y compris les clés et scores de départ, sont
conservés. Aucun réglage ni critère n'a changé après ces observations.

## Vérification

- 28 contrôles de développement : quatre comparaisons de segmentation/score
  sur l'exemple anglais déjà connu et 24 chaînes courtes comparées à
  l'énumération exhaustive.
- Douze initialisations et 24 affinages de clé ; toutes les permutations
  produites sont vérifiées bijectives.
- **{verification['scored_outputs_checked']} sorties** décodées et notées
  à nouveau par un code Python distinct ; chiffrés reconstruits depuis
  les vérités d'évaluation et métriques recalculées séparément.
- **{verification['exact_segmentations_recomputed']} optimums de segmentation**
  recalculés par un second programme dynamique, pour les sorties exactes
  et les lettres correctes connues.
- Écart maximal des scores : **{verification['maximum_score_difference']:.3g}**.

[Vérification structurée](results/calibration/verification.json) ·
[provenance et gel du code](results/calibration/provenance_verification.json) ·
[résultats détaillés](results/calibration/summary.json) ·
[agrégats et erreurs](results/calibration/aggregate.json).
Ces vérifications sont internes au projet, avec des sources et modèles
partagés ; elles ne remplacent pas une réplication externe.

## Conséquence pour la suite

Cette expérience satisfait la demande de tester des clés inconnues du
solveur avant le manuscrit. **La méthode actuelle n'est pas qualifiée pour
une application interprétée au Voynich.** Le résultat concerne cette famille
de substitution, ces corpus, ce dictionnaire et ce budget. Il ne réfute
ni toutes les méthodes de segmentation ni l'existence d'un message.

La prochaine correction à tester est une représentation explicite des mots
inconnus et des variantes historiques, avec pénalités calibrées. Les cas
actuels deviennent alors des données de développement : de nouveaux
passages réservés seront nécessaires pour évaluer cette correction. Les
témoins sans message restent requis avant une interprétation du manuscrit.
Aucune correction de ce type ni comparaison Voynich n'est exécutée ici.

[Reproduction et protocole](CALIBRATION.md) ·
[diagnostic anglais antérieur et attributions](README.md).
'''
    (ROOT/'RAPPORT.md').write_text(report)
    print(json.dumps({'passed':summary['passed'],'total':len(cases),'exact':a,'comparisons':comparisons}),flush=True)


if __name__=='__main__':
    main()
