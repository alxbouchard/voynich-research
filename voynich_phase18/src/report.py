#!/usr/bin/env python3
"""Render the phase-18 record from verified results; no new fitting."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT/name).read_text())


def number(value, digits=4):
    return f'{value:.{digits}f}'.replace('.', ',')


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(map(str, row))+' |' for row in rows])


def main():
    controls = load('results/controls_summary.json')
    real = load('results/real_summary.json')
    verification = load('results/verification.json')
    assert verification['status'] == 'passed' and verification['real_results_checked']
    p = load('PROTOCOL.json')
    rows = real['observed']
    names = {'initial': 'Initiale', 'final': 'Finale', 'latin': 'Latin', 'italian': 'Italien'}
    candidates = []
    for family in real['families']:
        for language in p['languages']:
            matched = [r for r in rows if r['family'] == family and r['language'] == language]
            primary = [r for r in matched if r['source_case'].startswith('ZL')]
            passes = len(matched) == 4 and all(r['gain_bits'] > 0 and r['coverage'] >= .995 for r in matched) and all(r['gain_bits'] > r['null_max'] for r in primary)
            if passes:
                candidates.append(f"{names[family].lower()} / modèle {names[language].lower()}")
    calibration = []
    true_key_advantages = []
    for family in p['families']:
        for language in p['languages']:
            rr = [r for r in controls['rows'] if r['family'] == family and r['language'] == language]
            for r in rr:
                saved = load(f"results/{r['name']}_{family}.json")
                true_key_advantages.append(saved['train']['objective']-saved['true_key_train']['objective'])
            calibration.append([names[family], names[language], len(rr),
                                number(100*min(r['accuracy'] for r in rr)),
                                number(100*min(r['position_accuracy'] for r in rr)),
                                number(100*min(r['coverage'] for r in rr)),
                                'Oui' if all(r['gate_passed'] for r in rr) else 'Non'])
    results_table = []
    for r in rows:
        interval = f"{number(r['null_min'])} à {number(r['null_max'])}" if r['null_count'] else 'Non calculé'
        exceed = f"{r['null_at_least_observed']}/19" if r['null_count'] else '—'
        results_table.append([r['source_case'].replace('_', ' / '), names[r['language']], names[r['family']],
                              number(r['gain_bits']), interval, exceed, number(100*r['coverage'], 2)])
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharex=True, constrained_layout=True)
    colors = {'initial': '#23789b', 'final': '#bb5d35'}
    for ax, group in zip(axes, ['ZL_A', 'ZL_B']):
        subset = [r for r in rows if r['source_case'] == group]
        for y, r in enumerate(subset):
            ax.plot([r['null_min'], r['null_max']], [y, y], color='#b3bac1', linewidth=7, solid_capstyle='round')
            ax.scatter([r['gain_bits']], [y], s=60, color=colors[r['family']], zorder=3)
            ax.annotate(number(r['gain_bits'], 3), (r['gain_bits'], y), xytext=(0, 10),
                        textcoords='offset points', ha='center', fontsize=9)
        ax.axvline(0, color='#4c5663', linewidth=.8, linestyle='--')
        ax.set(yticks=list(range(len(subset))),
               yticklabels=[names[r['language']]+' · '+names[r['family']].lower() for r in subset],
               title=group.replace('_', ' / '), xlabel='Gain sur pages réservées (bits / fenêtre de 4 caractères)',
               ylim=(-.7, len(subset)-.4))
        ax.invert_yaxis()
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='x', alpha=.15)
    fig.suptitle('Clés de position : résultats et témoins mélangés\nPoint = Voynich ; barre grise = étendue des 19 témoins', fontsize=13)
    for extension in ['png', 'svg']:
        fig.savefig(ROOT/'results'/f'position_comparison.{extension}', dpi=180)
    plt.close(fig)
    if candidates:
        conclusion = ('Le critère exploratoire de poursuite est atteint pour : **'+', '.join(candidates)+
                      '**. Il autorise à concevoir une nouvelle étude, pas à identifier une langue ou à annoncer un déchiffrement.')
    else:
        conclusion = ('**Aucune combinaison famille/langue n’atteint le critère exploratoire de poursuite sur les deux groupes ZL avec les sensibilités IT.** '
                      'Un gain isolé ne justifie donc pas de promouvoir cette famille en solution de déchiffrement.')
    text = f'''# Phase 18 — substitutions à l’initiale ou à la finale

30 octobre 2026. **Aucune langue, clé ou traduction du Voynich validée.**

Les seize contrôles synthétiques passent les seuils fixés. Les deux modèles
ont ensuite été appliqués aux transcriptions, avec des pages réservées et
des mélanges de lettres respectant leur rôle dans le mot. {conclusion}

![Comparaison des gains](results/position_comparison.png)

## Question et protocole

La première expérience emploie une table pour la première lettre du mot,
la seconde pour sa dernière lettre ; chacune conserve une autre table pour
toutes les autres positions. Ce sont deux expériences distinctes. Un mot
d’une lettre utilise la table de position. Les espaces restent fixes, les
passages incertains et les fins de ligne interrompent les fenêtres de calcul.
Les caractères EVA sont des unités de transcription, sans phonétique connue.

Le [protocole](PROTOCOL.json), le solveur et l’orchestrateur ont été enregistrés
dans le commit local `876da79` avant la calibration de phase 18. Ce gel local
n’est pas une préinscription externe. Aucun paramètre de recherche n’a été
modifié après lecture des résultats de cette phase. Le contrôle de calcul et
la rédaction ont été ajoutés ensuite. Le [brouillon](PROTOCOL_DRAFT.md) est intact.

Chaque ajustement utilise huit redémarrages de 60 000 propositions, puis au
plus huit passes gloutonnes. Le choix de clé repose uniquement sur l’objectif
d’apprentissage. Le modèle à une table reçoit le même nombre de propositions ;
cette égalité ne garantit pas la même difficulté d’optimisation.

## Calibration : retrouver un texte dont la clé est cachée

Les modèles de langue proviennent de César et de l’Enfer/Purgatoire de Dante,
déjà archivés en phase 10. Les textes chiffrés sont Pline et le Paradis.
Quatre clés sont tirées pour chaque langue et famille : **seize essais sur
deux textes**, pas seize corpus indépendants. Le solveur ne reçoit ni les
textes clairs ni les clés vraies. Ces derniers servent à mesurer l’exactitude.

{table(['Table distincte', 'Langue témoin', 'Clés', 'Exactitude minimale (%)', 'Position minimale (%)', 'Couverture minimale (%)', 'Seuils passés'], calibration)}

Seuils préfixés : exactitude globale ≥99 %, aux positions concernées ≥98 %,
couverture des signes observés en apprentissage ≥99,5 %, sur les huit contrôles
de chaque famille. Les espaces ne comptent pas comme lettres correctes.
Les erreurs, y compris les signes non vus, restent au dénominateur.
Les réussites portent exclusivement sur ces chiffres synthétiques.

La meilleure clé ajustée peut encore être imparfaite : dans les contrôles,
l’objectif d’apprentissage dépasse celui de la clé vraie d’au plus
{number(max(true_key_advantages), 6)} unités. Même après une calibration proche
de 100 %, la maximisation de cet objectif n’est donc pas un certificat de vérité.

## Voynich : pages exclues de l’ajustement

Les groupes Currier A/B et les transcriptions ZL/IT sont traités séparément.
La liste lexicographique des feuillets physiques est réservée aux indices
0, 5, 10, etc. Recto et verso restent dans le même ensemble. L’apprentissage
est plafonné à 24 000 lettres en lignes complètes. Cette partition reproduit
la phase 10 : elle n’est pas nouvelle pour l’analyste et ne réserve pas des
cahiers entiers. Elle ne garantit pas une représentation équilibrée des mains
et sections. Voir [les feuillets exacts](data/split.json).

Le gain est la diminution du score négatif de langue, en bits par fenêtre
de quatre caractères, espaces inclus, face à une seule table. Un gain positif
n’est ni un pourcentage de texte traduit ni une identification de langue.
Les valeurs absolues de deux modèles linguistiques ne sont pas comparables
comme probabilités de langue.

{table(['Corpus', 'Modèle de langue', 'Table distincte', 'Gain', 'Étendue des 19 mélanges', 'Mélanges ≥ observé', 'Couverture (%)'], results_table)}

IT est une autre transcription du même manuscrit, pas une réplication sur
un objet indépendant. Aucun témoin mélangé IT n’était prévu. Les décomptes
de dépassement sont descriptifs ; aucune p-valeur ni découverte corrigée pour
comparaisons multiples n’est revendiquée.

## Ce que les mélanges contrôlent

Pour chaque groupe ZL, dix-neuf témoins permutent les caractères dans les
groupes « feuillet physique × rôle dans le mot » : initiale, intérieure,
finale, singleton. Les longueurs de mots, les fins de ligne, les inconnues
et les fréquences de signes par rôle sont préservées avant filtrage des
segments courts. Apprentissage et test sont mélangés séparément. Les mêmes
témoins alimentent les deux modèles de langue et les deux familles.
Les clés sont réapprises intégralement sur chaque témoin.

**Limite vérifiée après exécution :** les segments de moins de quatre caractères
sont ensuite exclus. Un mélange peut échanger une lettre avec un tel segment.
Les fréquences par rôle ne sont donc pas exactement fixes dans le sous-ensemble
finalement noté : l’écart L1 maximal, sommé par feuillet/rôle/signe, vaut
{verification['max_retained_role_histogram_l1_after_short_span_filter']} occurrences sur les ensembles vérifiés.
Ce diagnostic ne change ni les tirages ni les résultats ; une éventuelle
suite devra laisser les segments exclus fixes avant de construire les témoins.

Ces mélanges détruisent beaucoup de contraintes locales, y compris celles
d’un générateur sans message. Les dépasser établit au plus une organisation
séquentielle. Cela ne suffit pas à démontrer le chiffrement testé.

## Vérification et portée

- {verification['fits_checked']} ajustements contrôlés : 32 sur témoins connus,
  24 sur transcriptions non mélangées et 228 sur mélanges.
- {verification['heldout_letter_predictions_checked']:,} prédictions de lettres réservées recalculées,
  en comptant les répétitions entre clés et modèles, pas des lettres uniques du manuscrit.
- Décodage, compte des positions, objectifs d’apprentissage, scores réservés,
  exactitudes et résumés recalculés par un second code Python.
- {verification['null_split_invariants_checked']} ensembles mélangés vérifiés pour les longueurs,
  barrières et comptes par rôle avant filtrage.
- Cinq tests ciblés passent, dont le cas d’un alphabet partiellement absent
  et la séparation des passages inconnus.
- Les 1 771 fichiers de l’archive des phases 1 à 17 ont été vérifiés avant
  le travail ; ces expériences historiques n’ont pas été relancées.

Les deux codes de calcul partagent les données et modèles figés. Ce contrôle
interne n’est pas une réplication par une autre équipe ni une expertise
linguistique. Les clés et sorties complètes restent archivées sous le nom
`test_decoded_NOT_TRANSLATION`. Aucune phrase n’est déclarée traduite.

Les conclusions restent limitées au périmètre du test : deux permutations
de caractères, espaces conservés, deux modèles de langue et un budget donné.
Ils ne couvrent pas les homophonies, abréviations, ligatures, segmentation
conjointe, autres langues ou mécanismes sans message.

## Suite utile

{conclusion}

Avant tout nouveau travail lexical, une suite devrait comparer les sorties
à des générateurs sans message plus structurés et à des chiffres connus,
préserver exactement les segments effectivement notés dans les mélanges,
et examiner la stabilité des clés sur des partitions de cahiers. Ces tests
restent à préparer et à exécuter ; aucun résultat de phase 19 n’est revendiqué.

[Instructions de reproduction](README.md) · [Résultats structurés](results/real_summary.json)
· [Vérification](results/verification.json) · [Attributions](../NOTICE.md)
'''
    (ROOT/'RAPPORT.md').write_text(text.replace(f"{verification['heldout_letter_predictions_checked']:,}", f"{verification['heldout_letter_predictions_checked']:,}".replace(',', ' ')))
    print(json.dumps({'report': str(ROOT/'RAPPORT.md'), 'followup_candidates': candidates}, ensure_ascii=False))


if __name__ == '__main__':
    main()
