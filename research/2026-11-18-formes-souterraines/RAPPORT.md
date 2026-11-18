# Peut-on prédire une racine renflée, puis lire un nom de plante ?

**Sur quarante pages botaniques tenues à part, le mot transcrit `or` manque les huit dessins où deux lecteurs reconnaissent un renflement compact.** Il en prédisait deux ailleurs. À f54r, les agrandissements montrent des prolongements effilés. À f38v, le dessin atteint le bord du parchemin et les lecteurs s’abstiennent. Un second test porte directement sur une plante qu'Ethel Voynich comparait à l'aristoloche. Sa légende est transcrite `opcheor` : la répétition d'un signe avant la fin est incompatible avec les noms *aristologia*, *aristologe* et *aristologie* dans les modèles littéraux examinés. [Résultats visuels détaillés](controle/NOTE.md) · [Essai de lecture du nom](nom/RAPPORT.md)

**Un lien précis entre légende et prose ressort de cet essai.** La forme du fragment 36 est aussi le cinquième groupe de f89r2.22 dans les deux transcriptions principales, sous la troisième rangée de plantes, tandis que la légende accompagne le quatrième dessin de la première rangée. Ce sont ses deux seules occurrences exactes dans le manuscrit selon ces éditions. La concordance de Stolfi les recensait en 2004, et un billet de 2022 comparait déjà leurs photographies. Une autre lecture ancienne donne `opchear` dans le paragraphe. Le nom proposé pour la plante ne peut donc pas être déduit du seul rapprochement. [Relevé de tout le manuscrit](nom/second/NOTE.md) · [Les deux inscriptions sur la photographie](nom/photo/legende-et-prose.jpg)

## Comment un scribe décrit la racine

Le *Livre des simples médecines* de Wellcome, copié vers 1470, explique le qualificatif *longue* de l'aristoloche par la longueur et la finesse de sa racine. Le peintre étire l'organe horizontalement sous la tige. Dans le *Gart der Gesundheit* de 1485, le bois correspondant s'arrête à la tige. Le même terme de plante peut donc figurer auprès de deux représentations où le détail qu'il décrit n'est pas également visible. Pour l'aristoloche ronde, le bois imprimé montre au contraire une masse arrondie. La prédiction sur l'exemplaire français a été déposée avant examen de ses images. Les deux bois allemands étaient déjà connus de l'équipe. [Photographies comparées, lectures et limites](herbier/RAPPORT.md)

## Du texte au dessin tenu à l'écart

Le test retient les 85 faces botaniques des sept premiers cahiers pour lesquelles ZL indique la même main et la même classe de Currier et où les deux éditions donnent de la prose. Sur les photographies anonymisées, deux agents IA ont coté séparément un détail concret. Un renflement doit dessiner un corps délimité, arrondi ou ovoïde, sensiblement plus large que l'axe auquel il se rattache. Les mots français et leurs équivalents médiévaux n'ont pas servi à entraîner le lecteur de signes. Les lecteurs IA ne constituent pas deux expertises humaines. Les 45 faces des cahiers A–C ont servi à fixer les formes candidates ; les 40 de D–G ont été dévoilées ensuite. [Critère, séparation et limites](PROTOCOLE.md) · [Prédictions déposées avant dévoilement](https://github.com/alxbouchard/voynich-research/blob/c46eabf/research/2026-11-18-formes-souterraines/PREDICTIONS.json)

En apprentissage, 11 dessins ont reçu deux votes positifs, 21 deux votes négatifs et 13 une lecture indéterminée. Sur la réserve, les nombres correspondants sont 8, 15 et 17. Les abstentions portent notamment sur la jonction des tiges et des racines, les prolongements au bord du parchemin et des structures intermédiaires. Le mot dans les 60 premières positions des deux transcriptions détermine la prédiction pour chaque face. Une absence du mot annonce une absence de renflement. Les votes indéterminés restent visibles dans les fichiers et sont exclus du tableau suivant.

| Forme et convention | Positifs retrouvés sur 8 | Fausses annonces sur 15 négatifs | Positifs manqués | Négatifs correctement classés |
|---|---:|---:|---:|---:|
| Mot `or`, espaces douteux joints | 0 | 0 | 8 | 15 |
| Finale `-od`, espaces joints | 3 | 5 | 5 | 10 |
| Mot `or`, espaces séparés | 0 | 2 | 8 | 13 |
| Finale `-dal`, espaces séparés | 1 | 4 | 7 | 11 |
| Mot déjà proposé `otoldy`, dans toute la prose | 1 | 2 | 7 | 13 |

Les deux annonces du mot `or` avec les espaces joints étaient indécises dans le test principal. Une seconde paire d'agents IA a repris six photographies sur lesquelles les bords du feuillet sont visibles. Les quatre témoins gardent la même cotation. Les deux lecteurs jugent f54r négatif et laissent f38v indéterminé. Les deux annonces supplémentaires lorsque les espaces sont séparés, f32v et f45v, correspondaient déjà à des absences dans le premier jugement. [Les deux cartes et les quatre témoins](bords/RESULTAT.md)

La finale `-od` donne trois vraies annonces sur huit décisions positives émises pour des images classables, soit 37,5 %. La fréquence des renflements sur les 23 images classables vaut 34,8 %. Huit autres annonces portent sur des images indéterminées. L'énumération des 298 598 400 permutations recto–verso par feuillet à l'intérieur de chaque cahier donne une probabilité unilatérale de 0,1925. Une autre implémentation a retrouvé les dénominateurs et les mots dans les deux transcriptions brutes, les résultats par cahier et la sensibilité à l'exclusion des feuillets déjà examinés pour `otoldy`. [Contrôle indépendant et permutations exactes](controle/NOTE.md) · [Résultats du programme principal](RESULTATS.json)

## Un essai de déchiffrement à partir d’un nom proposé

La relecture des carnets d'Ethel Voynich situe une conjecture de nom sur un seul fragment étiqueté, le 36 de f89r2. La transcription de six unités nous permet d'énoncer exactement quelles graphies pourraient être développées à partir de cette étiquette, même si on laisse un signe représenter plusieurs lettres. Aucune des quatre graphies examinées pour l'aristoloche ne satisfait la répétition de la première unité juste avant la fin. Quatre autres rubriques parmi 77 noms latins, dont *Althaea* et *Galanga*, s'obtiennent en réglant les développements pour un seul mot. Il reste à expliquer le nom réellement employé par le scribe, la langue et la fonction de la légende. [Le dessin dans les carnets](herbier/CIBLES.md) · [La contrainte de lecture, les cas témoins et les grandes notices](nom/RAPPORT.md)

## Reproduction

Les fichiers `cle-apprentissage.json` et `cle-reserve.json` donnent l'URL Yale et l'empreinte de chaque JPEG original. Après avoir placé ces photos dans un dossier, sous les noms f1v.jpg, f2r.jpg et ainsi de suite, la commande `python3 cartes.py DOSSIER apprentissage planches/apprentissage` régénère le premier lot. Remplacer les deux occurrences d'apprentissage par reserve pour le second. Les quatre fichiers lecteur conservés dans ce dossier sont les observations brutes. Exécuter ensuite `python3 -B langage.py predire`, puis `python3 -B langage.py evaluer`. [Code principal](langage.py) · [Second programme](controle/verifier.py) · [Sources de l'essai historique](herbier/sources.tsv)
