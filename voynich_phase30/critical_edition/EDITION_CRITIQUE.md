# Trois loci pour chercher un point d’appui vérifiable

**Proposition d’édition critique, 31 octobre 2026 — NOT_TRANSLATION.** Aucun mot Voynich n’est traduit ici. Les images déjà exposées servent à localiser les questions ; leur réouverture par le même assistant n’est pas une seconde expertise. Les propositions ci-dessous découlent du résultat de phase30 : les limites de groupes ne suffisent pas, et un alignement faux peut donner une clé unique. Il faut donc distinguer le tracé, le découpage, l’alignement et le sens.

Le dossier contient trois images avec [provenance et empreintes](IMAGE_PROVENANCE.json), les [variantes héritées de f1r](F1R_PRIOR_READINGS.json) et une [fiche vierge](RELECTURE_VIERGE.json). Les photographies sont créditées à **Beinecke Rare Book & Manuscript Library MS 408, Yale University**, folios indiqués. Les deux JPEG sont les fichiers natifs archivés ; f70v2 est une vue réduite déjà archivée. Les sources n’ont pas été retouchées. Les régions pâles de f1r requièrent aussi l’imagerie multispectrale publiée, qui n’est pas reproduite dans ce petit paquet.

## 1. f1r — quelle colonne, et à quoi sert-elle ?

