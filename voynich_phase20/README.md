# Phase 20 — déchiffrement et limites de mots

30 octobre 2026. **Calibration à clé inconnue exécutée : un contrôle sur
douze satisfait les deux seuils fixés. Aucun ajustement de phase 20 sur
le Voynich, aucune langue ni traduction du manuscrit validées.**

[Rapport de calibration](RAPPORT.md) · [protocole et reproduction](CALIBRATION.md)
· [paramètres figés](CALIBRATION_PROTOCOL.json) · [résultats](results/calibration/summary.json).

Les passages réservés contiennent 6 028 lettres : le bras exact en retrouve
5 983 (99,25 %), essentiellement grâce à l'initialisation. Le placement des
espaces reste insuffisant, même à lettres correctes connues. Le seuil prévu
avant calcul ferme donc l'application interprétée au Voynich. Le diagnostic
anglais préparatoire ci-dessous reste conservé avec ses limites d'origine.

La [phase 19](../voynich_phase19/RAPPORT.md) montre que des textes générés
sans message reproduisent le signal des finales. Pour poursuivre, nous
examinons une méthode qui utilise des probabilités de mots et de caractères
pendant la recherche d'une clé, y compris sans espaces connus.

La phase 4 avait déjà retiré les espaces et testé des substitutions
homophoniques avec un score de quatre caractères, en EVA et en signes
composés, dans les deux sens. Retirer les espaces à nouveau ne suffit donc
pas à constituer une nouvelle expérience. L'apport envisagé ici est de
faire intervenir les limites de mots et un modèle lexical dans le score
des clés. Le diagnostic préparatoire présenté ci-dessous ne réalise que le calcul
de segmentation à lettres décodées fixées.

## Méthode externe et exécution

