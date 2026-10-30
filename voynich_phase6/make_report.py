#!/usr/bin/env python3
"""Evidence-led report. All numerical tables read verified experiment outputs."""
import json, html
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
S=json.loads((ROOT/'results/summary.json').read_text());A=json.loads((ROOT/'results/adjacency_summary.json').read_text())
R=json.loads((ROOT/'results/constrained_real_summary.json').read_text())
REFERENCES=[
('Yale, Beinecke Library','Notice du manuscrit MS 408','https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript','Notice institutionnelle consultée. Identification de l’objet et accès aux reproductions. Les intitulés des sections illustrées ne sont pas des traductions.'),
('McCrone Associates, 2009','Materials Analysis of the Voynich Manuscript, projet MA47613','https://library.yale.edu/sites/default/files/2026-06/voynich_analysis.pdf','Rapport original du 1er avril 2009. Pages 1 et 2 examinées visuellement : prélèvements et méthodes analytiques. Les autres pages n’ont pas fait l’objet d’une revue complète ici.'),
('Lisa Fagin Davis, 2020','How Many Glyphs and How Many Scribes? Digital Paleography and the Voynich Manuscript','https://doi.org/10.1353/mns.2020.0011','Manuscript Studies 5(1), 164-180. Notice et résumé consultés, avec le compte rendu institutionnel de Yale de 2024. Attribution de cinq mains proposée par une étude paléographique ; aucune expertise indépendante menée ici.'),
('Claire Bowern et Luke Lindemann, 2021','The Linguistics of the Voynich Manuscript','https://doi.org/10.1146/annurev-linguistics-011619-030613','Annual Review of Linguistics 7, 285-308. Résumé éditeur consulté. Revue linguistique qui maintient l’hypothèse d’un contenu linguistique ; ni langue ni lecture déduites pour notre étude.'),
('Luke Lindemann et Claire Bowern, 2020, révision 2021','Character Entropy in Modern and Historical Texts: Comparison Metrics for an Undeciphered Manuscript','https://arxiv.org/abs/2010.14697','Prépublication, version 2. Résumé et présentation des corpus consultés. Comparaisons stratifiées par transcription, variété et main ; prévisibilité inhabituelle des caractères malgré des regroupements de signes.'),
('Sravana Reddy et Kevin Knight, 2011','What We Know About The Voynich Manuscript','https://aclanthology.org/W11-1511/','Actes du workshop LaTeCH, 78-86. PDF consulté, notamment introduction et sections sur la transcription et les vocabulaires A/B. Point de départ méthodologique ; ses informations historiques doivent être vérifiées par les sources matérielles.'),
('Marcelo A. Montemurro et Damián H. Zanette, 2013','Keywords and Co-Occurrence Patterns in the Voynich Manuscript: An Information-Theoretic Analysis','https://doi.org/10.1371/journal.pone.0066344','PLOS ONE 8(6), e66344. Texte accessible ; résumé et introduction examinés. Les auteurs interprètent l’organisation lexicale à grande distance en faveur d’un message. Cette interprétation n’est pas un déchiffrement.'),
('Torsten Timm et Andreas Schinner, 2019/2020','A possible generating algorithm of the Voynich manuscript','https://doi.org/10.1080/01611194.2019.1596999','Cryptologia 44(1). Résumé et dépôt des auteurs consultés. Échantillon publié dans TorstenTimm/SelfCitationTextgenerator analysé ici ; générateur non réexécuté. Un modèle de copie et modification ne prouve pas le procédé historique.'),
('Daniel E. Gaskell et Claire Bowern, 2022','Gibberish after all? Voynichese is statistically similar to human-produced samples of meaningless text','https://github.com/danielgaskell/voynich','Actes de l’International Conference on the Voynich Manuscript. Résumé et documentation du dépôt des auteurs lus. Ressemblances avec des productions humaines sans sens ; corpus non téléchargé ni réanalysé dans cette phase.'),
('Michael A. Greshko, 2025','The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext','https://doi.org/10.1080/01611194.2025.2566408','Cryptologia. Notice/résumé et implémentation publique utilisée dans les phases antérieures. Construction démonstrative, non clé du manuscrit. Le fichier chiffré déjà produit sur Pline sert de témoin descriptif ici.'),
('George Lasry, 2024','Deciphering Historical Syllabic Ciphers','https://doi.org/10.58009/aere-perennius0106','Notice institutionnelle de l’Université de Tartu et extraits indexés consultés. Téléchargement du PDF en erreur 503. Notre modèle lettres + neuf digrammes ne constitue pas une réplication de sa méthode syllabique historique.'),
('Nils Kopal, 2019','Cryptanalysis of Homophonic Substitution Ciphers Using Simulated Annealing with Fixed Temperature','https://ep.liu.se/en/conference-article.aspx?Article_No=12&issue=158&series=','Actes HistoCrypt. Résumé institutionnel consulté lors de la phase 4. Référence algorithmique pour la recherche de clés ; aucune prétention à reproduire exactement son implémentation.'),
('Nishant Kambhatla, Logan Born et Anoop Sarkar, 2023','Decipherment as Regression: Solving Historical Substitution Ciphers by Learning Symbol Recurrence Relations','https://aclanthology.org/2023.findings-eacl.160/','Findings EACL, 2136-2152. Résumé officiel consulté. Transformer entraîné sur des récurrences de symboles et des chiffres synthétiques. Méthode pertinente pour un comparatif futur, non entraînée ni exécutée ici.'),
('Rod Kinnison, 2026','The Voynich Manuscript’s positional entropy collapse: comparative evidence from languages and ciphers','https://doi.org/10.1080/01611194.2026.2697318','Cryptologia, publication en ligne le 7 septembre. Résumé éditeur uniquement ; accès intégral bloqué. Un chiffre à expansion reproduirait plusieurs profils statistiques. Aucune clé historique récupérée dans le résultat consulté.'),
('Torsten Timm, 2026','The challenge of analyzing a dynamic text: why the Voynich manuscript resists conventional interpretation','https://doi.org/10.1080/01611194.2026.2693462','Cryptologia, publication en ligne le 7 septembre. Résumé éditeur uniquement ; accès intégral bloqué. Argument en faveur d’une évolution du vocabulaire et de l’auto-copie. L’argument de l’auteur n’est pas traité comme un fait démontré.'),
('Xin Zhang et Victor S. Sheng, 2026','Does the Voynich Manuscript Mean Anything? Calibrated Tests Find Little Trace of Language','https://arxiv.org/abs/2610.34499','Prépublication v1 du 25 octobre, sans validation par les pairs établie. HTML consulté, dont sections sur les voisinages et annexe d’implémentation. Le code est annoncé pour une publication ultérieure ; aucune réplication intégrale revendiquée.'),
('Greg Hodgins, NSF-Arizona AMS Laboratory, 2009','Dating Results for Voynich Manuscript Parchment Leaves 8, 26, 47 and 68','https://voynich.nu/papers/Carbon_GH_2009.pdf','Rapport original du 17 février, hébergé sur voynich.nu. Méthodes, conclusion et figure 7 consultées. Intervalle combiné de calibration publié : 1404-1438 à 95,4 %. Il date le parchemin, pas directement l’écriture.')
]
(ROOT/'references/bibliography.json').write_text(json.dumps([dict(id=i+1,author=a,title=t,url=u,access_and_use=n) for i,(a,t,u,n) in enumerate(REFERENCES)],ensure_ascii=False,indent=2)+'\n')
for name,weight in [('DV','normal'),('DVB','bold')]:pdfmetrics.registerFont(TTFont(name,font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight=weight))))
W,H=595.276,841.89;M=44;CW=W-2*M
INK=colors.HexColor('#193039');TEAL=colors.HexColor('#137B80');GREY=colors.HexColor('#53636A');PALE=colors.HexColor('#EAF3F3')
styles={'body':ParagraphStyle('body',fontName='DV',fontSize=10,leading=14.2,textColor=INK,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8.7,leading=12,textColor=GREY),
 'table':ParagraphStyle('table',fontName='DV',fontSize=8.6,leading=11.5,textColor=INK),
 'th':ParagraphStyle('th',fontName='DVB',fontSize=8.6,leading=11.5,textColor=colors.white),
 'h2':ParagraphStyle('h2',fontName='DVB',fontSize=12.3,leading=16,textColor=TEAL),
 'h1':ParagraphStyle('h1',fontName='DVB',fontSize=23,leading=29,textColor=INK)}
