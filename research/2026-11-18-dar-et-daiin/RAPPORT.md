# Peut-on prévoir le mot suivant à partir de deux racines dessinées ?

**Sur les autres feuillets, aucune des 58 suites lisibles ne donne le mot annoncé.** Les deux dessins de départ avaient permis de retrouver `dar` sur une deuxième grande plante. Cette séance teste une question plus précise. Si le scribe emploie une formule pour parler de ces plantes, peut-on reconnaître le mot qui vient ensuite, puis lire la formule en clair ? Les essais localisent la limite du rapprochement. Ils ne donnent encore aucun sens vérifié à `dar` ni à `daiin`. [Deux lignes et quatre dessins sur une planche](../2026-11-18-renvois-entre-plantes/composant/photos/deux-phrases.jpg)

## Ce que les dessins permettaient d’annoncer

Sur la septième ligne de f18v, les mots 4 à 6 sont `qokol daiin qokol`. Sur f23r, aux mêmes places, on lit `qokchol dar qokchol`. Les deux grandes plantes occupent le même côté d’un bifeuillet. Les petits dessins qui leur ressemblent se côtoient sur f102r2. Nous avons donc annoncé `daiin` après `qokol`, et `dar` après la forme qui contient le signe supplémentaire transcrit `ch`. Ces groupes désignent des tracés dans la transcription EVA. Leur prononciation est inconnue. [Rapport de la séance précédente](../2026-11-18-renvois-entre-plantes/RAPPORT.md) · [Protocole de la nouvelle prédiction](AVANT.md)

Pour cette épreuve, huit feuillets déjà consultés sont écartés du lot principal. Un voisin compte seulement si les deux éditions, chacune lue avec deux conventions d’espacement, donnent le même groupe sur la même ligne, sans coupure du dessin. Ces lectures portent sur le même manuscrit. Les pages ont pu servir à des études antérieures. [Annonces enregistrées](PREDICTIONS.json.gz) · [Réponses, absences et témoins par lieu](VOISINS.json.gz)

| Règle | Annonces | Voisins lisibles | Mots exacts | Succès attendus en redistribuant les voisins |
|---|---:|---:|---:|---:|
| Les deux groupes d’origine, autres feuillets | 68 | 58 | 0 | 1,06 |
| Mêmes groupes sur les quatre feuillets de comparaison déjà consultés | 17 | 15 | 4 | 2,61 |
| Règle élargie à 15 autres familles graphiques, lot principal | 333 | 277 | 13 | 11,80 |

Dans le lot principal, 54 voisins sont lisibles après `qokol` et seulement quatre après `qokchol`. Aucun des 58 n’est `dar` ni `daiin`. Les dix autres annonces restent indéterminées. Les quatre succès des pages déjà consultées concernent tous `qokol daiin`. Pour la règle élargie, 37,4 % des redistributions sur les mêmes faces et aux mêmes positions de fin ou d’intérieur de ligne atteignent au moins treize succès. Annoncer toujours `daiin` donnerait seize succès sur ces 277 positions. [Calcul reproductible](prevoir.py)

Le dessin de f14r fournit une autre vérification. La formule `qokchol dar` figure sur cette page et sur f23r. Les deux racines présentent des segments. Le détail annoncé sur f14r, trois colliers à double contour comme ceux de f23r, manque. L’autre caractéristique annoncée, l’absence d’une série de dents, est visible mais se rencontre aussi sur sept des huit faces témoins tranchées. Le lecteur avait déjà vu f14r. [Trois grandes plantes, dix témoins et critères de lecture](dessins/RAPPORT.md)

## La lecture latine et le mot qui la contredit

En comparant les deux lignes à sept corpus, six paires de passages chez Celse retrouvent le groupe `dar` à droite du premier triplet. Elles représentent cinq dictionnaires différents. Toutes feraient lire `qokol` comme *et* et `qokchol` comme *est*. Deux proposent notamment *linum* (« lin ») pour `daiin`. Cette proposition se teste sur la ligne même : `daiin` revient au dixième mot de f23r.7 et devrait y garder sa valeur. Dans les deux passages latins prolongés à l’intérieur du paragraphe, on trouve respectivement *et* et *haec*. Les quatre autres alignements contredisent également le mot annoncé. Avec la coupure stricte de phrase, trois cas contredisent la lecture et les trois autres s’arrêtent avant le mot de contrôle. [Six alignements, lectures concurrentes et dénominateurs](parallele/RAPPORT.md) · [Celse dans l’imprimé de 1478](parallele/celse/RAPPORT.md)

## Ce que montrent les témoins historiques

- **L’organe peut être nommé explicitement.** Sur le feuillet 3v de Gonville & Caius, une recette anglaise demande de prendre à la fois la feuille et la racine de la plante nommée *mowsere*. Les deux manuscrits de Cambridge apportent 4 497 mots répartis en 373 extraits de catalogue. Chaque extrait garde ses limites. Les quatre rapprochements graphiques qu’ils fournissent ne permettent aucune annonce en EVA pour le mot de contrôle. [Transcriptions et deux feuillets photographiés](cambridge/SOURCES.md) · [Résultats du test](parallele/OUVERTURE-cambridge.json.gz)
- **L’ingrédient peut rester le même alors que le geste change.** Dans l’herbier d’Ulm de 1487, la formule *mit wein* (« avec du vin ») se retrouve dans les deux notices annoncées. La cuisson attendue manque dans les deux. L’une prescrit de prendre la graine avec du vin, l’autre de piler l’herbe puis de la mélanger au vin. [Les trois préparations et leurs photographies](temoin/RAPPORT.md)
- **La répétition n’identifie pas à elle seule la fonction du mot central.** Dans les ouvrages connus, le centre d’une suite du type A–B–A peut être un nom, une préposition ou un coordonnant. Dans le Voynich, en cachant le centre et en excluant la face étudiée de l’apprentissage, la règle propose un mot à 41 des 173 emplacements et n’en retrouve aucun. [Contrôles grammaticaux, résultats par ouvrage et limites](grammaire/RAPPORT.md)

### Reproduire le résultat principal

Depuis ce dossier, lancer `python3 -B prevoir.py annoncer` puis `python3 -B prevoir.py ouvrir`. La première commande enregistre les positions et les mots annoncés. La seconde produit les comparaisons et la distribution qui sert de témoin. Les sept commits antérieurs à ce rapport conservent la chronologie des protocoles et des annonces. Chaque volet ci-dessus renvoie à ses données, à ses sources et à sa méthode.
