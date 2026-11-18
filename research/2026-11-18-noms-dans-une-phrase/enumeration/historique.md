# Après « et » et un ingrédient, quel mot vient ensuite ?

Dans le livre de cuisine copié à Bolzano, on lit bien des listes comme « et aneth et oignon ». Pourtant, lorsque le premier mot X de la suite *et X et Y* désigne une matière culinaire, **le deuxième mot Y en désigne une dans 28 cas sur 59**. Dans 26 de ces 59 cas, les deux matières appartiennent effectivement à la même énumération. La phrase et le rôle grammatical des mots permettent de faire cette distinction. [Annotation des 90 fenêtres](annotation.tsv) · [Formes et repères extraits du texte](RESULTATS.json.gz)

## Deux lectures sur le même feuillet

La recette 12 du *Liber de coquina*, dans le manuscrit Vatican, Pal. lat. 1768, explique comment préparer des légumes hachés. L’instruction commence par une liste. En français, « prends du persil, du fenouil, de l’aneth et de l’oignon, puis hache fermement le tout au couteau sur une planche propre ». Dans la transcription de Francesca Cupelloni, la suite centrale est *feniculum et anetum et cepe et percute fortiter*. Sur la photographie du f. 161r, ces mots se suivent, près de la grande initiale. La fin d’*anetum* est abrégée et l’impératif *percute* apparaît à la ligne suivante. Une fenêtre de quatre mots donne donc deux matières, *anetum* et *cepe*. En commençant deux mots plus loin, au deuxième *et*, elle donne un ingrédient et une action, *cepe* et *percute*. [Édition AtLiTeG, f. 161r](https://corpus.atliteg.org/testi/liber-de-coquina-o/92?p=161r) · [Photographie du manuscrit, f. 161r](https://digi.vatlib.it/view/MSS_Pal.lat.1768/0339)

La recette 27 prescrit de cuire des pois chiches cassés avec de l’huile, du poivre et du safran, puis avec du fromage en morceaux. Dans *et pipere et zafrano*, les deux noms d’ingrédients sont à l’ablatif sous la dépendance de *cum*, placé avant l’huile. La fenêtre chevauchante qui commence deux mots plus loin donne *et zafrano et cum*. Le fromage appartient toujours à la liste, mais la quatrième place contient la préposition qui introduit le fromage. À la recette 99, après les instructions de cuisson, *et colora et assapora* demande au cuisinier de colorer puis d’assaisonner à son goût. [Édition AtLiTeG, f. 163r](https://corpus.atliteg.org/testi/liber-de-coquina-o/92?p=163r) · [f. 177v](https://corpus.atliteg.org/testi/liber-de-coquina-o/92?p=177v)

## Comment les mots ont été classés

Une lecture par un agent IA a coté **toutes** les fenêtres littérales du programme, soit 85 dans les 168 recettes numérotées du livre de cuisine et 5 dans les vers du *Macer*. Le lecteur disposait de la phrase et de la rubrique. Le *Macer* est segmenté par vers et la cuisine par recette et face. À l’intérieur de ces limites, la fenêtre peut chevaucher une ponctuation ou une autre fenêtre. La cotation qualifie le mot écrit à chaque position, sans lui substituer le mot voisin. Les exemples et les décisions ont été relevés après le calcul. L’édition du texte culinaire date le manuscrit de 1461–1465. La seule lecture sur le feuillet original pour cette vérification est celle de la recette 12. [Édition du livre de cuisine](https://corpus.atliteg.org/opera/liber-de-coquina-o/92) · [Protocole](PREDICTION.md) · [Programme](enumerer.py)

- **M**, matière. Un mot nomme une substance, un aliment ou un animal consommé dans la préparation. Cela comprend les termes collectifs comme les épices et la poudre de gingembre. *Cigno*, le cygne pour lequel on prépare une sauce, entre dans cette catégorie.
- **A**, action. Le mot exprime une opération, un ordre ou le résultat d’une opération sous forme de participe. Des carottes dites bouillies relèvent ici de l’action ; le nom des carottes désignerait l’aliment.
- **O**, autre. On y trouve notamment prépositions, adjectifs de qualité, parties anatomiques mentionnées à un autre titre, patients, symptômes et maladies. Dans la recette 79, *pedum* (« des pattes ») précise les extrémités laissées en place lorsque la viande est détachée. Il a été coté O. En le comptant comme matière animale, on obtiendrait 29/60 au lieu de 28/59, sans ajouter de matières coordonnées.
- **I**, indéterminé. Aucun mot n’a exigé cette classe pour trancher la seule question « matière, action ou autre ». La plante précise peut demeurer inconnue. Ainsi, dans la recette 49, *aciorum* dépend de « racines » dans une liste de végétaux à préparer.

| Ouvrage | Toutes les fenêtres | X matière | Parmi les X matières, Y matière | Y action | Y autre | X et Y matières coordonnées |
|---|---:|---:|---:|---:|---:|---:|
| *Liber de coquina* | 85 | 59 | 28/59 | 21/59 | 10/59 | 26/59 |
| *Macer*, toutes les notices | 5 | 1 | 1/1 | 0/1 | 0/1 | 1/1 |

À Bolzano, deux fenêtres réunissent deux ingrédients dont le rôle grammatical change. Dans la recette 69, les poulets sont revenus avec lard et oignons, puis les amandes pelées sont broyées. Dans la recette 148, une première phrase de l’édition demande de faire bouillir le vin avec les épices et le sucre. La phrase suivante demande d’y faire bouillir les sardines ou les harengs. *Zucaro* puis *sardelle* désignent bien deux aliments, mais le second est sujet d’une nouvelle instruction. Cette distinction explique la différence entre 28 et 26. Les fenêtres qui se recouvrent ou proviennent de la même recette ne constituent pas des essais indépendants. [Recette 69, f. 170r](https://corpus.atliteg.org/testi/liber-de-coquina-o/92?p=170r) · [Recette 148, f. 188v](https://corpus.atliteg.org/testi/liber-de-coquina-o/92?p=188v)

Dans le relevé, la dernière colonne indique si deux matières sont coordonnées dans une même liste. Elle porte la mention « sans objet » lorsqu’au moins un des deux mots désigne autre chose.

## Les cinq passages du Macer

Dans l’herbier latin médiéval, on peut préciser le sens de chacune des cinq suites survenues dans un même vers. Les chiffres ci-dessous renvoient à la numérotation continue des vers de l’édition de Baudet, dont le projet conserve la transcription figée. Les traductions sont celles de cette étude. [Édition latine](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&oldid=272959) · [Texte, édition et transmission](../../2026-11-18-noms-dans-les-notices/historique/README.md)

| Notice et vers | X, Y | Lecture de la proposition |
|---|---|---|
| III, absinthe, v. 65 | *nardus*, *acetum* | Si l’on y ajoute du *siler*, du nard et du vinaigre, poursuit le poète, cette boisson dissipera les nausées. Nard et vinaigre sont bien deux matières ajoutées. L’identification botanique du *siler* est laissée ouverte. |
| IV, ortie, v. 128 | *cancros*, *parotidas* | Le sujet est le cataplasme. Le texte lui attribue un effet sur des lésions cancéreuses et des tuméfactions de la région des oreilles, puis sur les luxations. Les deux mots de la fenêtre désignent des maux. |
| XXI, rose, v. 793 | *dolor*, *fervor* | Le passage annonce qu’avec ce remède on traitera la douleur et la chaleur de la tête. Ce sont deux symptômes. |
| XLIII, iris, v. 1472 | *contractis*, *frigore* | Prise avec du vin, la poudre doit traiter, entre autres, ceux qui souffrent de contractures et ceux que le froid a atteints. *Frigore* exprime la cause de l’atteinte et dépend du mot suivant, *laesis*. |
| LVIII, verveine, v. 1889 | *vitiis*, *praecipue* | Le texte énumère les affections, entre autres celles de la poitrine, puis précise que la plante serait « surtout » salutaire dans les affections pulmonaires. La quatrième place contient un adverbe. |

La cuisine fournit donc un exemple vérifié de ce qu’on pourrait chercher dans le Voynich et une mesure de sa fiabilité dans l’ouvrage de comparaison. Même lorsqu’on connaît déjà la conjonction et le premier ingrédient, le mot suivant peut introduire une instruction ou une préposition. Le seul cas de matière dans le *Macer* est trop isolé pour estimer une fréquence générale. [Annotation détaillée, avec l’emplacement du premier « et »](annotation.tsv)
