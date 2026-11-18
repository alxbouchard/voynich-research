# Peut-on prédire une étoile dessinée à partir du texte ?

**Sur sept faces du cahier final, les deux transcriptions placent le groupe `otor` sur huit lignes. Une étoile se trouve à la hauteur de quatre d'entre elles. Ces quatre lignes ouvrent chacune un paragraphe. Les quatre autres se trouvent à l'intérieur d'un paragraphe et n'ont aucune étoile à leur hauteur.** Ce résultat porte sur la fonction des marques en marge. L'hypothèse selon laquelle `otor` se lirait *stella* a également été essayée sur le texte et sur un passage latin connu. [Deux lignes avec le mot et leur marge](marges/CONTEXTE.jpg) · [Les dix-huit bandes photographiques telles que présentées aux lecteurs](marges/CONTACT.jpg) · [Prédictions conservées avant la lecture des marges](PREDICTIONS.json)

## Lire la marge à la hauteur du mot

Le point de départ est f68r1.26, où l’on voit une étoile près de `otor`. Le groupe revient dans le texte du dessus. Ce rapprochement avait déjà été relevé. Pour le tester dans un autre cahier, nous avons prédit la présence d'une étoile dans la marge à la hauteur de **toutes** les lignes contenant ce groupe entier en Q20. À chacune a été associée la ligne P0 suivante de la même face sans ce groupe. L'inventaire a été enregistré avant la préparation des cartes. Le dénominateur du cahier est de 1 079 lignes de prose chez Takahashi et 1 080 chez Zandbergen–Landini. Les deux traitements des espaces faibles retiennent les mêmes huit loci concordants. [Point de départ sur f68r1](../2026-11-18-mots-des-images/etoiles/texte-voisin/RESULTAT.md) · [Protocole](PROTOCOLE.md)

| Ligne avec `otor` | Étoile à cette hauteur | Début de paragraphe dans IT et ZL | Ligne voisine, sans `otor` |
|---|---|---|---|
| f104r.19 | Oui | Oui | f104r.20, absente |
| f104v.24 | Non | Non | f104v.25, absente |
| f105v.2 | Non | Non | f105v.3, centre à la limite, indéterminé |
| f106v.34 | Oui | Oui | f106v.35, absente |
| f107r.1 | Oui | Oui | f107r.2, absente |
| f113v.8 | Non | Non | f113v.9, absente |
| f113v.10 | Oui | Oui | f113v.11, absente |
| f116r.5 | Non | Non | f116r.6, absente |

Deux lecteurs IA en sessions séparées ont examiné la marge, avec l'écriture masquée et les codes en désordre. Ils s'accordent sur les dix-huit cartes, y compris l'abstention commune près d'une frontière. Parmi les sites concordants et leurs témoins, le mot prédit correctement 11 des 15 positions tranchées. La règle « début de paragraphe » en décrit 15 sur 15. Les transcripteurs ont eux aussi vu la mise en page. Ce second résultat mesure donc la concordance entre leur repérage des paragraphes et la photographie. Les lignes témoins immédiatement suivantes favorisent des continuations de paragraphes. Ces valeurs ne sont pas un taux de réussite applicable à d'autres pages. [Votes I](vote-marges-I.json) · [Votes II](vote-marges-II.json) · [Résultats détaillés](RESULTATS-MARGES.json)

Sur une neuvième ligne, f105v.31, seul Takahashi transcrit le mot entier. Les deux lecteurs placent le centre hors de cette ligne, et à l'intérieur du corridor de la suivante, f105v.32, qui ouvre un paragraphe sans `otor`. Une hampe voisine influençait le premier calage de ces deux bandes. Le préparateur a corrigé la géométrie à partir de l'écriture sans connaître les votes. Un lecteur avait vu les images initiales avant de rouvrir les deux cartes corrigées. Les seize autres images sont identiques entre versions. La proximité du centre avec la frontière justifie de garder cet exemple à part. Les modèles IA partagent des limites de vision et leurs votes ne sont pas deux expertises humaines. [Empreintes et déplacement des limites](marges/sensibilite_calage.json)

