# Audit statique des convolutions à contexte nul

Statut : **observation du code et des paramètres enregistrés seulement**. Aucun
modèle exécuté pour cet audit, aucune source ou copie runtime modifiée, aucun
gain de temps mesuré. Ce document est un supplément d'analyse après le gel de
la phase 51 ; il ne change ni ses cinq entraînements ni son protocole.

Le code inspecté est `j-luo93/xib`, branche `tacl`, commit
`50dd1d4133ad154d89f37c476ad7a4adff06e970`. Les références de lignes ci-dessous
désignent les fichiers exacts dans `upstream/xib/xib/`.

## Paramètres réellement enregistrés

Les fichiers `runs/51001/train/native/MODEL_INPUTS.json` et
`runs/51002/train/native/MODEL_INPUTS.json` ont été lus sans charger de
checkpoint. Ils enregistrent tous deux :

| Paramètre | Valeur commune |
| --- | --- |
| `cfg`, `use_new_model` | `FinalNon`, `true` |
| `context_weight` | `0.0` |
| `anneal_context_weight` | `false` |
| `start_context_weight`, `end_context_weight` | `0.0`, `0.0` |
| `use_base_embedding`, `dense_embedding` | `true`, `true` |
| `dim`, `feat_groups` | `100`, `pcv` |
| `dropout`, `g2p_window_size` | `0.5`, `3` |
| `optim_cls`, `learning_rate`, `aligner_lr` | `sgd`, `0.2`, `0.2` |
| `max_grad_norm` | `1.0` |
| `num_steps`, `num_rounds`, `char_per_batch` | `3000`, `1`, `80` |
| `use_feature_aligner`, `input_format`, `span_candidates` | `false`, `text`, `all` |
| `saved_model_path` | `null` |
| Taille du lexique effectivement préparé | 166 formes IPA |
| Unités connues / inconnues, avec DELETE | 29 / 25 |

La graine enregistrée est respectivement 51001 et 51002. SHA-256 des deux
documents lus :

- 51001 : `8d47f4f7afc70c28e394839aca61c8001e381f074e34a7870d3e7270678739cb`
- 51002 : `4f54addb7801d97bf282869777400dfe659a3cd554965ff38e2cb699d04f1ae2`

Ce constat confirme la configuration déclarée. Il ne constitue pas une mesure
des gradients ou du temps d'exécution des essais en cours.

## Calcul exécuté et contribution aux coûts

`cfg.py:247–263` définit `context_weight=0.0`, `dim=100` et
`use_new_model=True` ; `FinalNon` en hérite à `cfg.py:274–282`. Les embeddings
denses concatènent leurs groupes de traits dans `model/modules.py:149–168`.
Pour cette configuration, `model/extract_model.py:137–139` fixe la dimension
effective à `7 * dim`, soit **700**, et non 100.

Les deux `Conv1d(700, 700, 3, padding=1)` sont créées à
`model/extract_model.py:155–157`. `_get_repr` reconstruit les représentations de
tout le lexique à chaque appel (`247–257`), puis exécute sans condition les deux
convolutions et les deux dropout (`260–265`). Ce calcul ne dépend pas seulement
du nombre de caractères du minibatch source.

Dans `ExtractModelV2`, le résidu est :

```
before + normalize(after, dim=-1) * g.emb_norm * g.context_weight
```

Il apparaît à `model/extract_model.py:862–866`. Les deux sorties de contexte
passent par ce résidu pour les coûts de substitution et d'insertion (`868–876`).
Lorsque les valeurs et dérivées intermédiaires sont finies et que
`g.context_weight` vaut exactement zéro, leur **contribution directe aux coûts
et à la dérivée de la perte par ce chemin est nulle**. Les autres chemins des
embeddings phonétiques et de l'aligneur restent actifs.

Cette conclusion concerne la branche V2 réellement utilisée. Elle ne doit pas
être étendue automatiquement à l'ancienne classe `ExtractModel`, aux autres
modes de combinaison, ou à une configuration dont le contexte serait actif.

Avec 166 formes, une longueur IPA maximale de 9, 700 canaux entrants et
sortants et un noyau de 3, le compte nominal pour les deux convolutions avant
est :

```
2 * 166 * 9 * 700 * 700 * 3 = 4 392 360 000 MAC
```

Un MAC signifie ici une multiplication-accumulation. Ce compte dense inclut le
travail nominal sur le padding ; il n'est ni un comptage des instructions
effectivement exécutées par le backend, ni une durée. Il exclut biais,
dropout, normalisation et rétropropagation. Il motive une expérience de
performance, sans donner un facteur d'accélération garanti.

## Pourquoi une suppression simple ne serait pas équivalente

1. **RNG pendant le passage avant.** `get_known_unit_emb` applique un dropout
   (`model/extract_model.py:222–243`, particulièrement `227`). Après les deux
   dropout des convolutions, V2 appelle `get_alignment()` (`884`). Celui-ci
   rappelle `get_known_unit_emb` (`298–301`) : supprimer les deux tirages de
   contexte déplacerait le RNG avant la matrice d'alignement du même pas, et
   avant les pas suivants. Le nombre d'éléments seul ne prouve pas qu'un appel
   de remplacement consomme exactement le même état RNG sur le même backend.
2. **RNG à l'initialisation.** Les convolutions sont initialisées avant les
   embeddings de base (`model/extract_model.py:155–169`), dont les matrices
   denses sont initialisées aléatoirement (`model/modules.py:134–146`). Retirer
   les modules du constructeur changerait les paramètres initiaux utiles. Les
   conserver maintient aussi les noms et dimensions du `state_dict`.
