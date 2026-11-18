# Y a-t-il une formule répétée à travers une notice étoilée ?

Dans la transcription de Takahashi, six notices sur onze présentent `daiin` dans leur dernier tiers lorsque `qokal` figure dans leur premier tiers sur les faces d'apprentissage. Au terme de la réserve de sept nouvelles faces, la règle n'a désigné aucune notice. Le groupe `qokal` y réapparaît à quatre reprises, chaque fois dans le tiers médian. Les deux formes sont des identifiants de transcription EVA.

## Ce qui avait été gelé

L'apprentissage porte sur les 198 notices complètes d'au moins six groupes de f103r à f112v. Nous avons gardé les notices signalées à la fois par une ouverture et une fermeture, sur une seule face, dans la section de prose étoilée du cahier. Une notice transcrite peut avoir des limites différentes d'une notice définie par une étoile photographiée. Dans chaque notice, chacun des deux tiers extrêmes compte la partie entière du nombre de groupes divisé par trois.

La sélection devait retenir une seule paire de groupes distincts, à partir de leur présence au premier et au dernier tiers. Parmi 171 paires satisfaisant les conditions de présence et de répartition entre faces, `qokal` puis `daiin` obtient le score de découverte le plus élevé. La réserve d'emplacements est définie en fonction du premier tiers et de la longueur de la notice. Aucune forme du dernier tiers n'a été dévoilée dans le fichier intermédiaire d'emplacements.

Dans l'apprentissage, les fins de 22 notices sur 198 contiennent `daiin`. Six des onze notices déclenchées sont exactes, cinq ne contiennent pas la cible. L'espérance de doubles présences par permutation, en conservant la face et la classe de longueur, est 2,48. La probabilité nominale descriptive est 0,00196 pour cette paire, choisie parmi 171 après observation de l'apprentissage. Elle ne fournit pas un niveau de preuve corrigé de la sélection. Par exemple, les notices successives ouvertes à f103r.21 et f103r.24 comportent toutes deux un `qokal` au premier tiers. La première comporte un `daiin` au dernier tiers, à f103r.23 groupe 1. La suivante n’en comporte aucun dans cette fenêtre.

## Réserve prospective

| Lecture | Notices complètes | Notices avec le déclencheur au premier tiers | Notices avec la cible au dernier tiers | Succès prédits |
|---|---:|---:|---:|---:|
| H, espaces incertains séparés | 87 | 0 | 13 | 0 |
| ZL, espaces incertains séparés | 89 | 0 | 13 | 0 |
| ZL, espaces incertains joints | 89 | 0 | 11 | 0 |

La prédiction exacte, avec le lieu défini comme « dernier tiers de toute notice commençant par un premier tiers contenant `qokal` », a été scellée avant l'ouverture de la réserve. La liste de notices effectivement déclenchées est vide, et a aussi été scellée avant le décompte des cibles. En H, la couverture est 0/87. La précision des annonces est indéterminée. Le rappel rétrospectif des notices où la cible était présente est 0/13. Par exemple, `daiin` est au dernier tiers de la notice f113r.37, ligne f113r.38 groupe 4, en H et en ZL. Aucune lecture ne l'avait annoncé. Pour le contrôle d'ordre inverse, H compte six annonces de `qokal` au dernier tiers, toutes manquées ; ZL en compte cinq, toutes manquées selon les deux conventions. Les sept faces en réserve sont f113r, f113v, f114r, f114v, f115r, f115v et f116r. ZL indique 90 ouvertures dont l'une est suivie d'une autre ouverture sans fermeture marquée et n'a pas été retenue.

Le relevé explicatif suivant a été effectué après ouverture. Les quatre `qokal` de H sont situés aux rangs 17/28 (f113r.23 groupe 7), 18/42 (f114r.36 groupe 6), 6/13 (f114v.18 groupe 6) et 67/152 (f116r.23 groupe 5). Les déplacer après coup dans la définition du déclencheur changerait la question. Le contrôle de permutation conditionnelle, ainsi que la permutation supplémentaire préservant la position dans la ligne, sont dégénérés en réserve puisque le déclencheur est absent.

## Reproduction

Lancer successivement les trois commandes avec pour DOSSIER le répertoire contenant IT2a-n.txt et ZL3b-n.txt dans le dépôt. Le script utilise la bibliothèque standard Python.

```
python3 formule.py discover DOSSIER
python3 formule.py predict DOSSIER --lock choix.json
python3 formule.py unseal DOSSIER --lock choix.json
```

Les fichiers de référence sont PROTOCOLE.md (SHA-256 752ae4182098e25400633a05fdc9f0cf7ff9968e5aab9cbc11855e4aedc842bb), choix.json (19edc6eb93f352036bd84ec41cf0fef583baf777ea9e03ea8ba0357a1ea1e636), emplacements.json (7e87cc34aa9b4af364c6d66299fc276ec9a19abd6033f2b770ffe57080a298a1) et resultats.json.
