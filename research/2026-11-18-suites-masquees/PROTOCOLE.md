# Prédire un groupe caché à partir d’une suite répétée

Protocole du 18 novembre 2026, fixé avant le dépouillement. On cherche si deux voisins graphiques permettent de retrouver exactement un troisième groupe sur un autre feuillet du Voynich.

## Transcriptions et séparation des feuillets

Le premier calcul utilise les graphies simples identiques dans les relevés de Takahashi (IT 2a) et de Zandbergen–Landini (ZL 3b), en notation EVA. Le calcul croisé utilise des couples composés de cette lecture EVA et de la graphie v101 relevée au même rang par Claston (GC 2a). Répéter un couple dans deux passages exige que la même forme revienne dans chacune des deux notations. Nous n'imposons aucune correspondance de lettres entre les alphabets. [Catalogue des sources](https://www.voynich.nu/transcr.html)

| Fichier | SHA-256 |
|---|---|
| IT2a-n.txt | 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5 |
| ZL3b-n.txt | bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc |
| GC2a-n.txt | b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f |

Les feuillets 1, 14, 18, 19, 23, 49, 84 et 102 sont écartés des deux lots, car ils ont déjà servi d'exemples dans nos échanges. Le numéro N regroupe recto, verso et panneaux dépliants. Pour tous les autres, le SHA-256 de la chaîne UTF-8 `voynich-suites-v1|folio|N`, interprété comme un entier non signé en ordre grand-boutiste, affecte à la réserve les numéros de reste zéro modulo quatre. Les autres vont à l'apprentissage. Le partage porte sur des feuillets numérotés, sans prétention d'indépendance entre pages du même cahier ou les deux moitiés d'un bifeuillet. Le projet a déjà utilisé ces transcriptions.

On retient la prose IVTFF de type P0. Il faut pouvoir aligner les lignes IT et ZL au même identifiant avec le même nombre de groupes, sans virgule d'espace incertain, coupure de dessin ou champ vide. Seules les balises de début et de fin de paragraphe sont retirées. Un signe ambigu rend le groupe indisponible pour son calcul tout en conservant sa place. Le calcul EVA accepte seulement les lettres minuscules a–z en accord entre IT et ZL. Le calcul croisé demande en plus une ligne GC alignable de la même façon, et pour chaque groupe une graphie GC ASCII alphanumérique, casse conservée. Les caractères spéciaux de v101 sont donc exclus de cette épreuve. Un alignement ordinal entre alphabets peut encore se tromper si deux différences de segmentation se compensent.

Dans chaque ligne de réserve, toutes les positions d'indice i (base zéro) telles que `i % 5` égale le SHA-256 entier de `voynich-suites-v1|ligne|IDENTIFIANT` modulo cinq sont cachées. Les trois lectures du groupe sont retirées ensemble, y compris si un lecteur avait laissé un doute. Le modèle reçoit les positions visibles et des cases vides. Le dépouilleur conserve à part les lectures qui serviront au score. La sélection travaille sur la segmentation disponible. Elle ne garantit pas que tous les centres choisis seront lisibles.

## Apprentissage et annonces

Pour chacun des deux calculs on inventorie les suites de trois groupes consécutifs lisibles dans une même ligne. Chacun des trois peut être caché. Un cadre est défini par les deux groupes qui restent et par leurs places, par exemple `A B □`, `A □ C` ou `□ B C`. Chaque complétion est comptée une fois par numéro de feuillet où elle apparaît, même en cas de nombreuses répétitions sur la même page.

Pour remplir une case en réserve, une complétion doit être attestée sur au moins deux feuillets d'apprentissage distincts et sur strictement plus de feuillets que toute autre complétion du même cadre. Une égalité laisse le cadre sans proposition. Si plusieurs cadres proposent des formes différentes pour la même case, on s'abstient. L'annonce donne le groupe entier, la place et au moins deux témoins d'apprentissage. La réponse du calcul croisé doit être exacte dans les deux alphabets.

Le protocole, les programmes et les prévisions seront enregistrés dans Git avant la notation. Avant l'ouverture du corrigé, on présentera une prévision identifiable, choisie sans regarder la réponse. Priorité au calcul croisé, puis au calcul EVA si le croisé ne donne aucune annonce. On prend le premier emplacement par numéro de feuillet, identifiant de ligne en ordre lexical et indice.

## Vérification

On comptera séparément les masques lisibles, les annonces, les succès exacts, les erreurs, les désaccords non notables et les abstentions. Une forme témoin, la plus fréquente dans l'apprentissage de chaque calcul, sera notée exactement aux mêmes positions vérifiables. Pour un second témoin, les réponses de toutes les cases masquées lisibles seront redistribuées 5 000 fois sur leur propre face et selon leur position (début, intérieur ou fin de ligne). Les annonces restent fixes. Graine 20261118 pour chaque calcul. On donnera la moyenne des succès de ces permutations et la proportion corrigée des tirages au moins aussi bons. Ce contrôle conserve certaines propriétés locales, sans modéliser tous les mécanismes d'écriture. Les analyses EVA et croisée portent sur le même manuscrit et se recouvrent. Une réussite est une restitution graphique. Aucune langue ou traduction n'entre dans le test.
