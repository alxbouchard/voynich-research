# Proposition de comparaison après la phase 51

**Statut : proposition non exécutée.** Seul l'inventaire a été calculé avec la bibliothèque standard Python à partir des rapports et tables connus authentifiés. Aucun nouvel appel au parseur, import de modèle, apprentissage, inférence ou choix de langue n'a eu lieu. Aucun fichier existant ailleurs n'a été modifié. Ce dossier ne tire aucune conclusion sur le Voynich.

## Deux panels possibles, mêmes synonymes conservés

Le seul marqueur `+` dans les 799 formes sélectionnées appartient à l'anglais `22-45-1` : segments `b i + s k ɛː d`, chaîne `bi+skɛːd`. Il représente une expression comprenant une frontière lexicale. Le concept est **1419, FEAR (BE AFRAID)**, paramètre IE-CoR `45`. La [définition éditoriale](https://github.com/lexibank/iecor/blob/dd1ebc997bc38c824fb18a1ef234bbf2c229420b/cldf/parameters.csv) demande l'expression usuelle de l'état de peur et accepte explicitement des constructions à plusieurs mots. Remplacer cette entrée par le verbe anglais *fear* changerait donc aussi le choix lexical de la source.

| Langue | Entrées, 156 / 155 concepts | Candidats canoniques NFD, 156 / 155 | Maximum d'unités natives NFD, deux panels | Groupes de collisions canoniques NFD, deux panels |
|---|---:|---:|---:|---:|
| Vieux-islandais `non` | 156 / 155 | 153 / 152 | 9 | 3 |
| Anglais `eng` | 156 / 155 | 153 / 153 | 9 | 2 |
| Latin `lat` | 158 / 157 | 156 / 155 | 11 | 2 |
| Grec ancien `grc` | 158 / 157 | 157 / 156 | 11 | 1 |
| Finnois `fin` | 171 / 170 | 169 / 168 | 10 | 2 |

Les candidats et longueurs du tableau utilisent les résultats du **supplément NFD**, et ne réécrivent pas le préflight brut. Dans le panel 156, la forme anglaise en erreur est conservée mais n'est pas un candidat parseable : les nombres canoniques anglais ne sont donc pas ceux d'un lexique complet.

- **Panel 156** : 799 entrées ; une erreur anglaise après NFD. Il conserve toute la couverture commune mais ne permet pas un lancement complet avec le parseur actuel. Ne pas effacer `+`, coller arbitrairement les mots, transformer `+` en son, fractionner l'expression en deux réponses indépendantes ou remplacer la forme. Une prise en charge explicite des expressions serait une modification distincte, à spécifier et tester sur d'autres exemples avant les scores. Un traitement « absent » doit rester un échec ou une abstention avec dénominateur 156, jamais disparaître de la mesure de couverture.
- **Panel 155** : retirer **le concept 1419 de toutes les langues**, soit exactement cinq entrées : `302-45-1`, `22-45-1`, `112-45-1`, `110-45-1`, `fin-796_beafraid-1`. Il reste **794 entrées, sans erreur après NFD**. C'est une restriction technique commune, sans choix d'après scores ou cognats. Les cinq lignes retirées restent intégralement inventoriées dans le bilan, avec le motif. Ce panel fournit une option compatible avec le parseur actuel, pas une calibration déjà validée.

Sans NFD ajoutée, les panels 156 et 155 ont respectivement **146 et 144 erreurs** : 145 puis 144 formes grecques, auxquelles s'ajoute l'erreur anglaise dans le panel 156. La normalisation NFD doit donc être une convention explicite du futur protocole, distincte du résultat brut conservé. Les rapports amont prouvent l'équivalence `NFC(original)==NFC(NFD(original))` ; ils ne prouvent pas une validité linguistique.

## Contrôler les effets de taille, synonymes et longueur

**L'égalité des concepts ne suffit pas à égaliser les lexiques.** Avec tous les synonymes retenus, les nombres de candidats et leurs distributions de longueur restent différents dans les deux panels. Le bilan JSON conserve les histogrammes par longueur, les synonymes par concept, les homophones et toutes les erreurs. Aucun remplissage par doublons et aucun retrait opportuniste de synonymes n'est proposé pour donner artificiellement la même taille.

Le futur protocole devrait fixer avant tout score :