Bradley Hauer, Ryan Hayward et Grzegorz Kondrak,
[« Solving Substitution Ciphers with Combined Language Models », COLING 2014](https://aclanthology.org/C14-1218/),
[code officiel figé](https://github.com/bmhauer/hhk-decipherment/tree/2c7ad49cd4f4fa852168a8ce295bf739bf076adc).
L'article combine modèles de mots et de caractères ; sa section 6.5 traite
les espaces absents avec un découpage glouton par les plus longs mots.
Le modèle de chiffrement du programme est une substitution monoalphabétique
bijective, pas un modèle général d'écriture inconnue ou syllabique.

Neuf fichiers sources sont conservés sans modification dans `vendor/`.
Leurs empreintes et leur révision figurent dans
[vendor_sources.json](data/vendor_sources.json). Les modèles anglais
publiés, dérivés du New York Times selon le README des auteurs, sont
acquis localement et vérifiés par empreinte. Ils ne sont pas redistribués.
Les versions sont décrites dans [authors_model_sources.json](data/authors_model_sources.json).

Le programme MCTS des auteurs a exécuté 100 itérations sur leur propre
exemple de README, avec `PERL_HASH_SEED=0` et `PERL_PERTURB_KEYS=0`.
Les coefficients sont ceux du code publié. Une exécution par condition :

| Condition | Lettres correctes | Sortie |
| --- | --- | --- |
| Espaces fournis | 23/23 | `this is a top secret message` |
| Espaces retirés | 21/23 | `thisisatulsecretmessage` |

Les deux processus se terminent normalement, sans erreur standard.
Ce sont des tests d'installation sur un exemple public connu de l'analyste,
**pas une calibration sur des textes réservés ni une réplication complète
des expériences de l'article**. Le résultat sans espaces ne prouve pas
que davantage d'itérations donneraient exactement la même sortie.
Voir [les résultats bruts](results/authors_smoke_summary.json).

## Défaut observé sur cet exemple

À lettres fixées, le découpage glouton du code original donne :

| Lettres candidates | Découpage glouton | Score combiné (log naturel) |
| --- | --- | ---: |
| Celles du texte correct | `this i sato p secret message` | −61,833504 |
| Celles de la sortie erronée | `this is atul secret message` | −49,045070 |

Un score plus élevé est préféré. Le score avec découpage glouton classe
donc la sortie erronée devant les lettres correctes : ce problème précis
ne se réduit pas à un budget insuffisant de recherche de clé.

Un nouveau calcul dynamique compare toutes les segmentations couvertes
par le dictionnaire publié (123 619 mots), en conservant les deux mots
précédents dans son état. Il utilise exactement la même interpolation
de trigrammes de mots et de caractères. Il ne reçoit pas les espaces
corrects et n'utilise pas de faisceau tronqué.

Pour les lettres correctes, il retient `this is a top secret message`,
score **−33,307728**. Pour les lettres erronées, le meilleur découpage
reste `this is atul secret message`, score **−49,045070**. Le classement
entre ces deux candidats est ainsi corrigé sur cet exemple.

La comparaison exhaustive de **1 031 016 segmentations** confirme les
deux optimums. Une autre vérification appelle les modules Perl originaux
`NoSpace.pm` et `JMSmoothing.pm`, avec le dictionnaire complet et les seules
probabilités nécessaires à ces deux graphes de segmentation. Les découpages
gloutons concordent et l'écart maximal de score est inférieur à
**3 × 10⁻¹⁴**. Cette vérification partage les modèles sources ; elle ne
constitue pas une réplication externe.

[Audit détaillé](results/authors_exact_segmentation_audit.json) ·
[Vérification avec le code des auteurs](results/segmentation_verification.json).

## Limites du diagnostic préparatoire

- Le correctif a été développé après observation de l'erreur : ce n'est pas
  un test aveugle ou un protocole préinscrit.
- Dans ce diagnostic, le calcul exact choisit des espaces pour deux chaînes
  de lettres connues, sans rechercher une clé inconnue. La calibration
  ultérieure à clé inconnue est présentée dans le rapport lié en tête.
- Il se limite aux segmentations entièrement couvertes par le dictionnaire.
  Il ne modélise pas encore les mots inconnus, les variantes historiques,
  les unités graphiques incertaines ou les syllabes.
- L'anglais sert seulement au contrôle du programme publié. Rien ici
  n'identifie l'anglais comme langue du Voynich.
- Ce diagnostic ne mesurait pas la durée ou la mémoire d'une recherche
  complète de clé avec ce score. Le gain sur cet exemple ne garantit pas une meilleure
  récupération sur d'autres textes.

Le score a ensuite été intégré à un moteur de recherche de clé et testé
selon un protocole figé, avec le résultat défavorable décrit dans le
[rapport](RAPPORT.md). Il faudra corriger et recalibrer cette configuration
avant de la comparer aux témoins sans message et au manuscrit. Aucun texte
Voynich n'est présenté comme décodé.

## Reproduction du diagnostic anglais préparatoire

Pour les douze contrôles latins et italiens, suivre plutôt
[les instructions de calibration](CALIBRATION.md#vérification-et-reproduction).

Python 3 et Perl avec leurs bibliothèques standard suffisent. Depuis la
racine du dépôt, les modèles occupent environ 0,87 Go avec leurs archives.
Le premier script utilise le réseau seulement si un fichier manque ou
échoue à la vérification de son empreinte.

```sh
python3 voynich_phase20/src/acquire_authors_models.py
python3 voynich_phase20/src/smoke_authors.py --rerun
python3 voynich_phase20/src/audit_author_segmentation.py
python3 voynich_phase20/src/verify_segmentation.py
```

Sans `--rerun`, le contrôle d'installation relit ses résultats existants
après vérification des sources et modèles ; il ne prétend pas les recalculer.
`--rerun` remplace les sorties de ce contrôle. L'audit exhaustif peut prendre
plusieurs minutes. Les fichiers de travail et modèles restent dans `tmp/`,
ignoré par Git. Le petit audit `authors_short_nospace_score_audit.json`
conserve le calcul exploratoire initial, reproduit et étendu par l'audit
exact documenté ici.

## Licence et attribution

Le logiciel amont est sous **CC BY-SA 4.0**, avec attribution à Hauer,
Hayward et Kondrak et citation de leur article ci-dessus. La
[licence originale](vendor/hhk-decipherment/LICENCE) est conservée.
Les adaptations de calcul et les scripts de ce dossier `src/` sont aussi
diffusés sous CC BY-SA 4.0 ; ils ont été ajoutés par ce projet. Les modules
dans `vendor/` restent inchangés. Les droits sur les modèles et corpus
d'origine ne sont pas remplacés par cette licence ; seuls leurs liens et
empreintes sont publiés ici.
