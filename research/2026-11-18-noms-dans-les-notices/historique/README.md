# Macer Floridus, témoin des reprises de noms de plantes

Les 40 notices consécutives du *De viribus herbarum* totalisent 3 875 mots dans les extraits retenus. Le relevé de lecture situe une forme du même nom dans les onze premiers mots de chacune. La première occurrence a une graphie identique à la rubrique dans 15 notices. En étendant la recherche à l’intégralité de l’extrait, 19 notices contiennent la graphie identique. Ces deux constats montrent à quel point les débuts de chapitre de cet ouvrage favorisent une reprise rapide.

| Lot | Notices | Mots du corps | Extraits de moins de 100 mots | Graphie identique présente | Première occurrence identique |
|---|---:|---:|---:|---:|---:|
| Apprentissage, positions 1–20 | 20 | 1 974 | 1 | 8 | 7 |
| Validation, positions 21–40 | 20 | 1 901 | 3 | 11 | 8 |

## Sources et transmission

Le poème latin en hexamètres date de la fin du XIᵉ siècle et est traditionnellement attribué à Odon de Meung. Le calcul porte sur l’édition avec traduction de Louis Baudet publiée par Panckoucke à Paris en 1845, transcrite par Corpus Corporum puis diffusée sur Wikisource en latin. La révision figée porte le numéro **272959**. Le numéro romain **V** est répété en tête de la sixième rubrique, *Plantago*. Le fichier conserve la graphie source du numéro et lui adjoint sa position ordinale. [Édition dans le catalogue collectif de France](https://ccfr.bnf.fr/portailccfr/jsp/index_view_direct.jsp?record=bmr%3AUNIMARC%3A8820188) · [Transcription figée](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&oldid=272959) · [Contributeurs Wikisource](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&action=history)

Wellcome MS.458, copié en Italie en 1478, donne un point de comparaison manuscrit. Il contient 78 notices dans un ordre différent. Le catalogue signale au f. 2r l’incipit de page *Dicitur absinthii*. Le détail des deux nouvelles prédictions de graphie et de leur confrontation aux images figure dans `RESULTAT_MS458.md`. La photographie d’un autre exemplaire à Dresde, un imprimé illustré daté de 1501–1506, permet de voir des bois du cerfeuil et de l’arroche aux ff. 27v–28r. La rubrique *De atriplice herba* figure au bas de la page gauche et la forme *Atriplicem* sous le bois de la page droite. Le calcul utilise les rubriques de l’édition de 1845. [Manuscrit Wellcome](https://wellcomecollection.org/works/cfqd658f) · [Photographie et notice de la SLUB de Dresde](https://www.slub-dresden.de/besuchen/ausstellungen-corty-galerie/archiv-der-ausstellungen/ausstellungen-2020/bluehende-buecher/macer-floridus-1501-1506)

## Lecture de quelques formes

- *Absinthium* donne *absinthii*, génitif singulier dans la description de ses propriétés. Cette graphie se retrouve au f. 2r de MS.458. [Fac-similé Wellcome](https://iiif.wellcomecollection.org/image/b19209113_ms_458_0007.JP2/full/1600,/0/default.jpg)
- *Lilium* et *lilia* opposent le singulier et le pluriel du neutre. *Cepa* donne dès le deuxième mot *cepis*, ablatif pluriel après *de*.
- *Atriplex* donne *attriplicem*, avec le radical oblique en *-plic-* et un second *t* dans la transcription du vers. Une comparaison limitée aux quatre premières lettres manque cet exemple. [Chapitres de l’édition](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&oldid=272959)
- Un rapprochement de lettres peut aussi produire des faux amis. Dans la notice *Artemisia*, *Artemis* désigne la divinité. Dans la notice *Serpillum*, *serpat* est un verbe dans une explication étymologique. Le sémantisme de ces formes exclut de les compter comme des flexions du nom de plante. [Texte latin](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&oldid=272959)

## Reproduction

Le fichier `PROTOCOLE.md` consigne la sélection fixée avant calcul. `extract.py` vérifie l’empreinte de la source, conserve l’ordre et retire les en-têtes ainsi que les numéros de vers. L’entrée du score est `corpus.jsonl`, avec les champs `label`, `tokens`, `id` et `split`. Les autres champs documentent la rubrique originale et le nombre de mots total dans la notice. Le fichier annexe `premieres_formes.tsv` contient la première occurrence relevée par lecture en contexte après constitution du corpus. Les scripts d’extraction et de score n’en ont pas besoin. Le témoin mesure ici le comportement de noms développés dans l’édition et une relecture séparée établit la graphie manuscrite dans trois lieux seulement.

```sh
python3 extract.py
python3 -B verify.py
```

La révision originale complète réside dans `source.wiki.gz`. Son empreinte ci-après porte sur les octets décompressés. Source SHA-256 `41ca63622e4fbcc4f52c40d7c9261541c5b6d24ee59ebb2964ece69cee480e26`. Corpus JSONL SHA-256 `ab401a75ae802158f96fa5d9daa4b2ff09958f1dc9e6a1ad79bccef82fdf5e43`.

## Crédits de réutilisation

Macer Floridus, *De viribus herbarum*. Texte de la révision 272959 de Wikisource en latin, d’après l’édition Panckoucke et Corpus Corporum, Université de Zurich. Le texte ancien et son édition imprimée sont du domaine public. La page de transcription Wikisource porte la mention CC BY-SA 4.0 et sa source désignée, Corpus Corporum, annonce une réutilisation pour la recherche non commerciale avec attribution et partage à l’identique. Les modifications du corpus dérivé sont la sélection, le découpage, la minuscule, l’enlèvement des diacritiques et des balises, et l’ajout des identifiants et métadonnées. [Attribution et licence affichée sur Wikisource](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&oldid=272959) · [Dépôt Corpus Corporum](https://mlat.uzh.ch/) · [Licence CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
