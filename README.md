# Voynich : carnet de recherche et expériences

**État : aucun déchiffrement, aucune langue et aucune traduction validés dans ce projet.**

**Documentation sur Google Drive : [ouvrir le dossier partagé](https://drive.google.com/drive/folders/1bHdug2Ng5kM1uNuCQiDq9LqFK9kDE2hm?usp=sharing).** Ce dossier a été fourni par Alex pour centraliser la documentation de recherche. Ses autorisations de partage sont gérées dans Google Drive.

Ce dépôt réunit les 22 phases d'une étude exploratoire du manuscrit Voynich, Beinecke MS 408, menée avec l'assistance de ChatGPT/Codex. Il conserve les expériences réellement exécutées, leurs sources, les résultats négatifs, les corrections et les limites. Il ne constitue ni un article évalué par les pairs ni une expertise paléographique indépendante.

## Commencer

- [Bilan des 22 phases](docs/BILAN.md) : question, résultat et limite de chaque étape.
- [Index détaillé des phases](docs/PHASES.md) : rapports PDF, texte intégral, protocoles, code et résultats.
- [Reproduire les calculs](docs/REPRODUCTION.md) : installation, restauration des fichiers compressés et dépendances externes.
- [Sources et ressources](docs/SOURCES.md) : transcriptions, images Yale, imagerie multispectrale et travaux étudiés.
- [Journal et corrections](docs/JOURNAL.md) : évolution des hypothèses et traçabilité de cette migration.
- [Pistes ouvertes](docs/PISTES.md) : tests possibles et critères de réussite.
- [Phase 18, rapport et résultats](voynich_phase18/RAPPORT.md) : clés selon la position dans les mots, calibration et comparaison aux mélanges. [Protocole figé](voynich_phase18/PROTOCOL.json) ; [brouillon historique](voynich_phase18/PROTOCOL_DRAFT.md) conservé.
- [Phase 19, générateurs sans message](voynich_phase19/RAPPORT.md) : vérifier si des textes générés reproduisent le signal des finales. [Protocole figé](voynich_phase19/PROTOCOL.json) et [reproduction](voynich_phase19/README.md).
- [Phase 20, clés inconnues et espaces supprimés](voynich_phase20/RAPPORT.md) : douze contrôles et transfert des clés à des passages réservés. Un seul contrôle passe les deux seuils ; aucun essai Voynich. [Protocole et reproduction](voynich_phase20/CALIBRATION.md).
- [Phase 21, traitement des mots inconnus](voynich_phase21/RAPPORT.md) : correction réglée sur les anciens contrôles puis testée sur douze nouveaux. Découpage amélioré dans 12/12 cas, mais 5/12 seulement passent les deux seuils. [Méthode et reproduction](voynich_phase21/README.md).
- [Phase 22, correction prudente des fusions](voynich_phase22/RAPPORT.md) : aucun changement sur les douze nouveaux passages de transfert ; une fusion corrigée mais deux fausses coupures ajoutées sur les passages d'ajustement des clés. Correction non retenue. [Méthode et reproduction](voynich_phase22/README.md).

## Ce que nous avons établi

Les transcriptions possèdent une organisation graphique prédictible. Des solveurs récupèrent des textes artificiellement chiffrés dans les familles qu'ils savent modéliser, mais n'ont fourni aucune lecture validée du Voynich. Les scores de couverture, les correspondances de motifs et les proximités lexicales ne suffisent pas à attribuer un sens.

La [phase 19](voynich_phase19/RAPPORT.md) montre que des textes produits sans message intentionnel peuvent reproduire le signal statistique des finales retenu en phase 18. Ce signal seul n'est donc pas une confirmation de déchiffrement ; cela ne démontre pas que le manuscrit est dénué de sens.

La [phase 20](voynich_phase20/RAPPORT.md) récupère 99,25 % des lettres de douze passages chiffrés réservés, mais son découpage des mots échoue au seuil fixé dans onze cas. Cette configuration n'est donc pas appliquée au manuscrit. Le succès des lettres vient surtout de l'initialisation ; le calcul exact des espaces n'est pas une preuve de langue ou de sens.

La [phase 21](voynich_phase21/RAPPORT.md) permet les mots absents du dictionnaire. Sur douze nouveaux contrôles, elle retrouve 99,85 % des lettres et améliore le découpage face au modèle fermé. Cinq contrôles passent les deux seuils ; les six contrôles latins échouent encore au seuil des espaces. Aucune application au Voynich n'est engagée avec cette configuration.

La [phase 22](voynich_phase22/RAPPORT.md) conserve toutes les frontières existantes et autorise des coupures supplémentaires fortement soutenues par le contexte. Le gain observé sur les anciens passages ne se reproduit pas sur les douze nouveaux passages de transfert : les 126 frontières oubliées et les 103 fausses coupures restent identiques. Six contrôles passent les deux seuils, avant comme après correction ; ce chiffre ne représente donc aucun gain de méthode. Aucun essai Voynich.

Les espaces incertains restent des variantes. Les rapprochements entre les marges et le texte principal restent des hypothèses. Le traitement de 22 captures multispectrales de f116v n'a pas levé de façon sûre l'ambiguïté initiale `oror/aror sheey`.

## Organisation

Les dossiers historiques `voynich_20261028/` et `voynich_phase2/` à `voynich_phase17/` restent côte à côte pour préserver les chemins des scripts. Le dossier de phase 1 s'appelle `voynich_20261028` pour une raison historique. Chaque phase conserve ses propres conventions de filtrage, ses unités et ses critères ; les chiffres ne sont pas automatiquement comparables entre phases.

Les gros fichiers textuels sont conservés sous forme gzip, sans perte, dans `artifacts/compressed/`. Leur chemin d'origine et leur SHA-256 figurent dans [l'inventaire](artifacts/file_index.json). Les images sources et les grandes matrices binaires sont référencées séparément. Les 17 rapports PDF et leur extraction textuelle sont inclus. Les phases 18 à 22 ajoutent leurs rapports Markdown, figures et résultats structurés, avec des inventaires distincts.

