from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

ROOT=Path(__file__).resolve().parent.parent
R=json.loads((ROOT/'results/labels.json').read_text())
BLUE=colors.HexColor('#173447');TEAL=colors.HexColor('#19746b');LIGHT=colors.HexColor('#edf4f3')
for n,f in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Title2',fontName='DB',fontSize=24,leading=29,textColor=BLUE,spaceAfter=16))
styles.add(ParagraphStyle(name='Section2',fontName='DB',fontSize=16,leading=21,textColor=BLUE,spaceAfter=12))
styles.add(ParagraphStyle(name='Body2',fontName='D',fontSize=10,leading=15,spaceAfter=10))
styles.add(ParagraphStyle(name='Small2',fontName='D',fontSize=8,leading=11,spaceAfter=6))
styles.add(ParagraphStyle(name='Cell2',fontName='D',fontSize=8.5,leading=12))
styles.add(ParagraphStyle(name='Call2',fontName='DB',fontSize=11,leading=16,textColor=TEAL,spaceAfter=13))
story=[]
def p(s,style='Body2'):return Paragraph(s,styles[style])
def add(s,style='Body2'):story.append(p(s,style))
def table(rows,widths):
 t=Table([[p(str(c),'Cell2') for c in row] for row in rows],colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.8,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d5dfdf'))]))
 story.append(t);story.append(Spacer(1,12))
def img(name,w=240,h=160):
 path=ROOT/'audit'/name
 iw,ih=PILImage.open(path).size;scale=min(w/iw,h/ih)
 return Image(str(path),width=iw*scale,height=ih*scale,hAlign='LEFT')
def panels(items):
 cells=[]
 for name,title,caption in items:cells.append([p(title,'Small2'),img(name,234,150),Spacer(1,5),p(caption,'Small2')])
 t=Table([cells],colWidths=[251]*len(cells),hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),16)]));story.append(t);story.append(Spacer(1,14))
def page(title):story.append(PageBreak());add(title,'Section2')

add('Voynich | phase 14','Small2')
add('Étiquettes, images\net preuves de lecture'.replace('\n','<br/>'),'Title2')
add('Résultats du 29 octobre 2026','Small2')
add('Aucune traduction validée. Le test ne met pas en évidence un excès convaincant de répétitions entre les étiquettes et le texte de leur propre page.','Call2')
add('Cette phase confronte les translittérations ZL et IT aux images de Yale. Elle cherche des points d’appui vérifiables avant d’attribuer un sens aux signes. Les formes comme <b>okol</b> sont des notations EVA, sans prononciation ni traduction présumée.')
table([['Travail effectué','Périmètre exact'],['Images','20 références de pages, 19 images originales. Vue d’ensemble de ce choix raisonné; 16 recadrages documentés sur 5 pages.'],['Étiquettes répétées','474 loci à forme simple identique dans ZL et IT; sélection déterministe de 10 formes répétées sur au moins deux pages.'],['Test étiquette / prose','15 pages pharmaceutiques admissibles sur 16; comparaison exacte avec 10 000 permutations de blocs de pages.']], [135,367])
add('Résultat principal','Section2')
table([['Translittération','Étiquettes','Retrouvées\nsur leur page','Moyenne\naprès permutation','p, unilatéral'],['ZL','198','11 (5,6 %)','9,14','0,279'],['IT','202','11 (5,4 %)','8,50','0,193']], [102,74,112,130,84])
add('La variation de transcription et trois calculs de sensibilité ne changent pas la conclusion. L’absence de signal net ne prouve pas que les étiquettes et le texte sont sans rapport: les flexions, les composés et les espaces incertains peuvent masquer des répétitions.', 'Body2')
add('Décision: ne pas utiliser ces cooccurrences comme un dictionnaire. Conserver les cas localisés, les variantes et les images pour des hypothèses qui devront ensuite prédire d’autres passages.','Call2')

