# Phase 50 — moteur phonétique retrouvé et exécuté

17 novembre 2026. **NOT_TRANSLATION — aucun passage du Voynich déchiffré.**

La branche `tacl` du dépôt de Jiaming Luo contient un moteur plus complet que les branches précédemment inspectées. Son modèle `ExtractModelV2` fonctionne maintenant sur CPU avec quatre modifications de compatibilité explicites. Trois apprentissages courts sur des mots artificiels ont été exécutés. Ce résultat établit une capacité technique d'exécution ; il ne reproduit pas encore l'expérience linguistique publiée et ne valide aucune traduction.

## Ce qui change par rapport à l'inventaire précédent

Le dépôt `DecipherUnsegmented` fournit surtout une démonstration d'embeddings. Le `master` de `xib` n'était pas toute la publication : la branche [`tacl`, commit 50dd1d4](https://github.com/j-luo93/xib/tree/50dd1d4133ad154d89f37c476ad7a4adff06e970) contient les configurations finales, le modèle V2, l'apprentissage et l'évaluation. Son sous-module `dev_misc` est fixé au commit `8cb3c73bebe444dd22da25e44a3fe05d13aff8c5`. Les 103 fichiers archivés sont identiques à leurs blobs Git.

L'article étudie l'identification de mots apparentés avec segmentation et contraintes phonétiques. Il utilise un lexique d'une langue connue transcrit en IPA, avec des radicaux de référence, et teste aussi la proximité entre langues. Pour Gothic→Old Norse sans espaces ni valeurs phonétiques gothiques fournies, il rapporte A@10 = 0,213. Cette mesure recherche le couple radical–segment parmi dix candidats, avec un critère de préfixe ; ce n'est pas le taux de lettres déchiffrées ni de phrases traduites. [Article, tableau 2 et annexe](https://aclanthology.org/2021.tacl-1.5.pdf).

L'évaluateur de la branche archivée calcule des précisions, rappels et F1 de correspondances. Son paramètre `top_k_predictions` n'a aucun consommateur trouvé dans le code Python inspecté. Nous ne rebaptisons donc pas le F1 natif « A@10 » et ne prétendons pas reproduire le chiffre de l'article.

## Exécution effectivement réalisée

Les modifications sont conservées dans `build_runtime.py` et `COMPATIBILITY.json` : retirer un import CLTK inutilisé, conserver les lots sur CPU, sélectionner les colonnes pandas par liste, désactiver la recherche du commit Git du dossier temporaire. Le calcul de perte, l'optimiseur et les règles de segmentation ne sont pas modifiés. Les sources originales restent intactes. `setup.py` n'est pas exécuté : il référence des extensions absentes et inutilisées par le parcours testé.

Environnement observé : Python 3.9.6, PyTorch 2.8.0, pandas 1.5.3, deux fils CPU. Les versions effectivement importées sont archivées. La sélection pandas par liste évite une ancienne syntaxe dépréciée ; elle n'était pas une exigence de pandas 1.5.3. Le petit environnement temporaire réutilise des paquets système : aucune installation entièrement indépendante n'est revendiquée.

Le protocole technique est écrit et haché avant les trois lancements. Chaque lancement conserve sa commande, sa configuration résolue, ses journaux, ses prédictions et ses poids initiaux/finals. Il ne s'agit pas d'un préenregistrement externe.

Le jeu artificiel contient 16 mots distincts sur neuf caractères, répétés une fois dans un autre ordre : 32 occurrences, 174 caractères, réunies en 16 séquences. Le lexique connu contient les 16 mots. Les signes du côté inconnu sont permutés ; aucune table de correspondance n'est fournie au modèle. Les coupures internes restent présentes dans les lignes et objets du corpus, mais ne sont pas utilisées pour proposer les segments (`span_candidates=all`). Ces choix rendent l'essai délibérément petit et favorable, sans valeur linguistique historique.

Trois variantes, même graine et cinq étapes chacune :

| Variante | Modification des entrées | Ce qui doit rester identique |
|---|---|---|
| A | Annotations de correspondances d'origine ; IPA inconnue factice composée de `a`. | Référence technique. |
| B | Rotation des réponses connues dans les annotations. | Texte observé, lexique et apprentissage. |
| C | IPA inconnue factice remplacée par `i`, à longueur conservée. | Texte observé, lexique et apprentissage. |

Les valeurs phonétiques factices sont un dispositif de contrôle, pas des propositions sur une langue. Le modèle utilise le mode texte et tous les segments candidats. Les trois oracles de valeurs phonétiques/fréquences sont désactivés et aucun checkpoint antérieur n'est chargé. L'audit statique vérifie le trajet des données ; la vérification dynamique compare séparément les trois apprentissages dans `SMOKE_VERIFICATION.json`. Les trois variantes ne modifient pas les frontières des objets mots : elles ne constituent donc pas un test dynamique de leur non-influence.

Les trois processus ont terminé avec succès. La vérification séparée confirme que les 13 tenseurs d'état sont identiques bit pour bit entre variantes, à l'initialisation et à l'étape 5. Huit tenseurs, soit 835 valeurs, ont effectivement changé pendant l'apprentissage, dont les 100 poids de `unit_aligner`. Les prédictions et scores sont identiques ; le F1 natif vaut respectivement 0,4375, 0,0625 et 0,4375. La modification des réponses change donc l'évaluation sans effet observé sur ces poids appris.

Les mesures natives portent sur le même jeu que l'apprentissage ; aucune réserve indépendante n'est annoncée. Le nom `exact_content` du logiciel n'implique pas des frontières de mots toutes exactes : le comparateur admet un segment préfixe selon ses règles. Aucun taux obtenu ici ne doit être présenté comme une fraction du Voynich décodée. Cette invariance concerne une configuration, une graine et cinq étapes, pas tous les usages possibles du programme.

## Pourquoi l'expérience linguistique n'est pas encore reproduite

Les corpus alignés et lexiques phonétiques requis par `FinalNon` et `FinalUgaReal` manquent dans l'arbre publié. Le miroir Nacryos fournit des matériaux utiles, mais pas les fichiers gothique/vieux norrois transformés attendus.

Le fichier ougaritique/hébreu de l'auteur a été récupéré et vérifié au blob près : 4 535 lignes de données hors en-tête, dont 221 contenant les deux langues, 514 seulement l'ougaritique et 3 800 seulement l'hébreu. Il compte 735 formes ougaritiques et 4 103 formes hébraïques distinctes. Les lignes ne sont pas autant d'inscriptions ou de phrases. [Source primaire et format](https://github.com/j-luo93/NeuroDecipher/tree/480bad2487820e3737fecfdd108214efa769e34b/data).

Ce fichier appartient au parcours ACL 2019 et n'est pas le TSV phonétique TACL 2021. La conversion documentée de sa notation hébraïque ASCII vers l'IPA n'a pas été retrouvée dans les sources examinées. Aucune valeur phonétique n'a été inventée pour remplir cette lacune. `prepare_uga.py` produit seulement un inventaire vérifiable.

## Portée et suite

Le moteur publié n'est plus simplement une piste bibliographique : son apprentissage a été exécuté et les dépendances aux annotations sont testables. Il reste à établir un corpus linguistique et un lexique phonétique de provenance vérifiable, puis une calibration à valeurs inconnues avec données réservées et contrôles négatifs. Une reconstruction de données devra être distinguée d'une reproduction exacte de l'article.

Le Voynich n'a pas été fourni à ce moteur. Aucune langue, clé, prononciation ou traduction nouvelle n'est validée. L'objectif de déchiffrement reste ouvert.
