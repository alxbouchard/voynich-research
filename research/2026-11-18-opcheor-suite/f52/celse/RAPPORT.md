# Une règle peut lire quatre mots de Celse. Lit-elle la phrase ?

Sur f52v.4, deux tables faisaient déjà lire *quoque quod aeque* pour `ctheor ctheol cheeor`. Pour le quatrième groupe, `cheol`, elles donnaient *aod*. Sachant que Celse écrivait *ad*, nous avons essayé une règle supplémentaire. On réunit d’abord les `e` par paires, puis on ignore un `e` simple après `ch`. Le double `e` dans `cheeor` est ainsi conservé et le `e` simple de `cheol` disparaît. La même règle et les valeurs déjà apprises produisent désormais **quoque quod aeque ad**, quatre mots consécutifs de Celse IV.23. Le quatrième était connu quand la correction a été conçue. Une justification de cette convention par le tracé des signes reste à établir. [Règle fixée et prédictions des voisins](AVANT.md)

## Les mots immédiatement voisins

| Emplacement du Voynich | Prédiction de la règle | Mot trouvé autour du passage de Celse |
|---|---|---|
| `tchor`, avant les quatre groupes de f52v | Une ou deux lettres suivies de *aque* | *alterum* |
| `chckheey`, après les quatre groupes de f52v | *a*, une ou deux lettres, puis *en* ou *eia* | *omnes* |
| `ches`, avant les trois groupes de f100v | *a* suivi d’une ou deux lettres | *lac* en III.22, ou *id* en V.26 selon la table |

Aucune des deux tables ne peut produire un seul des trois voisins attendus aux emplacements qu’elle désigne. L’édition florentine de 1478 permet de vérifier les deux mots de IV.23 sur la page même. **Alterum** précède le passage, puis **omnes** se partage entre la fin d’une ligne et le début de la suivante. La phrase introduit une seconde règle qui s’applique également à toutes les affections semblables. [Lecture de l’imprimé et photographie](imprime/RAPPORT.md) · [Tous les tests par table](RESULTATS.json)

## Ce que les tables lisent ailleurs

Nous avons retiré les feuillets 52, 89, 96 et 100 du Voynich et les trois chapitres de Celse déjà utilisés. Chaque table permet encore de convertir entièrement 1 341 paires de mots et 336 triplets consécutifs. La table qui faisait lire *quoque quod in* sur f100v retrouve dans le reste de Celse **11 paires sur 1 341**. Celle qui faisait lire *quoque quod alia* en retrouve **5 sur 1 341**, sur les mêmes emplacements. Ces effectifs comptent les positions et peuvent inclure plusieurs fois les mêmes mots. Aucune des deux tables ne retrouve un triplet attesté parmi les **336** lisibles.

Ainsi, à f101r.5, `ctheol cheol` donne *quod ad* avec les deux tables. Le latin juxtapose bien ces deux mots ailleurs dans l’ouvrage. Cette rencontre de mots grammaticaux ne se prolonge pas ici en une suite de trois mots vérifiable. La correction restitue la citation qui l’a motivée, puis échoue à lire la phrase entière sur la même page et sur les autres feuillets évalués. [Liste exhaustive des positions et des sorties](RESULTATS.json) · [Programme de vérification](verifier.py)
