# « Racine » et « feuille » dans les légendes

J’ai examiné les photographies de trois faces. Sur f99r et f99v, les trois registres supérieurs montrent surtout des formes de racines isolées. Quelques dessins incluent aussi une feuille ou une tige. Sur f102v2, les deux rangs du haut comprennent surtout des fragments de feuilles. Les objets et les rangs ont été identifiés d’après les dessins et les notes du catalogue. Le format IVTFF leur attribue le même type de légende Lf (« fragment végétal »). [f99r](https://collections.library.yale.edu/iiif/2/1006246/full/full/0/default.jpg) · [f99v](https://collections.library.yale.edu/iiif/2/1006247/full/full/0/default.jpg) · [f102v2](https://collections.library.yale.edu/iiif/2/1006252/full/full/0/default.jpg) · [Trois photographies](PLANCHE.jpg)

**Aucun des mots entiers répétés au recto de la planche de racines ne se retrouve parmi les vingt légendes des mêmes registres au verso.** Exactement deux mots figurent dans deux légendes différentes de f99r dans la transcription Takahashi (H). Il s’agit de `oky` (f99r.4 et .24) et de `okary` (f99r.2 et .11). La transcription Zandbergen–Landini (ZL) confirme la répétition de `oky`, quel que soit le traitement des espaces incertains. Pour `okary`, elle la confirme seulement si on joint l’espace incertain. Les deux formes restent absentes du verso dans les deux lectures.

Quelques mots figurent une fois de chaque côté. Les deux transcriptions s’accordent sur `otoldy` (f99r.14 et f99v.2). ZL donne également `dar` de chaque côté. Leur rareté ne permet pas de donner à ces mots le sens de « racine ».

| Registres comptés | Toutes les légendes | Légendes avec au moins un mot entier lisible H / ZL | Maximum de légendes avec le même mot H / ZL |
|---|---:|---:|---:|
| f99r, trois registres dominés par les racines | 28 | 28 / 26 | 2 / 2 |
| f99v, trois registres dominés par les racines | 20 | 20 / 20 | 1 / 1 |
| f102v2, deux premiers rangs dominés par les feuilles | 14 | 12 / 11 | 1 / 1 |

Le recto et le verso appartiennent au même feuillet. Le lot des feuilles appartient à un autre feuillet. Les légendes peuvent nommer des plantes particulières, des préparations ou des propriétés. Les observations n'éprouvent ni les abréviations ni les phrases en prose.

## Choix des dénominateurs

Le protocole initial cherchait un mot présent dans au moins deux légendes de racines du recto, puis dans des légendes du verso. Il associait mécaniquement un commentaire « root » ou « leaf » du catalogue à la légende Lf suivante. Sur inspection, les descriptions de racines sont souvent intercalées entre deux légendes. La première méthode peut décaler une attribution. Ses résultats bruts sont conservés dans RESULTATS.json à seule fin d'audit. On ne peut pas en conclure que chaque légende comptée correspond au dessin précis du commentaire.

L'analyse par registres inclut tous les loci Lf situés entre les blocs de prose des trois rangées de f99r/v, ainsi que ceux des deux premiers rangs dessinés de f102v2. Elle élimine la décision concernant l'objet le plus proche de chaque mot et conserve toutes les étiquettes de ce voisinage. Les légendes de vase (Lc) et la prose (P0) sont exclues. La continuation f99r.7 est regroupée avec f99r.6. Chaque chaîne entière en minuscules EVA est comptée au plus une fois par légende. Les mots contenant des signes illisibles sont omis. Les deux traitements des espaces incertains sont calculés séparément. L'analyse a été ajustée après lecture des résultats du protocole initial. Deux graphies du lot étaient déjà connues d'un travail précédent. Ces pages ne constituent donc pas un corpus entièrement inédit.

Depuis le répertoire du dépôt, reproduire les données du rapport avec `python3 /chemin/vers/rangees.py .`. Le module compagnon compter.py doit se trouver à côté. Le fichier RANGEES.json contient les mots par emplacement et les quatre traitements.

## Et si le mot désignant la racine se trouvait dans la prose ?

Les trois petits paragraphes juste sous les trois registres riches en racines de f99r ont été comparés aux trois paragraphes correspondants de f99v. Les limites et la règle ont été écrites avant de lire leur contenu. Il s’agissait de prendre tous les mots présents dans chacun des trois paragraphes du recto, puis de regarder leur présence dans chacun des trois du verso. Les six blocs comprennent chacun 32 à 41 mots entiers lisibles en H.

Dans les deux transcriptions et avec les deux conventions d’espacement, `sheol` figure dans les trois paragraphes du recto et dans aucun des trois du verso. H donne aussi `daiin` dans les trois paragraphes du recto, puis dans un seul des trois au verso. Cette forme figure aussi dans le dernier paragraphe des deux faces, sous des dessins d'aspect différent. En ZL, `daiin` n'entre dans la liste des candidats que si on sépare les espaces incertains ; on retrouve alors le constat de H. Il n’y a aucun mot entier commun aux six paragraphes dans aucun des quatre traitements. Ces six petits blocs de longueur inégale se trouvent sur le même feuillet. Le résultat est compatible avec une description des propriétés de chaque plante dont le scribe varierait les termes.

[Protocole sur la prose](PROTOCOLE_PROSE.md) · [Comptages par paragraphe](PROSE.json). Le script `prose.py` s’utilise comme `rangees.py`.
