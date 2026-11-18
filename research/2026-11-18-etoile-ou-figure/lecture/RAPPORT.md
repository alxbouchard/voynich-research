# Que lirait-on autour de otedy si le mot désignait une étoile ou une figure ?

**L’essai a livré huit emplacements avec un voisin entier prédit. Le parchemin donne un mot différent aux huit.** Sur f103v.27, par exemple, les deux éditions donnent `lpar otedy qotar`. Avec `otedy` pour *stella*, le début peut se lire *quarta stella*, « la quatrième étoile ». Dans le traité d’Hygin, le troisième mot est *est*. Les valeurs apprises sur les deux premiers mots imposent alors `eot` pour *est*. La graphie réellement écrite, `qotar`, élimine cette lecture de la phrase. Trois autres interprétations compatibles avec son début échouent au même endroit. [Agrandissement de f103v.27](f103v-27.jpg) · [Détail du feuillet, Yale](https://collections.library.yale.edu/iiif/2/1006255/1706,1682,521,150/full/0/default.jpg) · [Graphies annoncées vers la droite](ANNONCES-droite.json)

L’exemple latin existe dans un livre imprimé au XVe siècle. Au f. 22v de l’édition vénitienne de 1482, on lit *Quarta stella ē* en fin de ligne, puis *Veneris Lucifer nomine*. La barre sur e abrège *est*. L’auteur évoque Vénus, ici sous le nom de Lucifer, l’astre du matin. Le calcul utilise les graphies développées de l’édition numérique. Il n’éprouve pas un code particulier de Vénus ni toutes les formes d’abréviation médiévales. [Détail de l’édition de 1482](hygin-1482-quarta.jpg) · [Folio complet, Bayerische Staatsbibliothek](https://api.digitale-sammlungen.de/iiif/image/v2/bsb00054123_00050/full/full/0/default.jpg) · [Hygin, livre II](https://www.thelatinlibrary.com/hyginus/hyginus2.shtml)

## De la figure avec étoile à la prose

Sur f73v.23, `otedy` figure près de la tête d’un personnage muni d’une étoile. Pour essayer de le lire, nous avons assigné à chacune de ses cinq unités EVA une ou deux lettres latines de suite. Les valeurs sont fixes et distinctes, et le même système s’applique ensuite aux voisins. Les choix latins avaient été fixés avant le dépouillement. Les 21 721 mots du témoin sont ceux qui restent dans les quatre livres après exclusion des titres en gras et des nombres romains en majuscules. La ponctuation sépare les contextes. Une graphie au singulier représente ici une hypothèse de lecture précise. Les pluriels et les cas obliques sortent du test. [Protocole](PROTOCOLE.md) · [Les huit mots, toutes les clés, lieux et empreintes](HYGIN.json) · [Légende de départ dans la roue](../../2026-11-18-du-dessin-au-paragraphe/NOMS-ET-IMAGES.md)

| Hypothèse nominative pour otedy | Tables possibles | Emplois exacts dans le corps du texte d’Hygin |
|---|---:|---:|
| *stella*, étoile | 3 | 25 |
| *sidus*, astre | 0 | 3 |
| *astrum*, astre | 5 | 0 |
| *femina*, femme | 5 | 0 |
| *mulier*, femme | 5 | 0 |
| *nympha*, nymphe | 5 | 1 |
| *figura*, forme ou figure | 5 | 5 |
| *virgo*, jeune fille ou Vierge | 1 | 6 |

Dans *sidus*, les lettres initiale et finale sont identiques. Comme les cinq signes de `otedy` sont tous différents et que le mot latin compte cinq lettres, l’injectivité l’exclut. Une autre représentation, avec homophones, changerait cette contrainte. En sens inverse, reconnaître des paires de mots une fois les valeurs ajustées est assez facile. Sur les 90 places où les deux voisins sont concordants, le mot de gauche a permis un ajustement chez Hygin à 17 places et celui de droite à 11 places. Nous avons demandé au mot restant, entièrement caché pour ce sens du test, de départager les interprétations.

| Sens du déchiffrement | Lieux avec ancre concordante | Deux voisins utilisables | Avec annonce | Sans annonce parmi les 90 | Annonces exactes |
|---|---:|---:|---:|---:|---:|
| Prédire à droite avec le mot de gauche | 122 | 90 | 3 | 87 | 0 |
| Prédire à gauche avec le mot de droite | 122 | 90 | 5 | 85 | 0 |

Les deux sens réutilisent les mêmes 90 fenêtres. Trois hypothèses ordinales (*quarta*, *quinta* ou *secunda stella*) et *enim stella* autorisaient `eot` ou `lt` sur f103v.27 ; aucune de ces deux graphies n’y apparaît. Les autres réponses strictement prédites vers la droite étaient `et` sur f108r.48 et `eot` sur f116r.20. Le manuscrit donne respectivement `qokedy` et `qoty`. À gauche de `otedy`, f46v.2 pouvait porter `y`, `eot` ou `osy` et donne `oldy`. Aux quatre autres places qui appelaient `eot` (f76r.41, f78v.8, f106r.43 et f111v.11), les réponses sont `shckhy`, `qokedy`, `daiin` et `otain`. Même en permettant rétrospectivement des valeurs nouvelles au troisième mot, aucune fenêtre entière ne s’ajuste à un trigramme d’Hygin avec ces ancres. Ces exclusions concernent des formulations attestées chez un seul auteur, dont les usages de *stella* sont beaucoup plus nombreux que ceux des autres mots proposés. [Annonces vers la gauche](ANNONCES-gauche.json) · [Les 122 lieux et les mots effectivement présents](VERIFICATION.json.gz)

## Ce que le test peut retrouver

Sur la vraie suite *quarta stella est*, une substitution secrète d’une lettre par signe permet de retrouver exactement le mot caché *est*, avec une seule proposition. Cette calibration prévue ne reproduit pas la longueur de l'ancre Voynich. Une seconde vérification, ajoutée après les résultats et prenant la même phrase, reproduit la structure graphique de l’essai. Nous avons codé *stella* en `otedy`, avec le double l porté par d. En donnant seulement `chpykty otedy`, l’interprétation *stella* et le texte d’Hygin au programme, celui-ci annonce uniquement `eot`. C’est bien l’encodage secret du troisième mot *est*. La démonstration établit la possibilité d’un succès lorsque cette clé est la bonne. [Recodage, annonce et réponse](CALIBRATION.json)

Dans toute la prose, hors de `otedy`, 46 paires de mots de suite (43 paires distinctes) sont composées uniquement de ses cinq signes et concordent entre les transcriptions. Aucune des 29 tables ne produit de paire de mots contigus attestée chez Hygin, et aucune permutation ne fait mieux. Le pouvoir de cette comparaison est limité. Sur ces 29 tables, huit seulement peuvent écrire ne serait-ce qu’une paire du témoin, et le contrôle retrouve une paire recodée pour chacune des huit. Pour *stella* les trois possibilités écrivent respectivement 8, 16 et 0 paires latines. [Détail des tables, des 120 permutations par table et des contrôles d’injection](VERIFICATION.json.gz)

## Reproduction

Télécharger les quatre pages HTML dans le même dossier sous les noms `voy-hyginus-latin1.shtml` à `voy-hyginus-latin4.shtml`. Le calcul vérifie leurs empreintes avant ouverture. Les annonces relatives à un sens sont calculées exclusivement à partir du fichier où seul le voisin opposé est visible. Les deux sens constituent des épreuves liées. Le fichier de résultats donne les unités EVA sous forme de listes pour préserver les glyphes composés. [Livre I](https://www.thelatinlibrary.com/hyginus/hyginus1.shtml) · [Livre II](https://www.thelatinlibrary.com/hyginus/hyginus2.shtml) · [Livre III](https://www.thelatinlibrary.com/hyginus/hyginus3.shtml) · [Livre IV](https://www.thelatinlibrary.com/hyginus/hyginus4.shtml)

```sh
python3 -B comparer_hygin.py latin /chemin/du/cache
python3 -B comparer_hygin.py annoncer
python3 -B comparer_hygin.py verifier /chemin/du/cache
python3 -B calibrer.py
```

Le détail de f103v.27 provient du cliché Yale 1006255, rectangle natif (1706,1682)–(2227,1832), agrandi à 870 pixels de largeur. Les coordonnées sont issues du recalage du visualiseur sur 2 874 correspondances avec un écart résiduel au 95ᵉ centile de 4,0 pixels, puis d’une inspection de l’image. Le détail de l’édition de 1482 provient du rectangle BSB (650,1690) de taille 1870 × 324. [Carte des mots f103v](https://www.voynichese.com/2/data/folio/script/f103v.js) · [Extrait historique original](https://api.digitale-sammlungen.de/iiif/image/v2/bsb00054123_00050/650,1690,1870,324/1450,/0/default.jpg)
