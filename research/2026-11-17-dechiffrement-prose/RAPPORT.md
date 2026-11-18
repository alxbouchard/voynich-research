# Trois essais pour déchiffrer la prose du Voynich

**Aucune des clés proposées par les deux recherches de textes connus n’a permis de lire la suite d’un passage.** L’essai le plus étendu porte sur 206 chapitres du traité médical de Celse. Dans les lignes où les deux transcriptions du Voynich concordent, six rapprochements avec Celse permettaient chacun de prédire trois mots. Les dix-huit prédictions ont échoué. Un essai distinct de restitution à partir du Voynich lui-même a retrouvé deux mots dans les transcriptions étendues, sur deux lignes différentes du folio 78. Le sens de ces mots reste inconnu.

## Ce qui a été mis à l’épreuve

| Hypothèse | Ce qu’elle devait prédire | Résultat dans les lignes communes |
|---|---|---|
| Chaque lettre d’un extrait historique a un signe fixe, sans espaces nécessaires | Après 12 signes appariés, retrouver au moins huit signes annoncés dans les 12 suivants | 15 suites testables, aucune confirmée. Meilleur résultat de 3 signes exacts. |
| Chaque mot d’un texte médical latin a un équivalent Voynich fixe, quelle que soit sa longueur | Après dix mots appariés, retrouver tous les mots annoncés sur les six suivants, au moins trois positions de deux mots distincts | Six appariements testables avec Celse, aucun mot annoncé exact. |
| Une formule répétée sur plusieurs feuillets permet de compléter un passage | Restituer un mot masqué sur un autre feuillet, sans avoir vu la réponse | Une proposition sur 368 positions, et elle échoue. |