path=OUT/'Voynich_phase6_etude_approfondie_2026-10-28.pdf';C=canvas.Canvas(str(path),pagesize=(W,H));C.setTitle('Voynich - étude approfondie et expériences contrôlées, phase 6');C.setAuthor('Analyse assistée par IA, dossier de recherche pour Alex')
page=0;y=0;bottoms=[]
def paragraph(text,style='body',gap=9):
 global y
 p=Paragraph(text,styles[style]);_,hh=p.wrap(CW,1000)
 assert y-hh>49,(page,text[:70],y,hh)
 p.drawOn(C,M,y-hh);y-=hh+gap
def section(text):paragraph(text,'h2',8)
def start(title,kicker='DOSSIER DE RECHERCHE  /  PHASE 6'):
 global page,y
 if page:bottoms.append(y);C.showPage()
 page+=1;C.setFillColor(TEAL);C.rect(0,H-8,W,8,fill=1,stroke=0)
 C.setFont('DVB',8);C.drawString(M,H-34,kicker);C.setFillColor(GREY);C.setFont('DV',8);C.drawRightString(W-M,H-34,'28 OCTOBRE 2026')
 C.setStrokeColor(colors.HexColor('#D8E2E3'));C.line(M,40,W-M,40);C.setFont('DV',7.5);C.drawString(M,27,'VOYNICH · MS 408 · AUCUNE TRADUCTION VALIDÉE');C.drawRightString(W-M,27,str(page))
 y=H-67;paragraph(title,'h1',17)
