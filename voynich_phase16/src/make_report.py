from pathlib import Path
import json,html
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

R=Path(__file__).resolve().parent.parent
OUT=R/'output/Voynich_phase16_points_appui_historiques.pdf'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans'
pdfmetrics.registerFont(TTFont('D',font+'.ttf'))
pdfmetrics.registerFont(TTFont('DB',font+'-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DM','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
W,H=595.28,841.89;M=43;PW=W-2*M
ink=HexColor('#20323E');teal=HexColor('#146B70');muted=HexColor('#52656D');pale=HexColor('#EAF2F2')
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Voynich - Phase 16 - Points d’appui historiques')
styles={name:ParagraphStyle(name,fontName='DB' if name in ['title','h'] else 'D',fontSize=size,leading=lead,textColor=ink,spaceAfter=0)
        for name,size,lead in [('title',23,29),('h',12,17),('body',9.6,14.1),('small',8,11.6)]}
x=json.loads((R/'results/analysis.json').read_text())

def para(text,y,style='body',width=PW,xpos=M):
 p=Paragraph(text,styles[style]);_,h=p.wrap(width,H);p.drawOn(c,xpos,y-h);return y-h
def heading(text,y):return para(text,y,'h')-7
def page(n):
 c.setFillColor(teal);c.rect(0,H-12,W,12,fill=1,stroke=0)
 c.setFont('DB',8);c.drawString(M,H-39,'VOYNICH | PHASE 16 | AUDIT DES ANNOTATIONS')
 c.setStrokeColor(pale);c.line(M,43,W-M,43)
 c.setFont('D',7.6);c.setFillColor(muted);c.drawString(M,29,'29 octobre 2026 | Étude exploratoire | Aucune traduction validée')
 c.drawRightString(W-M,29,str(n))
def box(text,y):
 p=Paragraph(text,styles['body']);_,h=p.wrap(PW-22,H)
 c.setFillColor(pale);c.roundRect(M,y-h-20,PW,h+20,5,fill=1,stroke=0);p.drawOn(c,M+11,y-h-10);return y-h-32
def image_at(path,y,width=PW,maxheight=None,xpos=M):
 im=Image.open(path);height=width*im.height/im.width
 if maxheight and height>maxheight:width*=maxheight/height;height=maxheight
 c.drawImage(str(path),xpos,y-height,width=width,height=height);return y-height
def table(rows,widths,y):
 data=[[Paragraph(html.escape(str(v)),styles['small']) for v in row] for row in rows]
 t=Table(data,colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),pale),('VALIGN',(0,0),(-1,-1),'TOP'),
 ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
 ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
 ('LINEBELOW',(0,0),(-1,0),.6,teal),('LINEBELOW',(0,1),(-1,-1),.3,pale)]))
 _,h=t.wrap(PW,H);t.drawOn(c,M,y-h);return y-h

