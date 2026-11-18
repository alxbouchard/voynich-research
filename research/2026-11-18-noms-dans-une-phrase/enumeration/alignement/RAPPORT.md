# Que prédit un code de mots entiers après une énumération ?

**Aucun des 88 alignements latins admissibles n’annonce le mot `chody` placé juste avant la suite `ckhol daiin okeoly daiin ckhy` à f99r.18. Le dernier groupe, `ckhy`, est en fin de ligne.** Nous avons ensuite mis de côté les voisins de trois autres fenêtres de même structure. Le mot `daiin`, prédit par le vote culinaire, se retrouve dans zéro des six places vérifiables. [Registre des alignements et des annonces](PREDICTIONS.json) · [Contrôle du passage initial](RESULTATS.json) · [Trois autres fenêtres](LOCAL-RESULTATS.json)

## Les 90 expressions historiques

Nous avons attribué un code EVA à chaque mot latin entier dans le patron **W et X et Y**, où W, *et*, X et Y doivent être distincts. Chez Macer, trois des cinq expressions ont un mot W dans le même vers. Dans le livre de cuisine de Bolzano, les 85 expressions répondent à cette condition. Elles donnent 83 tables culinaires distinctes ; chez Macer, on en compte trois. Une table peut prédire un groupe extérieur seulement si le mot latin correspondant est l’un des quatre mots déjà codés. Les 88 positions ont également été testées avec des mots latins remplacés par des symboles opaques. [Textes, index et inventaire des expressions](../enumerer.py) · [Procédure](PROTOCOLE.md)

| Position à prédire | Prévisions de Macer sur 3 | Prévisions culinaires sur 85 | Observation f99r.18 |
|---|---|---|---|
| Avant `ckhol` | 3 abstentions | 11 `daiin`, 2 `ckhy`, 72 abstentions | `chody` |
| Après `ckhy` | 3 abstentions | 11 `daiin`, 74 abstentions | Fin de ligne |
| Deux mots après `ckhy` | 3 abstentions | 6 `daiin`, 79 abstentions | Fin de ligne |

Un exemple de la cuisine est *speciebus et ovis et lardo*, au f. 171v de la recette 77. Le mot précédent est *et*, donc cette lecture annonce précisément `daiin` avant `ckhol`. Le mot suivant est *claro*, absent des cinq positions de départ : la table s’abstient. Dans l’édition de Macer, *siler et nardus et acetum*, vers 65, offre le même patron et ne prédit aucun des trois voisins. Les index retenus dans l’étude reconnaissent X et Y simultanément dans zéro des 88 positions. Ils contiennent des formes écrites précises et n’épuisent pas les noms fléchis des ingrédients. La ligne de f99r.18 avait déjà été vue dans l’enquête sur les noms de plantes ; sa vérification ici est rétrospective. [Alignements individuels](PREDICTIONS.json) · [Présentation du témoin culinaire](../../../2026-11-18-legendes-et-paragraphes/temoin/RESULTAT.md)

## Trois essais sur d’autres feuillets

L’alignement au même rang dans toutes les lectures a livré une seule autre fenêtre, à f105v.5. En cherchant également une suite unique avec des rangs de début différents entre les transcriptions, on en obtient deux de plus. Les prévisions pour ces nouveaux lieux ont été déposées avant d’en ouvrir les voisins. La décision commune aux trois positions est `daiin`, graphie majoritaire parmi les seuls alignements culinaires donnant une réponse. Chaque position reçoit un vote distinct.

| Fenêtre réservée | Mot avant W | Premier mot après Y | Deuxième mot après Y |
|---|---|---|---|
| f105v.5 · `qopchdy daiin chedy daiin okaildy` | `pchedal` | `opchedaiin` | Fin de ligne |
| f81v.7 · `sheckhal daiin qokeedal daiin chckhy` | Lectures divergentes | `schedy` | `qol` |
| f89r1.9 · `oiiin daiin qokeey daiin ckhol` | Lectures divergentes | `qokain` | `cheamy` |

Le seul autre panneau pharmaceutique est f89r1.9. Son mot central, `qokeey`, ne figure pas parmi les étiquettes concordantes du panneau. À la différence de f99r.18, cette répétition ne permet donc pas de prendre une légende locale pour X. Le contrôle concerne ici la récidive des mots dans une énumération ; il ne détermine aucune valeur linguistique pour `daiin`. [Réserve fixée pour f105v.5](RESERVE-PREDICTIONS.json) · [Prédictions pour les fenêtres alignables localement](LOCAL-PREDICTIONS.json)

## Une même table sur les deux panneaux pharmaceutiques

Le rapprochement de f89r1.9 et de f99r.18 impose une contrainte supplémentaire. Le mot `ckhol` ouvre le cadre à f99r et le ferme à f89r1. Deux lectures latines doivent lui donner exactement la même valeur, tout en laissant distinctes les valeurs de tous les autres codes. Aucune des neuf combinaisons de positions chez Macer ne satisfait cette contrainte. La cuisine conserve 23 des 7 225 paires de positions, correspondant à 22 tables distinctes. Ainsi *lardo et sale et pone* à f99r peut coexister avec *speciebus et ovis et lardo* à f89r1 si `ckhol` représente *lardo*. L’hypothèse a été examinée après lecture des deux fenêtres. Aucune des 22 tables ne lit l’un des deux voisins externes concordants du second panneau. [Tables communes et leurs restrictions](TABLE-COMMUNE.json)

Pour reproduire, exécuter depuis ce dossier `python3 -B aligner.py SOURCE predire`, `python3 -B elargir.py predire`, `python3 -B aligner.py SOURCE verifier`, `python3 -B elargir.py verifier`, `python3 -B local.py predire`, `python3 -B local.py verifier` et `python3 -B table_commune.py`. SOURCE est le fichier HTML de l’édition du livre de cuisine employé pour le relevé parent. [Calcul principal](aligner.py) · [Autres sections](elargir.py) · [Alignement local](local.py) · [Table partagée](table_commune.py)
