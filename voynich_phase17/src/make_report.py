from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
W,H=595.28,841.89;M=43;CW=W-2*M
INK=HexColor('#142a38');ACCENT=HexColor('#176d7b');MUTED=HexColor('#506572');PALE=HexColor('#edf4f5')
c=canvas.Canvas(str(OUT/'Voynich_phase17_spectral_et_cryptanalyse.pdf'),pagesize=(W,H))
c.setTitle('Voynich phase 17 : imagerie brute et test d’une formule marginale')
c.setAuthor('Dossier de recherche préparé pour Alex')

def para(text,y,size=10.2,leading=15,bold=False,color=INK,width=CW,x=M):
    s=ParagraphStyle('body',fontName='DVB' if bold else 'DV',fontSize=size,leading=leading,textColor=color)
    p=Paragraph(text,s);_,h=p.wrap(width,800);p.drawOn(c,x,y-h);return y-h

def top(n,title,subtitle):
    c.setFillColor(ACCENT);c.setFont('DVB',9);c.drawString(M,H-38,'VOYNICH / PHASE 17 / EXPÉRIENCE EXPLORATOIRE')
    y=para(title,H-67,25,30,True)
    y=para(subtitle,y-14,11,16,color=MUTED)
    c.setStrokeColor(HexColor('#ccd9de'));c.line(M,42,W-M,42)
    c.setFillColor(MUTED);c.setFont('DV',8)
    c.drawString(M,27,'Aucune traduction validée du texte principal')
    c.drawRightString(W-M,27,str(n))
    return y-25

