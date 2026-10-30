#!/usr/bin/env python3
"""Illustrated pilot edition. Source pixels remain separate from annotations."""
import json,re
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Flowable, KeepTogether
from reportlab.lib.utils import ImageReader
from matplotlib.font_manager import findfont,FontProperties

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'tmp/figures';FIG.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((ROOT/p).read_text())
protocol=read('PROTOCOL.json');summary=read('results/pilot_summary.json')
rows=read('results/aligned_loci.json');pairs=read('results/anchor_robustness.json')
annotations=read('results/image_annotations.json');maps=read('data/page_image_map.json')
sources={r['oid']:r for r in read('data/image_sources.json')}
for font,weight in [('DV','normal'),('DVB','bold')]:
 pdfmetrics.registerFont(TTFont(font,findfont(FontProperties(family='DejaVu Sans',weight=weight))))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
INK=colors.HexColor('#17313D');TEAL=colors.HexColor('#176F75');MUTED=colors.HexColor('#5A6B72')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=24,leading=29,textColor=INK,spaceAfter=14),
 'kicker':ParagraphStyle('kicker',fontName='DVB',fontSize=9,leading=13,textColor=TEAL,spaceAfter=10),
 'body':ParagraphStyle('body',fontName='DV',fontSize=10,leading=14.5,textColor=INK,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8.2,leading=11.5,textColor=MUTED,spaceAfter=7),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=13,leading=17,textColor=TEAL,spaceBefore=10,spaceAfter=8),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8,leading=11,textColor=INK),
 'head':ParagraphStyle('head',fontName='DVB',fontSize=8,leading=11,textColor=colors.white),
 'trans':ParagraphStyle('trans',fontName='DV',fontSize=8.1,leading=11.2,textColor=INK,wordWrap='CJK'),
}
story=[]
def p(s,style='body'):story.append(Paragraph(s,styles[style]))
def page(k,title,anchor=None):
 if story:story.append(PageBreak())
 if anchor:p('<a name="'+anchor+'"/>','small')
 p(k,'kicker');p(title,'title')
def table(data,widths,repeat=1):
 cells=[[Paragraph(escape(str(x)),styles['head' if i==0 else 'cell']) for x in row] for i,row in enumerate(data)]
 t=Table(cells,colWidths=widths,repeatRows=repeat,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),
  ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EEF5F4'),colors.white]),
  ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
  ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
 story.append(t);story.append(Spacer(1,9))
def crop(oid,bbox,name):
 target=FIG/(name+'.png');PILImage.open(ROOT/'images'/(oid+'.jpg')).crop(bbox).save(target)
 return target
def fitted(path,w,h):
 im=PILImage.open(path);scale=min(w/im.width,h/im.height)
 return Image(str(path),width=im.width*scale,height=im.height*scale,hAlign='LEFT')

class Facsimile(Flowable):
 def __init__(self,page):
  Flowable.__init__(self);self.page=page;self.mapping=maps[page];box=self.mapping['page_view_bbox_xyxy']
  im=PILImage.open(ROOT/'images'/(self.mapping['oid']+'.jpg')).crop(box)
  # Display derivative only; unmodified source JPEG is retained in the archive.
  im.thumbnail((1600,2200),PILImage.Resampling.LANCZOS)
  self.path=FIG/(page+'.jpg');im.save(self.path,quality=82,subsampling=0)
  self.scale=min(499/(box[2]-box[0]),598/(box[3]-box[1]));self.box=box
  self.width=(box[2]-box[0])*self.scale;self.height=(box[3]-box[1])*self.scale
 def draw(self):
  c=self.canv;c.drawImage(str(self.path),0,0,width=self.width,height=self.height)
  for a in annotations:
   if a['locus'].split('.')[0]!=self.page:continue
   x0,y0,x1,y1=a['word_bbox_xyxy_approximate'];s=self.scale;b=self.box
   c.setStrokeColor(colors.HexColor('#C43A32'));c.setLineWidth(1)
   c.rect((x0-b[0])*s,self.height-(y1-b[1])*s,(x1-x0)*s,(y1-y0)*s,stroke=1,fill=0)

