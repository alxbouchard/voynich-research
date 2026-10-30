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
S={x['case']:x for x in json.loads((ROOT/'results/summary.json').read_text())}
I=json.loads((ROOT/'results/prediction_intervals.json').read_text());G=json.loads((ROOT/'results/published_ink_gap_reanalysis.json').read_text())
P=json.loads((ROOT/'results/paired_transcriptions.json').read_text());V=json.loads((ROOT/'results/verification.json').read_text())
for name,weight in [('DV','normal'),('DVB','bold')]:pdfmetrics.registerFont(TTFont(name,font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight=weight))))
W,H=595.276,841.89;M=45;CW=W-2*M;INK=colors.HexColor('#193039');TEAL=colors.HexColor('#137B80');GREY=colors.HexColor('#53636A')
styles={k:ParagraphStyle(k,fontName='DVB' if k in ['h1','h2','th'] else 'DV',fontSize=size,leading=leading,textColor=colors.white if k=='th' else TEAL if k=='h2' else GREY if k=='small' else INK) for k,size,leading in [('h1',22,28),('h2',12,16),('body',10,14.3),('small',8.6,12),('table',8.7,12),('th',8.7,12)]}
path=ROOT/'output/pdf/Voynich_phase7_espaces_2026-10-28.pdf';C=canvas.Canvas(str(path),pagesize=(W,H));C.setTitle('Voynich, phase 7 : prédire les espaces et préserver les ambiguïtés');C.setAuthor('Analyse assistée par IA pour Alex');page=0;y=0;bottom=[]
def p(txt,style='body',gap=10):
 global y
 obj=Paragraph(txt,styles[style]);_,hh=obj.wrap(CW,1000);assert y-hh>50,(page,y,hh,txt[:50]);obj.drawOn(C,M,y-hh);y-=hh+gap
def start(title):
 global y,page
 if page:bottom.append(y);C.showPage()
 page+=1;C.setFillColor(TEAL);C.rect(0,H-8,W,8,fill=1,stroke=0);C.setFont('DVB',8);C.drawString(M,H-34,'VOYNICH  /  PHASE 7  /  EXPÉRIENCES SUR LES FRONTIÈRES');C.setFillColor(GREY);C.setFont('DV',8);C.drawRightString(W-M,H-34,'28 OCT. 2026');C.setStrokeColor(colors.HexColor('#D5E1E3'));C.line(M,40,W-M,40);C.setFont('DV',7.5);C.drawString(M,27,'PRÉDICTION GRAPHIQUE · AUCUNE TRADUCTION VALIDÉE');C.drawRightString(W-M,27,str(page));y=H-64;p(title,'h1',18)