[Image complète f1r](../../docs/PIECES_REFERENCES.md#piece-54c58f5b40d8b8) · [source Yale](https://collections.library.yale.edu/iiif/2/1006076/full/full/0/default.jpg).

Lisa Fagin Davis décrit trois colonnes marginales : deux alphabets latins décalés entourant des signes Voynich. Elle présente une lecture préliminaire et une interprétation historique de l’annotation ; sa fonction reste incertaine. Cela ne fournit pas une clé démontrée du texte principal. [Étude primaire, 8 septembre 2024](https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/).

La phase16 avait recodé manuellement un sous-ensemble en EVA. Ce recodage moderne, archivé sans modification, ne constitue ni une nouvelle lecture de l’encre ni une équivalence authentifiée. Par exemple :

| Signe noté en EVA dans l’ancien dossier | Colonne latine gauche | Colonne latine droite |
|---|---|---|
| `d` | `a` | `b` |
| `a` | `b` | `c` |
| `r` | `c` | `d` |
| `o` | `e` | `f` |
| `in` | `f` | `g` |
| `ch` | `i` | indéterminé dans le sous-ensemble |

Ces lettres latines sont des **lectures concurrentes de la table**, pas des traductions. Un signe EVA à plusieurs caractères peut représenter une unité ou un groupe : ce point doit lui aussi rester variable.

| Hypothèse conservée | Prédiction conditionnelle | Observation discriminante requise |
|---|---|---|
| F1-L : la colonne gauche code le texte principal | Une occurrence authentifiée du même signe `d` devrait décoder `a`, partout dans le domaine déclaré de la clé | Un alignement externe, fixé indépendamment de cette table et couvrant ce signe, doit donner cette lettre |
| F1-R : la colonne droite code le texte principal | La même occurrence devrait décoder `b` | Le même témoin doit donner `b`, avec une lecture d’encre et un rattachement de ligne indépendants |
| F1-E : la table est une tentative ou un exercice sans clé correcte du texte principal | Aucune correspondance principale n’en découle nécessairement | Des incohérences sur des témoins authentifiés réfuteraient L/R dans leur domaine annoncé ; elles ne prouveraient pas à elles seules la fonction historique E |
| F1-G : une ligne ou un groupe a été mal rattaché | Les associations changent au locus concerné | Des coordonnées, alignements de lignes et clichés multispectraux doivent résoudre le rattachement avant tout test lexical |

Il est interdit de choisir L/R parce qu’un fragment obtenu ressemble à un mot. Un témoin utilisé pour trancher devient une donnée de construction ; il ne peut plus servir de vérification séparée. L’absence actuelle d’un témoin n’est une réfutation d’aucune variante.

**Relecture proposée :** transcrire d’abord les trois colonnes et toutes les lacunes sans afficher les sorties de déchiffrement ; enregistrer les coordonnées des traits et les incertitudes ligne par ligne. Demander ensuite, séparément, une justification documentaire du rapport de cette table avec le texte principal. Un accord sur la forme des signes ne prouve pas le sens de la table.

## 2. f116v — `oror.sheey` ou `aror.sheey` ?

[Image complète f116v](../../docs/PIECES_REFERENCES.md#piece-5e50939f8052f1) · [source Yale](https://collections.library.yale.edu/iiif/2/1006277/full/full/0/default.jpg). Le passage se trouve dans les lignes supérieures. Les petits dessins de la marge gauche ne sont pas le segment à transcrire.

Le dossier de phase16 conserve `oror.sheey` dans ZL ; IT n’inclut pas f116v. `aror` est une alternative publiée, pas une correction imposée. L’ancienne comparaison à f104r est déjà exposée ; elle ne devient ni une découverte ni une réserve nouvelle. Les essais multispectraux de phase17 n’ont pas établi une lecture sûre de l’initiale.

| Hypothèse graphique | Prédiction sous une future règle fixe | Test qui ne suppose pas un sens |
|---|---|---|
| F116-O : `oror.sheey` | Dans une substitution simple sans ajout, les unités 1 et3 du premier groupe ont la même valeur ; le motif serait ABAB | Comparer les traits du premier signe aux deux classes graphiques candidates, sans fournir de mot cible |
| F116-A : `aror.sheey` | Dans cette même sous-famille, le motif serait ABCB avec première unité distincte de la troisième | Décrire le trait qui différencie l’initiale, sur les canaux disponibles et les comparateurs fixés |
| F116-S : frontière après le premier groupe | Deux mots si cette séparation est linguistique | Mesurer la séparation et le contexte de la main ; conserver l’alternative d’un seul groupe tant que non résolue |
| F116-M : le texte ordinaire voisin donne un équivalent | Une paire claire–chiffrée précise devrait pouvoir être délimitée et justifiée | Il faut un mécanisme documentaire de traduction ou de glose ; la proximité seule ne suffit pas |
| F116-N : juxtaposition sans équivalence connue | Aucun mot clair ne peut être utilisé comme indice | Reste la situation de départ tant qu’aucun lien externe n’est établi |

ABAB/ABCB sont des prédictions **conditionnelles à la sous-famille indiquée**, et non une analyse établie de la langue du manuscrit. Sous codes variables ou groupements différents, ces schémas doivent être recalculés à partir de la lecture fixée. `sheey` reste une translittération sans sens attribué. On ne remplace pas ce groupe par une formule religieuse ou médicale espérée.

Une récurrence graphique à f104r pourrait vérifier une constance de signes ; elle ne fournit pas à elle seule la valeur claire de ces signes. Pour en faire un témoin sémantique, il faudrait une justification supplémentaire qui n’a pas servi à choisir la lecture de f116v.

## 3. f70v2 — annotation de mois et texte Voynich

[Vue f70v2](../../docs/PIECES_REFERENCES.md#piece-844d75ce224462) · [source Yale native](https://collections.library.yale.edu/iiif/2/1006200/full/full/0/default.jpg).

René Zandbergen relève `mars` parmi les annotations ordinaires de mois du zodiaque, à f70v2, et traite ces annotations comme des ajouts. Ce relevé ne désigne aucun mot Voynich comme traduction du mois. [Relevé documentaire](https://voynich.nu/writing.html).

| Hypothèse conservée | Prédiction conditionnelle | Ce qui manque |
|---|---|---|
| Z-M : un segment Voynich précis désigne le même mois | Une règle construite sur d’autres paires doit donner le nom et la forme linguistique authentifiés à ce segment | Localisation du segment, langue, graphie et preuve de co-référence, établies sans choisir le meilleur score |
| Z-D : l’ajout ordinaire décrit le dessin sans doubler un mot Voynich | L’annotation ne fournit aucune équation claire–chiffrée | Une preuve positive serait nécessaire pour passer de D à M |
| Z-A : le rattachement d’une étiquette est incertain | Plusieurs alignements restent possibles | Relevé spatial complet, avec alternatives ; aucun alignement sélectionné selon son décodage |

Le dessin de poissons ne permet pas de décider si un groupe voisin est un nom de mois, un nom de signe, un nom d’étoile ou autre chose. Aucun de ces mots n’est fourni au solveur comme vérité. Les folios zodiacaux suivants sont des comparateurs distincts possibles, mais ils ont déjà été vus et ne sont pas des données historiquement aveugles.

## Ordre de travail proposé et condition d’application

1. Deux lectures indépendantes, si des spécialistes deviennent disponibles, commencent par les images et une fiche vierge. Elles enregistrent traits, espaces, coordonnées et variantes avant de voir les hypothèses lexicales. Aucun expert n’a été contacté et aucune lecture indépendante n’est simulée ici.
2. Un dossier documentaire distinct justifie, ou refuse, chaque lien avec un texte clair. Il peut conclure « aucune paire ». La concordance de deux transcriptions ne vaut pas équivalence sémantique.
3. Une nouvelle version du protocole fixe la famille, toutes les variantes de lecture, les alignements admissibles et le budget avant inférence. Les espaces, alphabet et codes préfixes libres du banc actuel doivent être justifiés ou recalibrés pour le cas réel.
4. Une règle unique doit résulter des seules paires de construction. Si plusieurs règles subsistent, publier l’ambiguïté. Garder ensuite un témoin documentaire distinct, qui ne choisit aucune branche. Toute tentative après lecture de ce témoin relève du développement et nécessite un autre témoin.
5. Si ces conditions sont remplies, appliquer la règle inchangée à des passages distincts préalablement désignés, conserver les erreurs et demander une vérification linguistique/historique indépendante. Ne pas choisir après coup les passages les plus lisibles.

**État actuel : zéro paire claire–Voynich admissible ; aucun témoin sémantique séparé.** La calibration informatique est acquise pour la famille artificielle testée. L’application historique reste bloquée par cette information absente. Une paire authentifiée serait un point d’appui utile ; notre essai ne démontre pas qu’une seule suffirait à identifier la clé entière.
