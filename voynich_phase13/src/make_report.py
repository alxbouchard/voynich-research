from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent.parent
summary=json.loads((ROOT/'results/summary.json').read_text())
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB')
INK=colors.HexColor('#192B3B');TEAL=colors.HexColor('#006B6E');PALE=colors.HexColor('#EFF5F5');GRAY=colors.HexColor('#50616D')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=25,leading=30,textColor=INK,spaceAfter=14),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=12,leading=16,textColor=TEAL,spaceBefore=15,spaceAfter=7),
 'p':ParagraphStyle('p',fontName='DV',fontSize=9.5,leading=14,textColor=INK,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11,textColor=GRAY,spaceAfter=7),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.2,leading=11,textColor=INK),
 'cap':ParagraphStyle('cap',fontName='DVB',fontSize=8.4,leading=12,textColor=TEAL,spaceAfter=16)}
def p(t,s='p'):return Paragraph(t,styles[s])
def table(data,widths):
 t=Table([[p(str(x),'cell') for x in row] for row in data],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
 ('LINEBELOW',(0,0),(-1,0),.8,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#DCE4E8')),
 ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));return t
def footer(c,d):
 c.setStrokeColor(TEAL);c.setLineWidth(.7);c.line(44,38,551,38)
 c.setFont('DV',8);c.setFillColor(GRAY);c.drawString(44,25,'Voynich · Phase 13 · 28 octobre 2026, Montréal');c.drawRightString(551,25,str(d.page))
story=[p('VOYNICH / EXPÉRIENCE 13','cap'),p('Tester l’appariement<br/>des lexiques','title'),
 p('<b>Aucune traduction validée.</b> Une adaptation de CSA_OptMatcher a été exécutée sur des témoins connus et sur le Voynich. Le moteur retrouve des correspondances contrôlées, mais les meilleures proximités lexicales du manuscrit ne constituent pas une lecture.'),
 p('1. Ce que les contrôles établissent','h'),
 table([['Épreuve','Mots correctement identifiés','Portée'],
 ['Substitution simple','64 / 64','Mots réservés, hors apprentissage'],
 ['Substitution + signe muet','64 / 64','Suppression du signe supplémentaire'],
 ['Fusion de deux lettres','59 / 59','59 cas évaluables sur 64 ; e et i partagent un signe'],
 ['Substitution homophonique','40 / 64','Après 20 000 pas ; 7 formes seulement ont une distance nulle'],
 ['Phénicien / ougaritique','82 / 105 (78,1 %)','Appariement du jeu public ; mesure sur le corpus ajusté']], [160,135,212]),
 Spacer(1,8),p('« Correctement identifié » signifie que le mot de référence est l’unique meilleur candidat. Cela ne signifie pas toujours que la clé restitue exactement ses lettres. Les trois premiers contrôles donnent aussi une distance nulle pour tous les cas évalués. Le benchmark phénicien/ougaritique ne constitue pas un test sur des pages inconnues.','small'),
 p('2. Une adaptation explicitement contrôlée','h'),
 p('Le calcul de distance d’origine renvoie 0 pour une chaîne vide comparée à une chaîne non vide. Ce cas est corrigé à 1. La version séquentielle du recuit modifie aussi les états avant l’acceptation : les propositions sont désormais copiées, et le meilleur état visité est conservé. Ce constat sur le mode séquentiel ne remet pas à lui seul en cause les expériences parallèles de l’article.'),
 p('Le noyau CPU a été vérifié sur <b>2 400 comparaisons</b> par énumération exhaustive indépendante des variantes. L’appariement des groupes a été comparé à la fonction originale sur 50 matrices. Les 49 résultats enregistrés ont été recalculés et leurs candidats réservés vérifiés.'),
 p('Périmètre : 40 ajustements Voynich/témoins, plus les contrôles et le benchmark. Le regroupement des glyphes depuis les images et la segmentation phonétique conjointe ne sont pas exécutés dans cette phase.','small'),
 PageBreak(),p('RÉSULTATS / LIMITES','cap'),p('Une clé stable ne suffit pas','title'),
 p('Chaque cas apprend sur 96 formes et compare celles-ci à 256 mots latins ou italiens. La table est ensuite appliquée à des formes absentes de toutes ses pages d’apprentissage. Le tableau présente les paramètres de l’article : N = 2, M = 1 ; les essais plus flexibles N = 2, M = 2 restent dans l’archive.'),
 p('3. Résultats sur les formes réservées','h')]
rows=[['Groupe / signes','Langue','Formes','Distance texte','Distance témoin','Signes identiques*']]
for d in summary['default_cases']:
 name=d['case'].split('_');group=name[1];mode='groupés' if name[2]=='COMPOSED' else 'EVA';lang='latin' if name[3]=='latin' else 'italien'
 rows.append([f'{group} / {mode}',lang,d['test_types'],f"{d['distance']:.3f}",f"{d['null_distance']:.3f}",f"{d['mapping_signs_agree']} / {d['mapping_signs_total']}"])
story +=[table(rows,[103,60,55,84,84,121]),Spacer(1,7),
 p('Distance normalisée entre 0 et 1 ; plus petite = meilleure proximité, pas meilleur sens. Le témoin permute les signes dans chaque mot. * Nombre de signes recevant exactement le même ensemble de valeurs lors d’une seconde initialisation. Les groupes A/B sont les classes Currier. « Groupés » traite cth, ckh, cph, cfh, ch et sh comme des unités.','small'),
 p('Une seule configuration retrouve sa table entière : A / signes groupés / latin. Pourtant, une seule de ses 395 formes réservées possède une variante identique à un mot du lexique. Un autre exemple illustre la limite : la forme <b>daiin</b> est appariée à <b>gallia</b> avec une distance de 0,429. Ce rapprochement autorise des modifications ; il ne traduit pas daiin.'),
 p('4. Ce que l’on peut conclure','h'),
 p('Les huit configurations sont plus proches des lexiques que leur témoin mélangé. Ce gain peut venir des régularités de formation des mots. Un seul témoin mélangé par cas ne permet pas de calculer une significativité. Sept tables sur huit changent entre les deux initialisations ; aucun passage cohérent n’est validé.'),
 p('Les petits lexiques latin/italien ne couvrent pas les langues historiques possibles. Les pages sont séparées par feuillet physique, mais avaient été étudiées lors de phases antérieures. Les résultats ne réfutent donc ni une langue ni un chiffrement. L’étape utile suivante est d’élargir les corpus historiques et de tester conjointement segmentation et correspondances.'),
 p('Source : Fabio Tamburini, Frontiers in Artificial Intelligence, 30 mai 2025, DOI 10.3389/frai.2025.1581129. Dépôts : github.com/ftamburin/CSA_OptMatcher et github.com/ftamburin/EditDistanceWild. Adaptation CPU avec valeurs à une lettre ; 8 recuits et 5 000 pas par essai principal, contre 16 et 100 000 dans l’article. Sources, corrections, graines et limites sont conservées dans l’archive.','small')]
out=ROOT/'output/Voynich_phase13_lexiques.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),rightMargin=44,leftMargin=44,topMargin=43,bottomMargin=50,title='Voynich - Phase 13 - Appariement des lexiques',author='Analyse expérimentale assistée').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
