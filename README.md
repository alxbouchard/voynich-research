# Voynich : carnet de recherche et expériences

**Mise à jour du 18 novembre 2026.** Le carnet couvre les 51 phases et 28 études sur les signes, les plantes, les bains et les diagrammes. [Consulter les découvertes et leurs rapports](DECOUVERTES.md).

**État : aucun déchiffrement, aucune langue et aucune traduction validés dans ce projet.**

**Documentation sur Google Drive : [ouvrir le dossier partagé](https://drive.google.com/drive/folders/1bHdug2Ng5kM1uNuCQiDq9LqFK9kDE2hm?usp=sharing).** Ce dossier a été fourni par Alex pour centraliser la documentation de recherche. Ses autorisations de partage sont gérées dans Google Drive.

Ce dépôt réunit les 17 phases d'une étude exploratoire du manuscrit Voynich, Beinecke MS 408, menée avec l'assistance de ChatGPT/Codex. Il conserve les expériences réellement exécutées, leurs sources, les résultats négatifs, les corrections et les limites. Il ne constitue ni un article évalué par les pairs ni une expertise paléographique indépendante.

## Commencer

- [Bilan des 17 phases](docs/BILAN.md) : question, résultat et limite de chaque étape.
- [Index détaillé des phases](docs/PHASES.md) : rapports PDF, texte intégral, protocoles, code et résultats.
- [Reproduire les calculs](docs/REPRODUCTION.md) : installation, restauration des fichiers compressés et dépendances externes.
- [Sources et ressources](docs/SOURCES.md) : transcriptions, images Yale, imagerie multispectrale et travaux étudiés.
- [Journal et corrections](docs/JOURNAL.md) : évolution des hypothèses et traçabilité de cette migration.
- [Pistes ouvertes](docs/PISTES.md) : tests possibles et critères de réussite.
- [Phase 18, projet de protocole](voynich_phase18/PROTOCOL_DRAFT.md) : clés selon la position dans les mots. **Non exécutée.**

## Ce que nous avons établi

Les transcriptions possèdent une organisation graphique prédictible. Des solveurs récupèrent des textes artificiellement chiffrés dans les familles qu'ils savent modéliser, mais n'ont fourni aucune lecture validée du Voynich. Les scores de couverture, les correspondances de motifs et les proximités lexicales ne suffisent pas à attribuer un sens.

Les espaces incertains restent des variantes. Les rapprochements entre les marges et le texte principal restent des hypothèses. Le traitement de 22 captures multispectrales de f116v n'a pas levé de façon sûre l'ambiguïté initiale `oror/aror sheey`.

## Organisation

Les dossiers historiques `voynich_20261028/` et `voynich_phase2/` à `voynich_phase17/` restent côte à côte pour préserver les chemins des scripts. Le dossier de phase 1 s'appelle `voynich_20261028` pour une raison historique. Chaque phase conserve ses propres conventions de filtrage, ses unités et ses critères ; les chiffres ne sont pas automatiquement comparables entre phases.

Les gros fichiers textuels sont conservés sous forme gzip, sans perte, dans `artifacts/compressed/`. Leur chemin d'origine et leur SHA-256 figurent dans [l'inventaire](artifacts/file_index.json). Les images sources et les grandes matrices binaires sont référencées séparément. Les 17 rapports PDF et leur extraction textuelle sont inclus.

```bash
python3 tools/verify_snapshot.py
python3 tools/hydrate.py
```

La première commande vérifie l'intégrité de cette édition. Elle ne réexécute pas les 17 expériences. Consulter ensuite les instructions de la phase concernée.

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
