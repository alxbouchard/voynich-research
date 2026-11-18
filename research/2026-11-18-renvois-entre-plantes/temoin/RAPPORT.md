# Prédire un terme entre deux herbiers latins

Une plante identifiée dans les deux ouvrages permet-elle de prédire un mot de sa notice avant de lire celle-ci ? Sur sept plantes, le premier degré médicinal a été annoncé cinq fois. Deux valeurs numériques correspondent, dont une seule avec la même forme latine. Aucune des sept annonces anatomiques ne se retrouve dans les quarante premiers mots de la notice correspondante. Les résultats portent sur deux rédactions différentes et sept paires. [Annonces fixées avant lecture](ANNONCES.json) · [Photographies de trois comparaisons](lectures-sur-images.jpg) · [Photographies des sept notices cibles](sept-notices-mayence.jpg)

## Ce que l’on peut lire

- **Absinthe.** Le manuscrit italien de 1478, f. 1v, donne la chaleur au premier degré et le pouvoir desséchant au second. À Mayence en 1484, le chapitre I s’ouvre également sur *calidum in primo gradu et siccum in secundo*. La prédiction *primo* est exacte. Toutefois *primo* ouvre aussi les degrés de l’aurone et de l’ache.
- **Aurone.** Quelques lignes plus haut sur le même f. 1v, le Macer donne le troisième degré de chaleur à l’aurone. Le chapitre II de Mayence lui attribue le premier degré de chaleur et le second de sécheresse. Les deux textes identifient la plante dans leur rubrique et divergent sur cette propriété.
- **Armoise.** Après dépouillement on reconnaît *herbarum matrem* dans le poème, aux positions 6 et 7, et *mater herbarum* dans l’imprimé, aux positions 13 et 14. Cette expression signifie « mère des herbes ». Dans ces deux ordres et ces deux formes, elle est propre à l’armoise parmi les 77 notices du Macer et les sept débuts du second ouvrage. Cet exemple, découvert après lecture, montre une épithète précise transmise avec variation de cas et d’ordre. Les sources ont pu hériter d’une tradition commune. [Folio de 1478](https://wellcomecollection.org/works/cfqd658f) · [Chapitre XII de 1484](https://www.digitale-sammlungen.de/en/view/bsb00027407?page=35) · [Détails photographiques](lectures-sur-images.jpg)

| Plante | Premier degré annoncé | Première valeur lue | Organe ou terme anatomique annoncé |
|---|---|---|---|
| Absinthe | 1, *primo* | 1, *primo* | *aures* |
| Aurone | 3, *tertius* | 1, *primo* | *nervos* |
| Guimauve | abstention | aucun degré numéroté dans les 40 mots | *nervos* |
| Ail | 4, *quarto* | 3, *tercio*, puis une borne à 4 | *pulmonis* |
| Aneth | 2, *secundus* | 2, *secundum*, borne d’un intervalle | *intestinorum* |
| Ache | 3, *tertius* | 1, *primo*, puis autre avis citant 3 | *splen* |
| Armoise | abstention | 3, *tercio* | *matrix* |

## Ce que les autres plantes permettent d’évaluer

Sept notices donnent exactement 5 040 façons de réattribuer les prédictions. Quand on conserve le critère du premier nombre, 1 668 réattributions égalent ou dépassent les deux succès observés. Pour la forme de l’ordinal, 2 160 égalent ou dépassent l’unique succès. Accepter un degré cité n’importe où dans la fenêtre donne quatre succès sur cinq, mais 712 réattributions en obtiennent autant ou davantage. Cette tolérance rapproche aussi des déclarations différentes, comme la borne supérieure pour l’ail et l’avis d’une seconde autorité pour l’ache. La forme moderne « céleri » recouvre ici le nom historique *Apium*, sans identification à l’espèce.

Le contrôle anatomique compare aussi les flexions. Aucun résultat sur sept dans la fenêtre fixée ; la photographie de la guimauve porte toutefois *ulceribus nervorum* un peu plus loin. Ainsi la longueur de l’extrait change la capacité de retrouver un terme réellement attesté. La fréquence élevée d’une formule médicale limite également sa capacité à identifier une plante particulière. [Débuts de notices et expansions](TRANSCRIPTION.json) · [Toutes les confrontations et permutations](RESULTATS.json)

## Sources et reproduction

Le texte de départ est une édition du poème médical *De viribus herbarum*, rédigé plusieurs siècles avant 1478. Le calcul emploie les 77 notices de l’édition et les photographies établissent les lectures de trois passages de la copie italienne sur les feuillets 1r et 1v. Les sept notices de la cible ont toutes été lues sur les images de l’*Herbarius* latin imprimé par Peter Schöffer, Mayence, 1484. Les deux textes diffèrent par leur rédaction, en vers et en prose. La parenté des traditions médicales empêche de présumer une indépendance de contenu. Les rubriques latines ont permis d’apparier les plantes avant lecture et le programme ne s’en sert pas pour annoncer les mots. Le projet avait déjà examiné certains chapitres pour d’autres questions. [Corpus, édition et variantes](../../2026-11-18-opcheor-paralleles/latin/SOURCE.md) · [Wellcome Collection, MS.458](https://wellcomecollection.org/works/cfqd658f) · [Bayerische Staatsbibliothek](https://www.digitale-sammlungen.de/en/view/bsb00027407?page=7) · [Images primaires, coordonnées et empreintes](SOURCES.json)

La transcription normalise la casse, développe les abréviations et écrit *et* pour le signe de conjonction. La dernière forme retenue à la vue 31 (graisse de porc dans la suite) est graphiquement incertaine. Les degrés sont classés dans leur phrase pour distinguer une qualité médicale de « selon [tel auteur] ». Le résultat sur la graphie compare les mots après développement des abréviations. La comparaison ignore les titres, la position du mot dans la page illustrée et les mots extérieurs à la fenêtre choisie. [Règles avant lecture](AVANT.md)

Depuis ce dossier, exécuter `python3 comparer.py annoncer`, puis `python3 comparer.py verifier`. L’empreinte SHA-256 du fichier des annonces enregistrée avant l’ouverture des cibles est `3b82535c305a08992ce7830ad7264448fb46e4c8d49732726a5415e071cfa4ad`.
