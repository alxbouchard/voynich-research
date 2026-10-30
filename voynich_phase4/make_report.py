#!/usr/bin/env python3
"""Build the phase-4 report from verified experimental outputs."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from matplotlib.font_manager import findfont,FontProperties
ROOT=Path(__file__).resolve().parent
S=json.loads((ROOT/'results/summary.json').read_text());assert S['verification']=='PASS'
for name,weight in [('DV','normal'),('DVB','bold')]:pdfmetrics.registerFont(TTFont(name,findfont(FontProperties(family='DejaVu Sans',weight=weight))))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
INK=colors.HexColor('#17313D');TEAL=colors.HexColor('#176F75');MUTED=colors.HexColor('#566A72')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=25,leading=30,textColor=INK,spaceAfter=15),
 'kicker':ParagraphStyle('kicker',fontName='DVB',fontSize=9,leading=13,textColor=TEAL,spaceAfter=11),
 'body':ParagraphStyle('body',fontName='DV',fontSize=10,leading=14.7,textColor=INK,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8.4,leading=12,textColor=MUTED,spaceAfter=8),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=13,leading=17,textColor=TEAL,spaceBefore=8,spaceAfter=8),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.5,leading=11.5,textColor=INK),
 'head':ParagraphStyle('head',fontName='DVB',fontSize=8.5,leading=11.5,textColor=colors.white),
 'sample':ParagraphStyle('sample',fontName='DV',fontSize=9,leading=13.5,textColor=INK,wordWrap='CJK',backColor=colors.HexColor('#EEF5F4'),borderPadding=9,spaceBefore=8,spaceAfter=13),
}
story=[]
def p(s,style='body'):story.append(Paragraph(s,styles[style]))
def page(k,title):
 if story:story.append(PageBreak())
 p(k,'kicker');p(title,'title')
def table(rows,widths):
 data=[[Paragraph(escape(str(c)),styles['head' if i==0 else 'cell']) for c in row] for i,row in enumerate(rows)]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EEF5F4'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.append(t);story.append(Spacer(1,10))
def num(n):return f'{n:,}'.replace(',',' ')
def dec(x,n=3):return f'{x:.{n}f}'.replace('.',',')

page('VOYNICH · PHASE 4 · 28 OCTOBRE 2026','Tester une clé<br/>homophonique')
p('<b>Résultat : aucune traduction validée.</b> Cette phase teste une hypothèse plus souple que la substitution simple : plusieurs signes peuvent représenter la même lettre. Le solveur dépasse le seuil prévu sur les textes de contrôle, mais ses sorties du Voynich ne permettent pas d’attribuer un sens au manuscrit.')
table([['Ce qui a été réalisé','Résultat'],['Contrôles à clé cachée, alphabet de 48 signes','4 essais : 2 clés latines et 2 clés italiennes'],['Lettres retrouvées hors ajustement de la clé','Latin : 96,784 % ; italien : 100 %'],['Configurations Voynich','16 essais : 2 langues × 2 groupes × 2 unités × 2 sens'],['Comparaisons par mélange de l’ordre des signes','16 témoins, chacun ajusté avec le même budget'],['Sens nouveau établi pour un mot','Aucun']],[285,214])
p('Le constat le plus utile','h')
p('Sur le contrôle latin, le solveur commet <b>921 erreurs sur 28 640 lettres évaluées</b>. Pourtant, sa sortie erronée obtient un meilleur score de séquences de quatre lettres que le texte exact. Une amélioration statistique ne constitue donc pas une validation du déchiffrement.')
p('Les 16 sorties du Voynich battent leur témoin mélangé sur ce score. Cela indique une organisation locale exploitable dans la transcription, pas l’identification d’une langue ou d’un message. Les meilleurs candidats ont été choisis après comparaison des variantes ; leur sélection reste exploratoire.','small')
p('Livrables : ce rapport, les codes Python et C++, les sources et crédits, les graines aléatoires, les clés candidates, les entrées chiffrées, les sorties complètes et les vérifications. Les candidats sont explicitement marqués comme non traduits.','small')

page('PROTOCOLE ET CONTRÔLES','Ce que le test mesure')
p('Le modèle impose une clé fixe : chaque unité chiffrée donne exactement une lettre ; plusieurs unités peuvent donner la même lettre. Un recuit simulé recherche la clé à partir des fréquences de groupes de quatre lettres, avec une pénalité sur les fréquences des lettres de sortie. Le recuit est une approche connue pour ces chiffres [4] ; le code employé ici est une implémentation propre, avec refroidissement.')
table([['Contrôle','Corpus du modèle','Texte chiffré à retrouver','Évaluation'],['Latin, 2 clés','César, Guerre des Gaules : 317 080 lettres','Pline, Histoire naturelle XVI','28 640 lettres ; 921 erreurs par clé'],['Italien, 2 clés','Dante, Enfer + Purgatoire : 268 869 lettres','Dante, Paradis, première copie uniquement','109 933 lettres ; 0 erreur par clé']],[85,147,127,140])
p('Pour chaque clé, 24 000 lettres servent à l’ajustement ; le reste sert à l’évaluation. Deux clés ne constituent pas deux textes indépendants. Le contrôle italien reste du même auteur que son modèle. Les contrôles synthétiques ne reproduisent ni les erreurs de lecture ni tous les mécanismes possibles du Voynich. La dernière lettre isolée du contrôle latin est exclue, car les segments de moins de quatre lettres ne sont pas évalués.','small')
p('Paramètres et séparation des données','h')
p('Chaque essai utilise 8 départs, 60 000 propositions par départ, puis une amélioration locale. La pénalité vaut 4 et la température initiale 0,002 fois la longueur ajustée. Aucun paramètre n’a été changé après le premier contrôle. Le seuil prévu était de 95 % de lettres exactes pour chacune des deux clés de chaque langue.','small')
p('Pour le Voynich, la source est ZL3b. Les groupes Currier A et B sont traités séparément, avec des clés distinctes. Une feuille physique sur cinq, dans l’ordre trié des identifiants, est réservée à l’évaluation. Les deux faces et panneaux regroupés d’une même feuille restent dans le même ensemble. La clé est ajustée sur au plus 24 000 unités ; les pages réservées ne servent pas à cet ajustement.','small')
p('« Réservé » ne signifie pas historiquement inédit : les phases précédentes ont déjà étudié ce corpus. La direction inverse renverse chaque segment retenu ; elle ne renverse ni l’ordre des pages ni celui du manuscrit.','small')

for lang,title in [('latin','Latin : des scores trompeurs'),('italian','Italien : aucun sens établi')]:
 rows=[r for r in S['real'] if r['language']==lang];best=S['best_post_hoc'][lang]
 page('RÉSULTATS · MODÈLE '+('LATIN' if lang=='latin' else 'ITALIEN'),title)
 p('Scores sur les segments réservés, en <b>bits par fenêtre de quatre lettres</b>. Plus bas signifie plus compatible avec ce modèle local. Ce ne sont ni des pourcentages de traduction correcte ni des entropies par caractère. Le témoin conserve les mêmes signes et les mêmes longueurs dans chaque segment, en mélangeant leur ordre.','small')
 data=[['Groupe / unités','Sens','Ajusté','Réservé','Mélangé','Lettres*']]
 for r in rows:
  data.append([r['subset']+' / '+('EVA' if r['units']=='EVA' else 'composées'),'direct' if r['direction']=='forward' else 'inverse',dec(r['train_metrics']['bits_per_quadgram']),dec(r['test_metrics']['bits_per_quadgram']),dec(r['matched_null_bits']),r['test_metrics']['output_distinct_letters']])
 table(data,[115,65,77,80,85,77])
 p('* Nombre de lettres distinctes produites sur l’ensemble réservé. EVA sépare les caractères de la translittération ; les unités composées regroupent certaines formes comme ch, sh ou iin à l’intérieur des mots. Ce sont des conventions de test, pas un alphabet original certifié.','small')
 p('Le meilleur score ne donne pas une lecture','h')
 sample='\n'.join(best['candidate_preview_NON_TRANSLATION'].splitlines()[:4])
 p('Extrait automatique, sans traduction ni insertion interprétative de mots :','small')
 p(escape(sample).replace('\n','<br/>'),'sample')
 if lang=='latin':
  ctl=S['controls'][0]
  p(f"Le meilleur essai, B / EVA / inverse, obtient {dec(best['test_metrics']['bits_per_quadgram'])}. Le texte latin exact du contrôle obtient {dec(ctl['true_plaintext_bits_per_quadgram'])}, et sa version erronée {dec(ctl['test_metrics']['bits_per_quadgram'])}. Ces textes différents ne définissent pas un classement sémantique ; surtout, le contrôle démontre directement que ce score peut préférer des erreurs.")
  p('Dans le contrôle latin, les substitutions erronées incluent f → t, g → t et x → s. Le modèle homophonique peut ainsi fusionner abusivement des lettres pour favoriser des motifs fréquents. La pénalité de fréquence limite ce comportement sans le supprimer.','small')
 else:
  p('Le meilleur essai est A / EVA / direct, avec '+dec(best['test_metrics']['bits_per_quadgram'])+' et 14 lettres de sortie. Le Paradis correctement retrouvé obtient 13,420 sur le même type de score. Ce décalage ne mesure pas une distance à une « vraie » traduction du Voynich, dont nous ne disposons pas.')
  p('Les sorties contiennent des fragments ressemblant à des suites italiennes, mais aucun passage n’a été validé avec une syntaxe, un sens et des correspondances indépendantes. Aucun mot du manuscrit ne reçoit ici une traduction. Un seul mélange par configuration ne permet pas un test de significativité robuste.','small')

page('LECTURES, LIMITES ET SUITE','Ce qui reste ouvert')
p('Les incertitudes de la transcription sont conservées dans le traitement : les variantes explicites [a:b], les signes illisibles, les signes rares codés et les interruptions graphiques coupent la séquence. Aucune première variante n’est imposée. Les unités trop rares sont également exclues avec une coupure. Les espaces sont ensuite retirés à l’intérieur de chaque segment.','small')
p('Les virgules, qui signalent des espaces incertains, sont traitées comme des frontières pour construire les unités composées. L’autre segmentation n’est pas testée dans cette phase. Les petits segments de moins de quatre unités sont exclus. Les taux de conservation et les listes de feuilles sont fournis dans encoding_audit.json.','small')
table([['Correspondance issue du pilote','Statut dans cette phase'],['okcheor · otcheody · otald','Formes provisoirement robustes dans les variantes étudiées ; sens inconnu'],['okols / okolssheey','Dépend d’une séparation incertaine ; pas une ancre lexicale robuste']],[220,279])
p('Ces répétitions ne sont pas du texte clair connu. Avec une clé fixe, deux suites identiques donnent automatiquement la même sortie ; cela n’ajoute aucune preuve de traduction.','small')
p('Portée de la conclusion','h')
p('Cette expérience ne réfute ni le latin, ni l’italien, ni l’homophonie en général. Elle ne couvre pas les syllabaires, les nomenclateurs, les signes nuls, les clés variables, toutes les segmentations ou les langues médiévales possibles. Les corpus de César et Dante restent des approximations historiques. Aucun contrôle contradictoire d’expert paléographe n’a été ajouté ici.','small')
p('Prochaine priorité proposée : améliorer les unités de lecture sur les fac-similés et comparer des modèles où un signe peut coder une syllabe. Tout nouveau mécanisme devra d’abord réussir des contrôles adaptés, puis produire des lectures cohérentes sur des pages qui n’ont pas servi à choisir ses règles. Ce travail futur n’est pas présenté comme déjà exécuté.','small')
p('Sources et reproduction','h')
p('[1] René Zandbergen et Gabriel Landini, <link href="https://www.voynich.nu/data/ZL3b-n.txt" color="#176F75">transcription ZL3b</link>, 2025 ; les crédits d’IT2a et le format IVTFF sont conservés dans les sources du dossier.<br/>[2] Perseus Digital Library, César, De Bello Gallico, édition XML sous CC BY-SA 4.0 ; l’édition normalisée conserve cette licence.<br/>[3] Michael A. Greshko, corpus de contrôle et licence du dépôt naibbe-cipher. Citation requise : The Naibbe cipher, 2025, <link href="https://doi.org/10.1080/01611194.2025.2566408" color="#176F75">doi:10.1080/01611194.2025.2566408</link>.<br/>[4] Nils Kopal, Cryptanalysis of Homophonic Substitution Ciphers Using Simulated Annealing with Fixed Temperature, HistoCrypt 2019, p. 107-116, <link href="https://ep.liu.se/en/conference-article.aspx?Article_No=12&amp;issue=158&amp;series=" color="#176F75">article source</link>.','small')
p('Vérification : les 36 objectifs du solveur sont recalculés indépendamment en Python ; les exactitudes des contrôles, les mélanges et la séparation des feuilles sont vérifiés. L’archive contient un manifeste SHA-256, les licences et les commandes de reproduction.','small')

def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#D5E2E5'));c.line(48,40,547,40)
 c.setFont('DV',8);c.setFillColor(MUTED);c.drawString(48,27,'VOYNICH · PHASE 4 · AUCUNE TRADUCTION VALIDÉE');c.drawRightString(547,27,str(doc.page))
target=ROOT/'output/pdf/Voynich_phase4_homophonie_2026-10-28.pdf'
SimpleDocTemplate(str(target),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=42,bottomMargin=52,title='Voynich, phase 4 : test homophonique',author='Étude assistée par ChatGPT').build(story,onFirstPage=footer,onLaterPages=footer)
print(target)
