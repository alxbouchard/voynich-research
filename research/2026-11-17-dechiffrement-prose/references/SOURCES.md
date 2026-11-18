# Corpus de comparaison indépendant

Les trois œuvres ont été choisies pour leur genre et pour l’accès à un texte édité. La personne chargée de constituer ce corpus n’a consulté aucune transcription ni aucun résultat du manuscrit étudié. La règle de sélection était fixée avant l’extraction. Chaque suite commence au premier chapitre de fond et s’arrête après 256 mots, ou au dernier mot du chapitre lorsqu’il est plus court. Les titres, les prologues et les tables ne comptent pas. Les œuvres couvrent un herbier en vers et deux traités médicaux en prose.

| Œuvre | Étendue exacte | Texte utilisé | Témoin de circulation au XVe siècle |
|---|---|---|---|
| Macer Floridus, *De viribus herbarum* | I, *Artemisia*, vers 1–30, 184 mots | [Transcription de l’édition indiquée comme Panckoucke, révision 272959](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&oldid=272959) | [British Library, Harley MS 2651](https://searcharchives.bl.uk/catalog/040-002048482). Le copiste date son travail de 1448. |
| Celse, *De medicina* | I, premier chapitre numéroté, §§ 1–5, 212 mots | [Charles Victor Daremberg, Leipzig, Teubner, 1891, XML Perseus figé](https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/669d3657637ee44fb0aed2c37dd0f95c2b062193/data/phi0836/phi002/phi0836.phi002.perseus-lat5.xml) | [University of Glasgow, incunable de Florence, 1478](https://www.gla.ac.uk/myglasgow/incunabula/a-zofauthorsa-j/c27/) |
| Aldebrandin de Sienne, *Le Régime du corps* | Première partie, *De l’air*, 256 premiers mots | Landouzy et Pépin, Paris, H. Champion, 1911. Lecture sur les fac-similés des [pages 11](https://fr.wikisource.org/wiki/Page:Aldebrandin_de_Sienne-Le_r%C3%A9gime_du_corps,_1911.djvu/101) [et 12](https://fr.wikisource.org/wiki/Page:Aldebrandin_de_Sienne-Le_r%C3%A9gime_du_corps,_1911.djvu/102) | [Description des manuscrits par les éditeurs](https://fr.wikisource.org/wiki/Le_R%C3%A9gime_du_corps/Introduction), à la notice « OXFORD, Bodley 179 ». |

Les éditions des XIXe et XXe siècles déterminent la forme des mots comparés. Les cotes et incunables attestent la circulation des œuvres. Une confrontation lettre à lettre avec ces témoins pourrait donner des variantes.

## Reproduction

Dans ce répertoire, exécuter `python3 build.py` avec Beautiful Soup 4 et lxml. Le script lit les fichiers conservés dans `sources/` et reconstruit `corpus.json` sans connexion réseau. La transcription française s’appuie sur la lettrine, les espaces et les lectures visibles du fac-similé. Elle réunit les mots coupés en fin de ligne, retient les mots du texte principal signalés par des crochets et retire l'appareil de bas de page. Le XML de Celse conserve la lecture corrigée des balises `choice` et exclut les notes. Les explicitations de numéros de vers de Macer sont retirées.

Chaque empreinte textuelle dans le JSON est le SHA-256 d’une ligne UTF-8 NFC formée des mots dans l’ordre, séparés par une espace simple, et terminée par un saut de ligne LF. L’orthographe de chaque édition et sa casse figurent dans le champ `tokens`, y compris les chiffres romains textuels. Les apostrophes intérieures sont unifiées en apostrophes droites. Une normalisation supplémentaire pour une méthode de déchiffrement devra s’appliquer de la même manière à toutes les œuvres concernées.

Le corpus représente trois débuts de chapitres. Il ne permet pas d’épuiser les formes du latin ou de l’ancien français, ni leurs variantes manuscrites.
