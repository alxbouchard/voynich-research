# Deux noms arabes sur une carte contemporaine du Voynich

Sur la figure du Taureau du manuscrit de Samarcande, Arabe 5036, f. 118v, les lettres de base donnent **الثريا** près de quatre disques d’or groupés sur la bosse et **الدبران** près de l’œil. Les articles définis figurent dans les deux inscriptions. Les deux ou trois étoiles supplémentaires mentionnées par al-Ṣūfī ont été vérifiées dans le texte d’un autre témoin, Oxford, Marsh 144. La photographie de Paris suffit à vérifier les emplacements des deux légendes. Le point du *bāʾ* dans la seconde est difficile à isoler de la peinture. [Deux agrandissements et sources](../../medieval/NOMS-ARABES.md) · [Protocole écrit avant le calcul](PROTOCOLE.md)

Sur le Voynich, l’hypothèse est qu’une même table permette de lire ces noms sur le groupe de sept étoiles (X.1) et sur l’étoile isolée voisine (X.3). Les deux étiquettes du Voynich sont assez distinctes pour qu’un ajustement au premier nom laisse des signes inconnus dans le second. La comparaison autorise même l’attribution de valeurs à ces nouveaux signes. Un signe déjà vu doit conserver sa valeur dans toute la paire. Il peut produire plusieurs lettres consécutives et deux signes peuvent produire les mêmes lettres. Les lettres arabes sont traitées dans leur ordre de lecture, avec leurs points consonantiques. Les signes de vocalisation sont omis. Les quatre transcriptions du Voynich et les deux sens de lecture sont traités séparément. [Emplacement des légendes et variantes de lecture](../../voynich/LIEN.md)

| Article défini dans les deux noms testés | Configurations à valeurs non vides | En autorisant un signe muet | Configurations donnant une table commune |
|---|---:|---:|---:|
| Deux articles, comme sur le témoin du XVe siècle | 24 | 172 | 0 |
| Aucun article, variante construite | 24 | 172 | 0 |
| Article seulement dans le nom des Pléiades, variante construite | 24 | 172 | 0 |
| Article seulement dans le nom d’Aldébaran, variante construite | 24 | 172 | 0 |

Pour les graphies de la carte, **16 des 196 configurations** permettent d’ajuster chacune des légendes prise séparément. Aucune paire d’ajustements n’attribue les mêmes valeurs à tous les signes partagés. La suppression hypothétique de l’article ajoute 588 configurations, sans table compatible. Les lignes sont des variantes du même problème. Aucun transfert vers le trait inscrit entre l’amas et le visage central n’a pu être évalué.

Une substitution synthétique des lettres des deux vrais noms fournit une table commune et restitue l’article **ال** après apprentissage sur le premier nom. L’article est déjà présent dans l’apprentissage. Ce contrôle vérifie le programme avec une solution connue. Un second contrôle retrouve une expansion en deux lettres répétée et un signe muet présent dans les deux chaînes. Un contre-calcul par énumération des partitions de chaque cible a retrouvé les nombres d’ajustements individuels et conjoints pour les 784 configurations. Pour reproduire le calcul principal, exécuter `python3 lire.py` dans ce répertoire. [Programme](lire.py) · [Détail de chaque configuration](RESULTATS.json)
