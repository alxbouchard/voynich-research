# Lecture de paires chiffrées dans un poème de bains connu

**Sur 33 notices choisies par position, les deux premiers mots du vers 1 identifient une seule expression latine dans 19 cas.** Leur clé suffit à lire les deux premiers mots du vers 2 dans 2 notices et ceux du vers 3 dans 1 notice. Dans les 63 autres transferts, au moins un signe manque à la clé. Si le lecteur peut chercher de nouvelles correspondances dans le poème dont le texte chiffré a été tiré, les 66 transferts lui rendent chacun une seule expression, qui est la bonne.

Le moteur reçoit des signes anonymes et leurs deux frontières de mots. Il cherche parmi **2 035 expressions distinctes, attestées à 2 137 positions dans 414 vers** de Pierre d’Éboli. Il ignore la clé, la notice, le vers et la position. L’expérimentateur conserve ces renseignements pour le décompte. La clé secrète pour le moteur est une permutation différente pour chaque pièce. Elle reste constante pour les trois paires de cette pièce, et sa génération est reproductible. [Règles enregistrées](PROTOCOLE.md) · [Source de l’édition et empreinte](../SOURCE.json)

| Mesure sur les 33 notices | Vers 1, amorce | Vers 2, transfert | Vers 3, transfert |
|---|---:|---:|---:|
| Expression et emplacement exacts seuls à l’amorce | 19/33 | — | — |
| Vraie expression comprise dans les possibilités de l’amorce | 33/33 | — | — |
| Tous les signes du transfert déjà couverts | — | 2/33 | 1/33 |
| Expression exacte entièrement lue, seule réponse à clé fixe parmi les paires du livre | — | 2/33 | 1/33 |
| Expression exacte seule avec possibilité de prolonger la clé | — | 33/33 | 33/33 |

Les 14 amorces ambiguës admettent de 2 à 8 expressions distinctes. Chaque transfert est évalué en repartant de l’amorce. Les deux observations d’une notice partagent donc leurs signes initiaux. Le prologue, compté séparément, fournit une amorce unique, deux transferts à couverture insuffisante et deux lectures exactes en prolongeant la clé.

### Quand la clé suffit

Dans la notice II, l’amorce `mollificat nervos` suffit pour lire `cessat in` au vers 2. Dans la notice XI, `ascribunt homines` suffit pour lire `usibus humanis` au vers 2. Dans la notice VIII, huit expressions conviennent à la première paire, parmi elles `cui petra`. Lorsqu’on applique les huit clés à la troisième paire chiffrée, une seule produit une expression du livre, `et caput`. Le deuxième couple de cette notice, `quod lapidem`, demande des signes supplémentaires. [Résultats détaillés](mesures.json)

Une vérification distincte retient, dans chaque notice, la première expression ultérieure dont toutes les lettres sont déjà présentes dans l’amorce. Seules 14 notices sur 33 offrent un tel cas. Le moteur lit la bonne expression comme seule réponse dans les 14. La sélection sur la couverture explique pourquoi ce résultat dépasse les trois succès de l’échantillon fixé par numéro de vers. Ces échantillons se recoupent.

### Effet d’un signe altéré

Lorsque le premier signe de chaque paire réservée est remplacé par le premier autre signe de la même paire, aucune des 66 paires modifiées n’offre une lecture, même par extension. Lorsque la même modification vise l’amorce seule, aucune des 33 amorces ne correspond encore à une expression du livre. Cette perturbation impose souvent deux signes identiques au début.

Un contrôle complémentaire échange partout les valeurs de deux signes dans la paire réservée. Il conserve sa longueur et toutes ses répétitions internes. Avec la première table inchangée, aucune lecture intégrale ne subsiste. Avec une extension, la vraie expression reste compatible dans **4/33** deuxièmes vers et **7/33** troisièmes vers. La clé partielle n’impose pas assez de contraintes pour repérer les 11 perturbations. Dans ces essais, chaque réponse qui survit est la seule du livre. [Règles complémentaires](COMPLEMENT.md) · [Résultats des échanges](mesures-complement.json)

### Bain XVI, « adibis aquas » puis « aquas aqua »

Ces deux expressions occupent les mots 4–5 du vers 8 et les mots 3–4 du vers 11. Le contrôle a été construit pour que toutes les lettres de la cible se trouvent déjà dans l’amorce. Le mot `aquas` est partagé. Dans le chiffre où chaque signe représente une seule lettre latine et chaque lettre a son signe, la première paire identifie `adibis aquas` à une seule position. La seconde se déchiffre intégralement en `aquas aqua`. [Bain XVI, édition Monumenta](https://monumenta.ch/latein/text.php?tabelle=Petrus_de_Ebulo&rumpfid=Petrus%20de%20Ebulo,%20De%20Balneis%20Puteolanis,%20%20016&level=3&domain=&lang=0&links=&inframe=1&links=1&hide_apparatus=)

L’ambiguïté apparaît lorsque l’on refait l’essai selon la règle plus souple réellement envisagée pour f75v. Après omission du signe introductif et dans l’ordre haut-bas fixé, le moteur reçoit `l·k·ch·y / t·o·l·y`. Chaque signe peut représenter une ou deux lettres, et plusieurs signes peuvent représenter la même suite. L’amorce admet alors **quatre expressions et neuf tables**. Le contrôle lui soumet ensuite une seconde paire fabriquée, `t·o·l·y / t·o·l`, entièrement composée de signes connus.

| Lecture possible de l’amorce | Tables | Lecture correspondante du contrôle | Attestation comme paire du poème |
|---|---:|---|---|
| `lesis oculis` | 2 | `oculis ocul` | Aucune |
| `adibis aquas` | 2 | `aquas aqua` | XVI, vers 11 |
| `aquas alias` | 4 | `alias alia` | Aucune |
| `calet arcet` | 1 | `arcet arc` | Aucune |

Les deux tables survivantes lisent les signes successifs `t·o` comme `a·qu` ou `aq·u`. La seconde expression ne départage pas ces deux décompositions. Les signes de la seconde paire ont été fabriqués à partir du latin connu pour tester la méthode. Une occurrence historique d’une seconde légende devrait être vérifiée séparément sur le manuscrit.

### Portée et reproduction

La méthode est sensible à un transfert entièrement couvert. Le contrôle par position montre toutefois que le même auteur et le même livre n’en procurent ici que **3 sur 66** aux endroits imposés. L’échec d’un transfert à clé fixe devient plus informatif lorsqu’on sait combien de signes la première clé permet de lire. La réussite des prolongements est mesurée dans une bibliothèque qui contient par construction toutes les réponses. Ce taux ne permet pas d’identifier la langue du manuscrit.

Le calcul construit un index des répétitions indépendamment de la procédure de confrontation. Il compare le catalogue intégral des positions, les clés proposées, ainsi que les extensions compatibles au calcul utilisé pour f75v. Pour le contrôle à une ou deux lettres par signe, il compare également toutes les segmentations candidates à une énumération indépendante. Les vérifications concordent. [Calcul principal](calibrer.py) · [Calcul des contrôles complémentaires](complement.py)

Depuis le dossier `lecture/`, exécuter `python3 source.py /chemin/vers/le-cache` pour préparer les vers de l’édition. Depuis `lecture/etalon/`, exécuter `python3 calibrer.py /chemin/vers/le-cache` puis `python3 complement.py /chemin/vers/le-cache`. Les sorties standard reproduisent respectivement `mesures.json` et `mesures-complement.json`.
