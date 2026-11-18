# À quelle fréquence la table proposée ferait-elle lire un début ātl ?

Les valeurs que Tucker et Janick donnent aux signes transcrits `o`, `k` et `t` impliquent que toute légende commençant par les unités `o k` ou `o t` produira les lettres *ātl* au début du mot. Le calcul dénombre cette conséquence indépendamment des espèces végétales proposées. Les deux suites apparaissent dans chacun des six contextes. [Table et prédictions du projet](../PREDICTIONS.md) · [Définition des types d’inscription dans IVTFF, p. 22](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf#page=22)

| Emplacement | Inscriptions brutes | Un seul groupe admissible | `ok` | `ot` | Début *ātl* selon la table |
|---|---:|---:|---:|---:|---:|
| Fragments de plantes (Lf) | 193 | 130 | 21 | 25 | 46/130 |
| Étoiles (Ls) | 76 | 48 | 8 | 11 | 19/48 |
| Figures zodiacales (Lz) | 299 | 171 | 55 | 44 | 99/171 |
| Récipients pharmaceutiques (Lc), lignes d’un même récipient réunies aux trois endroits précisés ci-dessous | 36 | 18 | 3 | 3 | 6/18 |
| Figures des bains (Ln), en gardant les 20 légendes distinctes répertoriées sur f75v | 63 | 47 | 11 | 8 | 19/47 |
| Cuves, conduits et autres éléments des bains (Lt) | 47 | 31 | 7 | 10 | 17/31 |

Chaque mot doit être entier, unique dans son inscription et identique au même lieu dans Takahashi et Zandbergen–Landini sous les deux traitements du blanc douteux. Chaque inscription donne au plus une observation. Les limites concernent l’écriture transcrite, les figures de zodiaque peuvent elles-mêmes porter une étoile, et la classe Lt comprend d’autres éléments que les seules cuves. Le préfixe est compté en EVA avec les bancs conservés. Ainsi `ockh` commence par les unités `o` et `ckh`. La classe des récipients est Lc. Le code Lp est réservé aux grandes plantes de l’herbier. [Mots retenus à chaque lieu et dénominateurs](resultats.json)

Les deux lignes de l’étiquette du fragment f99r.6–7 ont été réunies comme dans l’inventaire antérieur du projet. Pour les récipients, le comptage principal réunit les deux lignes de f89r2.29–30, les trois de f102r2.13–15, et les deux du récipient 214, f102v2.1–2. À raison d’une observation par ligne IVTFF, on retrouve 40 lieux de récipients, 21 mots admissibles, 4 débuts `ok` et 3 débuts `ot`. Pour les sept loci de f68r3.15 et suivants, le signe de localisation `+`, `*` ou `=` marque la disposition relative des inscriptions. Le catalogue compte les légendes des différentes étoiles de ce secteur séparément. En restreignant la série aux deux panneaux de f68r1 et f68r2 où chaque étoile a sa légende, on retrouve 16 débuts sur 39 inscriptions utilisables pour 53 emplacements. [Catalogue du cahier 9](https://www.voynich.nu/q09/index.html#f68r3) · [Cahier 19 et récipients](https://www.voynich.nu/q19/index.html)

À f75v.18–37, le catalogue compte vingt légendes disposées en dix paires. Le commentaire de la transcription envisage aussi dix inscriptions de deux mots. En réunissant les deux lignes de chaque paire, la ligne du tableau sur les figures des bains devient 53 inscriptions brutes, 29 groupes utilisables, 10 débuts `ok` et 6 débuts `ot`, soit 16/29. Les deux lectures conduisent à la présence de la suite calculée dans les bains et dans les autres sections. [Description de f75v](https://www.voynich.nu/q13/index.html#f75v) · [Transcription ZL et commentaires](https://www.voynich.nu/data/ZL3b-n.txt)

Ce décompte compare trois signes de la table publiée. La segmentation de la sortie *ātl…* en un véritable mot ou morphème « eau », et le caractère aquatique de la plante du fragment 140, demanderaient des preuves distinctes. Pour reproduire les données depuis ce dossier, exécuter `python3 -B compter.py`. [Programme](compter.py)