Le contrôle sur le cahier entier tient compte du nombre de mots lisibles sur les lignes d'ouverture de chaque face. Si l'on redistribue les occurrences de `otor` entre les positions lisibles de leur propre face, la probabilité d'en trouver au moins quatre sur une ouverture est de 19,9 à 20,0 % selon les espaces chez ZL (4/8) et de 28,6 % chez Takahashi (4/9). En comparant seulement les mots de quatre unités à la même silhouette `o-X-o-Y`, elle est respectivement de 56,7 % et 26,7 %. Le nombre d'ouvertures observé n'apporte donc pas d'argument fort en faveur de la lecture « étoile ». Les comptes bruts distinguent l'exposition en lignes de l'exposition en mots. [Analyse par face](paragraphes/RESULTATS.json) · [Plan de contrôle](paragraphes/PROTOCOLE.md)

## Deux roues, deux prédictions différentes

**f68v2, présence d'une étoile au milieu d'un rayon.** On compte quatre étoiles intercalées sur douze inscriptions radiales. Les lecteurs retrouvent ces quatre centres sur les images anonymisées. Les cartes du rayon laissent voir quelques fragments de traits écrits, sans transcription ni clef. Le mot entier `otor` n'apparaît dans aucune des douze inscriptions. Le début de mot `ot`, étudié auparavant sur les légendes du recto, est un indice plus large. Quand le premier mot commence ainsi, trois des cinq rayons signalés portent une étoile. Il y a deux fausses alertes et une étoile manquée. La mise en page répète les étoiles tous les trois rayons. Quatre des douze rotations du pronostic obtiennent le même résultat de 9/12. En comptant tous les mots, `ot` apparaît dans 3 des 8 groupes lisibles des rayons étoilés et 3 des 17 groupes des autres. L'organisateur et le préparateur avaient vu les commentaires du transcripteur et la disposition de ce panneau avant la vérification. [Rayons anonymisés de f68v2](reperes/cartes-B.png) · [Règle antérieure pour le motif du recto](../2026-11-18-mots-des-images/etoiles/motif-partage/RESULTAT.md) · [Rotations et dénominateurs](RESULTATS-RAYONS.json)

**f67r1, nombre d'étoiles.** La notice du folio décrit douze secteurs comportant une inscription et un compartiment voisin avec une ou deux grandes étoiles. Nous avons fixé la prédiction « une étoile par groupe écrit » avant de compter les étoiles par secteur. Les lecteurs dénombrent trois compartiments avec une étoile et neuf avec deux, soit 21 étoiles. Sur les onze inscriptions où les deux éditions et les deux conventions s'accordent sur les espaces, le nombre de groupes tombe juste 7 fois. Prédire deux étoiles partout donne 8/11. Deux manières de délimiter un secteur sur la roue sont plausibles. Elles donnent toutes deux le même total. Dans chacun des quatre découpages pris séparément, le texte atteint 7 ou 8 réponses justes sur 12, contre 9/12 pour la règle constante. Le classement des onze inscriptions ne permet donc pas d'employer les mots comme un dénombrement des étoiles. [Prédiction de multiplicité](MULTIPLICITE.md) · [Compartiments anonymisés de f67r1](reperes/cartes-A.png) · [Géométries et repères horaires](reperes/REPERES.md) · [Catalogue du feuillet](https://www.voynich.nu/q09/index.html#f67r1)

## Les mots qu'un lecteur médiéval pouvait rencontrer

