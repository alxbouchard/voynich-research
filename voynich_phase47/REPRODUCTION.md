# Reproduction de la phase 47

Python 3.9 ou ultérieur, bibliothèque standard. Depuis la racine du dépôt :

```sh
python3 voynich_phase47/src/analyse.py
python3 voynich_phase47/src/verify.py
python3 voynich_phase47/src/replay.py
```

Le premier programme lit uniquement les formes U/P/S de la table et les chaînes transcrites. Il n'utilise aucune correspondance de lettre claire, aucun dictionnaire ni modèle de langue. L'automate admet les concaténations arbitraires, puis leurs sous-chaînes.

Le contrôle séparé reconstruit les mêmes résultats par segmentation dans le dictionnaire explicite des jetons. Le terme Fact(A) est inclus pour les fragments commençant et finissant dans un seul jeton. Les rejets et la minimalité des témoins sont contrôlés indépendamment. Les cas jouets vérifient notamment les frontières ouvertes et les caractères hors alphabet.

Le rejeu copie les onze entrées figées, FREEZE.json et le vérificateur dans un dossier neuf. Il exige onze sorties identiques à l'octet. Aucun réseau, amélioration d'image, recherche de clé ou hypothèse linguistique ne participe au rejeu.

[Contrôles](results/CONTROLS.json) · [Vérification indépendante](results/verification.json) · [Rejeu](results/replay.json). Les contrôles de format concernent nos fichiers ; les avis et espaces des sources tierces restent inchangés.
