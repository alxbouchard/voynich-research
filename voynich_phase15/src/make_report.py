from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent.parent
BLUE=colors.HexColor('#173447');TEAL=colors.HexColor('#19746b');LIGHT=colors.HexColor('#edf4f3')
for n,f in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='D',boldItalic='DB')
S={
 'title':ParagraphStyle('title',fontName='DB',fontSize=23,leading=28,textColor=BLUE,spaceAfter=14),
 'head':ParagraphStyle('head',fontName='DB',fontSize=15,leading=20,textColor=BLUE,spaceAfter=10),
 'body':ParagraphStyle('body',fontName='D',fontSize=10,leading=14,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='D',fontSize=8.3,leading=11.5,spaceAfter=7),
 'cell':ParagraphStyle('cell',fontName='D',fontSize=8.4,leading=12),
 'call':ParagraphStyle('call',fontName='DB',fontSize=11,leading=16,textColor=TEAL,spaceAfter=12)}
story=[]
def para(s,sty='body'):return Paragraph(s,S[sty])
def add(s,sty='body'):story.append(para(s,sty))
def table(rows,widths):
 t=Table([[para(str(c),'cell') for c in row] for row in rows],colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),.8,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d5dfdf')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]))
 story.append(t);story.append(Spacer(1,12))
def num(x,n=2):return f'{x:.{n}f}'.replace('.',',')
cases=[json.loads((ROOT/'results'/f'{c}_{m}.json').read_text()) for c,m in [('ZL','strict'),('IT','strict'),('ZL','lattice'),('IT','lattice')]]

add('VOYNICH | PHASE 15 | 29 OCTOBRE 2026','small')
add('Les variantes résistent-elles<br/>au test sur d’autres feuillets ?','title')
add('Résultat: les transformations apprises n’améliorent pas le lien spécifique entre les étiquettes et le texte de leur propre feuillet. Aucune traduction validée.','call')
add('La phase 14 recherchait des répétitions exactes sur la même page. Cette phase autorise des préfixes, des terminaisons et certaines fusions de groupes écrits. Les règles sont apprises sur cinq feuillets, puis testées sur le sixième. Ses deux faces et ses panneaux sont toujours exclus ensemble de l’apprentissage.')
add('Le test porte sur <b>six feuillets physiques</b>: f88, f89, f99, f100, f101 et f102, soit 16 pages ou panneaux de prose. La question est locale: une forme d’étiquette transformée doit être davantage liée au bon feuillet qu’aux autres. Elle ne teste pas toute forme possible de grammaire ou de chiffrement.')
rows=[['Condition','Étiquettes','Bon feuillet','Autres','Écart, points','p exact']]
for r in cases:
 o=r['observed'];name=r['code']+' / '+('strict' if r['condition']=='strict' else 'variantes')
 rows.append([name,r['labels'],num(100*o['own_fraction'])+' %',num(100*o['background_fraction'])+' %',num(100*o['score']),num(r['full_null']['score']['p_exact'],3)])
table(rows,[112,68,90,78,82,72])
add('Pourcentages: moyennes des fractions par feuillet, et non fractions calculées en regroupant toutes les étiquettes. « Autres » est la moyenne sur les cinq autres feuillets. p exact: proportion des 720 permutations donnant un écart au moins aussi grand.','small')
add('La comparaison décisive','head')
add('Dans les quatre configurations, l’écart « bon feuillet moins autres » est inférieur à celui obtenu sans transformation. La perte va de <b>0,30 à 1,06 point de pourcentage</b>. Les correspondances supplémentaires ne rendent donc pas l’appariement plus spécifique.')
add('Les permutations qui conservent le nombre de panneaux par feuillet donnent la même conclusion: aucun résultat convaincant. ZL et IT sont deux lectures du même manuscrit, pas deux expériences indépendantes.','body')
add('Ce résultat réduit l’intérêt de cette famille de transformations pour retrouver un lien local. Il ne démontre ni que le texte est dépourvu de sens, ni que tout lien entre étiquettes et prose est impossible.','call')

story.append(PageBreak());add('Ce qui a réellement été essayé','title')
table([['Élément','Règle fixée avant l’ajustement'],['Unités','cth, ckh, cph, cfh, ch et sh sont indivisibles; les autres lettres EVA restent individuelles. Aucune valeur phonétique n’est attribuée.'],['Transformations','Identité, ou remplacement de 0 à 2 unités à une seule extrémité; au moins 3 unités restent inchangées. Au plus 3 règles ajoutées au modèle.'],['Soutien minimal','Une règle doit fonctionner sur au moins 3 graphies d’étiquettes distinctes réparties sur au moins 2 feuillets d’apprentissage.'],['Choix des règles','Maximiser le contraste entre bon texte et autres textes d’apprentissage. Chaque nouvelle règle doit améliorer ce contraste de plus de 0,01.'],['Branche avec variantes','Lectures explicites entre crochets, ligatures ordinaires, espaces incertains; jusqu’à 2 groupes adjacents peuvent être réunis. Aucune fusion à travers une ligne ou un dessin.']], [105,397])
add('Exemples effectivement produits hors ajustement','head')
table([['Étiquette','Transformation proposée','Forme retrouvée / locus'],['otoldy, f89r1.4','Retirer dy à droite','otol, f89r2.12'],['otoldy, f89r1.4','Remplacer ot par ch à gauche','choldy, f89r2.7'],['oteol, f100r.20','Remplacer ot par ch à gauche','cheol, f100r.24']], [144,181,177])
add('Ces exemples figurent dans les sorties de la configuration IT stricte. Le feuillet complet de chaque étiquette était tenu à l’écart de l’ajustement de ses règles. Ce sont des correspondances EVA vers EVA, sans traduction. Leur existence isolée ne compense pas l’échec du contraste global.','small')
add('Contrôles','head')
add('Sur des chaînes artificielles dont la prose ajoute systématiquement q aux étiquettes, le système retrouve la règle et les <b>120 correspondances sur les feuillets réservés</b>. Un contrôle sans lien donne zéro correspondance. Ces contrôles vérifient que le programme récupère un cas simple appartenant à sa famille; ils ne mesurent pas sa sensibilité à toutes les langues historiques.')
add('Les inventaires comprennent 561 à 845 règles candidates selon la condition. Les six exclusions de feuillet sont refaites dans chacune des 720 permutations, pour chacune des quatre conditions: <b>17 280 ajustements</b> dans les distributions de référence.','small')