1. **Une seule définition des données et de la représentation.** Choisir explicitement le panel, la convention NFD, les labels propres et le comportement natif de suppression de durée. Conserver tous les synonymes des concepts retenus, les collisions et leurs identifiants dans la provenance séparée. Ne fournir au moteur ni les concepts ni les cognats. Une borne native commune couvrant au moins 1–11 unités évite ici les exclusions de longueur ; toutes les occurrences plus longues d'un futur corpus devront être recensées avant lancement.
2. **Des essais appariés et une pondération par concept pour l'évaluation.** Chaque lexique doit rencontrer exactement les mêmes sources réservées, partitions, graines, budgets et conditions de segmentation. Regrouper d'abord les résultats d'un même concept puis donner un poids égal à chaque concept, avec couverture et abstentions visibles. Cette pondération évite qu'un concept à plusieurs synonymes soit compté comme plusieurs observations indépendantes ; elle ne corrige pas à elle seule le nombre d'occasions offertes par le lexique au moteur. Les concepts restent des métadonnées de préparation et d'évaluation.
3. **Des références propres à chaque lexique.** Ne pas comparer directement leurs pertes, meilleurs scores ou rangs bruts. Construire pour chaque condition des contrôles nuls conservant le même lexique complet, ses candidats, synonymes, homophones et histogrammes de longueur. Appliquer la même perturbation contrôlée des sources aux cinq conditions, puis refaire toute la procédure de sélection prévue. Comparer les écarts aux références de chaque condition et leurs incertitudes. Les résultats doivent aussi être présentés par longueur de source et longueur de cible, avec des dénominateurs communs fixés avant les scores. Hors support commun, conserver le bilan séparé au lieu de prétendre à une comparaison ajustée.
4. **Un contrôle explicite de sensibilité.** Un éventuel effet de taille résiduel ne doit pas être rebaptisé effet de langue. Garder les résultats complets et les analyses ajustées côte à côte. Si un prior uniformisé par concept puis par variante est envisagé, il faudra vérifier que le moteur sait réellement le représenter et valider cette modification séparément ; cela ne fait pas partie du présent inventaire. L'égalité simultanée des concepts, de tous les synonymes, du nombre de classes canoniques et des histogrammes de longueur n'est pas obtenue ici.

Les groupes de traits partagés restent une limite de la représentation. Exemple concret, vérifié dans les paramètres primaires : vieux-islandais `302-109-1`, `hals`, renvoie au **cou** (Concepticon 1333), alors que grec `110-132-1`, `háls`, renvoie au **sel** (Concepticon 1274). Leur projection sur les sept traits PCV est identique malgré ces concepts différents. Cela ne dit rien des sorties complètes du modèle. Les trois groupes PCV observés demeurent présents dans les deux panels ; aucun ensemble de réponses acceptées n'est élargi.

## Nature des témoins et portée des contrôles

Les [métadonnées IE-CoR](https://github.com/lexibank/iecor/blob/dd1ebc997bc38c824fb18a1ef234bbf2c229420b/cldf/languages.csv) classent vieux-islandais, anglais, latin et grec dans la famille indo-européenne. Dans une comparaison avec le gothique, latin, grec et anglais sont donc des **témoins apparentés**, à des distances différentes, pas trois témoins indépendants sans relation historique. Le finnois appartient à la famille ouralienne dans les [métadonnées NorthEuraLex](https://github.com/lexibank/northeuralex/blob/e9a8119f25cf6078299132d8c4e7db338d46ff23/cldf/languages.csv), mais cette classification ne garantit ni absence d'emprunts ni absence de contacts ou de ressemblances fortuites. Un seul témoin non indo-européen ne représente pas toutes les langues alternatives.

Une permutation des **annotations cibles** entre formes, à sorties fixées, mesure seulement une association conditionnelle à ces formes, ces lexiques, ces annotations et ce modèle. Une simple permutation des **noms des cinq langues** ne crée aucun nouveau témoin et ne modifie pas les scores. Ni l'une ni l'autre ne constitue un taux de fausse identification linguistique.

Pour estimer ce dernier, une expérience ultérieure devra inclure des sources de langue réellement connue mais masquée, indépendantes de la sélection de normalisation et de lexiques, ainsi que des cas où la bonne langue n'est pas dans le panel. Il faudra exécuter la procédure complète, compter les erreurs de désignation parmi tous les essais, fixer la règle d'abstention et corriger la sélection entre plusieurs lexiques. Des données ayant seulement des frontières ou du vocabulaire construits n'établiraient pas encore les performances sur du texte historique continu. Ce travail reste à concevoir et exécuter après la phase 51.

## Fichiers et reproduction de l'inventaire seulement

[PANEL_INVENTORY.json](../../docs/PIECES_REFERENCES.md#piece-9c354cd55209a1) contient les deux panels, comptes bruts/NFD, listes de toutes les entrées retenues et retirées, synonymes, distributions de longueur, collisions canoniques et groupes PCV. Il précise `inventory_computation_performed=true` et `training_or_inference_performed=false`. [build_inventory.py](../../docs/PIECES_REFERENCES.md#piece-41a0cd529777bc) n'importe que la bibliothèque standard et ne fait aucune requête réseau :

```sh
python3 chemin-local/build_inventory.py
```

Les entrées sont fixées au préflight `982a0cf7089b7d9638e392869adee4aeb2974d30b3ca1982237904d566989eea`, au supplément NFD `c7ebe1153f969aa2a5ec9997be6ac6314498bd71b6ff01f7798c19d42734fb2b` et à la provenance `1fafe4f2d01f05dbf2178ac62e47d10c0df0f57c402a3ab2346ee82013baad72`. Les six tables locales sont réauthentifiées. Le bilan inclut les URL de sources, commits, SHA de blobs et SHA-256, ainsi que l'empreinte du script. Sources primaires : IE-CoR CLDF v1.2.1, commit `dd1ebc997bc38c824fb18a1ef234bbf2c229420b`, et NorthEuraLex CLDF v4.1, commit `e9a8119f25cf6078299132d8c4e7db338d46ff23`, toutes deux sous CC-BY-4.0. Leurs transformations amont et limites sont détaillées dans le README du préflight.
