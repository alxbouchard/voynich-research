# Phase 47 — Naibbe sans clé, espaces ou extrémités imposés

**Le répertoire publié de formes Naibbe ne peut pas produire toutes les lignes retenues du Voynich, même avec des espaces arbitraires et des débuts ou fins de ligne tronqués.** Le test le plus permissif rejette 404 des 3 151 lignes ZL retenues et 807 des 4 051 lignes IT retenues. Changer uniquement les lettres claires attribuées à ces formes ne peut supprimer ces contradictions.

Cela écarte une recherche de clé comme solution complète **dans ce répertoire fixé**. Cela ne réfute pas un autre répertoire, une autre lecture des signes ou toute la famille des chiffres apparentés. Aucune traduction n'est produite.

## Source et différence avec la phase 1

Michael A. Greshko a conçu Naibbe comme un chiffre moderne réalisable avec des moyens du XVe siècle. L'[auteur](https://www.michaelgreshko.com/naibbe-cipher) ne le présente pas comme une solution du manuscrit. Référence : Greshko, M. A. (2025), *The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext*, **Cryptologia**, [DOI 10.1080/01611194.2025.2566408](https://doi.org/10.1080/01611194.2025.2566408).

Le [dépôt primaire inspecté](https://github.com/greshko/naibbe-cipher/tree/5145f526b52741a6dca14201147f687e62c7162e) contient un générateur et un décodeur qui consulte la table connue. Nous n'y avons pas identifié d'attaque reconstruisant la clé inconnue. La phase 1 avait réussi un aller-retour à table connue et testé directement les tokens Voynich, sans décodage des composés.

Cette phase ne répète pas simplement ce test. Elle retire la dépendance aux valeurs des lettres, autorise un nombre quelconque de jetons fusionnés, supprime tous les séparateurs d'une ligne et autorise la troncature des jetons aux deux extrémités. Elle vérifie donc une condition nécessaire avant de lancer une attaque de clé. **Aucune récupération de clé inconnue n'a été exécutée.**

Le protocole, le programme et les sources ont été figés au commit `87009fe609a52011c0f9fe15b32d72c7514b318e`. L'échec antérieur aux frontières fixes était connu avant ce gel.

## Contrainte indépendante des lettres claires

La table comporte 414 entrées : 23 lettres, six tables et trois positions. Nous utilisons seulement les formes graphiques et leur rôle :

- U : 137 formes unigrammes distinctes ;
- P : 138 formes de préfixe ;
- S : 138 formes de suffixe.

Un jeton élémentaire est dans `A = U ∪ PS`. L'ensemble contient 18 947 chaînes distinctes, de longueur maximale 12 caractères EVA. Nous admettons même les combinaisons ambiguës que le générateur peut normalement éviter : le test est volontairement plus permissif que le chiffrement publié.

Toute sortie, y compris avec réutilisation et suppression d'espaces, est une concaténation de ces jetons, notée `A*`. Une portion de texte coupée à des positions quelconques doit être une sous-chaîne de `A*`. Modifier l'affectation des lettres claires aux formes ne change pas cet ensemble. Aucun score latin, italien ou autre n'intervient.

Le programme construit un automate à 673 états. Tous les états sont accessibles depuis la racine et peuvent y revenir. En partant de tous les états et en acceptant tout chemin restant possible, on admet exactement les sous-chaînes, y compris celles commençant ou finissant au milieu d'un jeton. Cette liberté couvre les décalages de limites de ligne ; elle ne fournit pas une lecture.

## Texte retenu et résultats

Nous retenons les loci de prose dont la ligne entière ne contient que des caractères EVA minuscules et des séparateurs ordinaires après retrait des balises. Toute ligne contenant une inconnue ou une alternative est exclue en entier : aucun signe illisible n'est effacé pour recoller ses voisins. Les points, virgules et interruptions de dessin ne fournissent aucune lettre et sont retirés pour le test de ligne.

| Condition | ZL | IT |
|---|---:|---:|
| Lignes propres retenues | 3 151 | 4 051 |
| Lignes incertaines exclues | 979 | 67 |
| Tokens retenus | 26 200 | 33 749 |
| Tokens directement dans A | 21 249 | 27 272 |
| Tokens segmentables en une concaténation de A | 24 699 | 31 796 |
| Lignes sans séparateurs admises, extrémités fixes | 2 696 | 3 171 |
| Lignes admises, extrémités ouvertes | 2 747 | 3 244 |
| Lignes encore rejetées, extrémités ouvertes | **404** | **807** |
| Rejets dont le témoin utilise seulement l'alphabet du répertoire | 384 | 805 |

Les deux transcriptions n'ont pas les mêmes règles d'incertitude ni les mêmes lignes retenues : leurs nombres ne mesurent pas une différence de qualité ou deux réplications indépendantes. Les admissions ne représentent jamais un pourcentage de texte déchiffré. Elles signifient seulement qu'une suite de formes est possible dans la grammaire permissive.

## Témoins vérifiables

Pour chaque ligne rejetée, nous conservons son locus, ses caractères sans séparateurs, les indices d'un court fragment interdit et le fragment lui-même. Ce témoin est minimal par retrait d'un caractère à gauche ou à droite. Cette minimalité locale n'est pas une recherche du fragment le plus court de tout le manuscrit.

Les listes [ZL](results/ZL_CERTIFICATES.json) et [IT](results/IT_CERTIFICATES.json) permettent de contrôler chaque contradiction. Certains témoins comportent un caractère absent du répertoire ; ils sont distingués des enchaînements impossibles utilisant uniquement ses caractères. La conclusion ne repose donc pas seulement sur des signes absents.

Le contrôle séparé vérifie que 276 témoins ZL et 618 témoins IT sont entièrement contenus dans un seul token d'entrée. Parmi eux, respectivement 256 et 616 utilisent seulement l'alphabet du répertoire. Ces contradictions ne dépendent donc ni d'une jointure entre mots ni d'un caractère extérieur.

Les témoins dérivent des transcriptions : ce travail ne remplace pas une vérification paléographique des signes. Une autre convention graphique pourrait changer la compatibilité. En revanche, déplacer uniquement les espaces ou changer les lettres claires ne répare pas un fragment interdit dans ce répertoire.

## Contrôles et décision

Les 18 947 jetons élémentaires et leurs 27 106 sous-chaînes distinctes sont admis comme prévu. Les contrôles incluent aussi 2 428 coupes dans des concaténations et les 1 063 lignes, soit 34 809 tokens, du témoin Naibbe généré en phase 1. Ce dernier demeure un témoin à clé connue.

Le vérificateur indépendant emploie une segmentation par dictionnaire et la décomposition `Fact(A) ∪ Suffix(A) A* Prefix(A)`, au lieu de l'automate, pour contrôler les données réelles et les témoins. Des petits cas exhaustifs contrôlent aussi les différences entre lignes fermées et fragments ouverts. La [reproduction](REPRODUCTION.md) distingue validation du calcul, reconstruction de clé et traduction.

Nous n'engageons pas une recherche des seules correspondances secrètes des lettres dans les tables publiées comme voie vers une lecture complète : cette famille possède déjà des contre-exemples structuraux. Une suite pertinente devrait modifier une hypothèse supplémentaire, telle que le répertoire des unités graphiques, puis justifier cette modification par une preuve indépendante. Aucun remplacement de signes n'est choisi après coup pour faire disparaître les rejets.
