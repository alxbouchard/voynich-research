# Le mot de la ligne situé à l’aplomb d’une étiquette reprend-il son texte ?

**Aucune des 30 graphies annoncées sur les feuillets 88 et 89 n’occupe la case prédite.** Avant d’ouvrir les mots, nous avions publié la graphie attendue et le numéro de la case la plus proche de l’étiquette. Dans les lignes supérieures, 4 des 13 cases annoncées ont une lecture entière concordante en H et ZL dans les deux traitements du blanc incertain. Dans les lignes inférieures, 8 des 17 en ont une. Aucune de ces 12 lectures ne correspond à l’annonce. La transcription H et le visualiseur permettent de vérifier les 30 cases et donnent aussi zéro réussite. [Prédictions publiées avant l’ouverture](https://github.com/alxbouchard/voynich-research/blob/cb61bc3/research/2026-11-18-noms-dans-une-phrase/enumeration/mots-caches/PREDICTIONS.json) · [Les graphies réellement lues](RESULTATS.json)

**Exemple du feuillet 88.** L’étiquette f88r.25 se lit `ofaldo`. Ses coordonnées prédisaient ce mot au rang 6 de la dernière ligne du paragraphe supérieur, f88r.22, où on lit `chorcholsal`. De l’autre côté du dessin, les mêmes coordonnées prédisaient `ofaldo` au rang 7 de la première ligne du paragraphe inférieur, f88r.26, où on lit `okoldy`. Les deux résultats concordent dans les quatre traitements et aux deux positions correspondantes du visualiseur. [Carte sans transcription de prose](GEOMETRIE-MASQUEE.json) · [Résultats par étiquette](RESULTATS.json)

| Feuillet et ligne visée | Annonces | Graphies correctes / cibles concordantes | Correctes / cibles lisibles en H et dans le visualiseur | Contrôle d’un mot à droite, correctes / concordantes |
|---|---:|---:|---:|---:|
| 88, dernière ligne au-dessus | 5 | 0/3 | 0/5 | 0/5 |
| 89, dernière ligne au-dessus | 8 | 0/1 | 0/8 | 0/1 |
| 88, première ligne au-dessous | 6 | 0/1 | 0/6 | 0 case concordante |
| 89, première ligne au-dessous | 11 | 0/7 | 0/11 | 0/6 |
| **Total** | **30** | **0/12** | **0/30** | **0/12** |

## Comment les mots ont été cachés

Le registre photographique répertorie quatre rangées sur f88r/v et sept sur f89r1/r2. Il ne fournit aucune rangée du feuillet 101 admissible selon ces mêmes critères. Le feuillet 89, choisi en remplacement comme prévu, avait déjà été étudié pour des reprises de mots dans des paragraphes. Certaines lectures du feuillet 88 étaient également connues. Ce qui a été prédit avant le dévoilement est **le couple formé par une case géométrique déterminée et la graphie d’une étiquette**. La publication des trente annonces a précédé l’autorisation d’ouvrir les cibles. [Protocole public](https://github.com/alxbouchard/voynich-research/blob/cb61bc3/research/2026-11-18-noms-dans-une-phrase/enumeration/mots-caches/PROTOCOLE.md) · [Registre utilisé](../../../2026-11-18-paires-ingredients/rangees/rangees.tsv)

La carte de départ conserve les rectangles de Voynichese, les limites de paragraphes, le nombre de positions par ligne en H et la lecture des légendes. Les lettres et identifiants des mots de prose y ont été supprimés. Sur chacun des quatre panneaux le total des boîtes est égal au nombre de positions H. Le prédicteur choisit la boîte la plus proche par son centre horizontal. Le rang doit rester identique si l’on redresse l’axe d’après la pente des lignes de prose. Après ouverture, le mot associé à chaque boîte sélectionnée a été comparé à H. Les 30 égalités à ce niveau vérifient l’association des boîtes aux mots de H. [Programme de masquage et de prédiction](predire.py) · [Carte](GEOMETRIE-MASQUEE.json) · [Données de position de f88r dans Voynichese](https://www.voynichese.com/2/data/folio/script/f88r.js)

Les 37 légendes du registre donnent 74 couples légende–direction possibles. Dans 22 cas, il manque une ligne adjacente selon la règle. Dix-huit autres lectures de légende divergent, trois sont composées de plusieurs mots et une donne des rangs différents selon l’axe ou une égalité. Restent 30 annonces pour **27 cases distinctes**. Au-dessus des dessins de f88v, deux paires d’étiquettes pointent respectivement sur le même mot en fin de ligne. À f89r2, deux étiquettes pointent également sur le même rang de f89r2.28. Chaque couple a été conservé, avec les doublons de case signalés dans les données. [Registre complet des annonces et des abstentions](PREDICTIONS.json)

## Ce que disent les contrôles

Après déplacement d’un rang vers la droite, aucune des 12 cases dont les quatre lectures concordent ne contient la graphie annoncée. Les positions initiale et déplacée sont toutes deux recevables pour 10 annonces et donnent zéro de chaque côté. Un tirage uniforme entre les cases concordantes d’une même ligne est possible pour 23 annonces. Son nombre attendu de réussites est exactement zéro. Pour les sept autres annonces, aucun rang de leur ligne ne satisfait le critère strict de concordance. [Dénominateurs par annonce et par contrôle](RESULTATS.json)

Une vérification après coup précise la raison de ce résultat. Même en parcourant **tous les mots de chacune des lignes visées** dans chacune des quatre lectures séparément, puis dans le visualiseur, **aucun des 30 mots attendus n’apparaît ailleurs dans sa propre ligne**. L’hypothèse de la répétition littérale échoue donc dès le choix de la ligne. Les colonnes de cet échantillon ne permettent pas de dire si, quand un mot s’y trouve effectivement, il préfère la position à l’aplomb du dessin. Aucun sens de lecture ni aucune traduction n’est établi par ces distances. [Résultats de la recherche dans les lignes entières](RESULTATS.json)

## Reproduire

Le fichier de prédictions porte l’empreinte SHA-256 `a6a92c76b7d12da70fcad6546c93a8755f3b1a1c57c8b2340a3398a4ded74a6b`. Depuis ce répertoire, `python3 -B predire.py predire` régénère les numéros et les graphies en utilisant uniquement la carte publiée. Pour refaire aussi le masquage ou le dévoilement, télécharger les quatre fichiers JSON natifs de Voynichese (extension distante `.js`) et les quatre vues de référence dans un même dossier. La carte indique les empreintes des vues et des données de position. Le dévoilement contrôle les empreintes des données de position et celle de la carte publiée. Le masquage utilise Pillow pour lire les dimensions des vues. [Programme de prédiction](predire.py) · [Programme de vérification](verifier.py)

```sh
mkdir -p /tmp/voynich-cartes-88-89
for page in f88r f88v f89r1 f89r2; do
  curl -fsSL "https://www.voynichese.com/2/data/folio/script/${page}.js" -o "/tmp/voynich-cartes-88-89/${page}.json"
  curl -fsSL "https://www.voynichese.com/2/data/folio/image/glance/color/large/${page}.jpg" -o "/tmp/voynich-cartes-88-89/${page}.jpg"
done
python3 -B predire.py masquer --sources /tmp/voynich-cartes-88-89
python3 -B predire.py predire
python3 -B verifier.py /tmp/voynich-cartes-88-89
```
