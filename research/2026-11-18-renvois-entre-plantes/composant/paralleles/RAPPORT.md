# Une même clé pour les deux lignes du bifeuillet

**Aucune table commune** ne lit à la fois `qokol daiin qokol` sur f18v.7 et `qokchol dar qokchol` sur f23r.7 comme deux passages de l’un des sept corpus de référence. Le premier et le troisième mot de chaque ligne se répètent. Sur la seconde, le mot extérieur contient une unité `ch` supplémentaire. Il fallait que la table conserve la même valeur pour chaque signe dans les quatre mots distincts, y compris les `o` répétés. Les images avaient déjà désigné les deux pages et l’équipe en avait consulté les lignes. Le calcul qui choisit les clés a reçu uniquement les quatre formes d’ajustement. [Protocole](AVANT.md) · [Pourquoi ces deux pages sont liées](../BIFEUILLET.md)

| Corpus | Fenêtres de trois mots | Mot extérieur répété, centre différent | Lieux ajustables pour f18v seul | Lieux ajustables pour f23r seul |
|---|---:|---:|---:|---:|
| *Macer* | 13 813 | 14 | 6 | 0 |
| Celse | 80 756 | 936 | 460 | 90 |
| Herbier de Mayence (1485) | 201 | 2 | 1 | 0 |
| RIDGES | 16 374 | 115 | 77 | 5 |
| *Régime* | 1 382 | 11 | 0 | 0 |
| *Viandier* | 12 090 | 134 | 5 | 0 |
| Martino | 24 713 | 203 | 20 | 1 |
| **Total** | **149 329** | **1 415** | **569** | **96** |

Ces 1 415 fenêtres donnent 947 392 paires ordonnées distinctes à l’intérieur des ouvrages. Le test secondaire entre deux ouvrages de même langue en ajoute 29 616. Les 32 conventions portent sur trois découpages de `daiin`, zéro ou un signe muet et une ou deux lettres par signe prononcé, les valeurs des signes différents restant distinctes. Dans la transcription EVA sans signe muet, aucune des deux séquences ne se lit même isolément avec ce modèle. Avec `ii` ou `aiin` comme unité et toujours sans muet, trois ou un lieu, respectivement, conviennent pour f18v et aucun pour f23r. Les nombres plus élevés de la table autorisent le signe muet et dédoublonnent les lieux sur toutes les conventions.

Une seconde vérification a confronté directement les 922 778 couples de tables ajustables isolément, pour une même convention et dans les périmètres autorisés. Aucun couple ne donne aux signes communs des valeurs partout identiques. Ce décompte porte sur des tables et peut compter plusieurs découpages des mêmes mots. Les deux fichiers conservent les 1 415 lieux, tous les effectifs, toutes les tables d’un seul côté et la liste intégrale des solutions communes. [Annonces scellées avant ouverture](TABLES.json.gz) · [Ajustements isolés et contrôle par produit cartésien](ISOLES.json.gz)

**Voisins réservés.** Sur f18v.7, on lit `chod` et `dar` immédiatement à gauche et à droite du triplet. Sur f23r.7, on lit `shaiin` et `dairo`. La troisième forme de f14r.5 après `qokchol dar` est transcrite `dala` par H et `dalo` par ZL. Les deux traitements d’espace de chaque édition conservent cette différence. Ces cinq emplacements étaient réservés avant l’ajustement. Aucune clé n’a atteint cette étape, donc aucune prédiction du mot voisin n’a pu y être évaluée. [Ouverture des cinq emplacements](OUVERTURE.json.gz)

**Contrôle positif sur un texte réel.** Nous avons pris chez Celse *et objurgatione et* et *est eodem est*. Le mot extérieur change par insertion d’un s. Ces deux exemples ont été choisis pour le contrôle parce que les lettres des mots d’ajustement couvrent aussi les voisins. Une substitution tirée au hasard chiffre les passages. Le solveur ne reçoit que les quatre formes chiffrées et les 936 encadrements de Celse. Dans le découpage de base sans muet, il trouve une seule table, la bonne. Elle retrouve les quatre voisins *risus*, *minis*, *integritas* et *remissio*, puis *modo* après *est eodem* dans un troisième passage. Sur toutes les variantes réunies, il y a 132 ajustements, dont plusieurs répètent la même solution sous des conventions équivalentes pour ces mots. [Texte latin employé](https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/669d3657637ee44fb0aed2c37dd0f95c2b062193/data/phi0836/phi002/phi0836.phi002.perseus-lat5.xml) · [Résultats complets du témoin Celse](CELSE.json.gz)

Quatre petits corpus construits vérifient en plus le comportement avec double lettre ou unité muette, y compris lorsque le signe inséré `ch` reste muet. Dans chacun, la table injectée est retrouvée aux bons emplacements et prédit les cinq formes réservées. Cette vérification montre que le moteur sait reconnaître le mécanisme testé. Les résultats sur le bifeuillet excluent ces ajustements aux passages présents dans les sept sources. Ils laissent ouverte la lecture du manuscrit et la question de son rapport aux dessins. [Quatre défis avec clés, leurres et résultats complets](CALIBRATION.json.gz)

Depuis ce dossier, lancer `python3 -B paralleles.py annoncer CELSE.xml VIANDIER.html MARTINO.html`, puis `python3 -B paralleles.py ouvrir`, `python3 -B isoles.py`, `python3 -B calibrer.py` et `python3 -B celse.py CELSE.xml`. Les entrées externes sont contrôlées par empreinte et correspondent aux éditions de l’essai précédent. [Provenance et méthodologie des corpus](../../phrase/RAPPORT.md) · [Solveur](paralleles.py) · [Vérification exhaustive](isoles.py) · [Témoins construits](calibrer.py) · [Témoin latin](celse.py)
