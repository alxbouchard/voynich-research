# Retrouver une légende entière à partir d’une autre image

Deux modèles proviennent de la première rangée de f88r. Les huit candidats constituent toute la première rangée de f99v. Deux lecteurs IA ouverts sans historique ont vu une seule planche chacun, dans des ordres différents. Chacun pouvait classer le même candidat en tête pour les deux modèles. Les coupes, réalisées par une personne connaissant les cibles, peuvent influer sur les jugements. Les deux avis portent sur les mêmes images et des modèles d’IA apparentés. [Prédictions](../PREDICTIONS.md) · [Planche nacre](nacre.jpg) · [Planche silex](silex.jpg)

| Légende attendue et modèle de f88r | Cible de f99v | Rang sur nacre | Rang sur silex | Premier choix des deux lecteurs |
|---|---:|---:|---:|---:|
| `otaly`, cinquième fragment V20 | 99 | 2/8 | 2/8 | 97 |
| `otoky`, quatrième fragment V18 selon l’attribution éditoriale | 102 | 2/8 | 3/8 | 95 |
| `otoky`, cinquième fragment V20 si l’inscription intercalée appartient à son voisin | 102 | 8/8 | 7/8 | 97 |

Pour V20, chacun relève des brins longs et recourbés. Les brins du 97 se croisent et forment une boucle, également visible sur le modèle. Ceux du 99, le dessin attendu, s’écartent plus régulièrement. Sur V18, les deux lecteurs distinguent deux masses brunes avec des filaments latéraux. Au 95, qu’ils privilégient, les filaments se rangent autour d’un axe continu. Au 102, ils observent un corps renflé, des bandes transversales et une pointe effilée. Ils jugent plausible une partie souterraine et insuffisants les traits pour reconnaître la même espèce. Tous deux soulignent la faible fiabilité des rangs intermédiaires.

Si l’on impose rétrospectivement un choix entre les seuls 99 et 102, chacun choisirait le 99 pour V20 et le 102 pour V18. Cette comparaison éclaire la ressemblance générale qui a pu attirer l’attention des chercheurs. Le test prévu comportait les huit fragments et aucun des deux dessins attendus n’y arrive premier. Le rapport du projet geoffitect avait déjà attribué une ressemblance visuelle entre les deux dessins de `otaly` à un même type de racine. Les deux emplacements de chacun des mots figuraient déjà dans la liste de Timm et dans les relevés interlinéaires. [Comparaison publiée pour otaly, § 4.3](https://github.com/geoffitect/voynich/blob/master/reports/PROGRESS.md#43-otaly--visually-confirmed-cross-reference) · [Table des légendes de Timm, annexe II](https://www.academia.edu/38163968/How_the_Voynich_Manuscript_was_created) · [Descriptions de la première rangée de f99v, Stolfi](https://www.ic.unicamp.br/en/~stolfi/EXPORT/voynich/00-06-07-word-grammar/Notes/107/work/L16%2BH-eva/UNITS/f99v.L1)

## Relevé intégral des jugements

| Planche | Modèle masqué | Classement de la première à la huitième place | Confiance rapportée |
|---|---|---|---|
| nacre | X = V20 | A B E C H G F D | Modérée pour A devant B, faible au milieu. |
| nacre | Y = V18 | H D E G C A B F | Faible pour H devant D. |
| silex | X = V18 | G E F H D A B C | Moyenne pour un organe souterrain comparable à G, très faible pour l’espèce. |
| silex | Y = V20 | A B H D E G F C | Assez bonne pour un faisceau avec A/B, très faible pour l’espèce. |

La photographie de f88r laisse `otoky` entre les dessins V18 et V20. La position de `otaly` sous la courbe portant la feuille verte rend V20 localement identifiable. Sur f99v le mot associé au n° 99 est placé au-dessus de l’extrémité droite de la grande feuille voisine, à gauche de la partie haute du fragment 99. Le registre ZL le désigne par la note 99. Le mot du n° 102 est dans l’intervalle suivant le fragment bifurqué 101. Ces attributions spatiales ne disent pas si le scribe entendait nommer un dessin dans son ensemble. [Rangée de f88r](f88r-rangee.jpg) · [Rangée de f99v](f99v-rangee.jpg) · [Audit des attaches de f88](../../2026-11-17-herbier-etiquettes-f88/documentation/ATTACHES.json) · [Catalogue de f99v](https://www.voynich.nu/q19/index.html#f99v)

## Photographies et préparation

Les deux modèles réemploient des images masquées de l’expérience du 17 novembre, orientation conservée. Une bande de parchemin masque quelques traits de la couronne de V20 à proximité du texte. La planche retranche les identifiants antérieurs et ajuste l’échelle à chaque case. Pour f99v, le programme extrait huit régions polygonales, conserve une petite marge de parchemin puis masque les inscriptions et les dessins voisins. Des extrémités pâles et quelques pixels de la marge supérieure peuvent être tronqués. Les planches sont des découpages des photographies de Yale. [Source de f88r](https://collections.library.yale.edu/iiif/2/1037112/full/full/0/default.jpg) · [Source de f99v](https://collections.library.yale.edu/iiif/2/1006247/full/full/0/default.jpg) · [Clé des deux présentations](cle.json)

Pour régénérer les deux planches, exécuter `python3 -B fabriquer.py /chemin/vers/1006247.jpg` dans ce dossier avec Pillow. Les deux rangées non masquées du rapport sont des recadrages du JPEG natif. Sur f88r le rectangle va de (540, 125) à (2450, 950), réduit à 1200 pixels de large. Sur f99v il va de (338, 78) à (2695, 943), réduit à 1414 pixels. Les deux photographies originales ont respectivement les empreintes SHA-256 `a1d21ccad0df430b47f3b3df2829bbefb8c4d1644cb70310e6d1de4b01c20013` et `111f6dfc34b8ecb9230cb5a0d144afef4cbd788048ddda2f440108941c91d5e5`. [Programme](fabriquer.py) · [Modèle 4 conservé](modele-4.png) · [Modèle 5 conservé](modele-5.png)
