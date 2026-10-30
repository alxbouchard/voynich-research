#!/usr/bin/env python3
import json
from pathlib import Path
from matplotlib import font_manager
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
P=Path(__file__).resolve().parent
rows=json.loads((P/'results/report_summary.json').read_text());S={r['name']:r for r in rows}
V=json.loads((P/'results/verification.json').read_text())
for n,w in [('DV','normal'),('DVB','bold')]:pdfmetrics.registerFont(TTFont(n,font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight=w))))
W,H=595.276,841.89;M=44;CW=W-2*M;INK=colors.HexColor('#17323B');TEAL=colors.HexColor('#087D82');GREY=colors.HexColor('#536168')
styles={k:ParagraphStyle(k,fontName='DVB' if k in ['h1','h2','th'] else 'DV',fontSize=s,leading=l,textColor=colors.white if k=='th' else TEAL if k=='h2' else GREY if k=='small' else INK) for k,s,l in [('h1',21,26),('h2',12,16),('body',10,14.2),('small',8.5,11.9),('table',8.5,11.8),('th',8.5,11.8)]}
path=P/'output/pdf/Voynich_phase10_chiffrement_contextuel_2026-10-28.pdf';path.parent.mkdir(parents=True,exist_ok=True)
C=canvas.Canvas(str(path),pagesize=(W,H));C.setTitle('Voynich phase 10 : test de deux alphabets contextuels');C.setAuthor('Analyse assistée par IA pour Alex');page=0;y=0;bottom=[]
def num(v,n=3):return f'{v:.{n}f}'.replace('.',',')
def p(txt,style='body',gap=10):
 global y
 o=Paragraph(txt,styles[style]);_,hh=o.wrap(CW,1800);assert y-hh>52,(page,y,hh,txt[:70]);o.drawOn(C,M,y-hh);y-=hh+gap
def start(title):
 global page,y
 if page:bottom.append(y);C.showPage()
 page+=1;C.setFillColor(TEAL);C.rect(0,H-8,W,8,fill=1,stroke=0);C.setFont('DVB',7.7);C.drawString(M,H-32,'VOYNICH / PHASE 10 / CHIFFREMENT CONTEXTUEL');C.setFillColor(GREY);C.setFont('DV',8);C.drawRightString(W-M,H-32,'28 OCT. 2026');C.setStrokeColor(colors.HexColor('#D5E1E3'));C.line(M,40,W-M,40);C.setFont('DV',7.4);C.drawString(M,27,'EXPÉRIENCE EXPLORATOIRE · AUCUNE TRADUCTION VALIDÉE');C.drawRightString(W-M,27,str(page));y=H-60;p(title,'h1',16)
