#!/usr/bin/env python3
import json
from pathlib import Path
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
ROOT=Path(__file__).resolve().parent
S={r['case']:r for r in json.loads((ROOT/'results/pooled_summary.json').read_text())};O={r['case']:r for r in json.loads((ROOT/'results/summary.json').read_text())};T={r['case']:r for r in json.loads((ROOT/'results/toy_summary.json').read_text())}
for name,weight in [('DV','normal'),('DVB','bold')]:pdfmetrics.registerFont(TTFont(name,font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight=weight))))
W,H=595.276,841.89;M=44;CW=W-2*M;INK=colors.HexColor('#17323B');TEAL=colors.HexColor('#087D82');GREY=colors.HexColor('#536168')
styles={k:ParagraphStyle(k,fontName='DVB' if k in ['h1','h2','th'] else 'DV',fontSize=size,leading=leading,textColor=colors.white if k=='th' else TEAL if k=='h2' else GREY if k=='small' else INK) for k,size,leading in [('h1',21,26),('h2',12,16),('body',10,14.2),('small',8.4,11.8),('table',8.8,12),('th',8.8,12)]}
path=ROOT/'output/pdf/Voynich_phase9_dependances_2026-10-28.pdf';C=canvas.Canvas(str(path),pagesize=(W,H));C.setTitle('Voynich, phase 9 : dépendances locales entre groupes');C.setAuthor('Analyse assistée par IA pour Alex');page=0;y=0;bottom=[]
def p(txt,style='body',gap=10):
 global y
 obj=Paragraph(txt,styles[style]);_,hh=obj.wrap(CW,2000);assert y-hh>52,(page,y,hh,txt[:80]);obj.drawOn(C,M,y-hh);y-=hh+gap

def start(title):
 global y,page
 if page:bottom.append(y);C.showPage()
 page+=1;C.setFillColor(TEAL);C.rect(0,H-8,W,8,fill=1,stroke=0);C.setFont('DVB',7.7);C.drawString(M,H-32,'VOYNICH / PHASE 9 / DÉPENDANCES ENTRE GROUPES');C.setFillColor(GREY);C.setFont('DV',8);C.drawRightString(W-M,H-32,'28 OCT. 2026');C.setStrokeColor(colors.HexColor('#D5E1E3'));C.line(M,40,W-M,40);C.setFont('DV',7.4);C.drawString(M,27,'STRUCTURE GRAPHIQUE · AUCUNE TRADUCTION VALIDÉE');C.drawRightString(W-M,27,str(page));y=H-60;p(title,'h1',16)
