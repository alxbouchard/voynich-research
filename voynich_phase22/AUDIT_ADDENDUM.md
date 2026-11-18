# Addendum d'exécution du vérificateur

Après le calcul des douze nouveaux contrôles, le premier lancement de
`src/verify.py` a échoué avant de vérifier une sortie. La dépendance partagée
`phase22lib` place le dossier de phase 21 en tête des chemins Python ;
`import study` dans le vérificateur figé chargeait donc le programme de phase 21.
Il cherchait alors le fichier inexistant `voynich_phase22chemin-local/closed_solver`.

La correction est limitée au nouveau lanceur `src/run_verification.py` :
il charge explicitement `voynich_phase22/src/study.py` avant d'exécuter le
vérificateur figé, dont les octets et les assertions restent inchangés.
Le protocole, les paramètres, les sources, les passages, les clés, les modèles,
les solveurs et les résultats ne sont pas modifiés. Aucune nouvelle recherche
de clé n'est effectuée pour cette correction de lancement.

Cette intervention est postérieure à l'observation des résultats et est
déclarée comme telle ; elle n'est pas incluse dans le gel `9f96418`.
Le rapport et les figures sont également générés après l'expérience.