page('VOYNICH · PILOTE DE TRANSCRIPTION · 28 OCTOBRE 2026','12 pages, des lectures\ncontrôlables'.replace('\n','<br/>'))
p('<b>Ce document ne contient aucune traduction.</b> Il relie douze pages ou panneaux du manuscrit aux lectures Zandbergen-Landini (ZL3b) et Takahashi (IT2a), conserve leurs divergences et présente huit régions examinées sur les photographies de Yale.')
table([['Travail accompli','État'],['Photographies sources','14 fichiers originaux Yale téléchargés et vérifiés ; 12 vues retenues'],['Passages alignés','384 loci, lignes ou légendes'],['Accord exact après retrait des annotations','164 loci'],['Accord seulement après normalisation','29 loci'],['Divergences entre lectures','188 loci'],['Présents dans une seule source','3 loci'],['Correspondances étudiées sur les images','4 paires, soit 8 régions localisées']],[300,199])
p('Le premier résultat utile est une correction de méthode : <b>okols</b> dans f89v2.21 peut appartenir à <b>okolssheey</b> si un espace incertain est supprimé. Les trois autres paires résistent aux séparations et variantes testées. Cette robustesse concerne leur forme écrite, pas leur sens.')
p('La relecture des images est assistée par les transcriptions existantes. Elle ne constitue pas une expertise paléographique indépendante. Les autres passages sont des lectures importées, non une nouvelle transcription vérifiée signe par signe.','small')
p('Parcours : bilan et conventions ; quatre fiches de correspondance ; points litigieux ; fac-similé et comparaison intégrale pour chaque page. Les liens internes des tableaux permettent de rejoindre les fac-similés.','small')

page('MODE D’EMPLOI','Conserver l’incertitude')
p('EVA est une convention de représentation des formes. Les lettres latines affichées ci-dessous ne donnent pas la prononciation du manuscrit. La notation IVTFF permet de conserver les réserves des transcripteurs [2].')
table([['Notation','Sens dans les sources'],['.','Séparation apparente entre deux mots'],[',','Séparation incertaine : comparer espace et absence d’espace'],['[a:b]','Lectures concurrentes, première option privilégiée par la source'],['? / ???','Signe illisible / nombre indéterminé de signes illisibles'],['{...}','Ligature : signes liés graphiquement'],['@nnn;','Code d’un signe rare en EVA'],['<-> / <~>','Interruption par un dessin, avec éventuel décalage vertical']],[100,399])
p('Dans les tableaux, <b>A</b> signifie accord de la notation après retrait des commentaires et balises de paragraphe ; <b>N</b>, accord obtenu seulement après normalisation ; <b>D</b>, divergence ; <b>Z− / I−</b>, absence dans ZL / IT. Un accord peut encore contenir un signe illisible. Aucun de ces codes n’indique une traduction correcte.','small')
p('La normalisation utilisée pour N choisit notamment la première variante, retire les marques de ligature et traite les virgules comme des séparateurs. C’est précisément pourquoi la comparaison brute reste disponible. Les deux transcriptions ne doivent pas être considérées comme deux observations totalement indépendantes.','small')
p('Les encadrés rouges des fac-similés indiquent approximativement les huit formes examinées. Les coordonnées exactes des régions de travail sont conservées en pixels dans le dossier. Les 376 autres loci ne disposent pas encore d’un alignement géométrique vérifié.','small')
p('Sources : [1] Yale University Library, Beinecke MS 408, catalogue 2002046 et manifeste IIIF officiel. [2] René Zandbergen, format IVTFF, version 2.0.1, document du 8 juillet 2025. [3] Transcriptions ZL3b-n et IT2a-n, auteurs et historique indiqués dans leurs en-têtes. URL, fichiers et empreintes sont conservés dans l’archive.','small')

page('SÉLECTION DU PILOTE','Huit pages liées,\nquatre comparaisons'.replace('\n','<br/>'))
table([['Page','Rôle','Loci','A / N / D / absents']]+[[s['page'], 'Correspondance' if i<8 else 'Comparaison de mise en page',s['loci_union'],
 f"{s['counts'].get('accord_diplomatique',0)} / {s['counts'].get('accord_apres_normalisation',0)} / {s['counts'].get('divergence',0)} / {s['counts'].get('absent_ZL',0)+s['counts'].get('absent_IT',0)}"] for i,s in enumerate(summary['pages'])],[65,185,45,204])
