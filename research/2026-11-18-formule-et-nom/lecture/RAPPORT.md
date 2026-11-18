# Une prédiction de lecture sur les six mots de f89v2.9

Dans les deux éditions, la ligne se termine par **`dal chody cheor chey qoaiin chody`**. Le groupe `chody` est aussi le second terme d’une légende du même panneau. Posons deux correspondances quelconques pour `chody cheor`. Si chaque signe conserve sa valeur, le mot suivant `chey` est alors entièrement déterminé pour chaque table. La fin de la ligne donne un deuxième contrôle indépendant de la valeur des signes : la même forme `chody` revient. [Page et agrandissements](../../2026-11-18-cheor-en-contexte/images/F89V2.md) · [Protocole](PROTOCOLE.md)

La comparaison parcourt **122 632 fenêtres** de six mots. Elle respecte les limites de notices et de fragments des éditions de calcul. Elle peut traverser une ponctuation moderne. Pour chaque paire en deuxième et troisième positions, le programme apprend toutes les correspondances possibles, sans regarder les quatre autres mots. Le premier modèle donne une valeur non vide d’une à deux lettres à chaque signe, puis autorise trois lettres. Dans le second, le `ch` commun en tête des groupes est traité comme une marque initiale sans lettres propres. Le choix de ce second modèle a suivi l’échec du premier et a été enregistré avant son propre calcul. [Définition de la variante](VARIANTE.md) · [Sources des corpus](../../2026-11-18-phrase-et-doublets/lecture/RESULTAT.md) · [Source française, feuillet 17](../../2026-11-18-opcheor-paralleles/francais/RAPPORT.md)

| Corpus | Fenêtres | Amorces compatibles avec ch à valeur écrite non vide, 2 / 3 lettres au maximum | Amorces compatibles avec ch sans lettres, 2 / 3 | Mot prédit effectivement présent |
|---|---:|---:|---:|---|
| Macer latin | 13 582 | 17 / 62 | 119 / 550 | 0 |
| Celse latin | 97 632 | 118 / 340 | 1 110 / 3 775 | 1, variante sans lettres, maximum 3 |
| Gart allemand de 1485, douze ouvertures | 148 | 0 / 0 | 0 / 1 | 0 |
| RIDGES, six extraits germaniques | 11 188 | 4 / 20 | 235 / 419 | 0 |
| Livre français des simples, trois passages | 82 | 0 / 0 | 1 / 3 | 0 |

Les nombres d’amorces sont des nombres d’emplacements. Plusieurs tables peuvent convenir au même endroit. Aucun des deux modèles ne retrouve les six mots avec la répétition correcte. Le contrôle déplaçant les lettres de la prédiction de ch-e-y à ch-y-e n’obtient lui non plus aucun troisième mot juste. Le contrôle déplaçant la répétition du dernier mot ne fournit aucune fenêtre complète. Une seconde implémentation vérifie directement les trois premiers groupes étudiés par capture des blocs de lettres et références arrière, pour toutes les configurations du tableau. [Prédictions principales](PREDICTIONS.json.gz) · [Prédictions de la variante](PREDICTIONS-MARQUE.json.gz) · [Résultats principaux](VERIFICATION.json) · [Résultats de la variante](VERIFICATION-MARQUE.json)

Une hypothèse plus faible vérifie seulement l’initiale commune des trois mots et la reprise du premier en sixième position. Elle retient quatorze passages, tous dans Celse. Plusieurs comprennent une énumération avec *aut*, « ou ». Aucun ne fournit la fenêtre attendue sous une table fixe. Dans une langue connue, ce motif peut donc provenir de mots de liaison aussi bien que de mots désignant des objets.

## Le candidat allemand et le candidat latin

**Dans le livre allemand de 1482, `chody cheor` peut se lire *seinen samen*, « sa graine ».** Dans le modèle principal à deux lettres au plus, toutes les tables de ce couple prédisent *samen* pour le mot suivant. La photographie de l’incunable, au début du f. 180v, permet de vérifier la suite réelle : *man ſeinen ſamen trinckt mit wein*. Le mot est *trinckt*, « boit ». L’expression botanique convient au sujet qu’on imagine à la vue des plantes, mais la prédiction échoue. [Rubrique, photo et lecture de la ligne](samen/LECTURE.md)

**Dans l’édition de calcul de Celse, la variante à trois lettres obtient un mot juste.** Si `chody cheor` se lit *ulcera cum*, deux tables subsistent. Elles prédisent pour `chey` respectivement *cera* et *cra*. Une seule des deux formes figure dans le vocabulaire de Celse, et *cera* est effectivement le prochain mot dans cet ouvrage. Cela arrive à un seul emplacement parmi les 4 748 amorces admises par cette variante sur les cinq corpus. Le résultat a été choisi parmi de nombreuses comparaisons et la même amorce n’a qu’une seule occurrence dans Celse.

