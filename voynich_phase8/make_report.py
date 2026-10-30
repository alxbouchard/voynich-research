#!/usr/bin/env python3
import json
from pathlib import Path
from xml.sax.saxutils import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
ROOT=Path(__file__).resolve().parent
S=json.loads((ROOT/'results/transfer_summary.json').read_text());A=json.loads((ROOT/'results/image_audit.json').read_text())['items']
for name,weight in [('DV','normal'),('DVB','bold')]:pdfmetrics.registerFont(TTFont(name,font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight=weight))))
W,H=595.276,841.89;M=44;CW=W-2*M;INK=colors.HexColor('#183239');TEAL=colors.HexColor('#087E82');GREY=colors.HexColor('#536168')
styles={k:ParagraphStyle(k,fontName='DVB' if k in ['h1','h2','th'] else 'DV',fontSize=size,leading=leading,textColor=colors.white if k=='th' else TEAL if k=='h2' else GREY if k=='small' else INK) for k,size,leading in [('h1',22,27),('h2',12,16),('body',10,14.2),('small',8.4,11.5),('table',9,12),('th',9,12),('card',9,12.4)]}
path=ROOT/'output/pdf/Voynich_phase8_audit_images_2026-10-28.pdf';C=canvas.Canvas(str(path),pagesize=(W,H));C.setTitle('Voynich, phase 8 : éprouver les ambiguïtés sur les images');C.setAuthor('Analyse assistée par IA pour Alex');page=0;y=0;bottom=[]
def text_at(txt,x,top,width,style='body'):
 obj=Paragraph(txt,styles[style]);_,hh=obj.wrap(width,2000);obj.drawOn(C,x,top-hh);return hh
def p(txt,style='body',gap=10):
 global y
 obj=Paragraph(txt,styles[style]);_,hh=obj.wrap(CW,2000);assert y-hh>52,(page,y,hh,txt[:50]);obj.drawOn(C,M,y-hh);y-=hh+gap

def start(title):
 global y,page
 if page:bottom.append(y);C.showPage()
 page+=1;C.setFillColor(TEAL);C.rect(0,H-8,W,8,fill=1,stroke=0);C.setFont('DVB',7.6);C.drawString(M,H-32,'VOYNICH / PHASE 8 / TRANSCRIPTION ET IMAGES');C.setFillColor(GREY);C.setFont('DV',8);C.drawRightString(W-M,H-32,'28 OCT. 2026');C.setStrokeColor(colors.HexColor('#D5E1E3'));C.line(M,40,W-M,40);C.setFont('DV',7.3);C.drawString(M,27,'VARIANTES CONSERVÉES · AUCUNE TRADUCTION VALIDÉE');C.drawRightString(W-M,27,str(page));y=H-60;p(title,'h1',16)
def table(rows,widths):
 global y
 t=Table([[Paragraph(str(x),styles['th' if i==0 else 'table']) for x in r] for i,r in enumerate(rows)],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#EAF3F3')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]));_,hh=t.wrap(CW,1500);assert y-hh>52;t.drawOn(C,M,y-hh);y-=hh+12

def audit_image(a,x,top,width,height):
 im=Image.open(ROOT/a['crop_file']);scale=min(width/im.width,height/im.height);ww=im.width*scale;hh=im.height*scale;xx=x+(width-ww)/2
 C.drawImage(str(ROOT/a['crop_file']),xx,top-hh,width=ww,height=hh)
 mark=xx+(a['boundary_x_approx']-a['bbox_xyxy'][0])*scale
 C.setStrokeColor(TEAL);C.setLineWidth(1.5);C.line(mark,top+8,mark,top+1);C.line(mark,top+1,mark-3,top+5);C.line(mark,top+1,mark+3,top+5)
 return hh

start('Le modèle ne tranche pas les espaces incertains')
p('<b>Le modèle ne permet pas de corriger automatiquement les espaces incertains.</b> Sur 1 089 positions comparables, il suit la transcription IT dans 716 cas (65,7 %). La règle « toujours séparer » en suit 700 (64,3 %). Le gain ne dépasse donc que 16 positions.')
table([['Comparaison avec IT','Accord','Positions'],['Modèle figé, seuil 0,5','65,7 %','716 / 1 089'],['Toujours insérer un espace','64,3 %','700 / 1 089'],['Scores ≤ 0,1 ou ≥ 0,9 seulement','79,0 %','252 / 319']],[CW-200,85,115])
p('Le dernier choix ne couvre que 29,3 % des ambiguïtés et conserve <b>67 désaccords</b>. Le score est appris sur les frontières nettes ZL ; il n’est pas une probabilité établie de lecture correcte pour les frontières incertaines.')
p('Les scores extrêmes sont trop assurés pour ce transfert','h2',6)
fig,ax=plt.subplots(figsize=(7,2.5),layout='constrained');d=S['deciles'];ax.plot([0,1],[0,1],color='#ADB6BA',linestyle='--',linewidth=1,label='Accord idéal entre score et fréquence');ax.plot([r['mean_p'] for r in d],[r['IT_split_fraction'] for r in d],'o-',color='#087E82',linewidth=1.6,label='Fréquence observée dans IT');ax.set(xlim=(0,1),ylim=(0,1),xlabel='Score moyen du modèle pour « espace »',ylabel='Fraction séparée par IT');ax.grid(alpha=.15);ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False,fontsize=7,loc='lower right');fp=ROOT/'results/reliability.png';fig.savefig(fp,dpi=200);plt.close(fig)
C.drawImage(str(fp),M,y-180,width=CW,height=180);y-=190
p('Parmi les 171 scores inférieurs à 0,1, le score moyen vaut 0,028, mais IT sépare 30,4 % des positions. IT est un comparateur, pas une vérité linguistique. Ce désaccord indique un transfert insuffisant des scores vers ce sous-ensemble.','small')
p('Portée du résultat','h2',4)
p('Le résultat précédent à environ 90 % concernait les frontières nettes. Ici, la population et le comparateur changent. Le rééchantillonnage des cahiers situe le gain sur « toujours séparer » entre -1,6 et +10,7 points ; cet intervalle descriptif inclut zéro. Les modèles des plis partagent une partie de leur apprentissage.','small')