story.append(PageBreak());add('Interprétation et dossier de preuve','title')
add('Pourquoi le préfixe q ne suffit pas','head')
add('Un diagnostic descriptif ajouté après les résultats autorise uniquement le préfixe q, sans apprentissage. En ZL strict, les étiquettes retrouvées dans leur propre feuillet passent de 19 à 22 sur 198; en IT, de 16 à 20 sur 202. Les correspondances avec les autres feuillets augmentent aussi. Aucun sens grammatical ne découle de ces nombres; ce diagnostic n’est pas un nouveau résultat confirmatoire.')
add('Cette particularité des étiquettes est déjà discutée par Stolfi et Zandbergen. La présente expérience cherche une valeur prédictive locale supplémentaire, et ne revendique pas la découverte de la différence entre mots commençant ou non par q.','body')
add('Vérifications et limites','head')
add('<b>Reproductibilité.</b> Les ajustements observés ont été recalculés avec les mêmes résultats. Les p exacts ont été recomptés. La génération des candidats a aussi été reconstruite sans les données du feuillet tenu à l’écart: les règles choisies sont identiques. Les correspondances strictes ont été vérifiées directement dans les lignes originales, sans passer par le calcul de caractéristiques.')
verification=json.loads((ROOT/'results/verification.json').read_text())
add(f"Le contrôle indépendant porte sur {verification['strict_prose_occurrences_independently_verified']} références à des occurrences de prose dans les sorties strictes, avec répétitions possibles entre les lectures. Le dossier conserve les loci, les lignes brutes, les variantes, les règles de chaque pli et tous les scores des permutations.",'small')
add('<b>Portée.</b> Six feuillets constituent un petit échantillon; leur indépendance physique n’efface pas leurs relations de contenu. Les tailles diffèrent, d’où le contrôle restreint à 48 permutations conservant 2 ou 4 panneaux. Les pages avaient déjà été examinées dans des phases antérieures: elles sont réservées à l’évaluation de cet ajustement, pas historiquement inconnues de l’analyste. Aucune hypothèse phonétique ni lecture sémantique n’a été testée ici.')
add('<b>Décision.</b> Ne pas élargir les transformations au seul motif de produire davantage de ressemblances. Pour retenir une clé, il faudra une contrainte indépendante et des prédictions qu’elle réussit avec des règles fixes. Ce test ne fournit pas encore cette clé.','call')
add('Sources consultées','head')
add('René Zandbergen, <link href="https://voynich.nu/extra/labels.html" color="#19746b">Some special properties of labels in the Voynich MS</link>; <link href="https://voynich.nu/transcr.html" color="#19746b">translittérations et format IVTFF</link>.<br/>Jorge Stolfi, <link href="https://voynich.nu/hist/stolfi/grammar.html" color="#19746b">A Grammar for Voynichese Words</link>, 2000: modèles de structure interne des formes, sans valeur phonétique fournie.<br/>Xin Zhang et Victor S. Sheng, <link href="https://arxiv.org/abs/2610.34499" color="#19746b">prépublication arXiv:2610.34499</link>, déposée le 25 octobre 2026. Les auteurs comparent des modèles concurrents et des contrôles de déchiffrement; certaines statistiques ne les départagent pas. Cette phase ne reproduit pas leur étude et ne transforme pas son titre en preuve d’absence de sens.','small')
add('Reproduction: Python 3, numpy, threadpoolctl; ReportLab pour ce PDF. Le ZIP contient les données ZL/IT, le protocole local, son addendum, les scripts et les résultats JSON. Il n’inclut pas de nouvelles images. Le protocole n’a pas fait l’objet d’une préinscription externe.','small')

def footer(c,doc):
 w,h=doc.pagesize;c.setStrokeColor(TEAL);c.line(44,h-37,w-44,h-37)
 c.setFont('D',8);c.setFillColor(BLUE);c.drawString(44,h-29,'VOYNICH | PHASE 15 | TRANSFORMATIONS ET TESTS PAR FEUILLET')
 c.setFillColor(colors.HexColor('#60727c'));c.drawString(44,27,'29 octobre 2026 | Résultats exploratoires, aucune traduction validée');c.drawRightString(w-44,27,str(doc.page))
out=ROOT/'output/Voynich_phase15_variantes_et_prediction.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=44,rightMargin=49.28,topMargin=58,bottomMargin=48,title='Voynich - Phase 15 - Variantes et prédiction',author='Étude exploratoire assistée par ChatGPT').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