Dans un manuscrit du XVe siècle conservé à Göttweig, sept visages associés aux Pléiades portent chacun un nom, parmi lesquels *Merope*, *Electra* et *Sterope*. Aucune des sept légendes ne contient *stella*. Dans un autre manuscrit du même siècle, sept femmes ayant chacune une étoile rouge partagent un texte voisin et aucune n’a de légende individuelle. Sur le globe de Schöner de 1517, la légende de l'étoile polaire porte effectivement *Alrucaba stella polaris*, alors que l'inscription au pied d'Orion donne *Rigel*. Ces lectures attestent trois usages distincts des mots près d'un astre. [Sources et transcription des emplacements](historique/RESULTAT.md) · [Page aux sept figures de la Morgan Library](https://ica.themorgan.org/manuscript/page/23/77318) · [Légende de l'étoile polaire](historique/schoner-polaire.jpg)

Pour contrôler la mécanique du déchiffrement, nous avons masqué les lettres sur une carte de Cassiopée de Tycho Brahe publiée en 1573. Les cinq correspondances tirées du véritable mot *stella* lisent aussi le verbe **est** dans le paragraphe du même feuillet. Quand une unité peut valoir plusieurs lettres, six des quinze autres mots de la légende admettent un faux ajustement à *stella*. Leurs 32 tables donnent huit lectures erronées d'au moins trois lettres dans le paragraphe. Il faut donc un autre mot de vérification. [Fac-similé et calcul de contrôle](lecture/NOTE.md)

**Essai sur le Voynich.** Dans une lecture directe à valeurs fixes et non vides, le premier et le troisième signe de `otor` doivent reproduire la même suite de lettres, suivie d'une terminaison. Cette contrainte exclut *stella*, et les 19 graphies distinctes des paradigmes classiques de *stella*, *sidus* et *astrum* que nous avons testées. Ce répertoire grammatical inclut des formes reconstruites. En autorisant `o` à rester muet et en limitant chaque autre signe à trois lettres, une table permet `t` → *ste* et `r` → *lla*. Elle fait alors lire *llalla* au mot `ror` de f68r1.3. Elle ne lit aucune des 19 autres légendes réservées admissibles. Elle rend aussi *stella* auprès du fragment végétal f99v.3. [Démonstration et essais reproductibles](lecture/NOTE.md) · [Emplacement sur le dessin de la plante](../2026-11-18-mots-des-images/etoiles/texte-voisin/photo-f99v/LOCALISATION.md)

La légende `doaro` se trouve près d'un amas de sept étoiles. Le latin *Vergiliae* est une proposition conditionnelle si cet amas représente les Pléiades. Une table ajustée sur une autre légende, f68r1.17, ne prédit que **? · e · ? · ? · e**. Les sept autres lettres sont fournies au programme en lui donnant le nom désiré. Une table ajustée à une étiquette de fragment végétal prédit exactement les deux mêmes *e*. `doaro` reste transcrit sans traduction. [Lectures de l'amas et contre-exemple](lecture/NOTE.md)

## L'effet de la position d'écriture

Le rang absolu de `otor` est souvent élevé dans les lignes du cahier final. Nous avons donc fixé un contrôle sur les deux dernières positions, puis examiné les autres cahiers en excluant à la fois le cahier final et le cahier astronomique de l'ancre. Dans cette réserve, Takahashi place le mot dans les deux dernières positions 6 fois sur 26, contre 6,42 attendues en le déplaçant parmi les mots lisibles des mêmes lignes. ZL donne 6 sur 23 pour 5,71 attendues avec les espaces faibles joints, ou 5 sur 23 pour 5,67 attendues s'ils sont séparés. Aucun `otor` de cette réserve n'est le dernier mot de sa ligne. Restreindre les emplacements possibles aux mots de même forme graphique laisse très peu de positions interchangeables. Cette expérience ne confirme pas une préférence pour les fins de ligne. [Règle enregistrée](positions/PREUVE.md) · [Calcul et détail par face](positions/resultats.json)

Pour reproduire les résultats, exécuter les scripts à partir de la racine du dépôt. Les paramètres de fabrication des cartes figurent dans les dossiers consacrés aux marges et aux repères.

```sh
python3 -B research/2026-11-18-etoile-en-images/predire.py
python3 -B research/2026-11-18-etoile-en-images/evaluer_marges.py
python3 -B research/2026-11-18-etoile-en-images/evaluer_rayons.py
python3 -B research/2026-11-18-etoile-en-images/positions/tester.py
python3 -B research/2026-11-18-etoile-en-images/paragraphes/compter.py
python3 -B research/2026-11-18-etoile-en-images/lecture/lire.py
python3 -B research/2026-11-18-etoile-en-images/lecture/suite.py
python3 -B research/2026-11-18-etoile-en-images/lecture/verifier.py
```
