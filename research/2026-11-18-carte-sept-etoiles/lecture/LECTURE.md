# Peut-on lire les deux noms de mansions sur f68r3 ?

**Aucune table à valeurs constantes et non vides ne restitue les deux noms ensemble**, pour les 21 paires de graphies fixées à partir de deux témoins. La lecture sur un seul nom échoue aussi à restituer l’autre sans ajouter de nouvelles valeurs. Les deux étiquettes réellement comparées sont X.1, à droite des sept petites étoiles, et X.3, auprès de l’étoile solitaire à leur gauche. X.2 `oalcheol` accompagne la ligne courbe qui va de l’amas au médaillon central. Son sens reste inconnu. [Disposition sur le manuscrit](../voynich/LIEN.md) · [Les trois loci dans l’interlinéaire](https://www.voynich.nu/q09/f068r3_tr.txt)

## Les formes attestées

| Témoin | Troisième mansion | Quatrième mansion |
|---|---|---|
| Castillan alphonsin, édition de Madrid, p. 219–220 | `açoraya`, aussi `annexni` et `las estrellas dell Açoraya` | `addauaran`, aussi `la siguiente dell Açoraya`, `alfanic` et `mistah açoraya` |
| Latin, Stöffler et Pflaum, Venise, 1507, « Mansiones lune » | `Athoraye`, glosée `pleiades` ou `pluuiales` | `Aldebaran` ou `Aldelamen`, glosée `caput Thauri` |

Dans la section *Las mansiones o antiguas casas lunares segun los libros Alfonsíes*, les rubriques imprimées sont « Estrellas que formaban la tercera casa Alfonsí de la Luna » et « Estrellas que formaban la cuarta casa Alfonsí de la Luna ». L’extrait alphonsin de la quatrième explique le sobriquet `çaguero` par le fait que l’astre vient après l’`açoraya`. Il attribue `alcalayt` aux étoiles environnantes. Les noms tirés d’Ulugh-Beigh dans le commentaire appartiennent à une autre liste. La numérisation reproduit l’édition madrilène des *Libros del saber de astronomía* de 1863–1867. Une transcription diplomatique indépendante conserve `açoraya` et `addauara<n>`, avec marque d’expansion pour la nasale finale. [Édition, p. 219–220, vues 8–9](https://www.e-rara.ch/download/pdf/698074.pdf#page=8) · [Hispanic Seminary of Medieval Studies, « Del signo de Tauro »](https://www.hispanicseminary.org/t%26c/ac/docs/txt-ast.htm)

Le témoin latin est l’*Almanach noua* de Johann Stöffler et Jakob Pflaum, imprimé par Petrus Liechtenstein à Venise le 3 janvier 1507. La rubrique est à la vue 18, colonne de gauche, de l’exemplaire de Cracovie, Biblioteka Jagiellońska, Cim. 5923. La graphie `Athoraye` a été relevée sur le caractère gothique imprimé, de même que le double `u` de `pluuiales`. La marque de l’imprimeur et la date se trouvent à la vue 769. [Rubrique](https://jbc.bj.uj.edu.pl/Content/1028216/NDIGSTDR119761.pdf#page=18) · [Colophon](https://jbc.bj.uj.edu.pl/Content/1028216/NDIGSTDR119761.pdf#page=769) · [Notice de l’édition, Biblioteca Nazionale Braidense](https://opac.braidense.it/bid/BVEE008659)

## Calcul sur les deux témoins

Le protocole a été écrit et son SHA-256 transmis avant la programmation et le calcul. Les lectures H (Takahashi), U (Stolfi), V (Grove) et ZL ont été prises par paires de la même transcription. L’espace certain de `dchol.dal` et l’espace incertain de `dchol,day` ont d’abord été matérialisés. La branche secondaire autorise la soudure et conserve la terminaison de chaque lecture. `!` dans `dchol!day` sert à l’alignement interlinéaire. Le caractère `ch` est traité successivement comme signe composé et comme deux lettres EVA. Le sens de lecture est commun aux deux étiquettes. Chaque signe peut produire une lettre ou un groupe non vide de lettres consécutives, de longueur bornée uniquement par la cible. [Protocole enregistré](01-protocole.json) · [Description des signes d’alignement par Stolfi](https://www.ic.unicamp.br/~stolfi/EXPORT/00-EXPORT/98-12-28-interln16e6/)

| Épreuve | Configurations | Tables compatibles avec les deux cibles | Restitutions exactes de l’autre étiquette avec la première table figée |
|---|---:|---:|---:|
| `açoraya` avec `addauaran` | 48 | 0 | 0 dans les deux sens |
| `Athoraye` avec `Aldebaran` | 48 | 0 | 0 dans les deux sens |
| Autres correspondances fixées au sein du même témoin | 912 | 0 | 0 dans les deux sens |

Les 1 008 lignes comprennent des variantes emboîtées. Elles documentent les choix de lecture et ne constituent pas 1 008 observations indépendantes. Certaines incompatibilités apparaissent avant le calcul des lettres, par exemple lorsqu’une limite de mot de H demeure visible devant une cible en un seul mot. Les autres proviennent de la répétition d’un même signe ou de valeurs contradictoires entre les noms. Chaque table apprise avec X.1 laisse `ch` et `l` inconnus dans X.3. En sens inverse X.3 laisse toujours `r` inconnu dans X.1. Dans la lecture V directe à signe `ch` composé et expansions permises, X.1 admet 15 découpages pour `açoraya` et X.3 en admet 6 pour `addauaran`. Les valeurs communes n’en rendent aucune paire compatible. [Recensement par configuration](recensement.tsv) · [Sorties partielles et valeurs imposées par chaque nom](resultats.json)

## Ce que reproduit la proposition de Ponzi

Bax propose `taurn`. Ponzi propose de lire `tebartun` sur l’étoile solitaire et de rapprocher cette sortie du nom de la quatrième mansion. En prenant exactement ces deux sorties modernes et la lecture de Grove, on reproduit la table suivante. L’opération se distingue du test sur les noms effectivement imprimés. [Bax, proposition de 2014](https://stephenbax.net/wp-content/uploads/2014/01/Voynich-a-provisional-partial-decoding-BAX.pdf) · [Ponzi, 2 avril 2014, publié par Bax](https://stephenbax.net/?p=803)

| Apprentissage | Valeurs fixées par l’ajustement | Lecture accessible avant d’ajouter une valeur |
|---|---|---|
| `doary` supposé `taurn` | `d→t`, `o→a`, `a→u`, `r→r`, `y→n` | `t[c][h]a[l]tun` sur la solitaire, 5 positions renseignées sur 8 |
| `dcholday` supposé `tebartun` | `d→t`, `c→e`, `h→b`, `o→a`, `l→r`, `a→u`, `y→n` | `tau[r]n` sur l’amas, 4 positions renseignées sur 5 |

Les crochets contiennent les signes **encore sans valeur**, même si leur code EVA ressemble à une lettre attendue. Pour fabriquer `tebartun` après `taurn`, il faut ajouter `c→e`, `h→b` et `l→r`. La table combinée ainsi déterminée contient huit entrées et fait correspondre `r` et `l` au même `r`. La lecture par signe `ch` donne une table combinée à sept entrées avec `ch→eb`. Ni `tebartun` ni `taurn` ne figure parmi les noms des deux témoins. [Reconstitution calculée de la proposition historique](ponzi-reconstitution.json)

## Contrôles et reproduction

Un chiffre monoalphabétique appliqué à la vraie paire castillane donne exactement une table commune aux deux noms. Apprendre sur la première forme restitue cinq positions sur neuf de la deuxième. Quand le second mot est `ay`, attesté p. 219 et composé de deux signes vus auparavant, le transfert restitue les deux lettres. La fausse lecture `aa` échoue. Un contrôle distinct encode `açoraya` avec quatre signes dont l’un développe plusieurs lettres et retrouve une table commune avec la lecture tenue en réserve `ay`. Les deux ouvrages anciens établissent l’ordre de leurs propres mansions. Le test rejette cette famille de tables pour cet appariement sur le Voynich. D’autres modèles d’écriture et d’autres fonctions des étiquettes restent ouverts. [Page de contrôle](https://www.e-rara.ch/download/pdf/698074.pdf#page=8) · [Code](essai.py)

Pour reproduire le calcul depuis ce répertoire, exécuter `python3 essai.py`. Le calcul vérifie l’empreinte du protocole et refait chaque ajustement dans les deux sens. Les deux PDF sources ont pour SHA-256 `3df5434f9adc98d289abe59329e2a95ab4799f047c112964a1b1f353d7ce0ae2` (castillan) et `e4c6d01113c6137c7cc98f3a8463dadbff1d3a398d7599b57458d182d3111b77` (latin).
