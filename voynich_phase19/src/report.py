#!/usr/bin/env python3
"""Render the complete, verified message-free specificity experiment."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.hashsalt'] = 'voynich-phase19'
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def fmt(value, digits=4):
    return f'{value:.{digits}f}'.replace('.', ',')


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(map(str, row))+' |' for row in rows])


def label(row):
    if row['origin'] == 'Voynich':
        return 'Voynich ZL / '+row['template'][-1]
    if row['origin'] == 'Markov2':
        return f"Généré / {row['template'][-1]} / tirage {row['replicate']}"
    return 'Timm–Schinner (échantillon)'


def main():
    summary = read('results/summary.json')
    v = read('results/verification.json')
    assert v['status'] == 'passed' and v['fits_checked'] == 368
    rows = summary['observed']
    actual = {r['base_name']: r for r in rows if r['origin'] == 'Voynich'}
    generated = [r for r in rows if r['origin'] == 'Markov2']
    signals = [r for r in rows if r['origin'] != 'Voynich' and r['final_signal']]
    timm = next(r for r in rows if r['origin'] == 'Timm_published')
    markov_pass = sum(r['final_signal'] for r in generated)
    if signals:
        answer = ('**Oui : au moins un texte produit sans message intentionnel reproduit le signal en fin de mot, '
                  'selon le critère fixé avant calcul.** Ce signal n’est donc pas spécifique d’un message dans ce dispositif. '
                  'Cela ne prouve pas que le Voynich est dépourvu de sens.')
    else:
        answer = ('**Aucun des textes générés testés ne reproduit le signal selon le critère fixé.** '
                  'Cette absence est limitée aux générateurs, tirages et budget étudiés ; elle ne démontre ni un message ni une traduction.')
    table_rows = []
    for r in rows:
        ratio = fmt(r['gain_bits']/actual[r['template']]['gain_bits'], 2) if r['origin'] == 'Markov2' else '—'
        table_rows.append([label(r), fmt(r['gain_bits']), f"{fmt(r['null_min'])} à {fmt(r['null_max'])}",
                           fmt(r['excess_over_null_mean']), f"{r['null_at_least_observed']}/19",
                           fmt(100*r['coverage'], 2), 'Oui' if r['final_signal'] else 'Non', ratio])
    colors = {'Voynich': '#285f9e', 'Markov2': '#148565', 'Timm_published': '#bb6438'}
    fig, ax = plt.subplots(figsize=(10, 7), constrained_layout=True)
    for y, r in enumerate(rows):
        ax.plot([r['null_min'], r['null_max']], [y, y], color='#b8bec5', linewidth=6, solid_capstyle='round')
        ax.scatter(r['gain_bits'], y, s=55, color=colors[r['origin']], zorder=3)
        ax.annotate(fmt(r['gain_bits'], 3), (r['gain_bits'], y), xytext=(6, -5), textcoords='offset points', fontsize=9)
    ax.axvline(0, color='#59636e', linewidth=.8, linestyle='--')
    ax.set(yticks=range(len(rows)), yticklabels=[label(r) for r in rows],
           xlabel='Gain sur texte réservé (bits / fenêtre de 4 caractères)',
           title='Signal en fin de mot — score au modèle latin\nPoints : corpus ; barres grises : étendue de leurs 19 mélanges')
    ax.invert_yaxis()
    ax.margins(x=.14, y=.08)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='x', alpha=.15)
    ax.legend(handles=[Line2D([0],[0], marker='o', color='none', markerfacecolor=c, markeredgecolor=c,
                              label=l) for c,l in [(colors['Voynich'],'Voynich'),(colors['Markov2'],'Nouveaux textes générés'),
                                                   (colors['Timm_published'],'Échantillon publié')]],
              loc='upper center', bbox_to_anchor=(.5, -.09), ncol=3, frameon=False, fontsize=9)
    for extension in ['png','svg']:
        path = ROOT/'results'/f'message_free_comparison.{extension}'
        fig.savefig(path, dpi=180, **({'metadata': {'Date': None}} if extension == 'svg' else {}))
        if extension == 'svg':
            path.write_text('\n'.join(s.rstrip() for s in path.read_text().splitlines())+'\n')
    plt.close(fig)
    text = f'''# Phase 19 — les générateurs sans message reproduisent-ils le signal des finales ?

30 octobre 2026. Aucune langue, clé ou traduction du Voynich validée.

{answer}

Parmi les six nouveaux textes de Markov, **{markov_pass}/6** satisfont le critère.
L’échantillon publié Timm–Schinner **{'le satisfait également' if timm['final_signal'] else 'ne le satisfait pas'}**.
Tous les tirages et échecs figurent ci-dessous ; aucune graine n’a été choisie
après consultation d’un score.

![Signal observé et témoins](results/message_free_comparison.png)

## Question héritée de la phase 18

En phase 18, une seconde table de substitution réservée au dernier caractère
du mot améliorait le score hors ajustement. Avec le modèle latin, les gains
ZL/A et ZL/B dépassaient leurs mélanges. Cela justifiait une vérification de
spécificité, pas une identification du latin ni un déchiffrement.

La phase 19 conserve uniquement cette hypothèse : une table unique contre
une table ordinaire et une table finale, espaces fixes, avec le même solveur,
modèle de langue, budget et graine d’optimisation. Le [protocole](PROTOCOL.json)
et le code ont été figés localement dans `5afafb7`, avant génération et
ajustement de phase 19. Ce n’est pas une préinscription externe : le choix
de la finale et du modèle latin vient des résultats déjà connus de phase 18.

## Corpus et critère fixé

Deux observations ZL/A et ZL/B reprennent les feuillets réservés de phase 18,
avec les deux faces d’un même feuillet dans le même ensemble. Ces pages ont
déjà été vues dans le projet. Elles ne constituent pas un nouveau test aveugle.
Le plafond reste de 24 000 lettres d’apprentissage en lignes complètes.

Six textes nouveaux sont produits par un modèle de Markov d’ordre 2, trois
tirages par groupe A/B. Il apprend uniquement les transitions des mots
d’apprentissage retenus pour le score, selon le rôle du prochain signe
(initial, intérieur, final, singleton). Le repli vers les contextes plus
courts utilise un pseudo-compte de 1. Chaque mot est ensuite généré signe
après signe, indépendamment des autres mots, sans texte clair ni clé de
chiffrement. Les caractères d’apprentissage et de test sont régénérés avec
deux graines distinctes. Les lettres du test réel n’ajustent pas le générateur,
mais **ses longueurs et sa disposition sont connues et conservées**.

Un septième témoin est l’échantillon Timm–Schinner publié et déjà archivé.
La première ligne d’amorce issue du Voynich avait été retirée en phase 6.
Le générateur d’origine n’a pas été réexécuté. Ce texte, redisposé sur un
gabarit artificiel, est séparé chronologiquement par pages artificielles
entières ; ses volumes et sa partition diffèrent des observations ZL.

Chaque corpus reçoit dix-neuf mélanges de lettres par feuillet/groupe de
page et rôle dans le mot. Les clés sont réapprises sur chaque mélange.
Contrairement à la phase 18, les segments courts exclus du score restent
fixes : les fréquences des caractères **effectivement notés** sont donc
exactement préservées. Apprentissage et test sont mélangés séparément.

Le critère est identique pour chaque corpus : gain positif, supérieur aux
dix-neuf gains mélangés, et couverture des signes réservés par les signes
d’apprentissage ≥99,5 %. Le gain se mesure en bits par fenêtre de quatre
caractères, espaces compris. Les décomptes sont descriptifs ; aucune p-valeur,
équivalence statistique ou correction pour comparaisons multiples n’est
revendiquée. Le rapport d’amplitude n’est pas un seuil sélectionné après coup.

## Résultats complets

{table(['Corpus','Gain','Étendue des mélanges','Gain − moyenne des mélanges','Mélanges ≥ observé','Couverture (%)','Critère atteint','Gain / ZL associé'], table_rows)}

Le signe et l’amplitude sont à distinguer : un texte généré peut avoir un
gain différent de celui du manuscrit tout en passant le même critère de
signal. Le rapport d’amplitude compare chaque Markov au groupe ZL qui lui
fournit ses statistiques et son gabarit. Aucune telle correspondance stricte
n’est imposée à l’échantillon Timm.

La variation entre tirages combine les différences des textes générés et
la convergence d’un solveur heuristique à budget fixe. Un échec n’établit
pas l’optimum global. Avec trois tirages par gabarit, ces décomptes ne sont
pas une estimation générale d’un taux de faux positifs.

## Vérification

- Quatre contrôles latins chiffrés, huit ajustements, retrouvent les clés
  et scores de phase 18 : 99,9930 % des lettres réservées et 100 % des finales.
  Ce sont des réexécutions des mêmes contrôles, pas quatre nouvelles clés.
- **{v['fits_checked']} ajustements** vérifiés : huit de calibration et 360 d’étude.
- **{v['heldout_letter_predictions_checked']:,} prédictions** réservées recalculées par un second
  décodage et un second calcul de score ; ce total compte les répétitions.
- Les six générations, soit **{v['markov_characters_regenerated']:,} caractères**, sont reconstruites
  par un second code à partir des statistiques et graines archivées.
- Les comptes de transitions sont reconstruits à partir des seules pages
  d’apprentissage ; changer les lettres réservées à longueur constante
  n’affecte pas les sorties du générateur dans le test ciblé.
- **{v['null_split_invariants_checked']} ensembles mélangés** contrôlés ; écart des fréquences par
  rôle sur les caractères notés : **zéro**. Segments exclus, longueurs et
  barrières sont conservés.
- Les **{v['timm_source_words_verified']:,} mots** de l’échantillon archivé correspondent exactement
  au fichier publié après retrait de sa seule première ligne de texte.
- Les observations ZL non mélangées reproduisent les clés et scores de phase 18.
- Six tests ciblés réussis ; toutes les sorties portent `NOT_TRANSLATION`.

Ce contrôle est interne au projet, avec les mêmes sources et modèle de
langue. Il ne remplace ni une réplication indépendante ni une lecture
paléographique ou linguistique.

## Ce que cela change pour le déchiffrement

{answer}

Un générateur fondé sur le Voynich hérite nécessairement d’une partie de
sa structure, et peut reproduire fortuitement des mots de l’apprentissage.
Les trois tirages par gabarit partagent leurs statistiques : ce ne sont pas
des manuscrits indépendants. L’échantillon Timm conserve aussi l’influence
de ses paramètres et de son amorce. Aucun de ces modèles n’est établi comme
procédé historique de rédaction du manuscrit.

Cette expérience teste une mesure, pas l’existence générale d’un sens.
Le même résultat ne pourrait donc pas être utilisé pour déclarer le texte
« traduit », « latin », « faux » ou « dénué de message ». Une piste de
déchiffrement devra apporter des prédictions qui résistent à ces témoins
structurés, une clé stable, des lectures longues et une confirmation externe.

## Suite

Les tableaux, textes générés, clés, sorties complètes, graines, versions et
empreintes restent conservés. L’étape suivante devra rechercher un critère
qui distingue des mécanismes connus porteurs d’un message de générateurs
sans message, sur des corpus et partitions qui n’ont pas servi à le choisir.
La mesure des finales seule ne remplit pas ce rôle si des témoins structurés
la reproduisent. Aucun calcul de phase 20 n’est exécuté ici.

## Sources et reproduction

Les données Voynich et les modèles César/Pline viennent des archives du projet,
sans acquisition d’un nouveau corpus. Le modèle de Markov est développé ici.
Pour Timm–Schinner : [description officielle du générateur](https://github.com/TorstenTimm/SelfCitationTextgenerator#self-citation-text-generator),
[échantillon](https://github.com/TorstenTimm/SelfCitationTextgenerator/blob/master/executable/generate/generated_text.txt),
[article référencé](https://doi.org/10.1080/01611194.2019.1596999).
L’analyse porte sur l’échantillon archivé, pas sur une réplication complète
de cet article. Les droits et la licence MIT sont conservés.

[Notice de reproduction](README.md) · [Résultats JSON](results/summary.json)
· [Vérification](results/verification.json) · [Attributions](../NOTICE.md)
'''
    for key in ['heldout_letter_predictions_checked','markov_characters_regenerated','timm_source_words_verified']:
        text = text.replace(f"{v[key]:,}", f"{v[key]:,}".replace(',', ' '))
    (ROOT/'RAPPORT.md').write_text(text)
    print(json.dumps({'markov_signal_count': markov_pass, 'timm_signal': timm['final_signal'],
                      'signal_cases': summary['message_free_signal_cases'], 'report': str(ROOT/'RAPPORT.md')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