def table(rows,widths):
 global y
 t=Table([[Paragraph(str(x),styles['th' if i==0 else 'table']) for x in r] for i,r in enumerate(rows)],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#EAF3F3')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]));_,hh=t.wrap(CW,1000);assert y-hh>50;(t.drawOn(C,M,y-hh));y-=hh+14
def pct(x,n=1):return f'{100*x:.{n}f}'.replace('.',',')+' %'
def bpe(case,rep='raw',n=64,stratum='all'):return next(r for r in S[case]['bpe'] if r['representation']==rep and r['merges']==n and r['stratum']==stratum)
start('Un résultat concret :\nprévoir une partie de l’écriture')
p('<b>Sur les cahiers exclus de l’apprentissage, un modèle local retrouve environ neuf espaces nets sur dix.</b> Environ neuf espaces proposés sur dix correspondent aussi à la transcription. Il ne connaît ni la langue ni le sens des mots. Il prédit une convention graphique à partir des signes voisins.')
table([['Transcription','Espaces nets retrouvés','Propositions correctes','Cahiers exclus à tour de rôle'],['ZL',pct(S['ZL']['boundary_prediction']['all']['four']['recall']),pct(S['ZL']['boundary_prediction']['all']['four']['precision']),'14'],['IT',pct(S['IT']['boundary_prediction']['all']['four']['recall']),pct(S['IT']['boundary_prediction']['all']['four']['precision']),'14']],[105,130,130,CW-365])
p('Chaque cahier est testé avec un modèle appris sur les autres. Le contexte utilise jusqu’à deux caractères EVA de chaque côté de la position examinée. Les espaces incertains sont exclus de l’apprentissage des étiquettes et du calcul de cette performance. Les deux transcriptions portent sur le même manuscrit : elles constituent une vérification de sensibilité, pas deux manuscrits indépendants.')
p('Un deuxième test ne voit <b>aucun espace, même pendant l’apprentissage</b>. Il apprend des groupes récurrents de signes puis les applique au cahier exclu. Avec 64 regroupements successifs, ces groupes traversent 19,88 % des espaces incertains de ZL, contre 2,52 % des espaces nets. Le rapport est d’environ 7,9.')
p('Ce résultat ne justifie pas de retirer tous les espaces. Les espaces nets correspondent à des barrières statistiques fortes. Les incertains forment une catégorie intermédiaire, à conserver comme telle jusqu’à l’examen des images. Le problème n’est donc pas simplement « garder ou supprimer tous les blancs ».')
p('Livrable utile pour la suite','h2')
p('Une annotation de <b>2 394 séparations incertaines</b> associe à chacune son locus, son contexte, la probabilité de séparation estimée hors cahier et le résultat du regroupement sans espaces. Toutes les marques originales sont conservées. Aucune correction automatique et aucun sens supposé ne sont imposés.')
p('Il s’agit d’une avancée méthodologique dans ce dossier, pas d’une découverte revendiquée comme nouvelle dans la littérature. L’hypothèse des unités et frontières est notamment étudiée par Rozanova et Temerev [1]. Nos calculs utilisent une implémentation propre, des données filtrées différemment et des validations distinctes.','small')

start('Le test prédictif et ses témoins')
p('La source est l’IVTFF brut : « . » marque un espace jugé net par le transcripteur, « , » un espace incertain [2]. Les alternatives de signes, caractères illisibles et interruptions par dessin coupent le flux ; les fragments de moins de quatre caractères sont exclus. Les lignes ne sont jamais concaténées. Seuls les paragraphes classés Currier A ou B sont retenus.')
p('Deux modèles ont été fixés avant exécution : une paire de caractères voisins, puis un contexte de quatre caractères avec repli lissé vers la paire. Le seuil de décision reste 0,5. Aucun seuil n’est choisi sur les résultats de test. Les 14 cahiers se remplacent successivement comme ensemble exclu ; les témoins sont répartis en huit blocs contigus.')
rows=[['Texte','Rappel : espaces retrouvés','Précision : propositions correctes','F1']]
for name,label in [('ZL','Voynich ZL'),('IT','Voynich IT'),('Latin_Pliny','Pline, latin'),('Italian_Paradiso','Dante, italien'),('Naibbe_Pliny','Naibbe sur Pline'),('Timm_generated','Générateur Timm')]:
 m=S[name]['boundary_prediction']['all']['four'];rows.append([label,pct(m['recall']),pct(m['precision']),f"{m['f1']:.3f}".replace('.',',')])
table(rows,[122,138,155,CW-415])
p('<b>Le contrôle Naibbe fait mieux que le Voynich.</b> Un vrai texte transformé par un chiffre peut donc rendre ses séparateurs très prévisibles. Le générateur Timm, conçu sans message linguistique, obtient lui aussi une bonne performance. Retrouver les espaces n’identifie ni une langue ni la présence de sens.')
p('L’incertitude estimée par rééchantillonnage des cahiers donne pour ZL un rappel de 87,9 à 92,3 % et une précision de 89,6 à 90,9 % (quantiles 2,5-97,5 %). Ces intervalles rééchantillonnent des prédictions déjà calculées ; les modèles des plis partagent une grande partie de leur apprentissage. Ils ne constituent pas une confirmation indépendante.')
p('Comparabilité limitée : Pline contient environ 52 000 caractères, les autres témoins entre 51 000 et 172 000. Les genres, langues et partitions diffèrent. Ce tableau décrit ces six jeux précis avec un modèle identique ; il ne classe pas universellement les langues. Les données témoins et leur disposition artificielle héritent des limites documentées en phase 6.','small')

start('Apprendre des groupes sans aucun espace')
p('Le regroupement fréquent de paires, ou BPE, apprend uniquement sur les chaînes de caractères privées de leurs séparateurs. Ses règles sont figées puis appliquées au cahier absent de l’apprentissage. Un espace est dit « traversé » lorsqu’il tombe à l’intérieur d’un groupe ainsi formé. Les groupes sont graphiques : leur statut de lettre, syllabe ou mot reste inconnu.')
fig,ax=plt.subplots(figsize=(8.3,4.0))
for label,key,color in [('Espaces incertains ZL','2','#B07335'),('Espaces nets ZL','1','#137B80')]:
 for rep,style in [('raw','-'),('composed','--')]:
  x=[0,32,64,128];yy=[100*bpe('ZL',rep,n)['crossing_rates'][key] for n in x]
  ax.plot(x,yy,style,color=color,marker='o',markersize=4,label=label+(' : EVA brut' if rep=='raw' else ' : unités composées'))
ax.set_xlabel('Nombre de regroupements appris');ax.set_ylabel('Séparateurs traversés (%)');ax.set_xticks([0,32,64,128]);ax.grid(alpha=.17);ax.spines[['top','right']].set_visible(False);ax.legend(fontsize=8,frameon=False);fig.tight_layout();fp=ROOT/'results/space_crossing.png';fig.savefig(fp,dpi=180);plt.close(fig)
C.drawImage(str(fp),M,y-245,width=CW,height=245,preserveAspectRatio=True,anchor='c');y-=256
p('Le test principal est fixé à 64 regroupements ; 0, 32 et 128 sont des sensibilités. L’analyse en unités composées commence par dix regroupements EVA définis à l’avance. Elle maintient le contraste : 21,47 % des incertains sont traversés, contre 2,75 % des espaces nets.','small')
p('Le contraste se retrouve dans A et B : en EVA brut à 64 regroupements, 22,63 % contre 3,41 % dans A ; 18,53 % contre 2,13 % dans B. L’écart global entre catégories vaut 17,36 points, avec un intervalle descriptif par cahier de 14,71 à 19,69 points.')
p('Un témoin replace les frontières en permutant les longueurs des morceaux dans chaque fragment, sans changer les lettres. Sur 100 tirages, environ 55 % de ces frontières artificielles sont traversées. Les frontières nettes observées sont donc beaucoup plus respectées que ces frontières déplacées. Ce contrôle ne reproduit toutefois pas toutes les contraintes possibles d’un système d’écriture.')

start('Ce que cela change pour la transcription')
p('Deux classes à préserver','h2')
p('Il faut garder les espaces nets comme contraintes fortes et traiter les séparations incertaines comme des alternatives pondérées. Un point de code EVA n’est pas automatiquement une lettre linguistique ; un groupe appris n’est pas automatiquement une syllabe. Notre résultat rend la recherche suivante plus précise sans décider de la langue.')
p('Comparaison directe ZL / IT','h2')
p(f'Le rapprochement strict conserve {P["matched_lines"]:,} loci avec un flux de lettres identique et un seul fragment retenu de chaque côté. Parmi les 1 089 positions incertaines ZL de cet ensemble, IT sépare 700 positions et en joint 389. À l’inverse, 12 227 des 12 270 espaces nets ZL sont également séparés dans IT. Les ambiguïtés de segmentation sont donc localisées, mais cet accord partage l’objet et les conventions de transcription.'.replace(',', ' ',1))
p('Vérification complémentaire sur des mesures publiées','h2')
p('J’ai recalculé un petit jeu de mesures d’encre publié avec [1] : après leurs exclusions, 265 espaces nets mesurent en moyenne 4,98 pixels, contre 3,14 pour 21 incertains. Les distributions se chevauchent fortement (AUC 0,631). Ce sont les mesures des auteurs sur six feuillets, et non de nouvelles mesures d’image réalisées ici. Elles ne déterminent pas la fonction linguistique des espaces.')
p('Vérification et limites','h2')
p(f'{V["prediction_positions_recomputed"]:,} positions ont été recalculées, les premiers regroupements de chaque jeu contrôlés par une deuxième implémentation et les groupes primaires reconstruisent exactement leurs chaînes sources. Les prédictions peuvent échouer localement ; les exemples interactifs montrent ces erreurs. Les cahiers ont déjà été examinés dans les phases précédentes : cette validation est nouvelle pour ces modèles, pas vierge de toute exploration antérieure.'.replace(',', ' ',1))
p('Sources et reproduction','h2')
p('[1] Rozanova et Temerev, prépublication du 17 août 2026, <link href="https://arxiv.org/abs/2608.17096" color="#137B80">arXiv:2608.17096v1</link>. Code et mesures publiés dans <link href="https://github.com/lrozanova/voynich-units" color="#137B80">lrozanova/voynich-units</link>. Pas de réplication intégrale ni de validation par les pairs revendiquée.<br/>[2] René Zandbergen, <link href="https://voynich.nu/extra/sp_transcr.html" color="#137B80">format IVTFF et conventions de transcription</link>.<br/>[3] Michael A. Greshko (2025), The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext, DOI 10.1080/01611194.2025.2566408.<br/>[4] Torsten Timm et Andreas Schinner (2019/2020), A possible generating algorithm of the Voynich manuscript, DOI 10.1080/01611194.2019.1596999.','small')
p('L’archive contient le protocole préalable, les données, les annotations, toutes les prédictions et règles apprises, les témoins, les licences, les scripts et les empreintes SHA-256. Aucune traduction n’est fournie.','small')
bottom.append(y);C.save();(ROOT/'results/report_layout.json').write_text(json.dumps({'pages':page,'bottoms':bottom},indent=2)+'\n');print(path);print('pages',page,'bottoms',bottom)