def table(rows,widths):
 global y
 t=Table([[Paragraph(str(x),styles['th' if i==0 else 'table']) for x in r] for i,r in enumerate(rows)],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#EAF3F3')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]));_,hh=t.wrap(CW,1600);assert y-hh>52,(page,y,hh);t.drawOn(C,M,y-hh);y-=hh+13

def num(v,n=3):return f'{v:.{n}f}'.replace('.',',')
def pct(v):return num(100*v,1)+' %'

start('La fin d’un groupe aide à prévoir le début du suivant')
p('<b>Un effet de voisinage reste mesurable sur des cahiers exclus de l’apprentissage.</b> Dans le sous-ensemble ZL / Currier B, tenir compte du dernier caractère du groupe précédent fait passer la réussite sur le premier caractère suivant de <b>24,1 % à 32,6 %</b>. Le modèle de référence tient déjà compte de la section, de la main et de positions approximatives dans la ligne et le paragraphe.')
p('Cette dépendance est connue dans la littérature [1-3]. Notre apport dans ce dossier est son test hors cahier, avec des frontières conservatrices, des témoins et une vérification séparée des calculs. Ce n’est ni une clé ni une découverte de sens.','small')
table([['Données','Cibles','Gain moyen<br/>(bits / cible)','Intervalle descriptif'],*[['ZL / A' if k=='ZL_A' else 'ZL / B' if k=='ZL_B' else 'IT / A' if k=='IT_A' else 'IT / B',str(S[k]['primary']['n']),num(S[k]['primary']['gain_bits']),num(S[k]['bootstrap']['gain_ci'][0])+' à '+num(S[k]['bootstrap']['gain_ci'][1])] for k in ['ZL_A','ZL_B','IT_A','IT_B']]],[100,70,130,CW-300])
p('Un gain positif signifie que le modèle attribue, en moyenne, une meilleure probabilité au caractère réellement observé. Il ne s’agit pas d’un pourcentage de texte traduit. Les intervalles rééchantillonnent les cahiers, sans réapprentissage ; les ensembles d’apprentissage se chevauchent.','small')
p('Un contrôle qui conserve la position','h2',5)
p('Pour chaque corpus, 199 mélanges échangent les finales précédentes uniquement dans la même page et la même catégorie de position. Chaque mélange est réappris et testé. Les quatre gains Voynich observés dépassent leurs 199 témoins ; les moyennes témoins sont proches de -0,006 bit. Ce diagnostic est exploratoire et ne corrige pas tous les effets possibles de mise en page.')
p('Une modification de méthode à garder visible','h2',5)
p('<b>Ces résultats viennent du deuxième modèle.</b> Le premier, fixé avant les calculs, séparait trop strictement les catégories d’écriture. Dans ZL / B, 79,9 % des cibles appartenaient à une catégorie absente de l’apprentissage de leur pli. Le second partage une correction de voisinage entre catégories. Il a été défini après ce diagnostic, avant ses propres calculs. Les deux versions sont conservées.','small')
p('Périmètre : paires de groupes intérieures aux lignes ; aucun groupe comportant une virgule incertaine ou un signe ambigu n’est forcé. ZL et IT sont deux transcriptions du même manuscrit, pas deux manuscrits indépendants.','small',0)

start('L’effet se concentre sur le voisin immédiat')
p('Le test ci-dessous utilise exactement les mêmes cibles pour les trois distances. Seule la finale donnée au modèle change : celle du groupe situé un, deux ou trois rangs avant la cible. Aucun intervalle illisible ou ambigu n’est franchi.','body',7)
fig,ax=plt.subplots(figsize=(7,3),layout='constrained')
for k,color,style in [('ZL_A','#087D82','-'),('ZL_B','#B56832','-'),('IT_A','#087D82','--'),('IT_B','#B56832','--')]:ax.plot([1,2,3],[S[k]['lags'][str(i)]['gain_bits'] for i in [1,2,3]],marker='o',color=color,linestyle=style,label=k.replace('_',' / '))
ax.axhline(0,color='#59676C',linewidth=.8);ax.set(xticks=[1,2,3],xlabel='Distance du groupe précédent',ylabel='Gain hors cahier (bits / cible)');ax.spines[['top','right']].set_visible(False);ax.grid(alpha=.15);ax.legend(frameon=False,ncol=2,fontsize=8);fp=ROOT/'results/lag_profile.png';fig.savefig(fp,dpi=200);plt.close(fig)
C.drawImage(str(fp),M,y-218,width=CW,height=218);y-=228
p('Le gain disparaît aux distances 2 et 3 avec ce modèle. Cela ne démontre pas l’absence de relations plus longues dans le manuscrit. Effectifs communs : 1 996 cibles ZL/A, 6 820 ZL/B, 3 044 IT/A et 10 142 IT/B.','small')
p('Le signe q n’explique pas tout','h2',5)
table([['Partie du gain','ZL / A','ZL / B'],['Prédire q contre tous les autres',num(S['ZL_A']['primary']['q_binary_gain_bits']),num(S['ZL_B']['primary']['q_binary_gain_bits'])],['Distinguer les caractères autres que q',num(S['ZL_A']['primary']['non_q_within_gain_bits']),num(S['ZL_B']['primary']['non_q_within_gain_bits'])]],[CW-190,95,95])
p('Cette décomposition exacte du score laisse environ 81 % du gain ZL/A et 58 % du gain ZL/B dans la distinction entre caractères autres que q. Elle ne consiste pas à supprimer q puis à réapprendre.','small')
p('Exemple descriptif : dans nos paires intérieures ZL/B, q commence 36,3 % des groupes qui suivent une finale y, contre 8,5 % après une finale n. Ces fréquences brutes ne sont pas corrigées des positions et ne constituent pas une règle de traduction. EVA nomme des formes graphiques, pas des sons établis.','small',0)

start('Ce que les témoins permettent de conclure')
table([['Témoin','Cibles','Gain du voisin<br/>(bits / cible)'],['Pline, latin','5 240',num(S['Latin_Pliny']['primary']['gain_bits'])],['Dante, italien','20 830',num(S['Italian_Paradiso']['primary']['gain_bits'])],['Chiffre Naibbe sur Pline','20 830',num(S['Naibbe_Pliny']['primary']['gain_bits'])],['Échantillon du générateur Timm','6 344',num(S['Timm_generated']['primary']['gain_bits'])],['Témoin synthétique : lien imposé','4 480',num(T['Toy_dependent']['primary']['gain_bits'])],['Témoin synthétique : tirages indépendants','4 480',num(T['Toy_independent']['primary']['gain_bits'])]],[CW-230,85,145])
p('<b>Cette mesure ne détecte pas le sens.</b> Pline contient un vrai texte et n’obtient pas de gain ici. À l’inverse, un texte synthétique sans message, construit pour relier les bords des groupes, donne un gain très fort. Dante montre qu’une langue connue peut aussi produire un effet de voisinage.')
p('Les échantillons Naibbe et Timm utilisés ici ne reproduisent pas le gain Voynich avec le réglage principal. Cela limite ces deux échantillons comme explications complètes ; cela n’exclut ni tous les chiffres ni toutes les méthodes de génération. Les tailles et genres diffèrent, et les quatre témoins héritent d’une disposition artificielle en lignes.','small')
p('Robustesse et exception','h2',5)
p('Les quatre sous-ensembles Voynich conservent un gain positif avec les deux autres niveaux de lissage, les unités EVA composées, l’exclusion des répétitions identiques et la restriction aux lignes entièrement lisibles. Le gain est positif dans 39 des 40 plis corpus/cahier ; l’exception est le cahier D de IT/B. Ces plis ne sont pas indépendants.','small')
p('Conséquence pour les hypothèses de déchiffrement','h2',5)
p('Une proposition doit pouvoir reproduire ce lien entre la fin d’un groupe et le début de son voisin immédiat, en plus de la forme des groupes isolés. Le lien pourrait venir de la langue, d’une convention d’écriture, d’un procédé de chiffrement ou d’une règle mécanique. Le présent test ne les départage pas à lui seul.')
p('La recherche d’une clé doit donc conserver le contexte des groupes voisins. Une table de correspondances fondée seulement sur des mots isolés laisserait de côté une information qui se retrouve dans d’autres cahiers. Aucune valeur phonétique ni aucun mot traduit n’est attribué ici.','small',0)

start('Méthode reproductible et limites')
p('Données et validation','h2',5)
p('Corpus figé de phase 6, paragraphes P0 pour Voynich. Les virgules incertaines, alternatives, illisibles et interruptions restent des barrières. La cible et son prédécesseur sont des positions intérieures, hors premier et dernier groupe de ligne. Les sous-ensembles A/B et ZL/IT sont séparés. Un cahier entier est exclu à chaque tour ; les témoins utilisent huit blocs de pages du gabarit, sans chevauchement de pages.','small')
p('La référence estime le premier caractère par une succession de distributions lissées : corpus, section/main, puis section/main × quartile horizontal × quartile vertical du paragraphe. Une ligne unique forme une cinquième classe verticale. Les positions sont calculées dans la transcription, sans coordonnées d’encre ni largeur de dessin.','small')
p('Le premier modèle ajoute une table locale incluant la finale précédente. Le second multiplie la référence par le rapport appris P(initiale | finale précédente) / P(initiale), puis renormalise. Tous ces calculs utilisent uniquement les plis d’apprentissage. Ce deuxième modèle suppose que la correction est partageable entre catégories. Le lissage principal vaut 32 ; 8 et 128 sont des sensibilités, sans choix du meilleur réglage.','small')
p('Le premier modèle donne des gains très faibles : ZL/A 0,007, ZL/B 0,003, IT/A 0,009 et IT/B 0,003 bit, avec des intervalles englobant zéro. Son défaut de couverture est reproduit par les deux témoins synthétiques à catégories exclusives. La correction de méthode est une analyse complémentaire après résultats, pas une confirmation préenregistrée.','small')
p('Contrôles réalisés','h2',5)
p('3 582 mélanges conditionnels au total : 1 592 pour chaque version sur les huit corpus, plus 398 sur les deux témoins synthétiques du second modèle. Une seconde implémentation par comptages recalcule 190 328 évaluations position/modèle, toutes les probabilités principales et quatre premiers tirages de contrôle. L’écart numérique maximal est inférieur à 10⁻¹⁵. Les feuillets de test sont disjoints de ceux d’apprentissage.','small')
p('Références principales','h2',5)
p('[1] Reddy et Knight (2011), <link href="https://aclanthology.org/W11-1511/" color="#087D82">What We Know About The Voynich Manuscript</link>, §5.2.<br/>[2] Feaster (2022), <link href="https://ceur-ws.org/Vol-3313/paper12.pdf" color="#087D82">Rightward and Downward Grapheme Distributions in the Voynich Manuscript</link>.<br/>[3] Rozanova et Temerev (2026), <link href="https://arxiv.org/abs/2608.17096" color="#087D82">arXiv:2608.17096v1</link>, prépublication, §2.10 et limites.<br/>[4] Greshko (2025), The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext. DOI 10.1080/01611194.2025.2566408.<br/>[5] Timm et Schinner (2019/2020), A possible generating algorithm of the Voynich manuscript. DOI 10.1080/01611194.2019.1596999.<br/>[6] Zandbergen, <link href="https://voynich.nu/extra/sp_transcr.html" color="#087D82">conventions IVTFF</link> ; transcriptions ZL3b-n et IT2a-n.','small')
p('L’archive inclut le protocole initial, l’addendum daté, les sorties des deux modèles, les données figées, les témoins, les licences, les scripts et leurs empreintes. Elle reproduit la phase 9 à partir des entrées conservées ; elle ne réexécute pas toutes les phases antérieures.','small',0)
bottom.append(y);C.save();(ROOT/'results/report_layout.json').write_text(json.dumps({'pages':page,'bottoms':bottom},indent=2)+'\n');print(path);print('pages',page,'bottoms',bottom)
