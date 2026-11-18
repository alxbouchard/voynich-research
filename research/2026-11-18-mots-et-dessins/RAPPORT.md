# Le texte décrit-il les dessins du Voynich ?

**Le vocabulaire aide à distinguer les pages de plantes des pages de bains. Le siège de cet effet reste incertain, car toutes les pages de bains viennent du même cahier.** À l'échelle d'une inscription, nous avons fixé le groupe `okol` en étudiant deux feuillets botaniques, puis l'avons retrouvé sur un troisième. À cet endroit, l'inscription se trouve entre deux dessins végétaux. Nous ignorons encore quel élément elle désigne. [Photographie du troisième emplacement](photos_okol/f101v.10-detail.jpg)

## Reconnaître une page dont on ne voit que le texte

Nous avons pris 18 feuillets portant des plantes ou des bains, tous attribués à la même main de scribe et à la variété B de Currier. Sur neuf d'entre eux, un programme a compté les mots des 40 premiers emplacements de prose ordinaire. Pour chacun des neuf autres, il a reçu l'extrait de texte sans illustration, et a proposé la section d’après les mots rencontrés à l'apprentissage. Le modèle n'utilise ni les légendes, ni le numéro, ni la longueur du feuillet. Pour ce petit lot, répondre toujours « herbier » réussirait 5 fois sur 9. [Protocole](prose/PROTOCOLE.md) · [Prédictions individuelles](prose/PREDICTIONS.json)

| Comparaison | Takahashi | Zandbergen–Landini, espaces incertains joints | Zandbergen–Landini, espaces incertains séparés |
|---|---:|---:|---:|
| Partage initial par feuillets physiques | 9/9 | 8/9 | 9/9 |
| Après exclusion, pour chaque cible, de l’autre moitié de la même feuille de parchemin | 7/9 | 7/9 | 8/9 |

Huit feuillets de l'épreuve initiale avaient l'autre moitié de leur feuille de parchemin dans le lot d'apprentissage. Le second calcul, ajouté après ce constat, renseigne mieux sur la généralisation. Si l'on réattribue les catégories au hasard et que l'on refait l'apprentissage, un score au moins aussi élevé dans ce second calcul survient dans 10,1 %, 9,5 % ou 2,1 % des répartitions respectives. Les trois colonnes portent sur les mêmes feuillets. Comme tous les bains proviennent d'un seul cahier, le changement de sujet reste confondu avec les habitudes propres à ce cahier. [Résultats, feuillets mal classés et détail des permutations](prose/RAPPORT.md)

## Un mot générique répété près des dessins ?

Les catégories des éditeurs identifient l'objet proche de l'inscription. Nous avons appris une forme par catégorie, au besoin avec abstention, puis l'avons cherchée sur d'autres feuillets physiques. L'analyse principale retient les emplacements dont les deux translittérations donnent exactement les mêmes mots entiers avec les espaces incertains joints. Une forme avec deux occurrences au moins dans des emplacements distincts était nécessaire pour pouvoir la proposer. Les nombres ci-dessous se rapportent aux emplacements IVTFF, dont certains peuvent faire partie d'une légende sur plusieurs lignes. [Critères enregistrés](PROTOCOLE.md) · [Formes fixées avant le contrôle](PREDICTIONS.json) · [Spécification des emplacements, tableau 9](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf)

| Dessin près de l'inscription | Forme retenue | Épreuve sur les autres feuillets | Mot entier le plus répandu, même en choisissant après coup dans les deux lots |
|---|---|---|---|
| Étoile | Aucune des formes des 8 emplacements d'apprentissage concordants ne se répète | Abstention, 45 emplacements de contrôle concordants | 1 sur 53. En lecture Takahashi seule, `dchol` atteint 2 sur 76. Les quatre panneaux proviennent de deux feuillets physiques au total. |
| Figure humaine dans les bains | Aucune forme répétée dans les 21 emplacements d'apprentissage concordants | Abstention, 20 emplacements de contrôle concordants | 2 sur 41, pour `otedy` et `otoly`. Dans Takahashi seul, `dal` revient 3 fois à l'apprentissage puis 0 fois sur 28 emplacements réservés. |
| Fragment végétal | `okol`, sur f88 et f89 | 1 sur 93 emplacements concordants, à f101v.10 | 3 sur 136, pour `okol` et `otoldy`. |

