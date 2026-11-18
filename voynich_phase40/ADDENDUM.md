# Complément de périmètre, après les résultats

Le protocole figé sélectionne les marqueurs littéraux `@Ls` dans f68r1, f68r2 et f68r3. Cela produit 58 loci par transcription. L'examen de la sortie montre que six légendes supplémentaires de f68r3 portent les marqueurs `=Ls`, `+Ls` et `*Ls`, qui conservent le même type `Ls` mais expriment d'autres positions dans un groupe.

Le supplément `complete_labels.py` ajoute donc f68r3.14, .16, .17, .19, .20 et .21. Les sources, la clé, les règles d'admission et les résultats figés ne changent pas. Le résultat complet de 64 loci est conservé séparément dans `results/all_star_labels.json`, explicitement marqué comme postérieur aux résultats. Ce complément élargit l'inventaire ; il ne répare pas un critère de déchiffrement.

Deux sorties complètes s'ajoutent dans chaque source : f68r3.14 donne `ocare` depuis `otary` dans ZL et `ocore` depuis `otory` dans IT ; f68r3.20 donne `tarall` depuis `darall`. Aucun sens n'est proposé. Chaque décodage admissible est comparé à celui du solveur original et les 128 enregistrements sont reproduits lors de la réexécution.

Le contrôle de style global initial a signalé les fins de ligne CRLF et des espaces déjà présents dans les quatre interlinéaires tiers. Leurs octets sont conservés. Les contrôles de style du code et de la documentation du projet excluent ces sources ; aucun contenu source n'est normalisé pour effacer l'avertissement.