| Contrôle du candidat *ulcera cum cera* | Lecture imposée | Texte ou constat vérifié |
|---|---|---|
| Dernier mot de f89v2.9, retour de `chody` | *ulcera* | Le texte de calcul donne *misy*, premier mot de la phrase suivante de Celse. |
| `dal`, à gauche de la même amorce | Un mot commençant par *lc* | Le texte de Celse porte *purgant*. |
| Lecture sur l’imprimé de Florence (1478) | *cera* ou *cra* | *caera*, cinq lettres visibles. L’imprimé ponctue après *ulcera* et *implent*, puis donne *Myſi*. |
| `otair chody`, sur la légende du dessin 55 | Un des 29 mots de Celse compatibles avec `otair`, puis *ulcera* | Aucun de ces mots ne précède *ulcera* dans les 76 occurrences pourvues d’un voisin gauche. |
| `dar cheor` et `cheor cheekey`, sur f102v2 | *cum* avec un voisin à forme imposée | Aucun mot des 14 015 formes du lexique ne répond à `dar` ni à `cheekey`, pour 383 occurrences de *cum*. |

La table qui produit *cera* impose ch initial silencieux, o = u, d = lc, y = era, e = c, r = m. La suite de Celse change de proposition précisément au milieu des trois mots alignés. La première proposition s’achève avec les plaies, la seconde s’ouvre avec la cire. Le sujet et le contexte médical ne justifient donc pas d’attribuer au Voynich le mot « cire ». [Ligne de l’imprimé de 1478 et ponctuation](cire/LECTURE.md) · [Contrôles fixés sur les autres passages](TRANSFERT.md) · [Concordances](TRANSFERT.json)

## Ce que donne la même table sur quatre autres faces

Les quatre faces f2r, f2v, f3r et f3v contiennent 297 mots de prose concordants. La table lit entièrement **26 occurrences d’au moins trois signes, soit neuf graphies**. Trois de ces graphies sont les correspondances ayant servi à proposer ou retenir la table, pour quatre occurrences. Parmi les six graphies nouvelles, cinq donnent *eraum, eralcera, lcum, culcera, ccera*, absents du corpus. La sixième, `chor`, fournit *um* dix-sept fois.

La liste de mots de Celse semblait contenir *um*. En revenant au XML, on retrouve ses deux seules « attestations » dans **qüum** et **il!um**. Le traitement du caractère ü et du point d’exclamation avait détaché artificiellement la fin de ces mots. Nous avons conservé le calcul originel, réuni *qüum* en *quum* pour cette sensibilité, puis retiré le bloc corrompu *il!um* en conservant une coupure au lieu de lui imposer une lecture. Après correction, **aucune des 22 occurrences nouvelles sur ces quatre faces ne produit un mot attesté dans Celse**. La seule prédiction correcte du mot *cera* dans l’édition de calcul reste la même. Cette correction locale ne remplace pas une réédition intégrale du XML. [Décompte par lieu et résultat brut](TRANSFERT.json) · [Contrôle des formes sur le XML](SENSIBILITE.json) · [Texte de Daremberg encodé par Perseus](https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/669d3657637ee44fb0aed2c37dd0f95c2b062193/data/phi0836/phi002/phi0836.phi002.perseus-lat5.xml)

## Contrôles et reproduction

Sur la première amorce admissible d’un passage authentique du *Macer* chiffré pour l’expérience, le programme retrouve *terendo bibatur* et prédit toutes les lettres de *aut*. Seules dix lettres de la clé sont connues. Le mot suivant *si* reste partiellement lisible. Le texte-source y est dans le corpus et le chiffrement a été choisi par l’expérimentateur. Un second contrôle fabrique la structure des six mots et montre qu’un dernier mot modifié suffit à faire échouer le test malgré une prédiction correcte du troisième groupe. [Conditions et résultats des contrôles](ETALON.md)

Depuis ce répertoire, télécharger le XML (l’empreinte est vérifiée par l’importateur), puis lancer les commandes suivantes. Les prédictions des deux modèles ont été déposées aux commits `a38f399` et `4cc11b0` avant leurs vérifications respectives.

```sh
curl -L --fail -o /tmp/voy-f89-celsus.xml https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/669d3657637ee44fb0aed2c37dd0f95c2b062193/data/phi0836/phi002/phi0836.phi002.perseus-lat5.xml
python3 -B phrase.py predire /tmp/voy-f89-celsus.xml
python3 -B phrase.py verifier /tmp/voy-f89-celsus.xml
python3 -B phrase.py predire /tmp/voy-f89-celsus.xml marque
python3 -B phrase.py verifier /tmp/voy-f89-celsus.xml marque
python3 -B recouper.py /tmp/voy-f89-celsus.xml
python3 -B transfert.py /tmp/voy-f89-celsus.xml
python3 -B sensibilite.py /tmp/voy-f89-celsus.xml
python3 -B etalon.py
```