Le premier essai porte sur l’armoise dans l’herbier de Macer Floridus, sur le début du premier chapitre de Celse et sur le chapitre consacré à l’air chez Aldebrandin de Sienne. Ces choix de genre et de passage ont été faits sans consulter le texte du Voynich. Le corpus historique conserve les mots et les références des éditions. Un exemplaire de l’herbier est daté de 1448. L’exemplaire du *De medicina* conservé à Glasgow a été imprimé à Florence en 1478. Ces témoins établissent la circulation des œuvres au XVe siècle. Leur rapport avec le Voynich reste hypothétique. [Extraits et éditions](references/SOURCES.md) · [Harley MS 2651](https://searcharchives.bl.uk/catalog/040-002048482) · [Incunable de Glasgow](https://www.gla.ac.uk/myglasgow/incunabula/a-zofauthorsa-j/c27/)

L’épreuve principale conserve 1 073 lignes de prose dont les champs concordent dans les lectures de Zandbergen–Landini et de Takahashi, sur 96 numéros de feuillets. Elle couvre 7 949 champs lisibles. Les deux lectures complètes comptent respectivement 3 885 et 3 884 lignes de prose de type P0 sur 98 numéros de feuillets. Les désaccords de lecture et de séparation réduisent fortement l’échantillon commun. Les suites de caractères EVA comme `chaiin` sont des notations de signes. La prononciation reste inconnue. [Inventaire](donnees/CORPUS_INFO.json) · [Description des transcriptions EVA](https://www.voynich.nu/transcr.html)

## Une clé qui semblait marcher sur f76v

Dans le livre V, chapitre 26 de Celse, à partir du mot 1 294, le mot latin *si* occupe les positions 3, 7 et 9 du début de passage. Dans les lignes 31 à 33 de f76v, le même motif de répétition sur les dix premiers mots autorise provisoirement `si → chedy` et `est → otedy`. Une fois cette table fixée, les positions suivantes tranchent l’hypothèse.

| Position dans les six mots réservés | Mot latin | Prévision | Lecture commune du Voynich |
|---|---|---|---|
| 1 | si | chedy | chckhedy |
| 3 | est | otedy | oty |
| 6 | si | chedy | shckhedy |

Les deux transcriptions donnent trois suites différentes de celles annoncées. Une ressemblance graphique partielle serait un nouveau critère de réussite, à définir avant une nouvelle expérience. [Audit des positions et des lectures](C_etendu/AUDIT.json)

## Quelle partie du texte de Celse était réellement testable ?

Sur **607** passages de seize mots des trois extraits initiaux, quatorze présentaient suffisamment de répétitions dans les dix premiers mots. **Aucun** ne permettait de prédire trois positions représentant deux mots distincts dans les six derniers. Ce premier essai par mots entiers était incapable de départager les hypothèses. Nous avons donc consigné l’extension à tous les autres chapitres numérotés de Celse avant de les confronter au manuscrit, en gardant les mêmes seuils. [Protocole initial](PROTOCOLE.md) · [Extension](PROTOCOLE_C_ETENDU.md)

Les 206 chapitres des huit livres, hors proèmes et premier chapitre déjà testé, contiennent 97 412 mots. Ils offrent 94 327 passages bruts de seize mots, dont 90 944 entièrement en graphie latine. Les limites de chapitre et les mots grecs interrompent la recherche. Parmi les 4 644 passages latins ayant au moins deux répétitions dans leur début, **143** pouvaient annoncer la suite au seuil exigé. Ils représentent 106 motifs de début distincts. Le texte suivi du Voynich est également interrompu par toute lecture incertaine et tout changement de paragraphe.

| Transcription | Passages manuscrits de 16 mots | Rapprochements fournissant des prédictions | Suites confirmées | Meilleur nombre de mots exacts dans une suite |
|---|---:|---:|---:|---:|
| Lignes communes | 625 | 6 | 0 | 0 |
| Zandbergen–Landini | 3 809 | 33 | 0 | 1 |
| Takahashi | 18 083 | 207 | 0 | 1 |

Sur 99 brassages par vue conservant les mots de chaque segment, une suite a passé le seuil dans un seul brassage de Takahashi. Les 296 autres brassages ont donné zéro suite confirmée. Les éditions transcrivent les mêmes pages et certaines fenêtres se chevauchent. Le compte des appariements inclut ces recouvrements. Il faudrait une clé capable de lire un autre passage sur un autre folio, puis des indices historiques indépendants, pour envisager un sens. Aucun appariement n'a atteint la première étape. [Prédictions enregistrées](C_etendu/EMPREINTES.json) · [Tous les scores et les mélanges](C_etendu/RESULTATS.json)

Un contrôle a chiffré et inséré chacun des 143 passages latins testables à un endroit inconnu du moteur. Il a retrouvé 143 fois le bon passage à la bonne position. Dans 66 cas, cette réponse était unique. Dans les 143 témoins où deux mots distincts de la suite avaient été échangés, il a rejeté la lecture ciblée. Ces résultats mesurent sa sensibilité à un texte copié exactement sous une clé stable. Ils montrent aussi combien une seule concordance serait fragile. [Résultats des 429 essais synthétiques](C_etendu/CONTROLES_RESULTATS.json)

## Deux vérifications sur des passages précis

- **Celse et la substitution lettre à signe, f77r.26.** Douze signes d’affilée s’accordaient avec la répétition des lettres d’un extrait de Celse. Cette clé a ensuite prédit huit signes. Un seul était exact. Sur l’ensemble des 81 extraits historiques et des 12 618 fenêtres communes, 26 des 99 manuscrits mélangés ont égalé ou dépassé le meilleur score partiel de trois signes. Le moteur a retrouvé les 43 extraits de calibration injectés sous des clés inconnues et rejeté leurs 43 témoins à suite mélangée. [Détail signe par signe](A/RAPPORT.md)
- **Prédire le mot suivant à f9v.10.** Aux lignes f4r.3 et f47r.3, `chol chy` est suivi de `chaiin`. À f28v.3, il est suivi de `choiin`. La règle a donc annoncé `chaiin` pour le cinquième mot de f9v.10. Les deux transcriptions donnent `kyty`. Sur les versions complètes, elle a retrouvé `aiin` en ZL à f78r.37 et `qokain` en IT à f78r.18, avec respectivement 1 réussite sur 16 et 1 sur 9 propositions. Dans les deux cas, le seul mot précédent suffisait à donner la même réponse. [Lignes, témoins et résultats](B/RAPPORT.md)

Ces essais portent sur une copie littérale dans des graphies éditoriales déterminées et, pour les essais de déchiffrement, sur des substitutions stables. Ils laissent ouvertes d’autres langues, une rédaction originale, l’abréviation, la paraphrase et des systèmes où un signe change de valeur selon sa position. Les expériences ne permettent de choisir entre ces possibilités ni d’attribuer avec confiance un sens à un mot.

## Refaire la vérification

Depuis le dossier de l’étude, `python3 -B reproduire.py` régénère les prévisions, les scores et les mélanges dans un répertoire temporaire et les compare aux fichiers enregistrés. L’option `--ivtff ../../voynich_phase46/sources` reconstruit aussi le corpus du Voynich dans le dépôt. Dans l’archive autonome, utiliser `--ivtff ivtff`. Les prévisions A et B ont été annoncées avant ouverture des réponses. Le protocole initial est au commit local `8395f34`, l’extension à Celse au commit `f760fb8` et ses prévisions au commit `fe0521b`. Les lots réservés concernent cette campagne. Certains feuillets étaient connus des recherches antérieures. Les vérifications indépendantes ont été effectuées par des agents IA distincts à partir des mêmes éditions. Une expertise humaine des lectures et une preuve historique de traduction restent à établir.