def table(rows,widths=None):
 global y
 data=[[Paragraph(str(v),styles['th' if i==0 else 'table']) for v in row] for i,row in enumerate(rows)]
 t=Table(data,colWidths=widths or [CW/len(rows[0])]*len(rows[0]),hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#CBDCDD'))]))
 _,hh=t.wrap(CW,1000);assert y-hh>49,(page,'table',y,hh);t.drawOn(C,M,y-hh);y-=hh+14
def f(v,n=2):return f'{v:.{n}f}'.replace('.',',')
start('Décoder le Voynich :\nce que les tests établissent')
paragraph('Une recherche documentaire approfondie, deux expériences nouvelles et leurs fichiers de reproduction. Ce dossier poursuit les phases précédentes sur le manuscrit Voynich, conservé à Yale sous la cote MS 408. Il ne présente aucune traduction comme acquise.')
table([['Travail réalisé dans cette phase','Résultat vérifié'],['17 références principales examinées','Sources matérielles, articles, actes et prépublications ; niveau d’accès indiqué pour chacune.'],['80 exécutions nouvelles du solveur','16 contrôles de calibration, 32 configurations du manuscrit et 32 témoins mélangés.'],['8 jeux de données de voisinage','Deux transcriptions, deux variétés A/B et quatre témoins ; 1 600 randomisations.'],['Audit indépendant des calculs','80 fonctions de score recalculées et 227 810 comparaisons de distance vérifiées.']],[CW*.47,CW*.53])
section('Le résultat principal')
paragraph('<b>Le solveur corrigé sait récupérer les textes témoins, mais ne fournit pas de lecture du manuscrit.</b> Sur les unités tenues à l’écart de l’ajustement, les quatre contrôles latins dépassent 99,85 % de récupération ; les quatre contrôles italiens atteignent 100 %. Ce sont des essais synthétiques ciblés, pas une mesure de capacité générale à lire une écriture inconnue.')
paragraph('Les 32 sorties du manuscrit respectent désormais la segmentation imposée pendant l’ajustement. Quatorze la respectent entièrement sur les feuillets réservés, contre zéro avant correction. Cela corrige un défaut du modèle ; cela ne transforme pas les sorties en latin ou en italien.')
section('La piste à privilégier')
paragraph('Étudier ensemble les signes, les espaces et les voisinages. Dans les deux transcriptions, les dépendances entre la fin d’un mot et le début du suivant persistent après les mélanges de contrôle. Elles peuvent venir d’une langue, d’un codage, d’une convention graphique ou d’un procédé de génération : leur sens reste indéterminé.')
paragraph('Statut : exploration reproductible, non article évalué par les pairs. Les jugements de lisibilité sont une inspection interne, non une validation linguistique aveugle. Les lectures candidates sont explicitement marquées « aucune traduction validée ».','small')

start('Repartir de l’objet et des signes')
section('Ce que les sources matérielles permettent de dire')
paragraph('Le rapport radiocarbone original de Greg Hodgins donne, pour sa calibration combinée, un intervalle de <b>1404 à 1438 à 95,4 %</b>. Il distingue explicitement l’âge du parchemin de la date d’écriture [17]. Cette contrainte historique n’identifie ni une langue ni un système de chiffre.')
paragraph('Le rapport McCrone du 1er avril 2009 décrit des prélèvements et l’emploi de microscopie, de spectroscopie infrarouge, de diffraction X et d’analyse élémentaire au microscope électronique. Les deux premières pages ont été examinées ici [2]. Aucune nouvelle analyse chimique ou multispectrale n’a été réalisée.')
paragraph('L’étude paléographique de Lisa Fagin Davis propose cinq mains [3]. Cette attribution est une donnée de recherche à prendre en compte dans les comparaisons. Un identifiant de main n’est ni l’identité d’un auteur ni la preuve d’une langue distincte. Currier A et B désignent ici des classes de distribution, sans présumer deux langues.')
section('Transcrire, déchiffrer, traduire')
table([['Niveau','Ce qui serait nécessaire','État du dossier'],['Transcription','Relier chaque signe visible à un identifiant et conserver les hésitations.','Transcriptions ZL et IT existantes ; ambiguïtés exclues ou coupures explicites.'],['Déchiffrement','Une règle stable transforme les signes en unités interprétables.','Aucune règle validée sur le manuscrit.'],['Traduction','Une langue et une grammaire justifient le sens des passages.','Aucun passage traduit avec validation.']],[90,211,CW-301])
paragraph('La phase 3 avait aligné 384 loci sur un pilote de 12 pages et examiné huit zones d’image avec l’aide des transcriptions. Les formes <b>okcheor</b>, <b>otcheody</b> et <b>otald</b> restent des points de repère provisoires. Leur signification est inconnue. <b>okols</b> n’est pas retenu comme mot sûr lorsque l’espace est ambigu. Ce travail n’équivaut pas à deux lectures paléographiques indépendantes à l’aveugle.')
paragraph('Une amélioration de contraste peut faciliter l’examen d’encre déjà visible. Une reconstruction générative ne constitue jamais une preuve de la forme originale d’un signe. Une identification supposée de plante ne doit pas fournir arbitrairement le mot à obtenir.','small')

start('Pourquoi la littérature reste divisée')
table([['Famille de travaux','Ce qu’elle apporte','Ce qu’elle ne démontre pas'],['Structure linguistique [4-7]','Prévisibilité des signes, vocabulaires différenciés et organisation lexicale à plusieurs échelles.','Ni langue déterminée ni sens de mots récupéré.'],['Génération par copie [8-9,15]','Des procédés sans message peuvent produire certaines régularités voisines du Voynich.','Que le manuscrit a effectivement été fabriqué ainsi.'],['Chiffres constructifs [10,14]','Un texte porteur de sens peut être transformé en séquences présentant plusieurs propriétés comparables.','Que le procédé proposé est la clé historique.'],['Comparaisons calibrées [16]','Confronter générateurs et chiffres avec contrôles, budget de recherche et observations réservées.','L’exclusion de tous les systèmes possibles.']],[122,192,CW-314])
section('Les publications récentes changent les tests à faire')
paragraph('Deux articles publiés en ligne en septembre 2026 traitent, respectivement, de contraintes de position des signes [14] et d’évolution du vocabulaire [15]. Seuls leurs résumés éditeurs étaient accessibles. Je les utilise pour définir des questions, sans présenter leurs conclusions comme indépendamment vérifiées.')
paragraph('La prépublication de Zhang et Sheng du 25 octobre 2026 compare plusieurs générateurs et chiffres, puis recherche des traces de langue sans déchiffrement. Certains chiffres à clé variable réduisent l’écart avec les modèles de copie. Le code est annoncé pour une publication ultérieure [16]. Notre diagnostic de voisinage ne reproduit pas leur protocole complet, notamment leur test de récurrence des paires de mots entre blocs de pages.')
section('Conséquence pour notre recherche')
paragraph('Une ressemblance statistique peut être produite par des mécanismes différents. Un score favorable doit donc servir à choisir un test supplémentaire. Il ne peut pas attribuer un sens. Le désaccord entre travaux justifie des témoins contradictoires : vrais textes chiffrés, séquences sans message, permutations et données encore non utilisées pour choisir les modèles.')
paragraph('Cette revue est ciblée, non exhaustive. Les 17 références combinent sources institutionnelles, recherches publiées et prépublications. Les niveaux d’accès sont détaillés aux pages 10 et 11 ; « source trouvée » ne signifie pas « étude intégralement répliquée ».','small')

start('Les outils d’un spécialiste, avec leur statut')
table([['Approche','Application dans ce dossier','Suite utile'],['Codicologie et matériaux','Rapports originaux et notice Yale consultés.','Vérifier ordre des cahiers, changements de main et campagnes d’écriture ; accès matériel requis pour de nouvelles analyses.'],['Paléographie et transcription','Pilote visuel antérieur ; comparaison de deux transcriptions ; lectures incertaines signalées.','Double transcription aveugle des zones discriminantes, avec coordonnées et arbitrage documenté.'],['Statistique et théorie de l’information','Fréquences, segmentation, témoins mélangés, distances entre mots, information mutuelle.','Contrôles appariés en longueur et genre, incertitude entre pages et validation externe.'],['Cryptanalyse homophonique','Recherche de correspondances plusieurs signes vers une unité, modèles de langue et calibration.','Élargir au bruit et aux inventaires attestés ; vérifier que les contrôles restent résolubles.'],['Chiffres syllabiques et nomenclateurs','Modèle limité lettres + digrammes exécuté. Travaux historiques consultés [11-12].','Vraies syllabes, abréviations, mots codés et clés par section : essais distincts à préenregistrer.'],['Modèles neuronaux','Méthode de récurrence de symboles étudiée dans la littérature [13].','Entraînement et comparaison sur contrôles seulement ; aucune exécution de Transformer ici.'],['Hypothèse de génération sans message','Analyse d’un échantillon publié de Timm et Schinner.','Réexécuter plusieurs familles et paramètres avec un budget identique aux modèles chiffrés.'],['Validation sémantique','Aucun sens attribué aux formes récurrentes.','Clé figée, prédictions sur pages intactes et examen par lecteurs indépendants.']],[112,193,CW-305])
paragraph('Le choix des outils doit suivre les questions et les contrôles disponibles. Ajouter des familles de modèles augmente aussi la possibilité de trouver par hasard une lecture séduisante. Les essais doivent garder la trace des échecs et des modifications de méthode.','small')

start('Expérience A : corriger le solveur')
paragraph('La phase précédente autorisait une incohérence : une sortie pouvait contenir deux lettres séparées que notre propre règle aurait regroupées en un digramme. La correction impose cette cohérence sur les transitions observées dans les données d’ajustement. Elle n’utilise pas les transitions des feuillets réservés.')
section('Un modèle délibérément limité')
paragraph('Chaque inventaire contient 23 lettres normalisées et neuf digrammes fréquents, soit 32 unités. CV signifie consonne-voyelle, VC voyelle-consonne ; il s’agit de formes orthographiques, <b>pas d’une syllabification linguistique</b>. Les corpus sans espaces peuvent former des digrammes à cheval sur des mots. Plusieurs signes chiffrés peuvent correspondre à la même unité.')
paragraph('Le score combine des séquences de quatre unités et une pénalité sur les fréquences. Chaque étape emploie huit redémarrages et 60 000 propositions par redémarrage. La version corrigée part de la clé apprise en phase 5, la répare, puis la raffine. La vraie clé des contrôles n’est jamais fournie au programme de recherche.')
table([['Contrôles : deux clés par ligne','Unités exactes sur texte réservé','Erreurs par clé','Segmentation réservée'],['Latin CV',f(S['controls'][0]['accuracy']*100,4)+' %','31 / 22 571','100 %'],['Latin VC',f(S['controls'][2]['accuracy']*100,4)+' %','31 / 21 953','99,64 % des segments'],['Italien CV','100 %','0 / 95 503','100 %'],['Italien VC','100 %','0 / 92 993','100 %']],[145,130,102,CW-377])
section('Échecs de calibration conservés')
paragraph('Une première recherche sous contrainte, initialisée par les seules fréquences, échouait sur les contrôles latins VC et italiens CV : environ 10 % de récupération pour les premiers, 62,8 % et 0 % pour les seconds. Le passage par la clé déjà apprise a permis de les résoudre. Ces échecs figurent dans l’archive. L’option de température plus élevée est codée mais n’a pas été exécutée.')
paragraph('La calibration utilise deux clés sur le même texte par modèle, pas huit ouvrages indépendants. Les contrôles sont propres, sans erreurs de transcription ajoutées. Leur réussite ne mesure donc ni la robustesse au bruit ni l’adéquation historique du modèle. Le faible défaut résiduel de segmentation du contrôle latin VC est conservé, sans correction sur le texte réservé.','small')

start('Expérience A : résultat sur le manuscrit')
paragraph('Les 32 configurations croisent deux langues cibles, deux inventaires CV/VC, Currier A/B, EVA brut ou unités composées, et ordre direct ou inversé. Elles utilisent la transcription ZL et les mêmes séparations de feuillets que la phase 5. Chacune possède un témoin aux signes mélangés à l’intérieur des segments, traité avec le même budget.')
rows=[['Modèle cible','Segmentation entièrement cohérente sur réserve','Score min. à max.','Digrammes du meilleur score']]
for k,label in [('latin_CV','Latin CV'),('latin_VC','Latin VC'),('italian_CV','Italien CV'),('italian_VC','Italien VC')]:
 g=S['groups'][k];rows.append([label,str(g['full_canonical_count'])+' / 8',f(g['bits_min'])+' à '+f(g['bits_max']),f(g['best_two_letter_fraction']*100,3)+' %'])
table(rows,[94,157,120,CW-371])
paragraph('Scores en bits par séquence de quatre unités, non en bits par caractère. Ils dépendent de l’inventaire et du modèle de langue : les comparer directement entre latin et italien ne permet pas de choisir une langue. Le « meilleur » score de chaque groupe est sélectionné après consultation des résultats réservés ; il n’est pas une confirmation indépendante.','small')
section('Le problème que le score masque')
paragraph('Les quatre sorties les mieux notées utilisent entre 14 et 16 unités distinctes. Les digrammes y représentent au plus 0,385 % des unités, et zéro pour le meilleur candidat italien VC. La recherche tend donc à contourner l’option syllabique. Une cohérence de segmentation presque parfaite peut être obtenue avec une sortie peu diversifiée.')
paragraph('Exemple de sortie du meilleur score latin VC, sans insertion de mots :<br/><font face="DVB">goareaedomomocolliarimarime<br/>meaedimarimpe<br/>aimeadromimedolmarcolliaromoaeacromacrompoi</font>')
paragraph('Cette séquence n’est pas une traduction. Aucune lecture grammaticale suivie et aucune prédiction sémantique externe n’ont été validées. Les 32 configurations obtiennent un meilleur score que leur témoin mélangé ; un unique mélange par configuration ne fournit cependant pas une distribution d’incertitude, et cet avantage indique seulement que l’ordre des signes compte.')
section('Portée exacte du résultat négatif')
paragraph('Ces essais n’apportent pas de soutien à une lecture par les quatre inventaires testés. Ils ne réfutent ni toutes les langues ni tous les chiffres syllabiques. Le budget de recherche est fini ; les espaces, le bruit, les abréviations et les changements de clé restent insuffisamment modélisés.')

start('Expérience B : les mots voisins')
paragraph('Le test conserve les lignes et les pages des paragraphes dans ZL et IT, puis traite séparément A et B. Une lecture alternative, un signe illisible ou une séparation incertaine crée une exclusion ou une barrière. Aucune paire n’est comptée à travers une barrière ou une fin de ligne.')
section('Deux contrôles par jeu de données')
paragraph('Premier contrôle : mélanger les mots retenus à l’intérieur de leur page. Second contrôle : fixer le premier et le dernier mot retenu de chaque ligne, puis mélanger les positions intérieures dans la page. Chaque condition utilise 100 tirages. Les fréquences par page, les positions disponibles et les barrières sont conservées.')
rows=[['Texte','Mots utilisés','Répétition exacte','Voisin EVA à distance 1','Excès après mélange*']]
labels={'ZL_A':'ZL A','ZL_B':'ZL B','IT_A':'IT A','IT_B':'IT B','Latin_Pliny':'Pline, latin','Italian_Paradiso':'Dante, italien','Naibbe_Pliny':'Naibbe sur Pline','Timm_generated':'Générateur Timm'}
for r in A:
 o=r['observed'];d=r['nulls']['line_ends_fixed']['distinct_edit1_EVA']['observed_minus_mean']
 rows.append([labels[r['case']],f"{r['words']:,}".replace(',',' '),f(o['identical_adjacent']*100)+' %',f(o['distinct_edit1_EVA']*100)+' %',('+' if d>=0 else '')+f(d*100)+' pt'])
table(rows,[110,76,102,119,CW-407])
paragraph('* Différence avec la moyenne des 100 mélanges à extrémités de ligne fixées, en points de pourcentage. Distance 1 : une insertion, suppression ou substitution ; les mots identiques sont comptés séparément. Une mesure supplémentaire en unités composées est conservée dans les résultats.','small')
section('Ce que les témoins révèlent')
paragraph('L’excès de voisins proches apparaît dans ZL et IT, en A comme en B. Il apparaît aussi dans l’échantillon publié du générateur de Timm. Ce signal local peut donc exister sans message à traduire. Les répétitions exactes et les ressemblances à une modification près ne doivent pas être confondues : elles réagissent différemment aux mélanges.')
paragraph('Les quatre témoins sont placés sur une géométrie artificielle de lignes ZL. Dante est tronqué à 32 824 mots sur 33 409 ; Naibbe à 32 824 sur 34 809. Pline et Timm conservent respectivement 8 954 et 10 823 mots. La ligne initiale de Timm issue du manuscrit est retirée, mais le générateur reste conçu et amorcé pour l’imiter. Ces témoins ne forment pas un classificateur universel de langue.','small')

start('La frontière entre deux mots compte')
paragraph('L’information mutuelle mesure ici la dépendance entre la dernière lettre EVA d’un mot et la première du suivant. Elle est calculée sur les paires retenues à l’intérieur des lignes. Le graphique compare la valeur observée à celle des mélanges qui fixent les extrémités des lignes.')
fig,ax=plt.subplots(figsize=(9,4.9));key='last_first_mutual_information_bits'
for i,r in enumerate(A):
 n=r['nulls']['line_ends_fixed'][key];ax.plot([n['p025'],n['p975']],[i,i],color='#98AAAD',linewidth=6,solid_capstyle='round');ax.scatter(n['mean'],i,color='#667B81',s=24,zorder=3);ax.scatter(r['observed'][key],i,color='#137B80' if i<4 else '#B07335',s=52,zorder=4)
ax.set_yticks(range(8),[labels[r['case']] for r in A]);ax.invert_yaxis();ax.set_xlabel('Information mutuelle, en bits');ax.set_xlim(0,.265);ax.grid(axis='x',alpha=.18);ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0);fig.tight_layout()
figpath=ROOT/'results/boundary_information.png';fig.savefig(figpath,dpi=190,bbox_inches='tight');plt.close(fig)
ih=278;C.drawImage(str(figpath),M,y-ih,width=CW,height=ih,preserveAspectRatio=True,anchor='c');y-=ih+8
paragraph('Points colorés : observations. Barres grises : quantiles 2,5 % et 97,5 % des 100 mélanges ; point gris : leur moyenne. Ces barres décrivent les mélanges, pas un intervalle de confiance autour de l’observation.','small')
section('Interprétation circonscrite')
paragraph('L’excès d’information par rapport aux mélanges est d’environ 0,097 bit en ZL A et 0,207 en ZL B ; IT confirme la même direction avec 0,109 et 0,228. Le témoin italien montre aussi une dépendance importante. Ce signal n’est donc pas une signature propre au Voynich ni une mesure directe de sens.')
paragraph('Les échantillons Naibbe et Timm testés n’atteignent pas les valeurs du sous-ensemble B. Cela ne rejette pas ces familles de procédés : un seul texte ou paramétrage a été examiné pour chacun. Il faut expliquer simultanément les voisinages, les frontières, les positions dans la ligne et les changements entre sections.')
paragraph('Toutes ces comparaisons sont exploratoires. Les valeurs p brutes figurent dans les fichiers, sans correction des comparaisons multiples ; aucune probabilité de « présence d’un langage » n’en est déduite.','small')