def table(rows,widths):
 global y
 t=Table([[Paragraph(str(x),styles['th' if i==0 else 'table']) for x in row] for i,row in enumerate(rows)],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#EAF3F3')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]));_,hh=t.wrap(CW,1800);assert y-hh>52,(page,y,hh);t.drawOn(C,M,y-hh);y-=hh+13

start('Deux alphabets testés.<br/>Aucune clé validée.')
p('Le premier signe d’un groupe pourrait-il changer de lecture après une finale <b>y</b> ? Nous avons testé cette règle avec deux alphabets de substitution, chacun à correspondances uniques. Le solveur retrouve au moins <b>99,98 % des lettres</b> de huit témoins chiffrés. Sur le Voynich, cette réussite ne se transforme pas en déchiffrement.')
p('Résultats sur les feuillets réservés','h2',5)
t=[['Corpus / langue visée','Gain de la seconde table','Étendue des 19 témoins mélangés','Témoins faisant au moins aussi bien']]
for corpus,lang in [('ZL_A','latin'),('ZL_A','italian'),('ZL_B','latin'),('ZL_B','italian')]:
 r=S[f'{corpus}_wb_perm_{lang}'];n=r['null'];t.append([corpus.replace('_',' / ')+'<br/>'+('Latin' if lang=='latin' else 'Italien'),num(r['gain_bits']),num(n['min'])+' à '+num(n['max']),str(n['at_least_observed'])+' / 19'])
table(t,[112,103,151,CW-366])
p('Gain = score de la table unique moins score des deux tables, en bits moyens par fenêtre de quatre caractères. Un gain positif est meilleur selon le modèle de langue. Il ne représente pas des mots traduits. Les décomptes sont descriptifs, sans p-valeur revendiquée.','small')
p('<b>Dans A</b>, les gains restent dans l’étendue obtenue avec des mots mélangés. <b>Dans B</b>, le modèle contextuel dégrade le score dans les deux langues. Les résultats ne fournissent donc pas d’appui convaincant à cette clé à deux alphabets.')
p('Ce que cela change pour la recherche','h2',5)
p('La dépendance entre groupes voisins reste une observation utile, déjà connue dans la littérature [1]. La transformer en cette règle de substitution particulière ne suffit pas. Il faut conserver la contrainte de voisinage sans lui attribuer prématurément une valeur phonétique.')
p('Portée : latin représenté par César, italien représenté par Dante, caractères EVA bruts et espaces conservés. Ce résultat n’exclut ni toutes les langues ni tous les chiffres contextuels.','small',0)

start('Un bon score peut favoriser une clé fausse')
p('Le premier modèle autorisait plusieurs signes à produire la même lettre. Il obtenait <b>97,5 à 99,0 % de lettres correctes</b> sur les témoins, mais échouait précisément sur les initiales dont la lecture change après y. Les clés fausses recevaient même un meilleur score que la vraie solution.')
table([['Étape du développement','Initiales après y : latin','Initiales après y : italien','Décision'],['1. Tables libres, espaces omis','74,1 %','81,9 %','Échec'],['2. Tables libres, espaces fixes','78,7 %','96,9 %','Échec en latin'],['3. Deux permutations, espaces fixes','99,73 %','99,96 à 100 %','Seuils atteints']],[205,100,105,CW-410])
p('Étapes 1 et 2 : deux clés par langue. Étape 3 : quatre clés par langue, dont deux nouvelles. Tous ces essais utilisent les mêmes deux textes clairs et la même séparation apprentissage/test. Ce ne sont pas huit corpus indépendants.','small')
p('Le défaut du score initial est démontrable','h2',5)
p('Sur le latin, la clé incorrecte dépasse l’objectif d’apprentissage de la vraie clé d’environ <b>4 287 unités</b> ; sur l’italien, d’environ <b>575 unités</b>. Rechercher plus longtemps le maximum de cet objectif ne rendrait donc pas la vraie clé optimale. Ce diagnostic concerne ce score et ces témoins.')
p('La troisième étape change la famille de chiffres','h2',5)
p('Une permutation interdit que deux signes différents d’une même table deviennent la même lettre. Cette contrainte correspond aux témoins construits ici, mais elle exclut l’homophonie. Le succès final calibre cette famille plus étroite ; il ne réhabilite pas les tables libres.')
p('Les seuils étaient : au moins 95 % de lettres correctes, 90 % dans les initiales déclenchées et 99,5 % de couverture d’apprentissage. Les espaces imposés ne sont jamais comptés comme lettres correctes. Résultat final : <b>99,98596 à 100 %</b> sur toutes les lettres ; <b>99,7326 à 100 %</b> dans le sous-ensemble déclenché.')
p('<b>Chronologie conservée.</b> Le protocole initial précède les résultats. Deux addendums documentent les changements après échec des contrôles, avant leurs nouveaux calculs. Il s’agit d’un développement exploratoire, et non d’une confirmation préenregistrée. Aucun modèle ayant échoué à son contrôle n’a été appliqué au Voynich.','small',0)

start('La règle exacte et ses limites')
p('La table spéciale lit uniquement le premier caractère d’un groupe connu situé après un groupe connu finissant par <b>y</b>, dans la même ligne. La table de base lit tous les autres caractères. L’état est calculé sur le texte chiffré. Chaque table est une permutation des 26 lettres ; les espaces sont fixes.')
p('Les groupes à espace incertain, alternatives ou signes illisibles restent des barrières. Aucune lecture nouvelle ni correction de transcription n’est imposée. Les correspondances candidates sont apprises sans texte clair ni clé vraie dans les arguments du solveur.')
p('Sensibilité à la seconde transcription','h2',5)
table([['Sous-ensemble IT','Gain avec le latin','Gain avec l’italien'],['A',num(S['IT_A_wb_perm_latin']['gain_bits']),num(S['IT_A_wb_perm_italian']['gain_bits'])],['B',num(S['IT_B_wb_perm_latin']['gain_bits']),num(S['IT_B_wb_perm_italian']['gain_bits'])]],[180,163,CW-343])
p('IT retrouve des gains positifs dans A et négatifs dans B. Aucun ensemble de 19 mélanges n’est calculé pour IT. ZL et IT sont deux transcriptions du même manuscrit, pas deux réplications indépendantes.','small')
p('Apprentissage et évaluation','h2',5)
p('Un feuillet physique sur cinq dans la liste lexicographique commune est réservé au test. L’apprentissage utilise les autres feuillets, avec un plafond de 24 000 lettres en lignes complètes. Contrairement au test prédictif de phase 9, cette expérience réserve des feuillets, pas des cahiers entiers. Les clés sont sélectionnées uniquement sur l’apprentissage.')
p('Le score combine les fréquences de suites de quatre caractères et une pénalité de fréquences de lettres. Huit redémarrages de 60 000 propositions sont utilisés pour chaque ajustement. Les modèles de langue viennent de César et d’Inferno/Purgatorio ; Pline et Paradiso servent aux témoins. Les jeux ne sont pas intervertis.','small')
p('Pourquoi les mélanges restent un contrôle limité','h2',5)
p('Les mots intérieurs connus sont permutés dans leur ligne, en gardant les extrémités, les barrières et le contenu des mots. Les deux modèles sont réappris pour chacun des 19 tirages. Ce contrôle détruit certains voisinages, mais il ne simule pas toute la structure du manuscrit.')
p('Le budget de recherche ne garantit pas l’optimum global. Les langues, genres, unités graphiques et frontières du modèle sont restreints. Un échec ne réfute donc pas une langue inconnue, des abréviations, des ligatures, une autre segmentation ou d’autres mécanismes de chiffrement.','small',0)

start('Calculs vérifiés et dossier reproductible')
p('Une seconde implémentation reconstruit les encodages, les textes candidats, les scores et les comparaisons sans importer le programme d’ajustement. Elle contrôle aussi les espaces fixes, les permutations et l’absence de feuillet commun entre apprentissage et test.')
table([['Vérification','Volume'],['Ajustements reconstitués','200'],['Comparaisons à une / deux tables','100'],['Prédictions de lettres contrôlées','4 899 916'],['Caractères des témoins rechiffrés / déchiffrés','736 376'],['Écart absolu maximal sur l’objectif d’apprentissage','1,72 × 10<super>-8</super>']],[350,CW-350])
p('Ces vérifications portent sur les calculs, pas sur le sens. Elles partagent les données et les tables de langue figées avec le programme principal ; elles ne remplacent pas une validation linguistique indépendante.','small')
p('Une sortie qui ne doit pas devenir une traduction','h2',5)
p('Premier segment réservé, ZL/A, f1r.1 :<br/><b>EVA :</b> fachys ykal ar ataiin shol shory<br/><b>Sortie mécanique du candidat latin :</b> guerap adus um utullo pris prima')
p('Cet exemple est le premier segment du test, sans sélection d’un passage favorable. La présence de fragments évoquant une langue ne valide ni la clé ni une traduction. Les sorties complètes restent marquées comme non validées dans les fichiers.','small')
p('Contenu du dossier','h2',5)
p('Protocoles et addendums ; sources figées et licences ; trois solveurs ; clés connues des témoins ; 200 ajustements et leurs sorties ; tous les mélanges ; vérification indépendante ; instructions de reproduction et empreintes SHA-256. La reproduction commence aux entrées figées, sans prétendre refaire l’examen des images.','small')
p('Références et provenance','h2',5)
p('[1] Reddy et Knight (2011), <link href="https://aclanthology.org/W11-1511.pdf" color="#087D82">What We Know About The Voynich Manuscript</link>, §5.2.<br/>[2] Feaster (2022), <link href="https://ceur-ws.org/Vol-3313/paper12.pdf" color="#087D82">Rightward and Downward Grapheme Distributions</link>.<br/>[3] Zandbergen, <link href="https://www.voynich.nu/extra/sp_transcr.html" color="#087D82">conventions et limites des transcriptions IVTFF</link>.<br/>[4] César : Perseus Digital Library, De bello Gallico, CC BY-SA 4.0. Dante et Pline : textes historiques fournis dans le dépôt de Michael A. Greshko, attribution et licence jointes. Les chiffres contextuels de cette phase sont construits pour le test, sans attribution historique.','small',0)
bottom.append(y);C.save();(P/'results/report_layout.json').write_text(json.dumps({'pages':page,'bottoms':bottom},indent=2)+'\n');print(path);print('pages',page,'bottoms',bottom)