page('Un même groupe, plusieurs contextes')
add('Le cas <b>okol</b> illustre la difficulté des ancrages par l’image. Les trois recadrages ci-dessous sont compatibles avec la lecture publiée, mais celui du diagramme zodiacal reste très pâle. L’inspection était guidée par les translittérations, elle ne constitue pas une lecture paléographique indépendante.')
panels([('f88r_15.png','f88r.15 | okol','Dans une rangée de fragments végétaux, près d’une feuille et d’une tige courbée. L’étiquette n’est pas écrite sur le récipient de gauche.'),('f82v_44.png','f82v.44 | okol','À gauche d’une figure au bord d’un bassin. Cette proximité ne dit pas si le mot désigne la figure, un geste ou autre chose.')])
panels([('f73v_1.png','f73v.1 | lecture publiée okol','Entre des figures d’un diagramme zodiacal. Contraste faible: lecture autonome non assurée.'),('f99r_1.png','f99r.1 | inscription sur un récipient','Le rattachement matériel est ici visible, mais ZL lit okaradag et IT okoramog. Les variantes sont conservées.')])
add('Ce que cela permet de dire','Section2')
add('Une attribution telle que « okol = récipient » ne découle pas du seul emplacement en f88r. Pour la défendre, il faudrait expliquer les autres contextes et obtenir des prédictions indépendantes. Une même forme peut aussi avoir des usages symboliques, génériques ou homonymes: les images ne tranchent pas entre ces possibilités.')
add('Sources visuelles: Yale, Beinecke MS 408, images 1037112, 1006223, 1006207 et 1006246. Les fichiers PNG du dossier conservent exactement les pixels recadrés; leur réduction dans ce PDF sert uniquement à la mise en page.','Small2')

page('Dix formes à suivre, sans sens attribué')
add('Critères fixés avant le calcul: étiquette simple d’au moins trois caractères EVA, accord exact ZL/IT au même locus, présence sur au moins deux pages; classement par fréquence décroissante puis ordre alphabétique. Les occurrences signalées sont celles qui satisfont tous ces critères.')
rows=[['Forme EVA','Étiquettes / pages','Contextes IVTFF','Prose ZL / IT']]
for c in R['candidates']:rows.append([c['eva'],f"{c['n_agreeing_labels']} / {c['n_pages']}",', '.join(c['contexts']),f"{c['prose_occurrences']['ZL']} / {c['prose_occurrences']['IT']}"])
table(rows,[90,115,177,120])
add('Lf: fragment végétal; Lt: tube, bassin ou autre élément biologique; Ln: figure; Lz: élément zodiacal; L0: court texte sans rattachement clair. Ce sont des catégories documentaires, pas des traductions. Les comptes de prose portent sur tout le corpus admissible, pas seulement les 15 pages du test.','Small2')
add('Un candidat ciblé: okeoly','Section2')
add('Dans les deux fichiers, <b>okeoly</b> apparaît trois fois en prose: f58v.25, f99r.18 et f101r.10. Il figure aussi parmi les étiquettes retenues, dont f99r.25. Le texte f99r.18 précède la rangée du dessin associé à f99r.25: le voisinage immédiat n’est donc pas une règle suffisante.')
story.append(img('f99r_25.png',160,125));story.append(Spacer(1,7))
add('Ce cas est une piste d’alignement textuel, choisie après inspection des résultats; aucune significativité propre ni signification lexicale n’est revendiquée. Six des dix formes du tableau ont été examinées en zoom dans cette phase; les autres restent des candidats issus des fichiers.','Small2')

page('Les incertitudes font partie des données')
panels([('f88r_2.png','f88r.2 | osal / oral','Désaccord de signe médian entre ZL et IT. L’image est conservée sans départager artificiellement les deux lectures.'),('f88r_24.png','f88r.24 | otor,am / otor.am','La virgule marque un espace incertain dans ZL; le point marque un espace retenu dans IT. Une séparation visible ne suffit pas à établir une frontière linguistique.')])
panels([('f99r_4.png','f99r.4 | oky','Première occurrence sur cette page, entre des fragments végétaux.'),('f99r_24.png','f99r.24 | oky','Seconde occurrence, près d’une longue racine. La répétition ne prouve pas que les deux dessins désignent une même espèce.')])
add('Marginalia: ne pas transformer une inscription en clé','Section2')
story.append(img('f116v_margin.png',502,155));story.append(Spacer(1,8))
add('f116v: écriture marginale, croix et figures observées. Cette phase ne propose ni nouvelle lecture, ni datation, ni attribution de main. Le lien de cette écriture avec le texte principal reste à établir avant d’en faire un ancrage.', 'Small2')

