from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent.parent
for n,f in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=22,leading=27,textColor=HexColor('#133642'),spaceAfter=13),
 'body':ParagraphStyle('body',fontName='DV',fontSize=10,leading=14.5,spaceAfter=9),
 'sub':ParagraphStyle('sub',fontName='DVB',fontSize=12,leading=16,textColor=HexColor('#133642'),spaceBefore=10,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11,spaceAfter=7),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.5,leading=12)}
story=[]
def p(t,s='body'):story.append(Paragraph(t,styles[s]))
def tab(rows,widths):
 t=Table([[Paragraph(str(c),styles['cell']) for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dcebee')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,HexColor('#548291')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f3f6f7')])]))
 story.extend([t,Spacer(1,9)])
data=json.loads((ROOT/'results/rule_audit.json').read_text())
p('VOYNICH · PHASE 12 · OCTOBRE 2026','small')
p('Reconstruire les règles','title')
p('<b>Aucune traduction validée.</b> Cette phase tente une lecture automatique à partir des seules règles de suppression et des 18 mots de départ du guide de Scott Schechter. Elle vérifie aussi deux affirmations indépendantes : les signes déclarés sans contenu et la conjugaison latine présentée comme preuve.')
p('1. Une règle universelle ne reproduit pas toutes les lectures','sub')
p('Le guide demande de retirer systématiquement les groupes EVA <b>cth, ckh, cph, cfh</b>, supposés sans information. Le code consulte pourtant le glossaire avant cette suppression. Sur 1 845 occurrences de prose contenant ces groupes et reconnues par le code, appliquer la suppression en premier conserve 1 732 lectures, en change <b>95</b> et en perd 18.')
tab([['Forme EVA','Après suppression','Lecture directe','Lecture après suppression','Occurrences'],['shckhy','shy','HEUS','HIC','60'],['sheckhy','shey','HEUS','HEC','35']],[85,103,90,145,80])
p('Ces 95 divergences concernent deux formes avec <b>ckh</b>, soit 5,20 % des 1 827 occurrences dont les deux lectures existent. Elles montrent une incompatibilité entre la règle universelle du guide et certaines entrées du glossaire. Elles ne donnent pas le sens réel de ckh. Le document 18-null-analysis.md envisage lui-même que ces signes portent de l’information.')
p('2. Propagation sans le glossaire complet','sub')
p('Un programme distinct part des 18 paires du guide et explore toutes les suppressions autorisées : préfixes, ch/f médians, t/g/p finaux et les quatre groupes ci-dessus. Il conserve toutes les réponses accessibles. Le glossaire complet sert ensuite uniquement à comparer les résultats, jamais à choisir une lecture.')
tab([['Variante','Occurrences avec candidat','Dont plusieurs réponses','Désaccord avec le glossaire*'],['Préfixes originaux','5 496 / 34 411 (15,97 %)','0','406 / 5 490'],['Préfixes étendus','6 485 / 34 411 (18,85 %)','164','1 226 / 6 438']],[116,151,98,138])
p('* Dénominateur : occurrences où le programme original fournit aussi une lecture. Il s’agit d’accord interne, pas d’exactitude de traduction. Dans la variante étendue, qokol peut conserver NOCET ou devenir GRATIA après retrait du préfixe qo. La procédure seule ne choisit pas entre ces attributions.','small')
p('<b>Portée limitée :</b> ce test porte sur la propagation des mots de départ. Il n’implémente pas l’ensemble des tables de substitution, la reconstruction des voyelles ou les choix guidés par le contexte. Sa faible couverture ne réfute donc pas le système complet. Les 18 sens de départ restent eux-mêmes non confirmés.','small')
story.append(PageBreak())

p('Contrôle linguistique et résultats','title')
p('3. L’argument des conjugaisons nécessite une correction','sub')
p('Le dépôt présente plusieurs formes de NOCERE comme des conjugaisons correctes. Le dictionnaire Lewis et Short classe <i>noceo</i> dans la deuxième conjugaison, avec le parfait <i>nocui</i>. Les tableaux d’Allen et Greenough permettent de vérifier les personnes et temps revendiqués [1-3].')
tab([['Forme du dépôt','Étiquette revendiquée','Forme du latin standard'],['NOCIS','2e personne singulier, présent','NOCES'],['NOCITIS','2e personne pluriel, présent','NOCETIS'],['NOCERAT','3e personne singulier, plus-que-parfait','NOCUERAT']],[116,240,147])
p('Les formes de référence se déduisent du thème noce- au présent et de nocu- au parfait : noc-e-s, noc-e-tis, nocu-erat. Des formes comme NOCET et NOCUIT sont, elles, compatibles avec le latin. Cette vérification ne permet pas d’affirmer que toute variante médiévale ou occitane est impossible. Une variante invoquée pour sauver l’analyse doit toutefois être attestée précisément, avec la valeur grammaticale annoncée.')
p('Démonstration sur trois folios','sub')
tab([['Folio','Occurrences retenues','Candidats, règles originales','Candidats, règles étendues'],['f1r','202','29','40'],['f75r','422','85','95'],['f103r','522','102','109']],[60,120,161,162])
p('Ces folios illustrent l’application des règles ; ils ne sont pas inconnus de l’auteur et ne constituent pas une validation aveugle. Aucun passage complet n’est confirmé par cet essai. Les sorties sont des variantes des 18 significations de départ, pas des sens nouveaux découverts.')
p('Traçabilité et vérification','sub')
p('Le corpus conserve 34 411 occurrences de prose, soit 7 069 formes différentes ; 80 occurrences incertaines ou atypiques sont exclues. Toutes les classes de lignes P sont incluses. Le parseur original, toutes classes confondues, retrouve séparément les 37 886 occurrences de la phase précédente. Un second algorithme vérifie indépendamment les <b>14 138 prédictions</b> (deux variantes × 7 069 formes). Les 12 fichiers amont sont vérifiés par empreintes Git et SHA256.','small')
p('Source expérimentale : <link href="https://github.com/scott-schechter/voynich-decoded">github.com/scott-schechter/voynich-decoded</link>, commit 71f2f3c91e9113d285ab21e024f1dd70c1f43c44. Fichiers : 07-reproduction-guide.md, 02-verb-paradigms.md, 18-null-analysis.md, decode.js et glossary-export.js. Le protocole, le code et les mesures sont joints dans l’archive.','small')
p('[1] <link href="https://atlas.perseus.tufts.edu/dictionaries/entry/urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:lat.ls.perseus-eng2-n31073/">Lewis et Short, entrée noceo, Perseus / Tufts</link>.<br/>[2] <link href="https://dcc.dickinson.edu/sites/default/files/2nd_conj_pres.pdf">Allen et Greenough, deuxième conjugaison, présent</link>, Dickinson College.<br/>[3] <link href="https://dcc.dickinson.edu/sites/default/files/2nd_conj_plperf.pdf">Allen et Greenough, deuxième conjugaison, plus-que-parfait</link>, Dickinson College. Sources consultées le 29 octobre 2026 UTC.','small')

def footer(c,d):
 c.setStrokeColor(HexColor('#c4d6db'));c.line(46,43,549,43);c.setFont('DV',8);c.setFillColor(HexColor('#53707a'));c.drawString(46,29,'Voynich · Phase 12 · Règles et contrôle linguistique');c.drawRightString(549,29,str(d.page))
out=ROOT/'output/pdf/Voynich_phase12_regles_et_langue.pdf'
SimpleDocTemplate(str(out),pagesize=(595,842),leftMargin=46,rightMargin=46,topMargin=43,bottomMargin=57,title='Voynich phase 12 - Règles et contrôle linguistique',author='Analyse réalisée avec ChatGPT').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