page(1);y=H-65
y=para('Un rapprochement graphique,<br/>pas encore une lecture',y,'title')-15
y=box('Deux pistes vérifiées : la table marginale de f1r et les signes mêlés aux annotations de f116v. Une comparaison avec f104r mérite d’être conservée. Aucun mot ni aucune phrase du texte principal n’a reçu un sens validé.',y)
y=heading('f116v et f104r : le lien précis',y)
y=para('La translittération ZL donne <b>oror.sheey</b> sur f116v. Une autre lecture publiée propose <b>aror sheey</b>. Sur f104r.28, ZL écrit <b>aror,sheey</b> et IT <b>arorsheey</b>. La virgule ZL marque un espace incertain. Les deux corpus concordent donc sur la suite de signes de f104r, pas sur son découpage.',y)-12
image_at(R/'audit/f116v_BW_pair.png',y,width=224,maxheight=121)
image_at(R/'audit/f104r_pair.png',y,width=224,maxheight=121,xpos=M+PW-224)
y-=131
para('f116v, traitement multispectral.<br/>Premier signe encore discuté : o / a.',y,'small',224)
para('f104r.28, photographie Yale.<br/>Suite transcrite aror,sheey / arorsheey.',y,'small',224,M+PW-224)
y-=39
y=table([['Recherche hors f116v','ZL','IT'],['oror sheey, espaces sûrs','0','0'],['aror sheey, espaces sûrs','0','0'],['aror sheey / arorsheey, espace incertain admis','1 : f104r.28','1 : f104r.28']],[305,102,102],y)-13
y=para('Les recherches entre lignes consécutives d’un même paragraphe n’ajoutent aucune occurrence. IT ne contient pas f116v : il ne fournit donc pas une seconde lecture indépendante de l’annotation cible.',y)-12
y=heading('Ce que ce lien permet, et ce qu’il ne permet pas',y)
y=para('Il fournit deux endroits à comparer signe par signe. Il ne prouve ni une citation, ni une recette, ni une équivalence entre les annotations en alphabet latin et le texte principal. Le rapprochement était déjà signalé par Anton le 21 avril 2016, puis discuté en 2017. Cette phase le vérifie ; elle ne le découvre pas.',y)-12
y=para('Images : Beinecke Rare Book & Manuscript Library MS 408, f104r et f116v. Multispectral : The Lazarus Project and The Chester F. Carlson Center for Imaging Science at Rochester Institute of Technology. Traitements de Roger Easton.',y,'small')
assert y>55,y;c.showPage()

page(2);y=H-65
y=para('Essai de la table marginale',y,'title')-15
y=para('La table préliminaire publiée par Lisa Fagin Davis en 2024 aligne des lettres latines et des signes du manuscrit. Nous avons recodé manuellement un sous-ensemble en EVA, sans compléter les entrées illisibles. Les ambiguïtés j/k donnent quatre clés fixes, sans apprentissage.',y)-13
y=table([['Groupes EVA retenus','Lettres, colonne gauche','Lettres, colonne droite'],
 ['d · a · r · o','a · b · c · e','b · c · d · f'],
 ['in · n · e · ch','f · g · h · i','g · h · i · j ou k'],
 ['l · f · s · p · t','l · o · p · s · x','m · p · q · t · y'],
 ['y','j ou k','l']],[170,170,169],y)-13
y=para('Ces correspondances restent conditionnelles à la lecture de la table et au regroupement des signes. Les formes composées cth, ckh, cph, cfh, ch, sh et in sont conservées ; un signe sans valeur reste entre crochets.',y)-14
y=heading('Résultat mécanique',y)
rows=[['Corpus','Groupes entièrement substituables','Proportion']]
for code in ['ZL','IT']:
 k=x['corpora'][code]['coverage']['left_j'];n=k['fully_mapped_occurrences'];d=k['clean_word_occurrences']
 rows.append([code,f'{n:,} / {d:,}'.replace(',',' '),f'{100*n/d:.2f} %'.replace('.',',')])
y=table(rows,[80,315,114],y)-11
y=para('<b>Ce pourcentage mesure la couverture de la table partielle, pas le déchiffrement.</b> Le dénominateur contient uniquement les groupes alphabétiques sans marque d’incertitude, hors f116v. Les quatre clés couvrent les mêmes groupes. ZL et IT représentent le même manuscrit.',y)-14
y=heading('Exemple contrôlable : f1r.10',y)
y=table([['Entrée EVA','Substitution obtenue'],['dain os teody','Colonne gauche : abf ep xhea[j/k]'],['Même entrée','Colonne droite : bcg fq yifbl']],[180,329],y)-12
y=para('Les lignes entièrement substituables sont toutes conservées dans les résultats : 35 en ZL et 48 en IT, dont plusieurs très courtes. Aucun de ces résultats n’est présenté comme une traduction. Aucun test linguistique exhaustif n’a été réalisé sur toutes les langues ou sur les entrées omises.',y)-15
y=box('<b>Décision :</b> cette table partielle ne fournit pas une clé validée. Sa couverture limitée ne suffit pas non plus à réfuter toutes les interprétations possibles des annotations marginales.',y)
y=para('Source de la table : Lisa Fagin Davis, « Multispectral Imaging and the Voynich Manuscript », 8 septembre 2024, figure screenshot-696.png. Le tableau source et les images examinées sont conservés dans le dossier de recherche.',y,'small')
assert y>55,y;c.showPage()