p('Les pages f1r, f2r, f75r et f103r couvrent une ouverture, une mise en page botanique, une page à bassins et une page de paragraphes étoilés. Cette sélection raisonnée n’est pas un échantillon aléatoire du manuscrit.','small')
p('127 loci portent un marqueur d’incertitude : espace douteux, variante ou signe illisible. En incluant les codes de signes rares, 130 loci sont signalés pour examen ; un signe rare n’est pas nécessairement incertain. Ces effectifs recoupent les catégories du tableau.','small')

for i,pair in enumerate(pairs,1):
 page(f'CORRESPONDANCE {i} / 4',pair['word']+' : deux contextes')
 p('Statut : <b>'+('forme stable dans les variantes et séparations testées' if pair['stable_under_tested_segmentations'] else 'correspondance conditionnelle à la séparation des mots')+'</b>. Sens : inconnu.','small')
 for role,title in [('label','Légende'),('body','Texte courant')]:
  a=next(x for x in annotations if x['locus']==pair[role]);mp=maps[a['locus'].split('.')[0]]
  p(f'{title} · {a["locus"]}','h')
  path=crop(a['oid'],a['context_bbox_xyxy'],a['locus'].replace('.','_'))
  story.append(fitted(path,499,138));story.append(Spacer(1,8))
  p(escape(a['note_fr']),'small')
  p('ZL : '+escape(re.sub(r'<(?![-~]>)[^>]*>','',pair['tests']['ZL'][role]['raw']))+'<br/>IT : '+escape(re.sub(r'<(?![-~]>)[^>]*>','',pair['tests']['IT'][role]['raw'])),'small')
 if pair['word']=='okols':
  p('Conséquence : la phase 2 comptait okols comme un mot séparé en traitant la virgule comme un espace. La nouvelle édition conserve aussi la lecture jointe okolssheey. Ce cas est rétrogradé, pas effacé.','small')
 elif pair['word']=='otcheody':
  p('La même forme rapproche une légende près d’une étoile et un paragraphe d’une autre section. Cela ne suffit pas à affirmer qu’il s’agit du nom de cette étoile.','small')

page('POINTS LITIGIEUX','Des différences\nà laisser ouvertes'.replace('\n','<br/>'))
for locus,zl,it,oid,bbox,note in [
 ('f93r.12, fin de ligne','sheodom','sheedom','1006238',[970,1110,1250,1270],'La divergence porte sur o / e. Le fond est traversé par une zone colorée. Les deux lectures sont conservées.'),
 ('f47v.13, troisième forme','chdlety','chdlcty','1006167',[1250,2900,1570,3050],'La divergence porte sur e / c dans la translittération. La présence de la forme otald en fin de ligne ne résout pas cette différence.')]:
 p(locus,'h');story.append(fitted(crop(oid,bbox,locus[:5]+'_dispute'),320,100));story.append(Spacer(1,6))
 p('ZL : '+zl+' ; IT : '+it+'. '+note,'small')
p('Trois loci présents dans une seule source','h')
p('f89v2.26 est présent dans IT (?ds??o) et absent de ZL ; f2r.14 (ytoail) et f2r.15 (ios.an.on) apparaissent seulement dans ZL. Une absence est conservée comme différence de couverture, sans créer artificiellement une lecture dans l’autre source.','small')
p('L’historique publié de Zandbergen signale le retrait en 2025 d’un locus jugé parasite sur f89v2. Ce n’est pas une découverte de cette étude. La comparaison conserve la trace de la différence entre fichiers.','small')
p('Étape suivante pour le déchiffrement : utiliser en priorité les trois correspondances stables comme contraintes provisoires, puis comparer des familles de clés plus larges sur des contrôles adaptés. Aucun test de nouvelle famille de chiffrement n’est revendiqué dans cette phase consacrée aux images et aux lectures.','small')