start('La prochaine recherche doit prédire')
section('Priorité 1 : fixer les signes et les frontières')
paragraph('Constituer un petit ensemble de zones à forte valeur discriminante, relu sans proposition de traduction. Conserver plusieurs transcriptions lorsque nécessaire. Tester ensuite si les dépendances traversant les espaces diminuent avec des regroupements de signes justifiés par les images. Une amélioration obtenue seulement en fusionnant arbitrairement les formes ne serait pas probante.')
section('Priorité 2 : confronter des modèles explicites')
paragraph('Comparer, à budget égal, substitution fixe, chiffre à expansion, nomenclateur, clés par section et génération par copie. Chaque modèle doit produire du texte sur la géométrie du manuscrit. Les règles de changement de clé et le taux d’erreur doivent être pénalisés : autoriser une exception pour chaque difficulté rendrait tout texte explicable.')
section('Priorité 3 : étendre les contrôles historiques')
paragraph('Remplacer le face-à-face César/Pline et Dante par plusieurs auteurs, genres et traditions d’abréviation. Séparer ouvrages d’entraînement et d’évaluation, puis ajouter des erreurs mesurées. Les corpus modernes peuvent aider à construire des méthodes, mais ne suffisent pas à calibrer une lecture médiévale.')
section('Ce qui compterait comme un déchiffrement')
table([['Exigence','Preuve attendue'],['Règles fixées avant le test','Inventaire, segmentation et clé publiés sans ajustement mot par mot.'],['Généralisation','Lecture suivie sur des feuillets jamais utilisés pour choisir les règles.'],['Explication complète','Grammaire, variantes et erreurs documentées ; peu d’exceptions ad hoc.'],['Prédictions externes','Étiquettes, nombres ou relations textuelles prédits avant leur examen.'],['Reproduction indépendante','D’autres lecteurs récupèrent les mêmes passages avec les mêmes règles.']],[145,CW-145])
paragraph('Les feuillets réservés actuels ont déjà servi à comparer plusieurs essais et phases. Ils permettent des diagnostics, mais ne sont plus une réserve totalement intacte pour une annonce finale. Un nouveau lot de confirmation ou une validation externe sera nécessaire.','small')
paragraph('<b>Décision actuelle :</b> poursuivre l’étude des frontières et des modèles concurrents, conserver les résultats négatifs, et ne publier aucune traduction du manuscrit. Le dossier fournit une base contrôlable pour cette suite ; il n’en garantit pas le succès.')

