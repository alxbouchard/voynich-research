# Phase 51 — prolongation séparée du budget de calcul

**Préparation administrative, sans lancement au moment de sa rédaction.**
`PREPARATION_RECORD.json` conserve ce constat historique ; il ne sera ni supprimé
ni transformé en autorisation. L’état réel ultérieur sera enregistré dans
`CHECKED_LAUNCH_STATE.json`, `ORCHESTRATION.json` et les dossiers `runs/`.
La campagne initiale reste intacte.
Cette variante administrative conserve le modèle natif, les données, les cinq graines,
les 3 000 pas, l’inférence et l’évaluateur. Elle porte seulement le plafond de chaque
apprentissage de 3 600 à 10 800 secondes. Le plafond des inférences reste 300 secondes.
Le délai total du lanceur est ajusté en conséquence.

La décision vient du temps observé (environ 44 minutes pour 1 400 pas), sans choix
fondé sur la réserve ou des scores linguistiques. Les cinq graines redémarreront de
leur initialisation propre. Aucun poids partiel ou préfixe du banc ne sera repris.
Les essais initiaux et leurs interruptions éventuelles seront conservés séparément ;
leurs résultats ne seront pas mélangés à cette campagne. Le critère sera calculé
uniquement si les cinq nouveaux essais terminent réellement les 3 000 pas et leurs
inférences initiales/finales. Un dépassement reste un calcul incomplet.

Le banc de détachement des contextes est indépendant. Même s’il réussit sur dix pas,
son candidat ne sera pas adopté dans cette campagne. Aucune équivalence sur
3 000 pas n’est supposée.

Avant tout lancement : vérifier la fin des deux drivers initiaux, conserver le gel
des trois graines encore en attente, arrêter leur ordonnanceur sans worker actif,
attendre et auditer la fin du banc, puis figer et auditer cette copie. Au maximum
deux jobs de modèle au total.

L’entrée usuelle unique est désormais le lanceur administratif séparé :

```sh
chemin-local/python launch_checked.py --execute
```

Cette commande est une instruction pour un lancement futur, pas une exécution
effectuée par cette préparation. Sans `--execute` ou sans gel valide, elle refuse
avant de lancer un enfant. Il ne faut pas lancer directement `run.py` ou
`orchestrate.py`, qui conservent volontairement leur code scientifique audité.

`launch_checked.py` authentifie le gel, les 240 fichiers inchangés et les trois
fichiers de l’amendement relus dans `AUDIT_RESOURCE_AMENDMENT.json`. Il exige un
dossier `runs/` encore absent, le maintien du HOLD initial, les deux RUN initiaux
terminaux avec leurs JOB cohérents, un waiter du banc terminal et tous les
RUN/ACTIVE_JOB du banc terminaux. Un JSON incomplet ou un refus de lecture bloque
le lancement. Aucun `os.kill` n’est utilisé pour supposer qu’un PID est mort.

L’arrêt réel de l’ancien ordonnanceur doit être documenté après retour de son outil
dans `../voynich-phase51-iecor/SCHEDULER_STOP_RECORD.json`, avec `status: stopped`,
`scheduler_sha256` égal à l’ancien `orchestrate.py`, un `session_id` non vide et le
`session_exit_code` entier effectivement observé. Ce reçu administratif n’est pas
fabriqué par le lanceur. Il ne remplace pas les contrôles des RUN et JOB.

La revue effective du banc doit également être inscrite dans
`../voynich-phase51-iecor/BENCH_REVIEW_RECORD.json` : `status: reviewed`,
`optimization_adopted: false` et `waiter_state_sha256` égal à l’empreinte de son
état terminal courant. Le lanceur authentifie ce reçu sans choisir une variante
du modèle à partir des résultats.

Trois verrous `fcntl` exclusifs sont conservés pendant la supervision : celui de
cette campagne, celui du waiter initial, puis celui du banc. Cet ordre évite de
perturber un waiter encore actif. Le lanceur attend son enfant sans relancer un
essai. Une interruption de l’attente ou une sortie de l’ordonnanceur laissant des
workers non résolus conserve les verrous et inscrit l’incertitude dans l’état de
supervision. Une intervention externe doit établir leur état réel ; aucun statut
de fin n’est inventé. Le plafond de deux nouveaux drivers reste celui du scheduler.
Un SIGINT reçu pendant le lancement ou la supervision est signalé sur stderr et
enregistré ; il ne vaut pas constat de fin des workers. Si l’utilisateur demande
explicitement l’arrêt, root doit arrêter les processus réels et vérifier leurs
journaux avant de fermer la supervision. La garde ne remplace pas ce traitement.

Ces contrôles organisent les lanceurs coopérants du projet : ils ne constituent
pas une sandbox globale du système et n’empêchent pas une invocation directe qui
les contournerait, ni une terminaison forcée du superviseur par le système.
`test_launch_checked.py` vérifie les refus et les verrous avec des fichiers
temporaires et des processus simulés, sans modèle.

Les scripts scientifiques et les 240 fichiers originaux autres que le protocole et
le driver sont identiques octet pour octet au gel initial. `ORIGINAL_FREEZE.json`
et `ORIGINAL_PROTOCOL.json` conservent ce référentiel. Les autres fichiers du dossier
sont des suppléments administratifs. Aucune traduction n’est produite ici.
