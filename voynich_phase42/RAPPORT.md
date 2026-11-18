# Phase 42 — les signes marginaux de f49v sont-ils des compteurs ?

**Aucune clé numérique ni traduction validée.** Les règles de comptage examinées échouent dans les deux transcriptions, avec toutes les variantes d'espaces explicitement marquées. Le résultat retire une famille précise de candidats ; il ne démontre ni l'absence de message ni l'impossibilité de déchiffrer le manuscrit.

## Ce que montre l'image

L'[original Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006171), conservé à 2 935 × 3 769 pixels, porte une colonne de signes isolés à gauche des 26 lignes. Plus à gauche, cinq marques se lisent probablement 1, 2, 3, 4, 5 près des lignes physiques 2 à 6. Un agent IA séparé, sans accès aux transcriptions ni à la lecture attendue, confirme cet alignement ; il juge la première marque moins certaine. Son [compte rendu](evidence/AI_IMAGE_READING.md) et les [cadrages natifs](PLANCHES.md) sont conservés. Ce contrôle n'est pas une expertise humaine indépendante et ne date pas les annotations.

La [description de Zandbergen](https://www.voynich.nu/q07/index.html) rapproche la main des chiffres de celle de la foliation. La [Note034 de Stolfi](https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/Notes/034/Note-034.html) proposait déjà un comptage des mots ou des lettres, tout en envisageant des annotations ultérieures. **L'alignement ne prouve pas que les signes voisins valent ces nombres.**

## Test fixé avant les résultats

Le [protocole](PROTOCOL.json), les sources et le programme ont été figés au commit `36973d1`, après consultation des sources mais avant calcul. Ce test exploratoire n'est pas aveugle. ZL et IT sont deux lectures du même manuscrit, avec une histoire commune ; elles ne représentent pas deux confirmations indépendantes.

Les mesures sont le numéro de ligne, le nombre de mots, le nombre de codes EVA et un regroupement mécanique des formes `ch`, `sh`, `ckh`, `cth`, `cph`, `cfh`. Ces deux derniers comptes ne sont pas des nombres établis de lettres ou de glyphes historiques. Cette distinction suit les [limites de l'alphabet EVA](https://www.voynich.nu/extra/sp_analysis.html).

Chaque compte est essayé sur la ligne seule, puis cumulé avant ou après la ligne, depuis le début de la page ou du paragraphe. Les morceaux de texte séparés par la plante appartiennent à la même ligne. Les signes marginaux sont exclus du compte. Les 648 combinaisons de comptes de mots autorisées par les virgules ZL sont toutes examinées, y compris les cas intermédiaires. Les alternatives de lecture sont conservées. Les inconnues IT n'imposent aucune identité entre elles.

Les rapprochements `f/p` et `r/@192;` sont chacun essayés séparément puis ensemble, sans modifier les sources. `@192;` n'est donc pas automatiquement interprété comme le chiffre 2. Les divergences aux lignes 15 et 24 restent celles des transcriptions.

## Résultat et preuve

Les **128 familles donnent 13 088 configurations de compte**. Ce nombre inclut des cas dépendants ou équivalents ; ce n'est ni un nombre d'expériences indépendantes ni une probabilité statistique.

Pour qu'un même signe représente une valeur fixe dans un compteur cyclique, les différences de comptes entre ses occurrences doivent toutes être divisibles par la période. Le programme calcule leur plus grand commun diviseur, appelé G. Dans **toutes les configurations, G = 1** : aucune période supérieure à 1 ne convient. Cette exclusion vaut pour toutes les périodes dans cette famille, sans se limiter à une recherche jusqu'à 64. Elle n'exige pas que des signes différents aient des valeurs différentes.

Exemple simple, commun aux deux sources : `o` est aux lignes 2 et 10, soit un écart de 8 ; `p` est aux lignes 9 et 16, soit un écart de 7. Une période commune devrait diviser 8 et 7. La seule possibilité est 1, qui ne fournit aucun code numérique distinctif. Pour le cumul de mots IT avant chaque ligne, deux écarts imposés sont 28 et 29, ce qui donne la même contradiction. Les autres comptes possèdent leurs propres [certificats](results/ANALYSIS.json).

Le test conditionnel supplémentaire attribue 1–5 aux signes voisins des chiffres. Il autorise une transformation affine ordinaire à coefficients rationnels, ou une transformation affine réversible modulo 6 à 64. **Aucun candidat ne satisfait simultanément les cinq nombres et les répétitions.** Le rejet sans valeurs supposées est déjà suffisant ; l'ambiguïté du premier chiffre ne le change pas.

## Portée et suite

Le [contrôle des calculs](results/verification.json) utilise un autre parseur et les différences entre toutes les paires, avec des certificats de Bézout. Les contrôles artificiels vérifient le programme, sans constituer une preuve de déchiffrement. Une reproduction en dossier neuf est documentée dans [REPRODUCTION.md](REPRODUCTION.md).

Nous écartons ces compteurs comme clé de lecture de f49v. Nous ne corrigeons pas les espaces ou les signes pour sauver l'hypothèse. D'autres unités graphiques, des erreurs non marquées, des règles non linéaires ou une annotation tardive restent hors du test. Aucun sens n'est attribué au texte courant. L'objectif de déchiffrement demeure ouvert ; cette piste n'apporte pas la correspondance indépendante entre texte et sens nécessaire pour annoncer une traduction.
