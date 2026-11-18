# Les étiquettes du zodiaque ouvrent-elles les notices du cahier étoilé ?

**Aucune des 299 étiquettes n’a de copie certaine à l’ouverture des 285 paragraphes marqués dans les transcriptions testées.** Le test retrouve pourtant des inscriptions identiques au début de lignes intérieures. Par exemple, `otaiin`, l’étiquette f71v.7, ouvre la ligne f106v.30 dans ZL et IT. Cette ligne prolonge un paragraphe.

René Zandbergen a relevé une proximité entre les distributions de fréquence des étiquettes zodiacales et des premiers mots de paragraphes étoilés. Nous avons testé une conséquence supplémentaire qu’aurait un index littéral. Si l’on recopiait l’étiquette entière au début de sa notice, les premiers mots devraient coïncider. Le point de départ et les critères sont consignés dans le commit local `f4dcc90`, avant notre décompte. [Étude éditoriale](https://www.voynich.nu/extra/labels.html) · [Protocole](PROTOCOLE.md)

| Transcription et virgules incertaines | Étiquettes entières certaines / 299 | Ouvertures avec copie certaine / 285 | Autres débuts de ligne avec copie certaine | Maximum de paires possibles à l’ouverture, incertitudes incluses |
| --- | ---: | ---: | ---: | ---: |
| ZL, jointes | 271 | 0 | 26 / 795 | 38 |
| ZL, coupées | 271 | 0 | 25 / 795 | 38 |
| IT, jointes | 295 | 0 | 34 / 794 | 5 |
| IT, coupées | 295 | 0 | 34 / 794 | 5 |

La dernière colonne suppose qu’à chaque étiquette appariée correspond une notice distincte. Les premiers mots certains des deux groupes ont une intersection vide. Dans ZL, 25 étiquettes et 13 ouvertures ont un premier mot incertain selon la convention de lecture prudente fixée. Même en accordant à chacun la lecture la plus favorable possible, ils permettent au plus 38 paires. Dans IT, les effectifs sont 3 et 2, soit au plus 5 paires. Ces plafonds donnent des possibilités théoriques. Aucun des liens ainsi accordés n’a été lu. L’écart de plafond tient en partie aux différences de notation de l’incertitude entre les transcriptions.

Pour la recherche de copies entières, les mots d’une étiquette composée doivent se retrouver dans le même ordre en tête de la première ligne, avec leurs limites. Pour la borne maximale, seul compte le premier mot. La borne vaut donc aussi si une étiquette composée débordait sur la ligne suivante. Les décomptes de lignes intérieures sont descriptifs. Les positions partagent des contraintes graphiques et les deux transcriptions décrivent le même manuscrit.

Le corpus utilisé ici sélectionne les 285 lignes de type `P0` explicitement marquées `<%>` sur les 23 pages étoilées du cahier 20. Zandbergen indique 292 premiers mots dans son étude sur RF1b avec des repères de paragraphes empruntés à ZL. Les listes de positions utilisées dans cette publication et dans notre calcul n’ont pas été réconciliées. Les étoiles physiques forment encore un autre décompte. Le catalogue relève, par exemple, un écart entre les étoiles et les paragraphes à f111v. [Description du cahier 20](https://www.voynich.nu/q20/index.html)

Ces résultats écartent un répertoire général qui reproduirait littéralement, dès le premier mot des paragraphes marqués, les étiquettes du zodiaque. Une relation thématique, des formes fléchies ou la présence d’un nom ailleurs dans le texte restent compatibles avec cette observation. Le sens d’`otaiin` reste inconnu. Dans l’herbier imprimé de Fuchs (1542), cinq légendes dont on connaît la notice donnent également zéro égalité entre leur premier mot et le nom du titre, notamment à cause des terminaisons latines. [Comparaison sur les images de Fuchs](FUCHS.md)

Le calcul principal se reproduit depuis ce dossier avec `python3 study.py`. Les deux fichiers d’entrée sont authentifiés avant le calcul. Un second calcul en bibliothèque standard a confirmé indépendamment les dénominateurs, l’intersection vide et les maxima 38 et 5 par appariement biparti. Les deux implémentations ont été réalisées par des agents IA et exploitent les mêmes sources. [Résultats avec les couples de loci](results.json) · [Calcul indépendant](verification/audit.py) · [Audit](verification/AUDIT.json) · [Transcriptions et provenance](../../voynich_phase46/NOTICE.md)