start('Six frontières, trois feuillets')
p('Pour chaque page, les scores minimum et maximum ont été retenus avant l’examen ciblé des lignes. Les flèches indiquent la frontière approximative ; les images sont de simples découpes des scans. Examen par l’assistant, non aveugle, guidé par les deux transcriptions.','small',10)
cardwidth=(CW-20)/2;rowheight=187;top=y
short=[
 'L’encre est pâle ; la boucle de k rend la largeur du blanc dépendante de la hauteur examinée.',
 'Les signes y et d se distinguent. La décision de séparer reste une convention de transcription.',
 'Un blanc est visible entre l’ovale et la hampe, même quand IT les joint dans un groupe.',
 'Les prolongements inférieurs sont proches. IT sépare aussi ol et shedy, hors de la cible.',
 'Deux l se suivent : IT joint le premier à okeeol et sépare le second. Conserver les deux virgules ZL.',
 'IT sépare ici et lit qokchy là où ZL lit qokeey. La divergence de signes reste ouverte.'
]
for idx,a in enumerate(A[:6]):
 x=M+(idx%2)*(cardwidth+20);yy=top-(idx//2)*rowheight
 text_at(f'<b>{a["id"]} · {a["locus"].split(",")[0]}</b> · score {a["p4"]:.4f}'.replace('.',',',0),x,yy,cardwidth,'card')
 audit_image(a,x,yy-27,cardwidth,75)
 txt=f'<b>ZL</b> {escape(a["ZL_local"])}<br/><b>IT</b> {escape(a["IT_local"])}<br/>{short[idx]}'
 hh=text_at(txt,x,yy-111,cardwidth,'small');assert hh<76,(idx,hh)
y=top-3*rowheight-5
p('<b>Notation :</b> virgule = espace incertain ZL ; point = séparation transcrite. EVA code les formes des signes, pas leur son ni leur sens. Ces six cas ciblés ne mesurent pas une performance sur l’ensemble du manuscrit.','small',0)

start('Un désaccord malgré un score extrême')
a=A[6]
p('<b>Feuillet 113v, ligne 43 : qok,aiinos.</b> Le score « espace » tombe à 0,000113. Le modèle recommande donc de joindre. IT conserve pourtant une séparation : <b>qok.aiin.os</b>.')
hh=audit_image(a,M,y-8,CW,175);y-=hh+25
p('Image Yale 1006271, découpe native [1990, 2710, 2370, 2800]. La flèche vise la frontière après qok. Un intervalle entre les traits est visible. Cela ne suffit ni à démontrer une frontière de mot ni à justifier sa suppression.','small')
p('Ce septième cas a été sélectionné après le calcul : c’est le désaccord modèle/IT le plus extrême du sous-ensemble examiné. Il documente une limite ; il ne constitue pas un test représentatif des images.','small')
p('Décision pour l’édition de travail','h2')
p('Les <b>2 394 virgules d’origine restent intactes</b>. Le registre associe maintenant les scores figés, les 1 089 correspondances strictes avec IT et sept examens d’image localisés. Aucun texte corrigé automatiquement et aucune traduction ne sont produits.')
p('Une variante est conservée lorsque la lecture des signes, la séparation ou les deux restent incertaines. Le score sert à ordonner les examens ; il ne doit pas être utilisé comme poids probabiliste fiable avant validation adaptée aux ambiguïtés.')
p('Ce que cette étape apporte au déchiffrement','h2')
p('Elle empêche de fabriquer un texte d’entrée artificiellement certain. Toute hypothèse de chiffre ou de langue devra expliquer plusieurs segmentations admissibles, respecter les frontières robustes et réussir sur du texte réservé. Un accord local avec quelques signes ne suffira pas.')

start('Protocole, vérifications et sources')
p('Comparaison des transcriptions','h2',5)
p('Modèle de phase 7 figé : contexte de quatre caractères EVA, apprentissage sur les autres cahiers. Les virgules ZL ne sont pas des étiquettes d’apprentissage. Aucune remise au point du seuil en phase 8. Un seul fragment conservé par locus et par transcription ; flux de caractères strictement identique. Les fragments peuvent exclure une partie du début ou de la fin de ligne.','small')
p('Ce filtrage retient 1 913 loci, comprenant 1 089 frontières incertaines ZL. Les transcriptions partagent le même manuscrit et des conventions ; elles ne sont pas deux observations linguistiques indépendantes. Les parties où les signes divergent sont exclues de cette comparaison chiffrée.','small')
table([['Sous-ensemble','Modèle','Toujours séparer'],['Currier A : 289 frontières','68,2 %','53,6 %'],['Currier B : 800 frontières','64,9 %','68,1 %']],[CW-200,100,100])
p('Le classement reste informatif (AUC 0,729), mais le seuil 0,5 fonctionne mal pour cette nouvelle cible, notamment en Currier B. Le modèle à deux caractères obtient 62,5 % d’accord ; les bords des groupes BPE64 obtiennent 65,9 %. Aucune variante ne suffit à trancher les lectures.','small')
p('Audit des images et reproduction','h2',5)
p('Six cibles fixées par la règle minimum/maximum sur f1r, f75r et f103r ; un septième cas ajouté après les résultats et identifié comme tel. Localisation manuelle assistée, sans évaluateur indépendant. Aucune mesure automatisée de largeur d’encre ni validation de frontière linguistique revendiquée. Les coordonnées sont celles des JPEG Yale, origine en haut à gauche.','small')
p('Vérification indépendante : reconstruction des 1 089 paires, recomptage de la matrice de désaccords, AUC obtenue par 272 300 comparaisons directes, contrôle SHA-256 des quatre scans et égalité exacte des pixels des sept découpes. La vérification ne certifie pas l’identification paléographique manuelle. L’archive contient les scripts, données figées, variantes et protocole.','small')
p('Sources primaires et dépendances','h2',5)
p('[1] Yale, Beinecke MS 408, <link href="https://collections.library.yale.edu/catalog/2002046" color="#087E82">notice et images numérisées</link>. Identifiants : 1006076 (f1r), 1006208 (f75r), 1006254 (f103r), 1006271 (f113v). Les trois premières images ont été acquises en phase 3 ; la quatrième lors de cette étape. Images sources conservées avec empreintes.','small',7)
p('[2] René Zandbergen, <link href="https://voynich.nu/extra/sp_transcr.html" color="#087E82">conventions IVTFF et historique des transcriptions</link>. Corpus figés ZL3b-n et IT2a-n ; ZL et Takeshi Takahashi (IT). Les fichiers bruts et leur provenance sont conservés dans le dossier de recherche.','small',7)
p('[3] Notre phase 7 : prédictions hors cahier, données de segmentation et BPE64 figés. L’archive de phase 8 reproduit ses nouveaux calculs à partir de ces sorties. Elle ne réexécute pas toute la chaîne des phases 1 à 7. Les résultats sur les ambiguïtés sont exploratoires ; le protocole local ne constitue pas un préenregistrement indépendant.','small',7)
p('<b>Conclusion :</b> le manuscrit reste non déchiffré dans ce dossier. La présente étape fournit une transcription à variantes mieux documentée et invalide l’usage des scores de phase 7 comme certitudes pour corriger les espaces incertains.','small',0)
bottom.append(y);C.save();(ROOT/'results/report_layout.json').write_text(json.dumps({'pages':page,'bottoms':bottom},indent=2)+'\n');print(path);print('pages',page,'bottoms',bottom)