Le seul succès prédictif porte sur un fragment végétal. Les deux lectures concordantes donnent `okol` à f88r.15, `okol.shol.dy` à f89r2.10 et `okol` à f101v.10. Sur ce dernier feuillet, le mot est entre une grande feuille arrondie et trois feuilles dentelées. On le trouve aussi dans la prose des bains, par exemple f77v.42 dans les deux transcriptions. À f89r2.10, d'autres transcripteurs lisent `otol`. Même le choix du meilleur mot végétal change avec certains espaces incertains. [Trois inscriptions sur les photographies](photos_okol/NOTE.md) · [Présence dans la prose du manuscrit](OKOL_DANS_LA_PROSE.json)

Dans la réserve, six légendes de récipients sont intégralement concordantes sur les faces qui portent aussi un fragment végétal. Aucune ne contient `okol`. Sur ces mêmes faces, aucune des 60 inscriptions végétales concordantes ne contient le mot non plus. L'unique occurrence se trouve sur une face où les transcriptions n'indiquent aucune légende de récipient. La proportion de bonnes réponses parmi les prédictions émises ne donne donc pas une mesure fiable de spécificité. Les petites figures du zodiaque portant une étoile sont classées à part par les éditeurs et ne portent pas d'indication sûre de la chose nommée. [Toutes les conventions de lecture et les témoins locaux](RESULTATS.json) · [Exemple du zodiaque](https://www.voynich.nu/q10/index.html#f70v2)

## Chercher expressément le mot « racine »

Les trois premières rangées de f99r et de f99v montrent surtout des racines. Sur 28 légendes du recto, deux groupes reviennent chacun dans deux légendes chez Takahashi, `oky` et `okary`. Aucun des deux ne figure dans les 20 légendes correspondantes du verso. Les deux transcriptions confirment l'absence au verso et la répétition de `oky` au recto. `otoldy`, en revanche, figure une fois de chaque côté. Le tracé du dessin laisse parfois une hésitation entre la racine, la feuille et la plante entière. L'analyse par rangées a été ajoutée pour éviter de trancher artificiellement ces attributions. [Deux faces du feuillet et planche de feuilles](racines/PLANCHE.jpg) · [Comptages par rangée](racines/NOTE.md)

Dans les paragraphes immédiatement sous ces rangées, `sheol` apparaît dans les trois paragraphes du recto et dans aucun des trois au verso, bien que les deux faces montrent principalement des racines. Aucun mot entier lisible n'est commun aux six paragraphes dans l'une ou l'autre transcription. Cette observation concerne six petits passages d'un seul feuillet. Un texte peut décrire des usages ou des plantes différentes et varier son vocabulaire. [Résultats par paragraphe](racines/PROSE.json)

## Comment un auteur du XVe siècle procède sur une page lisible

Dans le *Gart der Gesundheit* de 1485, dix des douze premiers chapitres numérotés portent une plante sur la page du titre. Les dix titres donnent un nom particulier. Sur quatre de ces dix pages, un terme signifiant « herbe » apparaît dans les 24 premiers mots du paragraphe. Ainsi, le chapitre V porte le titre *Agrimonia* et dit ensuite *diß krut*, « cette herbe ». C'est un exemple historique précis de deux usages différents sur la même page. [Chapitre V à Munich](https://www.digitale-sammlungen.de/view/bsb00032739?page=22) · [Photo de l’inscription et de la phrase](herbier_1485/agrimonia-titre-texte.jpg) · [Contrôle historique](herbier_1485/NOTE.md)

Pour avancer vers une lecture, le test le plus discriminant serait désormais **à l'intérieur d'un même cahier**. Des lecteurs qui ne voient que les dessins pourraient classer, par exemple, les plantes portant une fleur clairement dessinée et celles où seules des feuilles sont visibles. Un autre lecteur, privé des images, essaierait de prédire ce détail à partir de la prose sur des feuillets réservés. Une forme qui y réussirait serait une candidate à vérifier dans d'autres manuscrits et contextes. Ce test demanderait d'abord de vérifier que les deux sortes de dessins sont suffisamment représentées.

[Instructions de reproduction](REPRODUCTION.md)