```bash
python3 tools/verify_snapshot.py
python3 tools/hydrate.py
```

La première commande vérifie l'intégrité de l'archive initiale des phases 1 à 17. Elle ne réexécute pas ces expériences et ne couvre pas les ajouts des phases 18 à 22. Pour ceux-ci, voir les notices et vérificateurs de [phase 18](voynich_phase18/README.md), [phase 19](voynich_phase19/README.md), [phase 20](voynich_phase20/CALIBRATION.md), [phase 21](voynich_phase21/README.md) et [phase 22](voynich_phase22/README.md). Consulter ensuite les instructions de la phase concernée.

## Lire les résultats correctement

1. Une transcription EVA représente une convention de signes, pas des sons connus.
2. Une clé qui améliore un score n'est pas une traduction.
3. Les transcriptions ZL et IT décrivent le même manuscrit ; elles ne constituent pas deux manuscrits indépendants.
4. Les pages exclues d'un ajustement ont parfois été vues dans des phases antérieures. Ne pas les présenter comme totalement inconnues de l'analyste.
5. Un contrôle synthétique positif établit une capacité dans la famille construite, pas une capacité générale de déchiffrement.
6. Les modifications après observation des résultats sont conservées dans les addenda.

## Droits et attribution

Les textes, codes et images tiers conservent leurs droits et crédits d'origine. Aucune licence globale n'est attribuée aux transcriptions ou aux travaux d'autres auteurs. Voir [NOTICE](NOTICE.md). Aucun service automatique, entraînement distant ou publication publique n'est activé par ce dépôt.

Date de cette édition : 30 octobre 2026 UTC. Les dates internes des rapports sont conservées telles quelles, avec leurs conventions UTC ou Montréal.
