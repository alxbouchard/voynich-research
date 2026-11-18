# Peut-on lire les amorces de f43 dans une langue vernaculaire ?

Les lettres EVA sont des noms de signes. Sur les deux faces du feuillet 43, nous avons demandé à une même clé de lire `dshedy qotedy` et `dshedy tedy`, puis de prédire le prochain groupe entier. **Aucune prédiction n’atteint le mot suivant, ni au recto ni au verso.** Une formule plausible en italien du XVe siècle aboutit à une nouvelle prédiction au feuillet 75, qui échoue elle aussi.

## Les deux mots connus donnent beaucoup de lectures

Nous avons cherché dans deux chapitres médicaux en français du *Régime du corps* (œuvre du XIIIe siècle), le *Viandier* dans son témoin français du XVe siècle et le *Libro de arte coquinaria* de Maestro Martino. Les deux derniers recueils fournissent des instructions vernaculaires de la période. Seul le premier échantillon traite des bains ou d’hygiène. Le français de ces témoins ne couvre ni toutes les orthographes ni tous les genres du XVe siècle. [Transcription du Régime](../../2026-11-18-gestes-des-bains/francais/TRANSCRIPTION.md) · [Édition du Viandier](https://histolf.ulb.be/index.php/textes-gh/260-1450-viandier-taillevent-ms-vaticane-texte-et-traduction) · [Édition de Martino](https://www.uni-giessen.de/de/fbz/fb05/germanistik/absprache/sprachverwendung/gloning/tx/martino2.htm)

| Témoin | Mots examinés | Couples avec préfixe | Clés de 1–2 lettres par signe, communes aux deux faces | Clés par blocs | Clés par blocs après mélange, médiane [min–max] |
|---|---:|---:|---:|---:|---:|
| Régime du corps | 1 494 | 22 | 0 | 5 | 4 [0–10] |
| Viandier | 12 844 | 225 | 0 | 24 | 58 [39–76] |
| Martino | 27 048 | 1 062 | 0 | 72 | 146 [118–184] |

Un couple rapproche deux passages réels du même ouvrage. Le premier mot est commun et le deuxième contient exactement la forme courte à sa fin. Dans le calcul par blocs, le `d` initial est muet, les racines `sh` et `t` peuvent porter jusqu’à huit lettres chacune, `edy` transmet une terminaison, et `qo` un préfixe. Cette latitude admet aussi bien *maladies froides / maladies des* que *eaue froide / eaue de*. Dans chacun des 99 mélanges des deux livres de cuisine, la même règle trouve davantage de clés que dans l’ordre authentique. Le moteur retrouve bien les mots réservés de témoins connus artificiellement recodés. Les limites, l’échantillonnage et le découpage des apostrophes sont documentés dans le protocole et le code. [Protocole](PROTOCOLE.md) · [Annonces initiales](ANNONCES.json.gz)

## Le troisième groupe tranche au feuillet 43

| Position réservée | Graphies annoncées par une clé commune | Observé dans les deux transcriptions |
|---|---|---|
| f43r.9, après `dshedy qotedy` | `tedy`, `shedy`, `edy` | `dor` |
| f43v.13, après `dshedy tedy` | `shedy`, `qot`, `qotedy`, `qo` | `ckhedy` |

Les clés ajustées sur une seule face ajoutaient deux possibilités au recto, `td` et `ey`, également écartées. Nous avons ensuite permis aux signes nouvellement rencontrés de recevoir des valeurs. Six clés distinctes s’ajustent alors aux trois groupes des deux faces, toutes chez Martino. Elles recouvrent trois familles de lectures. La première associe les formes italiennes de « susdit » (*preditte/ditte*), suivies de *cose* ou *zucche* au recto. Une autre associe *in niun loco / in un bon*. La dernière donne *ma falla cocere / ma la sua*. Les passages complets, numérotés dans l’édition, sont conservés dans les résultats. Cette opération a utilisé les mots à expliquer. [Résultats au feuillet 43](OUVERTURE.json)

Le couple *in niun loco / in un bon* existe jusque sur les deux faces du feuillet 46 d’un témoin de Martino, daté vers 1460–1480 par la Library of Congress. Au recto, il est question de garder la pâte d’un beignet sans aucun trou. Au verso, les herbes d’une omelette cuisent dans du bon beurre. Les valeurs `sh=i`, `t=u`, `edy=n`, `qo=ni` donnent les deux débuts. Sur `dor`, trois partages de *loco* sont possibles. Une autre édition imprime *niuno*, ce qui retire l’emboîtement exact de *un*. Ces passages montrent concrètement comment deux contextes historiquement authentiques et différents réalisent le même motif. [Clichés rapprochés](martino-f46.jpg) · [Notice du manuscrit](https://www.loc.gov/item/2014660856/) · [Folio 46 recto](https://tile.loc.gov/storage-services/service/rbc/rbc0001/2017/2017medren60856/0095.jp2) · [Folio 46 verso](https://tile.loc.gov/storage-services/service/rbc/rbc0001/2017/2017medren60856/0096.jp2) · [Variante dans l’édition AtLiTeG](https://corpus.atliteg.org/testi/libro-de-arte-coquinaria/109)

## Nouvelle épreuve au feuillet 75

En retirant f43 et les huit recettes italiennes ayant servi à l’ajustement, les six clés, appliquées sans modification, fournissent en tout 84 positions de paires entièrement lisibles dans le Voynich, dont 73 avec troisième groupe comparable. **Une seule position correspond à une paire attestée** parmi les 25 842 mots italiens réservés. En f75r.11, `shedy dor` se lit, suivant la clé, *le cose*, *le zucche* ou *in loco*. Les vraies continuations du témoin ne sont encodables par aucune de ces clés. Chaque clé réussit cependant un contrôle positif sur un trigramme véritable de Martino composé avec ses seules valeurs. [Prévision du transfert](TRANSFERT-AVANT.md) · [Annonces](TRANSFERT-ANNONCES.json.gz) · [Ouverture](TRANSFERT-OUVERTURE.json.gz)

Le troisième groupe est `chekam`. Lui donner cinq nouvelles valeurs permet *le cose sopraditte*, *in loco frescho* et *in loco fresco*, et élimine toutes les suites de *le zucche*. Douze clés sont désormais compatibles. Deux attentes précises en découlent pour les mots suivants. Après *le cose sopraditte*, l’italien fournit *le quali*, ce qui annonce `shedy` au rang 4. Une occurrence de *in loco fresco* fournit *perche s’…*, ce qui annonce `a` au rang 5. Le second résultat dépend du traitement éditorial de l’apostrophe. [Annonce avant vérification](F75-AVANT.md) · [Clés et prédictions](F75-ANNONCES.json.gz)

Le groupe `chekam` clôt le tronçon de f75r.11. À l’intérieur de cette ligne, ces deux prédictions sont donc impossibles à évaluer. Nous avons consigné, avant de lire f75r.12, l’hypothèse distincte d’une continuation dans l’ordre des lignes de transcription. On trouve `ssheckhy qokal` aux rangs 4 et 5 dans les quatre traitements de transcription et d’espaces. **Les deux annonces échouent avec cette hypothèse.** Les groupes figurent de part et d’autre du dessin, ce qui laisse ouverte leur continuité syntaxique. Les coordonnées des deux détails du cliché natif ont été retrouvées par alignement du visualiseur sur l’image de Yale (erreur au 95e percentile d’environ 4 px). [Critère avant ouverture](CHANGEMENT-DE-LIGNE.md) · [Résultats](CHANGEMENT-RESULTATS.json) · [Détails du manuscrit](f75r-suite.jpg) · [Original de Yale](https://collections.library.yale.edu/iiif/2/1006208/full/full/0/default.jpg)

Ailleurs, après retrait des deux feuillets et des douze recettes désormais utilisées, les clés étendues peuvent lire 1 328 positions de paires dont 1 034 ont un troisième groupe alignable. La seule paire italienne retrouvée est *le soe* pour `shedy chedy`, à cinq endroits. Aucun troisième mot n’est prédit. Cette expérience exclut les lectures continues testées selon les règles décrites. Le rôle du premier `d`, l’italien, le français et le contenu des illustrations restent des questions ouvertes. [Résultats après transfert](F75-ANNONCES.json.gz)

## Reproduction

Depuis ce dossier, télécharger les deux pages HTML du *Viandier* et de Martino liées plus haut. La transcription du *Régime* et les deux éditions du Voynich sont présentes dans ce dépôt. Les empreintes des sources normalisées sont incluses dans les annonces. Exécuter dans cet ordre avec Python 3.

```sh
python3 -B essayer.py /chemin/viandier.html /chemin/martino.html
python3 -B ouvrir.py
python3 -B transferer.py annoncer /chemin/martino.html
python3 -B transferer.py verifier
python3 -B suivre.py annoncer /chemin/martino.html
python3 -B suivre.py verifier
python3 -B enjambement.py
```

Pour recomposer les planches, placer les scans 0095 et 0096 (Martino) et le cliché de Yale f75r dans un répertoire sous les noms `voy-d-martino-0095.jp2`, `voy-d-martino-0096.jp2` et `voy-d-f75r-n.jpg`. Exécuter `python3 -B planche.py /chemin/des/scans` avec Pillow.