codes={'accord_diplomatique':'A','accord_apres_normalisation':'N','divergence':'D','absent_ZL':'Z−','absent_IT':'I−'}
for pageid in protocol['pages']:
 mp=maps[pageid];src=sources[mp['oid']]
 page('FAC-SIMILÉ · '+pageid,pageid,anchor='image_'+pageid)
 p(f"Yale, Beinecke MS 408 · image {mp['oid']} · source {src['width']} × {src['height']} pixels. Vue du panneau, avec marges.",'small')
 story.append(Facsimile(pageid));story.append(Spacer(1,8))
 p('<link href="#text_'+pageid+'" color="#176F75">Consulter les lectures comparées</link> · Encadré rouge : région cible, lecture provisoire.','small')
 page('TRANSCRIPTIONS COMPARÉES · '+pageid,pageid+' : lectures',anchor='text_'+pageid)
 p('<link href="#image_'+pageid+'" color="#176F75">Revenir au fac-similé</link> · A accord ; N accord normalisé ; D divergence ; Z− / I− absent. Lectures importées ; seules les régions cibles ont été examinées. Les retours à la ligne dans une cellule sont typographiques.','small')
 rs=[r for r in rows if r['page']==pageid]
 cells=[[Paragraph(x,styles['head']) for x in ['Locus','État','ZL3b','IT2a']]]
 for r in rs:
  locus=r['locus'].split('.')[1]
  if any(a['locus']==r['locus'] for a in annotations):locus+=' *'
  cells.append([Paragraph(locus,styles['cell']),Paragraph(codes[r['status']],styles['cell']),
   Paragraph(escape(r['diplomatic_ZL'] or '[absent]'),styles['trans']),
   Paragraph(escape(r['diplomatic_IT'] or '[absent]'),styles['trans'])])
 t=Table(cells,colWidths=[38,33,214,214],repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),
  ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F1F5F4'),colors.white]),
  ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
  ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
 story.append(t);story.append(Spacer(1,8));p('* Région du mot cible localisée sur l’image ; cela ne valide pas toute la ligne.','small')

page('REPRODUCTION ET PORTÉE','Ce que cette édition établit')
p('Les douze fac-similés sont reliés à des photographies sources identifiées. Les 384 loci conservent les deux lectures, leurs absences et les signes d’incertitude. Les huit régions d’intérêt disposent de coordonnées et d’extraits traçables. La robustesse de trois correspondances est établie uniquement pour les variantes effectivement testées.')
p('Ce que cette édition n’établit pas','h')
p('Elle ne détermine ni la langue, ni la prononciation, ni le sens des quatre formes. Elle ne corrige pas automatiquement les divergences, ne fournit pas une transcription entièrement validée des douze pages et ne remplace pas une relecture experte indépendante.')
p('Fichiers et reproduction','h')
p('audit_transcription.py reconstruit l’alignement et les tests de séparation. make_edition.py reconstitue ce document. verify_pilot.py contrôle les sources, les coordonnées, les effectifs et les cas de séparation incertaine. Le README décrit la portée des résultats et l’usage du dossier.','small')
p('Sources en ligne','h')
for label,url in [('Yale : catalogue du manuscrit','https://collections.library.yale.edu/catalog/2002046'),('Yale : manifeste IIIF officiel','https://collections.library.yale.edu/manifests/2002046'),('Transcriptions et historique','https://www.voynich.nu/transcr.html'),('Définition IVTFF','https://www.voynich.nu/software/ivtt/IVTFF_format.pdf'),('Description du folio 89','https://www.voynich.nu/q15/index.html')]:
 p(escape(label)+'<br/><link href="'+url+'" color="#176F75">'+url+'</link>','small')
p('Crédit des photographies : Cipher manuscript (Voynich manuscript), General Collection, Beinecke Rare Book and Manuscript Library, Yale University. Les fichiers sources sont conservés sans retouche. Les fac-similés du PDF sont recadrés et réduits pour l’affichage ; les extraits ne sont pas reconstruits par IA.','small')

def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#CBD7D8'));c.line(48,43,547,43)
 c.setFont('DV',7.6);c.setFillColor(MUTED);c.drawString(48,29,'VOYNICH · Édition pilote · Lectures provisoires, aucune traduction')
 c.drawRightString(547,29,str(doc.page))
pdf=OUT/'Voynich_pilote_12_pages_2026-10-28.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=40,bottomMargin=59,
 title='Voynich : édition pilote de douze pages, images et lectures comparées',author='Étude réalisée avec ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(pdf)
