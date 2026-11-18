# Une instruction de six mots est-elle répétée dans trois notices ?

« De foliis ejus tritis factum cataplasma », « un cataplasme fait de ses feuilles broyées », est un vers identique de la bétoine, du pavot et du pastel dans l’édition du *Macer*. La suite exacte se retrouve aux vers **433, 1062 et 1768**. Dans les paragraphes des grandes plantes du Voynich, les deux transcriptions et les deux traitements des espaces permettent d’observer **2 388 fenêtres de six mots**. Aucune ne reparaît intégralement sur un second feuillet. Le protocole conditionnait l’essai des valeurs de signes à une telle reprise. Il ne fournit donc aucun candidat de six mots à déchiffrer. [Prédiction et limites](PROTOCOLE.md) · [Vers du Macer](../../2026-11-18-opcheor-paralleles/latin/vers.tsv) · [Données détaillées](resultats.json)

| Longueur en mots | Voynich, dans une ligne, ≥2 / ≥3 feuillets | Voynich, lignes franchissables, ≥2 / ≥3 feuillets | *Macer*, dans un vers, ≥2 / ≥3 notices | *Macer*, vers franchissables, ≥2 / ≥3 notices |
|---|---:|---:|---:|---:|
| 2 | 270 / 78 | 301 / 87 | 957 / 344 | 1 045 / 365 |
| 3 | 9 / 0 | 9 / 0 | 291 / 54 | 321 / 60 |
| 4 | 0 / 0 | 0 / 0 | 83 / 12 | 96 / 14 |
| 5 | 0 / 0 | 0 / 0 | 29 / 7 | 37 / 9 |
| 6 | 0 / 0 | 0 / 0 | 15 / 5 | 21 / 6 |
| 7 | 0 / 0 | 0 / 0 | 6 / 3 | 12 / 3 |
| 8 | 0 / 0 | 0 / 0 | 3 / 2 | 9 / 2 |

Le Voynich fournit 1 569 lignes P0 de la section H sur 128 faces de **64 feuillets numérotés**. Chaque séquence est comptée une fois comme forme. Un même feuillet compte pour une seule unité quelle que soit la répartition entre ses faces. Les trois mots `chol chy chaiin` se lisent sur f4r.3 et f47r.3, parmi les neuf suites de longueur maximale sur deux feuillets. La paire `chol daiin` est la plus répandue des suites les plus longues atteignant trois feuillets. Ses 24 occurrences s’étendent sur 18 feuillets. L’identité du même référent biologique sur ces feuillets reste inconnue. [Transcription de Takahashi](https://www.voynich.nu/data/IT2a-n.txt) · [Transcription de Zandbergen et Landini](https://www.voynich.nu/data/ZL3b-n.txt)

Sur les données latines, huit est la borne supérieure de recherche et plusieurs suites l’atteignent. Par exemple, *a medicis datus est gradus huic in utroque* se lit aux vers 340 (*Apium*), 627 (*Pulegium*) et 717 (*Acidula*). Aucune borne supérieure sur les répétitions plus longues du poème n’a été estimée. Les vers de ce poème formulé en hexamètres et les lignes graphiques du manuscrit ne sont pas des unités de même nature. [Texte historique et provenance de l’édition](../../2026-11-18-opcheor-paralleles/latin/SOURCE.md)

## Sensibilité à l’édition et au volume

Pour les suites qui peuvent traverser un changement de ligne, Takahashi donne seul 17 triplets sur deux feuillets et aucun sur trois. Zandbergen–Landini en donne 11 sur deux et aucun sur trois avec les blancs douteux joints, 21 sur deux et un sur trois avec les blancs séparés. Ce dernier est `s aiin daiin` à cheval sur f39r.13–14, f52v.10–11 et f55r.3–4. Takahashi donne respectivement `saiin`, `sols.aiin` et `saiin` à gauche de la coupure. La suite de trois mots dépend de la transcription. Aucune des quatre lectures ne fait apparaître quatre mots répétés entre deux feuillets. Dans la seule édition ZL on compte entre 5 032 et 5 682 fenêtres de six mots avec franchissement de ligne. Dans IT on en compte 7 153. Le consensus n’en conserve que 2 388. En limitant la recherche à l’intérieur d’une ligne, le consensus n’en conserve que 864. [Résultats par transcription](resultats.json)

Le *Macer* fournit 13 582 fenêtres de six mots en franchissant les vers dans une notice. Dans un second essai, nous avons tiré sans remise **2 388 fenêtres du poème** dans ce total. Sur 1 999 tirages, 1 232 gardent une suite de six mots dans au moins deux notices, **69 gardent une suite dans trois notices**, et 17 gardent la formule des feuilles dans ses trois notices. La probabilité combinatoire exacte de garder ses trois occurrences particulières sous ce tirage est 0,543 %. L’échantillonnage réduit artificiellement la couverture du poème et ne reproduit ni la disposition des lignes ni le regroupement réel des lacunes du Voynich. Il montre quantitativement pourquoi une instruction même réellement présente peut cesser d’être détectable sur trois notices. [Contrôle fixé après les premiers dénombrements](COMPARAISON-VOLUME.md) · [Programme](compter.py)

## Comment vérifier le décompte

Le code réemploie le lecteur IVTFF qui contrôle les empreintes des deux transcriptions. Un mot alternatif, douteux ou contenant une ligature balisée est écarté. Une note éditoriale attachée à un tracé exclut également le mot concerné. Les ruptures physiques, les frontières explicites de paragraphe, le changement de page ou une interruption de la succession des lignes coupent la fenêtre. Lorsqu’on traverse une ligne, les positions relatives doivent autoriser la continuité. Un espacement horizontal signalé par le localisateur « = » l’interrompt. Pour une suite commune, les mots et le locus de chacun doivent s’accorder. Les rangs des mots dans leurs lignes peuvent différer quand une virgule antérieure est séparée au lieu d’être jointe. Parmi les occurrences ayant les mêmes mots et les mêmes loci, la plus faible multiplicité des quatre traitements est conservée. La copie de 1478 sert à vérifier la prédiction de la notice d’ortie et le calcul des six mots dans trois notices porte sur l’édition numérisée. [Format IVTFF](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf) · [Vérification photographique de l’ortie](../temoin/RAPPORT.md)

Pour régénérer le tableau des résultats, lancer `python3 -B compter.py` depuis ce dossier.