page('Méthode, limites et reproduction')
add('<b>Extraction.</b> Les commentaires IVTFF sont retirés; les interruptions de dessin sont traitées comme séparateurs. Les loci inexistants (!) sont exclus. Les étiquettes Lf/Lc simples d’au moins trois lettres sont retenues sur les pages $I=P ayant de la prose. Les formes ambiguës, les espaces incertains et les signes rares ne sont pas résolus par supposition. f101r, sans étiquette Lf/Lc admissible, sort du test.')
add('<b>Statistique.</b> Pour chaque étiquette, compter 1 si sa forme exacte existe au moins une fois dans la prose de la même page. Permuter l’affectation des textes entre les 15 blocs d’étiquettes, sans dissocier les étiquettes d’une page. Graine: 20261029; p = (1 + nombre de scores permutés au moins égaux au score observé) / 10001.')
table([['Calcul de sensibilité','p ZL','p IT'],['Permutations au sein de chaque cahier','0,389','0,208'],['Étiquettes identiques dédupliquées par page','0,326','0,149'],['Moyenne des proportions par page','0,191','0,134']], [330,86,86])
add('<b>Vérifications.</b> Un décompte direct confirme les diagonales des matrices. Un contrôle positif construit retrouve 16 associations uniques (p = 0,00010); un contrôle sans association donne 0 (p = 1). Ces contrôles vérifient le calcul, pas un modèle de déchiffrement. Chaque recadrage PNG a été rouvert et comparé pixel par pixel à l’extrait source.')
add('<b>Limites.</b> ZL et IT représentent le même manuscrit et ne sont pas deux réplications indépendantes. Les pages, faces d’un même feuillet et panneaux de dépliants peuvent être dépendants; la permutation par page ne modélise pas toutes ces relations. La longueur de prose varie. L’échantillon visuel est raisonné, non aléatoire. L’inspection est non aveugle. Ni installation complète de TranscriptTool, ni modèle phonétique avec segmentation conjointe n’ont été exécutés ici.')
add('<b>Étape suivante proposée.</b> Utiliser les variantes comme branches concurrentes, tester une grammaire ou une correspondance commune aux étiquettes et à la prose, puis geler les règles avant une évaluation sur d’autres feuillets. L’alphabet analytique AAA de Zandbergen fournit une piste d’alignement des traits; il ne donne pas de valeurs phonétiques.')
add('Sources et dossier reproductible','Section2')
add('Yale, Beinecke MS 408: <link href="https://collections.library.yale.edu/catalog/2002046" color="#19746b">notice et images originales</link>; manifeste IIIF et empreintes SHA-256 inclus dans le dossier.<br/>René Zandbergen: <link href="https://voynich.nu/transcr.html" color="#19746b">translittérations</link>, ZL3b-n (13 mai 2025), IT2a-n, format IVTFF; <link href="https://voynich.nu/extra/sta-aaa.html" color="#19746b">alphabet analytique AAA</link>.<br/>Jorge Stolfi: <link href="https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/98-02-01-lotsa-labels/labels-t.html" color="#19746b">collection historique d’étiquettes</link> (1998), consultée pour comparaison, sans adopter ses identifications d’objets comme vérités sémantiques.','Small2')
add('L’archive contient les données, les 19 images, les 16 recadrages, le protocole local, les scripts Python et les résultats JSON. README.txt donne les commandes. Le protocole local précédait le calcul; il ne s’agit pas d’une préinscription externe.','Small2')

def footer(c,doc):
 w,h=doc.pagesize;c.setStrokeColor(TEAL);c.line(44,h-37,w-44,h-37)
 c.setFont('D',8);c.setFillColor(BLUE);c.drawString(44,h-29,'VOYNICH | PHASE 14 | IMAGES ET ÉTIQUETTES')
 c.setFillColor(colors.HexColor('#60727c'));c.drawString(44,27,'29 octobre 2026 | Étude exploratoire, aucune traduction validée')
 c.drawRightString(w-44,27,str(doc.page))

out=ROOT/'output/Voynich_phase14_images_et_etiquettes.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=44,rightMargin=49.28,topMargin=58,bottomMargin=48,title='Voynich - Phase 14 - Images et étiquettes',author='Étude exploratoire assistée par ChatGPT').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