for first,last,title in [(0,9,'Sources et niveau de lecture (1/2)'),(9,17,'Sources et niveau de lecture (2/2)')]:
 start(title,'BIBLIOGRAPHIE ANNOTÉE  /  CONSULTATION AU 28 OCTOBRE 2026')
 for i in range(first,last):
  a,t,u,n=REFERENCES[i]
  paragraph(f'<b>[{i+1}] {html.escape(a)}.</b> <link href="{html.escape(u,quote=True)}" color="#137B80">{html.escape(t)}</link><br/>{html.escape(n)}','small',11)
 if last==17:
  section('Données et logiciels de cette étude')
  paragraph('ZL3b-n et IT2a-n : versions et crédits dans les métadonnées des phases précédentes, source <link href="https://www.voynich.nu/transcr.html" color="#137B80">voynich.nu/transcr.html</link>. Corpus de César : Perseus, licence CC BY-SA 4.0 conservée. Dante et Pline : provenance et normalisation documentées dans l’archive. Échantillon Timm : <link href="https://github.com/TorstenTimm/SelfCitationTextgenerator" color="#137B80">dépôt des auteurs</link>, licence MIT conservée. Naibbe : crédit et licence Greshko conservés.','small')
  paragraph('L’archive contient le protocole, les inventaires, les clés candidates, les résultats complets, les contrôles échoués, les graines aléatoires, les données nécessaires, les scripts et un manifeste SHA-256. Les articles consultés ne sont pas redistribués. La vérification indépendante des résultats externes n’est pas revendiquée.','small')
bottoms.append(y);C.save();(ROOT/'results/report_layout.json').write_text(json.dumps({'pages':page,'content_bottom_y':bottoms,'min_allowed_y':49},indent=2)+'\n');print(path);print('pages',page,'bottoms',bottoms)