3. **Gradients nuls contre gradients absents.** Couper un graphe peut remplacer
   un gradient tensoriel nul par `None`. Le code applique le clipping à tous
   les paramètres avant `optimizer.step()` (`training/trainer.py:324–330`).
   Il faut vérifier le même ensemble de gradients, les mêmes groupes de
   paramètres et l'état de l'optimiseur ; une égalité mathématique ne prouve
   pas une égalité bit à bit de l'accumulation flottante et du clipping. Le
   gestionnaire inclut les convolutions dans le groupe non-aligneur
   (`training/manager.py:403–406`).
4. **Valeurs non finies.** `0 * NaN` n'est pas zéro. Une optimisation qui évite
   le calcul pourrait masquer une défaillance numérique du natif. Les tests
   doivent vérifier la finitude des sorties originales et des gradients, et
   ne pas annoncer une équivalence universelle hors de ce domaine.
5. **Artefacts de diagnostic.** Les histogrammes des deux représentations de
   contexte sont écrits à `training/trainer.py:263–271`. Les remplacer par des
   constantes changerait les traces, même si les prédictions étaient égales.
   Les matrices exportées par `get_alignment()` ne consomment pas directement
   ces représentations, mais dépendent des paramètres appris et, en mode
   entraînement, du RNG conservé.

## Première comparaison prudente, non exécutée

Le premier candidat doit **conserver tout le passage avant natif** : mêmes
modules, initialisations, convolutions, dropout, valeurs et représentations
retournées. Après `_get_repr`, détacher uniquement `known_ctx_repr` et
`known_ins_ctx_repr` du graphe de rétropropagation ; conserver sans changement
`known_unit_emb` et `lost_unit_emb`. Il ne s'agit pas encore de supprimer les
convolutions avant, ni de modifier le calcul des coûts. Les histogrammes et
consommations RNG avant devraient alors rester observables à l'identique.

Le candidat détaché peut produire `None` pour les quatre gradients des
convolutions. Une variante visant l'équivalence stricte devra matérialiser des
gradients nuls correspondants avant le clipping, uniquement après avoir établi
que les gradients natifs sont bien nuls. Cette matérialisation et son ordre
font partie du candidat à contrôler, pas d'une équivalence présumée.

Plan borné proposé pour un essai futur, distinct des résultats de phase 51 :

1. Attendre un créneau libre. Ne jamais dépasser **deux entraînements ou
   validations d'entraînement simultanés** ; ne pas démarrer ce test à côté des
   deux essais actuellement actifs. Les cinq runs de phase 51 restent natifs
   et inchangés.
2. Figer un wrapper candidat séparé, ses hashes, l'environnement et les règles
   de comparaison. Ne modifier ni `upstream` ni `runtime`. Utiliser uniquement
   des données d'apprentissage, sans ouvrir les cognats ou les résultats de
   réserve pour choisir les conditions du test.
3. Charger un même état initial local autorisé dans deux processus isolés, ou
   restaurer exactement les mêmes paramètres et états RNG. Utiliser les mêmes
   minibatches, états d'optimiseur et valeurs des paramètres globaux ; conserver
   deux threads CPU. Fixer à l'avance les graines 51001 et 51002, sans choisir
   celle qui s'accorde le mieux.
4. Comparer d'abord **un pas**, puis **dix pas consécutifs** sans synchroniser
   artificiellement les paramètres après chaque pas. Capturer avant/après :
   états RNG Python/NumPy/Torch, représentations, coûts `sub`/`ins`, matrice
   d'alignement, pertes, gradients par paramètre avant et après clipping,
   présence de gradients `None`, norme de clipping, paramètres et état de
   l'optimiseur. Vérifier la finitude de toutes les valeurs inspectées.
5. Exiger l'égalité bit à bit pour annoncer une trajectoire identique sur ces
   essais. Si elle échoue, conserver tous les écarts absolus/relatifs, identifier
   leur origine et parler au plus d'une proximité numérique explicitement
   bornée, jamais d'une équivalence acquise. Ne pas élargir une tolérance après
   lecture des résultats pour rendre le test positif.
6. En mode évaluation, comparer les mêmes checkpoints sous les mêmes paramètres
   finaux : matrices exportées et axes, scores, spans et cibles IPA. Les deux
   trajectoires d'entraînement peuvent seulement être comparées ainsi après
   les vérifications précédentes.
7. Mesurer ensuite le temps et la mémoire, sur les mêmes données et avec un
   nombre de répétitions fixé. Si le détachement passe, l'évitement des
   convolutions avant avec préservation démontrée du RNG sera une **seconde
   modification séparée**, pas une extension silencieuse du premier test.

Aucun résultat de ce futur test n'est disponible. Même une accélération
équivalente confirmée sur ce domaine ne constituerait pas une validation
linguistique ou une traduction du manuscrit.

## Empreintes des sources inspectées

| Fichier sous `upstream/xib/xib/` | SHA-256 |
| --- | --- |
| `model/extract_model.py` | `1f0a14a12cac454dc6001319753e3b683a9542013262a4aef56ded96ec840b8a` |
| `model/modules.py` | `dfe7e7bbe23df0c3821849fe6e58b3227b024a0b64f8a0cb4d9098bf2573142d` |
| `training/trainer.py` | `31f89728f104d8a144c56ab46bb1d02a6dbae9b52fea9339fda46425c49fc22b` |
| `training/manager.py` | `1f0edf4f68f881f2385c752b9659437ce49a97e7b9d55e9a1bfa6f68ffbb75f4` |
| `cfg.py` | `7bf034a0d68fde30aade18f91cedf74e616c8c5c202aee155abb680b973aa3e0` |