page(3);y=H-65
y=para('Preuve, limites et suite utile',y,'title')-17
y=heading('Une vérification reproductible',y)
y=para('Deux versions figées du corpus : ZL3b-n (13 mai 2025) et IT2a-n (version modifiée le 25 juin 2025). Trois traitements des espaces et variantes : lecture stricte ; première variante publiée et virgules séparatrices ; première variante et virgules supprimées. Les interruptions par un dessin sont toujours des barrières. Les rares signes inconnus ne servent jamais de jokers.',y)-12
y=para('Les requêtes jointes arorsheey et ororsheey ont été ajoutées après le premier calcul pour documenter l’occurrence de f104r.28. Cet ajout est déclaré dans ADDENDUM.txt. Le protocole est local et exploratoire ; les résultats négatifs publiés étaient connus avant l’essai. Aucun seuil statistique ni gain de significativité n’est revendiqué.',y)-12
y=para('Vérifications effectuées : recalcul identique ; recherche littérale indépendante du cas f104r.28 ; concordances reliées aux lignes originales ; contrôle d’exclusion de f116v ; six recadrages PNG comparés aux pixels sources après correction EXIF. La reproduction depuis l’archive extraite vérifie les mêmes résultats.',y)-16
y=heading('Pourquoi la piste ne donne pas encore du texte clair',y)
y=para('Nous ne disposons pas d’un passage dont le sens soit connu indépendamment et dont l’équivalence avec le texte principal soit démontrée. L’écriture voisine peut être un commentaire, une copie, un essai de lecture ou un ajout sans rapport. Une ressemblance de formes ne tranche pas entre ces possibilités.',y)-12
y=para('L’examen des images a été guidé par les transcriptions existantes. Il ne constitue pas une lecture paléographique à l’aveugle. Les images visible et multispectrale montrent la même inscription ; elles ne sont pas deux témoins historiques indépendants. Aucune identité de main ou date précise des annotations n’est établie ici.',y)-15
y=box('<b>La prochaine preuve à chercher :</b> un parallèle historique daté pour une formule marginale, conservant plusieurs mots dans le même ordre et vérifiable sur son manuscrit source. Il faudra ensuite démontrer son lien avec f104r ou un autre passage. Sans ce second lien, même une lecture correcte de la marge ne déchiffre pas le livre.',y)
y=heading('Sources et accès aux données',y)
sources=[
 ('Images de Yale, MS 408','https://collections.library.yale.edu/manifests/2002046'),
 ('Jeu public d’images de 2014, publié en 2024','https://drive.google.com/drive/folders/1mNQGKQDSCR4M_c2M2JrsU5soghvYwMig'),
 ('Lisa Fagin Davis, billet et table préliminaire, 2024','https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/'),
 ('Anton, comparaison f104r / f116v, 21 avril 2016','https://www.voynich.ninja/printthread.php?page=7&tid=437'),
 ('Koen Gheuens, étude des graphies de f116v, 2023','https://herculeaf.wordpress.com/2023/08/28/f116v-most-likely-readings-based-on-glyph-shapes/'),
 ('René Zandbergen, corpus et conventions EVA / IVTFF','https://www.voynich.nu/transcr.html')]
for title,url in sources:
 y=para(f'<link href="{html.escape(url,quote=True)}" color="#146B70">{html.escape(title)}</link>',y,'small')-5
y-=5
y=para('Dossier : données, sources des images, coordonnées des recadrages, protocole, addendum, scripts, sorties JSON, vérification et empreintes SHA-256. Les fichiers temporaires d’accès sont exclus. Toutes les sorties textuelles sont des translittérations ou substitutions, jamais des traductions.',y,'small')
assert y>55,y
c.save();print(OUT)
