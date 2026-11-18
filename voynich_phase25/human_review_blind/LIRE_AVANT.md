# Lecture indépendante — formulaires vierges

Ce paquet est destiné à un nouveau lecteur qui n’a pas consulté les résultats, les réponses de l’assistant ou les correspondances texte–dessin. **Aucune lecture humaine n’a encore été effectuée.** Le nombre de cartes est fixé ; ne pas éliminer une carte parce qu’elle paraît peu intéressante.

1. Ouvrir `index.html` localement, puis les PNG natifs si nécessaire. Aucune connexion, installation ou envoi automatique n’est nécessaire.
2. Lire `FEATURES.json` : les trois profils ont chacun douze traits dans un ordre fixé. Les définitions anglaises sont normatives. 1 = présence visible ; 0 = absence visible lorsque la partie pertinente peut être jugée ; champ vide / JSON null = inconnu, jamais zéro par défaut.
3. Remplir l’un des deux formats : les trois CSV ou `annotations_blank.json`. Ajouter nom/pseudonyme, date, qualité et observations. Respecter les unités focales indiquées ; un fragment voisin ne fournit pas les traits du motif.
4. Garder l’orientation livrée : gauche/droite et hauteur des mains se jugent sur l’image sans rotation. Ne pas déduire le sens d’un mot, une espèce, un usage ou une grossesse d’une ressemblance.
5. Ne consulter ni transcriptions, ni pages originales, ni moteurs de recherche, ni résultats du test pendant cette passe. Signaler toute reconnaissance d’une page, tout texte identifiable et toute expérience préalable du manuscrit dans `recognized_source_or_text`. Des fragments de glyphes peuvent subsister : le masquage n’est pas un aveugle strict.
6. Remettre les formulaires terminés au responsable du projet, qui en conserve une empreinte SHA-256 et une date avant de montrer des correspondances ou scores. Aucun envoi n’est exécuté par ce paquet.

Les 35 cartes ont été choisies et découpées par un opérateur déjà exposé au manuscrit. Certains cadres et masques coupent des détails ; la reconnaissance d’une page par sa forme reste possible. Une carte contient uniquement un contexte collectif sans unité individuelle assurée : laisser les traits inconnus. L’indépendance concerne votre codage, pas la constitution initiale de l’échantillon.

Après scellement de cette première passe seulement, une seconde passe vérifie les rattachements sur les images originales avec les formulaires séparés du paquet de rattachement. Ces deux lectures ne prouvent pas qu’une inscription désigne l’objet voisin.

Crédit des images : Yale University Library, Beinecke MS 408. Recadrages exacts et masques blancs ; aucune restauration de contours. Les SHA-256 des PNG sont dans `cards_index.json`.
