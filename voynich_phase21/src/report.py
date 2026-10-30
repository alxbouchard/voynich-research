#!/usr/bin/env python3
"""Report phase-21 development and fresh-control results separately. CC BY-SA 4.0."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import common as c


def main():
    summary=c.read(c.OUT/'summary.json');cases=summary['cases'];v=c.read(c.OUT/'verification.json')
    assert v['passed']
    p=c.read(c.ROOT/'PROTOCOL.json');aggregate={}
    for mode in ('initializer','closed','open','oracle_closed','oracle_open'):
        rows=[x['rows'][mode]['transfer'] for x in cases]
        correct=sum(x['correct_letters'] for x in rows);total=sum(x['letters'] for x in rows)
        tp=sum(x['boundary_tp'] for x in rows);fp=sum(x['boundary_fp'] for x in rows);fn=sum(x['boundary_fn'] for x in rows)
        aggregate[mode]={'correct_letters':correct,'total_letters':total,'accuracy':correct/total,
            'boundary_f1_macro':sum(x['boundary_f1'] for x in rows)/len(rows),
            'boundary_f1_micro':2*tp/(2*tp+fp+fn),'boundary_tp':tp,'boundary_fp':fp,'boundary_fn':fn,
            'passes_both':sum(x['character_accuracy']>=.95 and x['boundary_f1']>=.90 for x in rows),
            'all_letters_correct_cases':sum(x['correct_letters']==x['letters'] for x in rows)}
    diagnostics=[];observed_key_success=0
    for case in cases:
        name=case['case'];folder=c.DATA/'controls'/name;truth=c.read(folder/'truth.json')
        fit=(folder/'fit.txt').read_text().strip();transfer=(folder/'transfer.txt').read_text().strip()
        truekey=''.join(c.ALPHABET[truth['encryption_key'].index(x)] for x in c.ALPHABET)
        key=case['rows']['open']['key'];correct_seen=all(key[ord(x)-97]==truekey[ord(x)-97] for x in set(fit))
        observed_key_success+=correct_seen
        wrong=[{'cipher':x,'predicted':key[ord(x)-97],'true':truekey[ord(x)-97],
                'fit_count':fit.count(x),'transfer_count':transfer.count(x)}
               for x in sorted(set(fit+transfer)) if key[ord(x)-97]!=truekey[ord(x)-97]]
        diagnostics.append({'case':name,'all_fit_observed_mappings_correct':correct_seen,'wrong_mappings':wrong,
            'transfer_positions_with_unobserved_cipher_symbol':sum(x not in fit for x in transfer),
            'open_fit_minus_oracle_score':case['rows']['open']['fit']['score']-case['rows']['oracle_open']['fit']['score']})
    improvement=sum(x['rows']['open']['transfer']['boundary_f1']>x['rows']['closed']['transfer']['boundary_f1'] for x in cases)
    c.save(c.OUT/'aggregate.json',{'aggregate':aggregate,'observed_key_successes':observed_key_success,
                                  'improved_boundary_cases':improvement,'diagnostics':diagnostics})
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'voynich-phase21-v1'})
    x=np.arange(12);fig,axes=plt.subplots(2,1,figsize=(12,7.3),sharex=True,gridspec_kw={'height_ratios':[1,1.6]})
    for mode,offset,color,label in [('closed',-.1,'#a1a8b0','Dictionnaire fermé'),('open',.1,'#087e77','Mots inconnus permis')]:
        acc=[100*r['rows'][mode]['transfer']['character_accuracy'] for r in cases]
        axes[0].scatter(x+offset,acc,color=color,s=35,label=label,zorder=3)
        f1=[r['rows'][mode]['transfer']['boundary_f1'] for r in cases]
        axes[1].bar(x+offset*1.8,f1,.34,color=color,label=label)
    axes[0].axhline(95,color='#ad3c3c',linestyle='--',linewidth=1)
    axes[0].set(ylim=(92,101.5),ylabel='Lettres correctes (%)',title='Clé transférée sans réajustement à un second passage')
    axes[1].axhline(.90,color='#ad3c3c',linestyle='--',linewidth=1,label='Seuil : 0,90')
    axes[1].set(ylim=(0,1.04),ylabel='F1 des limites de mots',title='Découpage amélioré dans 12/12 cas ; seuil atteint dans 5/12')
    axes[1].legend(ncol=3,loc='lower center',bbox_to_anchor=(.5,-.37),frameon=False)
    labels=[]
    for case in cases:
        lang,length,trial=case['case'].split('_');labels.append(('Lat.' if lang=='latin' else 'It.')+f'\n{length}/{trial}')
    axes[1].set_xticks(x,labels,fontsize=8)
    for ax in axes:
        ax.axvline(5.5,color='#bbbbbb',linewidth=.8);ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
    fig.suptitle('Phase 21 — nouveaux passages, nouvelles clés, paramètres figés',fontsize=14)
    fig.text(.5,.035,'Comparaison sur les mêmes nouveaux passages ; anciens contrôles exclus avec une marge de 50 mots.\nSeuil global non atteint : aucun essai sur le Voynich.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.89,bottom=.23,hspace=.43,left=.085,right=.98)
    fig.savefig(c.OUT/'open_vocabulary_comparison.png',dpi=160)
    svg=c.OUT/'open_vocabulary_comparison.svg';fig.savefig(svg,metadata={'Date':None})
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n');plt.close(fig)
    fmt=lambda value,n=2:f'{value:.{n}f}'.replace('.',',')
    rows=[]
    for case in cases:
        r=case['rows'];opened=r['open']['transfer']
        rows.append(f"| {case['case']} | {fmt(opened['character_accuracy']*100)} % | {fmt(r['closed']['transfer']['boundary_f1'],4)} | {fmt(opened['boundary_f1'],4)} | {fmt(r['oracle_open']['transfer']['boundary_f1'],4)} | {'Oui' if case['passes_gate'] else 'Non'} |")
    a=aggregate['open'];b=aggregate['closed'];initial=aggregate['initializer']
    report=f'''# Phase 21 — mots inconnus : progrès confirmé, calibration encore incomplète

**La correction améliore le découpage sur les douze nouveaux contrôles.
Elle satisfait les deux seuils dans {summary['passed']}/12 cas, contre
{b['passes_both']}/12 pour le modèle fermé sur ces mêmes passages.
Le seuil global exigeant douze réussites n'est pas atteint : aucun essai
sur le Voynich n'a été exécuté.**

![Comparaison réservée](results/open_vocabulary_comparison.png)

## Séparation du développement et du test

Les 24 anciens passages de phase 20 ont servi à choisir un couple de
paramètres parmi 16 possibilités, en utilisant leurs lettres correctes.
Le meilleur F1 moyen de développement est 0,9178, avec coefficient
d'orthographe 1 et pénalité supplémentaire 0. C'est une mesure utilisée
pour régler le modèle, pas une performance réservée.

Le modèle, les paramètres, le générateur et le vérificateur ont ensuite
été figés dans **`8456988`**, avant sélection, génération ou ajustement des
nouveaux chiffrés. Les douze nouvelles paires de passages sont disjointes
entre elles et séparées d'au moins 50 mots des extraits de phase 20.
Les douze clés sont nouvelles. Les œuvres restent Pline et le *Paradiso*,
connues de l'analyste par le projet ; il ne s'agit donc pas d'un aveugle
global ou d'une préinscription externe.

Chaque clé est cherchée sur environ 250, 500 ou 1 000 lettres sans espaces,
puis appliquée sans changement à environ 500 autres lettres. La langue
est fournie. César et *Inferno/Purgatorio* servent seuls à entraîner les
modèles. Les graphies normalisées de phase 10 restent en vigueur.

## Résultats complets sur les passages de transfert

Les seuils fixés sont précision des lettres ≥95 % et F1 des espaces ≥0,90
dans chaque contrôle. Le F1 n'est pas un taux de traduction. La dernière
colonne de scores fournit les lettres correctes au seul découpeur, après
la recherche de clé, pour diagnostiquer ses limites.

| Contrôle | Lettres correctes, ouvert | F1 fermé | F1 ouvert | F1 ouvert, lettres correctes connues | Deux seuils |
| --- | ---: | ---: | ---: | ---: | --- |
{chr(10).join(rows)}

`latin_250_2` reste sous le seuil : **0,899328859**, même si un arrondi à
deux décimales afficherait 0,90. Le critère n'a pas été arrondi ou assoupli.

Le modèle ouvert restitue **{a['correct_letters']}/{a['total_letters']}
lettres ({fmt(a['accuracy']*100)} %)**, avec toutes les lettres correctes
dans {a['all_letters_correct_cases']}/12 passages de transfert. Les
correspondances de clé sont exactes pour tous les signes vus pendant
l'ajustement dans **{observed_key_success}/12 contrôles**. Les neuf erreurs
de transfert portent exclusivement sur des signes absents du passage
d'ajustement ; leur correspondance ne peut pas être considérée comme identifiée.

La moyenne des F1 par passage passe de **{fmt(b['boundary_f1_macro'],4)} à
{fmt(a['boundary_f1_macro'],4)}**. Les F1 regroupant tous les espaces sont
{fmt(b['boundary_f1_micro'],4)} et {fmt(a['boundary_f1_micro'],4)}. Le gain
apparaît dans les douze comparaisons, mais les textes proviennent de deux
œuvres : ce n'est pas une estimation générale d'un taux de réussite.

## Ce que la correction apporte et ce qu'elle ne résout pas

Le modèle fermé transforme les mots absents en fragments du dictionnaire.
Le modèle ouvert peut conserver une forme inconnue entière, évaluée par
son orthographe et sa longueur apprises sur l'entraînement. Il réapprend
aussi les probabilités lexicales avec une classe de mot inconnu : cette
comparaison évalue une configuration complète, pas l'effet isolé d'une
unique modification.

Les coupures superflues chutent de **{b['boundary_fp']} à {a['boundary_fp']}**
sur les passages réservés. En contrepartie, les séparations oubliées
augmentent de **{b['boundary_fn']} à {a['boundary_fn']}**. Le moteur fusionne
encore certains mots voisins ou déplace leurs limites. Par exemple, sur
un passage latin connu, `suco quam` devient `sucoquam`, et `sextum` devient
`sex tum`. Ces exemples illustrent des erreurs de segmentation, sans
inférence sur le texte du Voynich.

Les six contrôles latins échouent au seuil des espaces même lorsque les
lettres correctes sont fournies. Le modèle ouvert atteint alors le seuil
dans les six contrôles italiens ; l'échec italien restant après recherche
de clé comprend quatre lettres dont le signe chiffré n'avait jamais été vu.
Cela oriente le prochain diagnostic vers les limites de mots latines et
la gestion explicite des correspondances non observées.

La récupération des lettres vient encore surtout de l'initialisation :
elle restituait {initial['correct_letters']}/{initial['total_letters']}
lettres, contre {a['correct_letters']} après l'affinage ouvert. Le bras
fermé finit à {b['correct_letters']}. Dans ces contrôles, le nouveau score
préserve mieux les bonnes clés et apporte surtout un découpage plus fidèle ;
il ne constitue pas une nouvelle preuve générale de déchiffrement.

## Vérification et traçabilité

- 32 tests courts : C++, programme dynamique Python et énumération de
  **4 096** découpages concordent.
- Douze recherches initiales et 24 affinages, à budget identique entre les
  deux bras ; les vérités de contrôle n'entrent pas dans la recherche de clé.
- **{v['scored_outputs_checked']} sorties** reconstruites et notées par un
  second code ; métriques et chiffrés recalculés indépendamment.
- **{v['exact_open_optima_recomputed']} optimums de segmentation ouverte**
  recalculés par un programme Python distinct ; écart maximal de score
  **{v['maximum_score_difference']:.3g}**.
- Les 24 extraits correspondent aux sources ; les exclusions de phase 20,
  la disjonction des passages et les douze nouvelles clés sont vérifiées.
- Code et protocole figés inchangés après le début du test.

[Vérification](results/verification.json) · [résultats complets](results/summary.json)
· [agrégats et diagnostics des clés](results/aggregate.json).
Ces contrôles sont internes, avec les mêmes sources et modèles ; ils ne
remplacent pas une réplication externe ou une expertise linguistique.

## Conclusion opérationnelle

La prise en charge des mots inconnus apporte un progrès vérifié sur des
passages réservés. **La configuration reste insuffisante pour une application
interprétée au Voynich**, puisque sept contrôles échouent à la règle fixée.
Les résultats ne désignent ni la langue ni le procédé de rédaction du manuscrit.

La prochaine piste à tester est un modèle plus précis des frontières entre
mots, pour réduire les fusions abusives sans réintroduire les nombreuses
coupures de phase 20. Les signes jamais observés doivent rester explicitement
indéterminés. Toute correction utilisera ces résultats comme développement
et sera évaluée sur de nouveaux passages réservés. Les témoins sans message
restent nécessaires avant une interprétation du manuscrit.

[Méthode, reproduction et attribution](README.md) · [protocole figé](PROTOCOL.json).
'''
    (c.ROOT/'RAPPORT.md').write_text(report)
    print(json.dumps({'open':a,'closed':b,'observed_key_success':observed_key_success,'improved':improvement}),flush=True)


if __name__=='__main__':main()