def table(data,y,widths):
    style=ParagraphStyle('cell',fontName='DV',fontSize=9,leading=12,textColor=INK)
    d=[[Paragraph(str(x),style) for x in row] for row in data]
    t=Table(d,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
                          ('LINEBELOW',(0,0),(-1,0),.7,ACCENT),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#dbe4e7')),
                          ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                          ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    _,h=t.wrap(CW,800);t.drawOn(c,M,y-h);return y-h

y=top(1,'Les images donnent des contraintes,<br/>pas encore une lecture',
      'Les 22 captures brutes de f116v ont été traitées. Le premier signe de la suite dite « oror / aror sheey » reste trop ambigu pour imposer une lecture sûre.')
y=para('Comparaison du même fragment',y,12,16,True)
img=ROOT/'figures/report_comparison.png';iw=440;ih=iw*640/1060
c.drawImage(ImageReader(img),(W-iw)/2,y-12-ih,width=iw,height=ih)
y=y-ih-23
y=para('Même région, contrastes différents. Les deux vues du haut proviennent de captures individuelles après normalisation locale. Les vues du bas sont des composantes calculées. Une composante peut atténuer l’écriture et amplifier le fond : elle n’est pas une nouvelle couche de texte.',y,9,13,color=MUTED)
y=para('Ce qui a réellement été exécuté',y-20,12,16,True)
y=para('Rotation sans rééchantillonnage, alignement, médiane 3 × 3 et contraste local. L’analyse en composantes principales (ACP) porte sur les 22 captures, puis sur les 12 captures de réflexion et les 10 de fluorescence séparément. Neuf composantes sont conservées.',y-8)
y=para('Les 22 recadrages sont identiques pixel par pixel à une extraction indépendante. Les translations atteignent 3 pixels et les résidus estimés 1 pixel : de très fins contours isolés restent sujets aux artefacts.',y-12)
y=para('Limites : aucun étalonnage chimique ; observation guidée par les lectures publiées ; aucune identité de main ni date établie. Les captures montrent la même inscription.',y-12,9,13,color=MUTED)
y=para('Images : Beinecke Rare Book & Manuscript Library MS 408, f116v. The Lazarus Project and The Chester F. Carlson Center for Imaging Science at Rochester Institute of Technology. Nouveaux calculs documentés dans le dossier.',y-12,8,11,color=MUTED)
assert y>48,('page1 overflow',y)
c.showPage()

y=top(2,'Une formule proposée à l’épreuve',
      'Hypothèse testée : un passage du manuscrit cacherait littéralement « six marix morix vix ». Cette lecture de la marge reste provisoire ; son équivalence avec le texte principal n’est pas démontrée.')
y=para('Deux modèles fixes',y,12,16,True)
y=para('1. Substitution bijective : un signe par lettre, et une lettre par signe.<br/>2. Substitution homophonique : plusieurs signes peuvent représenter la même lettre, mais chaque signe garde une valeur unique. Aucun joker pour les caractères illisibles. Recherche dans les deux sens, sans franchir les barrières de paragraphe, de lacune ou de dessin.',y-7)
y=para('<b>Résultat :</b> aucune correspondance bijective ; aucune correspondance homophonique conservant les quatre mots. En supprimant les espaces, les candidats suivants apparaissent :',y-13)
data=[['Corpus et unités','Candidats homophoniques','Après extension « maria »'],
      ['ZL, caractères EVA','37','1'],['ZL, signes composés','9','0'],
      ['IT, caractères EVA','40','3'],['IT, signes composés','12','0']]
y=table(data,y-12,[CW*.43,CW*.27,CW*.30])
y=para('Les deux traitements des espaces incertains donnent ici les mêmes nombres de candidats. ZL et IT sont deux transcriptions du même manuscrit, pas deux livres indépendants. « Signes composés » regroupe notamment ch, sh, cth et ckh. L’extension autorise un intervalle de 0 à 8 unités et conserve les valeurs déjà imposées.',y-10,8.5,12,color=MUTED)
y=para('Les candidats ne deviennent pas une traduction',y-17,12,16,True)
y=para('<b>f104r.22-23 :</b> une correspondance mécanique apparaît uniquement en sens inverse et sans espaces, hors du paragraphe contenant aror,sheey. Elle échoue à l’extension « maria » avec la même clé pour tous les intervalles testés.',y-7)
y=para('<b>f79r.9-10 :</b> seul candidat prolongé commun à ZL et IT, en EVA caractère par caractère. Il commence au dernier caractère de qokal, traverse plusieurs mots et retrouve « maria » sans aucun intervalle après vix. Il ne restitue donc pas le groupe intermédiaire visible dans la marge. Deux autres cas prolongés existent seulement dans IT, sur f85r1 et f101r.',y-11)
y=para('<b>Diagnostic supplémentaire :</b> 32 brouillages internes aux paragraphes ZL donnent 2 à 10 correspondances, contre 37 dans l’ordre original. Le motif est plus fréquent dans le texte réel que dans ces contrôles ; cela peut refléter sa structure répétitive. Ce calcul exploratoire ne démontre ni le sens de la formule ni une clé.',y-11)
y=para('L’extension et les brouillages ont été ajoutés après le premier balayage. Ils ne constituent pas une validation indépendante sur des pages réservées. Ces essais ne couvrent ni les syllabaires, ni les abréviations, ni les valeurs variables selon le contexte, ni toutes les lectures de la marge.',y-13,9,13,color=MUTED)
assert y>48,('page2 overflow',y)
c.showPage()

y=top(3,'Le parallèle historique reste limité',
      'Un rapprochement avec une formule ancienne peut éclairer le genre d’une annotation. Pour décoder le livre, il faudrait encore établir une équivalence textuelle et une règle qui prédit d’autres passages.')
y=para('Une attestation vérifiée',y,12,16,True)
y=para('Peter Murray Jones et Lea T. Olsan publient une photographie d’un charme inscrit au bas du folio 129v du manuscrit British Library Sloane 3160, daté du XVe siècle. Leur transcription contient <b>erex + arex + rymex</b>. La formule concerne l’accouchement. La photographie et le passage ont été vérifiés dans l’article : pages imprimées 412 et 414, figure 1.',y-8)
y=para('Le rapprochement avec les groupes terminés en -ix et les croix de f116v est une <b>hypothèse de genre</b>. Les mots diffèrent. Il ne démontre pas une copie de cette source, une parenté entre les deux textes, le sujet du Voynich ni la langue du texte principal. Aucun parallèle exact de plusieurs mots n’a été établi dans cette phase.',y-12)
y=para('Ce que le dossier permet de reproduire',y-22,12,16,True)
y=para('Le dossier conserve les 22 recadrages en 16 bits, leurs empreintes et coordonnées, les 22 contrastes individuels, neuf composantes ACP, les corpus ZL et IT, tous les candidats et clés partielles, les contrôles et les scripts. L’extension « maria » n’ajuste jamais une valeur déjà imposée par la première formule.',y-8)
y=para('Contrôles logiciels : témoins positifs de substitution et d’homophonie, contradictions de signes répétés, 6 817 petites comparaisons exhaustives, contrôle des barrières, vérification de chaque candidat accepté. Un second calcul vectorisé reproduit les 37 correspondances ZL avant les brouillages. Les résultats numériques et textuels sont recalculés avant livraison.',y-11)
y=para('Constat scientifique',y-22,12,16,True)
y=para('<b>Aucun passage du texte principal n’a reçu une traduction validée.</b> Les données brutes n’ont pas résolu l’ambiguïté ciblée. La formule proposée ne fournit pas de clé vérifiée. Une prochaine percée devra produire une correspondance justifiée et des prédictions correctes sans réajuster la clé à chaque mot ; accumuler des rapprochements visuels ne suffira pas.',y-8)
y=para('Sources',y-22,12,16,True)
sources=[
 ('Lisa Fagin Davis, imagerie multispectrale, 8 septembre 2024','https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/'),
 ('Koen Gheuens, étude des graphies de f116v, 28 août 2023','https://herculeaf.wordpress.com/2023/08/28/f116v-most-likely-readings-based-on-glyph-shapes/'),
 ('Jones et Olsan, Bulletin of the History of Medicine 89/3 (2015), 406-433 ; DOI 10.1353/bhm.2015.0076','https://api.repository.cam.ac.uk/server/api/core/bitstreams/4cfee618-728c-480e-ae25-c70d29403be4/content'),
 ('René Zandbergen, translittérations et conventions EVA / IVTFF','https://www.voynich.nu/transcr.html')]
for title,url in sources:y=para(f'<link href="{escape(url)}" color="#176d7b">{escape(title)}</link>',y-7,8.6,12)
assert y>48,('page3 overflow',y)
c.save();print(OUT/'Voynich_phase17_spectral_et_cryptanalyse.pdf')
