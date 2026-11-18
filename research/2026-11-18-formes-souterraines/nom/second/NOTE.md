# Que lisent les 52 tables sur une deuxième légende ?

**Aucune des 52 tables apprises sur `opcheor` ne peut écrire une deuxième rubrique du Macer, même en choisissant librement la suite de signes.** L’absence de deuxième nom dans les légendes ne permet donc de départager aucun des quatre noms de départ. [Protocole au commit 33464a2](../TRANSFERT.md) · [Résultats par table et par lieu](resultats.json)

| Rubrique compatible avec le groupe de départ | Subdivisions distinctes | Séquences distinctes capables d’écrire ce même nom, toutes ses tables réunies | Autres rubriques écrivables, pour chaque table |
| --- | ---: | ---: | ---: |
| *abrotanum* | 3 | 1 | 0 sur 76 |
| *althaea* | 1 | 1 | 0 sur 76 |
| *elleborus niger* | 45 | 15 | 0 sur 76 |
| *galanga* | 3 | 7 | 0 sur 76 |

Les 77 titres latins ont été conservés dans leur ordre de lettres, sans accents ni espace intérieur. Le groupe d’apprentissage comporte six positions et cinq signes distincts, `o p ch e o r`. Chaque signe reçoit une chaîne non vide. Les deux `o` ont la même valeur. Des signes différents peuvent avoir une valeur identique. Le calcul énumère toutes les coupes avant de chercher, de gauche à droite, toutes les suites de signes qui épellent chaque titre. Le JSON contient les coupes, tables et séquences exactes. Pour *abrotanum* et *althaea*, la seule séquence est celle de départ. Les quinze possibilités pour *elleborus niger*, réunies sur ses 45 tables, sont les suivantes.

```text
ch p ch e ch r    ch p ch e o r     ch p o e ch r
ch p o e o r      o ch ch e o r     o ch p e o r
o p ch e ch r     o p ch e o ch     o p ch e o r
o p o e ch r      o p o e o r       o p p e o r
o p p o e o r     o p r e o ch      o p r e o r
```

Les trois tables de *galanga* donnent ensemble sept possibilités.

```text
o p ch e o ch    o p ch e o p    o p ch e o r
o p r e o ch     o p r e o r     o r ch e o p    o r ch e o r
```

## Les 192 autres légendes de fragments

Les deux éditions partagent 194 lignes Lf actives. Les lignes f99r.6 et .7 appartiennent à la même inscription, ce qui donne 193 légendes distinctes. Après retrait de f89r2.5, 192 restent pour l’épreuve. Chaque table s’applique à tous les groupes de la légende entière, en conservant la liste des groupes de chaque édition. Un signe inconnu empêche la lecture de l’ensemble.

| Résultat par table, sur 192 légendes | Nombre |
| --- | ---: |
| Même lecture dans les deux éditions, hors des 77 rubriques | 3 |
| Deux lectures entièrement couvertes mais divergentes | 1 |
| Au moins un signe certain absent du vocabulaire de la table dans une des éditions, sans ambiguïté de signe IVTFF | 173 |
| Au moins une incertitude de transcription | 15 |
| Retour du nom appris ou lecture d’un autre titre | 0 |

Les trois accords concernent `opchor` (f100v.3), `oror` (f102v2.3) et `cheor` (f102v2.11). En f102v2.4, IT2a donne `eeor` et ZL3b `chor`. Les lectures restent distinctes pour toutes les tables. Les blancs incertains affectent le découpage de sept légendes externes. Parmi les 177 sans signe incertain dans les deux éditions, l’accord exact sur les groupes EVA passe de 136, blancs douteux joints, à 140, blancs séparés. Aucune des quatre légendes couvertes ne change de découpage.

## Où le groupe entier opcheor réapparaît-il ?

Les deux éditions ont **une seule occurrence en dehors de la légende source**. C’est le cinquième groupe de f89r2.22, dans une ligne P0 sur le panneau du fragment. La légende f89r2.5 et cette ligne sont les deux seuls lieux du manuscrit où la forme entière concorde. Les blancs douteux joints ou séparés donnent exactement les mêmes lieux et positions. L’occurrence dans le paragraphe atteste une reprise écrite sur la même page. Le référent de ce mot en prose demeure inconnu.

| Périmètre | Lignes P0, IT2a / ZL3b | Occurrences P0 concordantes | Occurrences concordantes dans les autres lignes |
| --- | ---: | ---: | ---: |
| f6r, f52r, f56v | 38 / 38 | 0 | 0 |
| f66v seule | 13 / 13 | 0 | 0 |
| f96r seule | 13 / 13 | 0 | 0 |
| f38r, comparaison indirecte | 6 / 6 | 0 | 0 |
| 129 faces de l’herbier selon la métadonnée IVTFF `$I=H` de ZL3b | 1 569 / 1 569 | 0 | 0 |
| Manuscrit entier | 3 884 / 3 885 | 1 | 1 (légende source Lf) |

Pour les six cibles, les éditions contiennent uniquement des lignes P0. En particulier, les 13 lignes du panneau transcrit f66v donnent 113 positions IT2a et 111 ou 114 positions ZL3b selon le découpage. Une mention historique faisant intervenir une autre disposition de f66v n’ajoute aucune ligne au panneau transcrit. Le fichier de résultats distingue le contrôle des 85 faces, les autres faces d’herbier et l’ensemble du manuscrit, avec les nombres de lignes et de positions par édition et par convention. [Transcriptions et contrôle des empreintes](transfert.py) · [Attributions historiques](../../herbier/CIBLES.md)

Pour reproduire les résultats depuis ce répertoire, exécuter `python3 -B transfert.py` dans un environnement disposant de Pillow, utilisé par le module d’inventaire de l’herbier.
