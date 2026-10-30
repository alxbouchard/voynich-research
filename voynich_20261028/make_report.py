#!/usr/bin/env python3
"""Create the French research report from the executed results."""
from pathlib import Path
import collections
import csv
import hashlib
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from analyse import ROOT, OUT

REPORT=ROOT/'output/pdf/Etude_Voynich_2026-10-28.pdf'
FIG=ROOT/'tmp/figures'
REPORT.parent.mkdir(parents=True,exist_ok=True);FIG.mkdir(parents=True,exist_ok=True)
AUDIT=json.loads((OUT/'audit.json').read_text())
INTEGRITY=json.loads((OUT/'integrity.json').read_text())
MODELS=json.loads((OUT/'models.json').read_text())['corpora']
CONTROL=json.loads((OUT/'naibbe_control.json').read_text())
PROBE=json.loads((OUT/'fixed_key_probe.json').read_text())
ZL=AUDIT['corpora']['ZL3b-n.txt'];IT=AUDIT['corpora']['IT2a-n.txt']
NAVY='#17354B';TEAL='#087E86';GRAY='#52616D';LIGHT='#EAF1F4';AMBER='#A16A1B'

from matplotlib.font_manager import findfont, FontProperties
pdfmetrics.registerFont(TTFont('DejaVu',findfont(FontProperties(family='DejaVu Sans'))))
pdfmetrics.registerFont(TTFont('DejaVu-Bold',findfont(FontProperties(family='DejaVu Sans',weight='bold'))))
pdfmetrics.registerFont(TTFont('DejaVu-Italic',findfont(FontProperties(family='DejaVu Sans',style='oblique'))))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu-Italic',boldItalic='DejaVu-Bold')
STYLES={
 'title':ParagraphStyle('title',fontName='DejaVu-Bold',fontSize=27,leading=33,textColor=colors.HexColor(NAVY),spaceAfter=12),
 'h1':ParagraphStyle('h1',fontName='DejaVu-Bold',fontSize=19,leading=24,textColor=colors.HexColor(NAVY),spaceAfter=13),
 'h2':ParagraphStyle('h2',fontName='DejaVu-Bold',fontSize=11,leading=16,textColor=colors.HexColor(TEAL),spaceBefore=9,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='DejaVu',fontSize=9.5,leading=14.2,textColor=colors.HexColor(NAVY),spaceAfter=8),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=8,leading=11.7,textColor=colors.HexColor(GRAY),spaceAfter=6),
 'table':ParagraphStyle('table',fontName='DejaVu',fontSize=8.1,leading=11.5,textColor=colors.HexColor(NAVY)),
 'thead':ParagraphStyle('thead',fontName='DejaVu-Bold',fontSize=8.1,leading=11.5,textColor=colors.white),
 'callout':ParagraphStyle('callout',fontName='DejaVu-Bold',fontSize=11,leading=16,textColor=colors.HexColor(NAVY),spaceAfter=10),
}
W=A4[0]-92
story=[]


def p(text,style='body'):
    story.append(Paragraph(text,STYLES[style]))


def heading(k,title):
    p(f'ÉTUDE VOYNICH / {k:02d}', 'small');p(title,'h1')


def table(rows,widths=None):
    cells=[[Paragraph(str(c),STYLES['thead' if i==0 else 'table']) for c in row] for i,row in enumerate(rows)]
    t=Table(cells,colWidths=widths or [W/len(rows[0])]*len(rows[0]),hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor(NAVY)),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor(LIGHT)]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),
        ('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor(TEAL))]))
    story.append(t);story.append(Spacer(1,9))


def newpage():story.append(PageBreak())


def fmt(x,n=2):return f'{x:.{n}f}'.replace('.',',')
def integer(x):return f'{x:,}'.replace(',',' ')


def chart_style(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['bottom','left']].set_color('#B8C7D1')
    ax.tick_params(colors=GRAY,labelsize=9)
    ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)


def model_chart():
    fig,ax=plt.subplots(figsize=(8,3.25),dpi=170)
    for key,label,color,style in [('real_leaf','Texte réel, feuilles séparées',TEAL,'-'),('real_quire','Texte réel, cahiers séparés',NAVY,'--'),('shuffled_leaf','Lettres mélangées dans chaque mot',AMBER,'-')]:
        vals=[r['bits_per_EVA_char'] for r in MODELS['ZL3b-n.txt'][key]]
        ax.plot(range(4),vals,marker='o',label=label,color=color,linestyle=style,lw=2)
    ax.set_xticks(range(4));ax.set_xlabel('Nombre de lettres EVA précédentes utilisées',fontsize=10,color=NAVY)
    ax.set_ylabel('Bits par lettre EVA, test',fontsize=10,color=NAVY)
    ax.set_ylim(1.9,4.05);chart_style(ax);ax.legend(frameon=False,fontsize=8.5,loc='upper right')
    fig.tight_layout();path=FIG/'modeles.png';fig.savefig(path,bbox_inches='tight');plt.close(fig);return path


def section_chart():
    rows=list(csv.DictReader((OUT/'ZL3b-n_pages.csv').open()))
    vals={}
    for section in ['H','B']:
        groups=collections.defaultdict(list)
        for r in rows:
            if r['section']==section and r['currier']=='B' and r['hand']=='2':
                groups[r['leaf']].append(100*float(r['e']))
        vals[section]=[sum(v)/len(v) for v in groups.values()]
    fig,ax=plt.subplots(figsize=(8,2.65),dpi=170)
    for x,s in enumerate(['H','B']):
        a=vals[s];jitter=np.linspace(-.10,.10,len(a))
        ax.scatter(np.full(len(a),x)+jitter,a,color=TEAL if s=='B' else NAVY,s=35,alpha=.8)
        ax.plot([x-.21,x+.21],[np.mean(a)]*2,color=AMBER,lw=3)
    ax.set_xticks([0,1],['Botanique, 10 feuilles','Bains, 10 feuilles'])
    ax.set_ylabel('Proportion de e (%)',fontsize=10,color=NAVY);ax.set_xlim(-.55,1.55)
    chart_style(ax);fig.tight_layout();path=FIG/'sections.png';fig.savefig(path,bbox_inches='tight');plt.close(fig);return path


def footer(c,doc):
    c.saveState();width,height=A4
    c.setFillColor(colors.HexColor(TEAL));c.rect(0,height-8,width,8,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor('#D5DFE5'));c.line(46,39,width-46,39)
    c.setFont('DejaVu',7.2);c.setFillColor(colors.HexColor(GRAY))
    c.drawString(46,26,'Alex | Reprise expérimentale | 28 octobre 2026')
    c.drawRightString(width-46,26,f'{doc.page:02d}')
    c.restoreState()


heading(1,'Voynich : reprise de l’étude')
p('Audit des données, tests de structure et tentative de lecture avec une clé publiée.','small')
p('Aucun déchiffrement validé à ce stade. Les données de la démonstration alchimique fournie ne correspondent pas aux pages citées. Les essais exécutés ici laissent ouverte la piste d’un chiffrement réversible.','callout')
p('L’objectif était de reprendre le travail sur des données vérifiables. Deux transcriptions complètes ont été authentifiées, puis les calculs et tests ont été exécutés localement. Ce rapport distingue les observations, les interprétations et les conditions nécessaires à une véritable lecture.')
p('Le contrôle décisif : la page f1r','h2')
s=AUDIT['submitted_sample'];zf=ZL['f1r'];itf=IT['f1r']
table([
 ['Mesure','Extrait du code fourni','Vraie f1r : ZL','Vraie f1r : IT'],
 ['Occurrences de qokeedy',s['qokeedy'],zf['qokeedy'],itf['qokeedy']],
 ['Lettres EVA retenues',s['characters_no_spaces'],zf['characters_no_spaces'],itf['characters_no_spaces']],
 ['Proportion de e',fmt(s['e_percent'])+' %',fmt(zf['e_percent'])+' %',fmt(itf['e_percent'])+' %'],
 ['Entropie H0, sans espaces',fmt(s['H0_no_spaces'],3),fmt(zf['H0_no_spaces'],3),fmt(itf['H0_no_spaces'],3)]
],[W*.28,W*.25,W*.235,W*.235])
p('Unités : lettres latines de transcription EVA, pas nombre de glyphes médiévaux. Sur les pages authentiques, les mots contenant une lecture inconnue sont exclus; les alternatives utilisent la première lecture proposée. L’extrait fourni est archivé intégralement dans le dossier.','small')
p('Trois résultats à retenir','h2')
p('<b>1. La preuve initiale échoue.</b> Grok annonçait environ 68 qokeedy sur f1r. Le mot est absent de cette page dans les deux transcriptions. La plante décrite n’y figure pas : f1r est classée « texte seul ». [S3-S4]')
p('<b>2. Une structure mesurable demeure.</b> Les modèles prédisent mieux le texte réel que des lettres mélangées, sur des feuilles et des cahiers exclus de l’apprentissage.')
p('<b>3. Une faible entropie n’exclut pas un message.</b> Un contrôle Naibbe restitue exactement 52 641 lettres de latin normalisé, avec certaines statistiques proches du Voynich. Sa clé publiée ne suffit cependant pas à lire le manuscrit.')

newpage();heading(2,'Des données traçables')
p('Les deux fichiers ont été récupérés en entier depuis le site de René Zandbergen. Leur format, leur version, leur empreinte SHA-256, le nombre de loci et l’unicité des identifiants ont été contrôlés avant les analyses. Les comptes de loci correspondent à l’inventaire publié. [S2-S5]')
table([
 ['Corpus','ZL3b-n','IT2a-n'],
 ['Version','3b, 13 mai 2025','2a, modifiée le 25 juin 2025'],
 ['Loci (entrées de transcription)','5 385','5 215'],
 ['Pages / panneaux avec texte','227','225'],
 ['Tokens avant exclusions','39 026','37 919'],
 ['Tokens lisibles retenus','38 623','37 759'],
 ['Tokens contenant une inconnue','403','160']
],[W*.42,W*.29,W*.29])
p('Les pages et panneaux ne sont pas des feuilles physiques. Les côtés recto/verso et les panneaux d’un même folio sont regroupés; le grand dépliant 85/86 est conservé dans un seul groupe. On obtient 101 groupes pour la séparation des données. Les différences avec les chiffres annoncés dans les anciens échanges sont conservées, sans forcer artificiellement les comptes.')
p('Normalisation publiée dans le protocole','h2')
p('Les commentaires IVTFF sont retirés; les interruptions de dessin deviennent des espaces; les accolades de ligature sont enlevées; la première lecture alternative est utilisée. Les virgules, qui marquent des espaces incertains, séparent les mots dans l’analyse principale. Une variante les joint pour mesurer la sensibilité. Les caractères rares ou illisibles deviennent « ? » et le mot concerné est exclu du corpus lisible.')
p('Les changements de main indiqués dans le texte sont appliqués dès la ligne correspondante. Les tests d’association avec les sections utilisent seulement le texte en paragraphes, avec au moins 100 lettres lisibles par page. Les modèles excluent les marginalia de type Lx et les loci signalés comme erronés.')
p('Ce que garantit le contrôle d’intégrité','h2')
p('Le dossier enregistre <b>data_real=true</b> et <b>gate_pass=true</b> pour les deux fichiers. Cela signifie « transcription savante identifiée et intégralement analysable ». Cela ne garantit ni chaque lecture paléographique, ni le découpage en mots, ni une vérification de chaque signe sur les photographies.')
p('Les résumés historiques mentionnent des essais du 6 février 2026. Leurs fichiers originaux n’ont pas été retrouvés parmi les éléments accessibles. Leurs scores et leurs conclusions ne sont donc pas recyclés comme résultats vérifiés de cette reprise. Les sorties présentées ici sont nouvelles et conservées.')

newpage();heading(3,'Pourquoi la lecture alchimique échoue')
p('Les six extraits attribués à f1r, f68r, f75r, f86v, f87r et f103r ne sont retrouvés exactement dans aucune des deux transcriptions, après normalisation. Pour les dépliants, tous les panneaux correspondants ont été recherchés. Des variantes de lecture restent possibles, mais les citations données ne constituent pas des transcriptions vérifiées.')
p('Une erreur de référence affecte aussi le test final proposé : dans ZL, f116v ne fournit que deux mots Voynich dans un locus de marginalia Lx, <i>oror sheey</i>. Elle ne constitue pas une page de texte courant sur laquelle tester un long rituel inédit. IT ne contient pas cette entrée. [S3-S4]')
table([
 ['Affirmation de la théorie','Ce que le test permet de dire'],
 ['e = eau; o = soleil, à partir de leur forme','Les lettres EVA sont des conventions de transcription. Leur forme typographique moderne n’est pas une preuve de la forme ni du sens des signes originaux. [S2]'],
 ['Entropie faible = texte artificiel alchimique','H0 mesure une distribution de caractères. Elle ne donne pas leur sens. Les modèles de chiffrement doivent être contrôlés sur des textes dont la lecture est connue.'],
 ['q au début = initiation; y à la fin = clôture','Les positions sont mesurables. Les étiquettes « initiation » et « clôture » restent des interprétations non identifiées.'],
 ['Répétitions = proportions de Fibonacci','68 n’est pas un nombre de Fibonacci. Dans ZL, 29,46 % des mots ont 5, 8 ou 13 lettres EVA; cela ne fournit ni règle de dosage ni test contre un modèle nul.'],
 ['80 à 85 % de succès de traduction','La couverture mécanique du dictionnaire atteint environ 92,5 % des tokens lisibles. Aucune traduction de référence ne permet de calculer une exactitude sémantique.'],
 ['Prédiction supérieure à 50 % = validation','Le nombre de classes et la vérité de référence ne sont pas définis. La probabilité de hasard ne peut donc pas être fixée arbitrairement à 50 %.']
],[W*.32,W*.68])
p('Le problème d’identification du sens','h2')
p('On peut permuter les étiquettes eau, terre, feu ou matière sans modifier une seule fréquence, une entropie ou la vraisemblance du texte. Les statistiques internes invoquées par Grok ne choisissent donc pas entre ces lectures. De plus, des actions comme « infusion » sont ajoutées par paraphrase, sans règle de composition fixée à l’avance.')
p('Conclusion limitée : la démonstration fournie est invalidée. Une éventuelle dimension médicale, rituelle ou alchimique du manuscrit n’est pas, à elle seule, réfutée par cet audit.','small')

newpage();heading(4,'La structure résiste aux contrôles')
p('Des modèles de caractères utilisent de zéro à trois lettres EVA précédentes. Le modèle est ajusté sur quatre groupes de données et évalué sur le cinquième. Les cinq partitions séparent les feuilles physiques; une seconde analyse sépare les cahiers entiers. Aucun recto/verso d’une même feuille ne traverse la séparation.')
story.append(Image(str(model_chart()),width=W,height=W*3.25/8))
p('Un score plus bas indique une meilleure prédiction. Le contrôle mélange les lettres à l’intérieur de chaque mot : longueurs et fréquences de lettres sont conservées. Le modèle est réappris sur ce contrôle. Un seul mélange fixé par la graine a été utilisé; la figure n’est pas un test de significativité.','small')
rows=[['Contexte','ZL, feuille exclue','IT, feuille exclue','ZL, cahier exclu','ZL, mélangé']]
for o in range(4):
    rows.append([o,fmt(MODELS['ZL3b-n.txt']['real_leaf'][o]['bits_per_EVA_char'],3),fmt(MODELS['IT2a-n.txt']['real_leaf'][o]['bits_per_EVA_char'],3),fmt(MODELS['ZL3b-n.txt']['real_quire'][o]['bits_per_EVA_char'],3),fmt(MODELS['ZL3b-n.txt']['shuffled_leaf'][o]['bits_per_EVA_char'],3)])
table(rows,[W*.12,W*.22,W*.22,W*.22,W*.22])
p('Résultat : avec deux lettres de contexte, le score ZL passe de 3,866 à 2,131 bits par lettre EVA. Le contrôle mélangé reste à 3,496. L’avantage demeure lorsqu’un cahier entier est exclu (2,166). Le modèle à trois lettres est légèrement moins bon sur les données nouvelles, ce qui interdit d’assimiler complexité et progrès.')
p('Les positions de q et y sont également stables : dans ZL, 99,35 % des q sont initiaux et 87,79 % des y sont finaux. En revanche, seuls 40,40 % des mots se terminent par y. Il faut distinguer ces deux dénominateurs.')
p('<b>Interprétation :</b> le corpus contient des contraintes fortes sur l’ordre des signes. Ces scores ne choisissent pas entre langage, chiffrement, notation spécialisée et procédé de production sans message. Ils ne permettent pas de rejeter les langues naturelles ou les chiffrements dans leur ensemble.')
p('Paramètres : alphabet prédit a-z et ?, marque de début ^ réservée au contexte; lissage additif 0,5; calcul à l’intérieur des mots lisibles; pas de symbole final prédit. Tous les scores portent sur des lettres EVA, pas sur une segmentation paléographique indépendante.','small')

newpage();heading(5,'e et les bains : un signal limité')
p('Avant les nouveaux résultats quantitatifs, trois implications de fréquence ont été fixées : e plus fréquent dans les bains, k plus fréquent en botanique et o plus fréquent dans l’astronomie ou le zodiaque. Ce sont des implications ajoutées pour rendre la proposition testable; elles ne découlent pas nécessairement d’une traduction correcte.')
story.append(Image(str(section_chart()),width=W,height=W*2.65/8))
p('Chaque point est une feuille physique; la barre indique la moyenne. On compare les paragraphes de Currier B, main 2 : dix feuilles botaniques et dix feuilles de bains. Dans ZL, la moyenne de e est de 9,29 % en botanique et de 12,80 % dans les bains.','small')
testsZ=ZL['section_tests'];testsI=IT['section_tests']
table([
 ['Prédiction','Écart ZL','p nominal corrigé, ZL / IT','Lecture'],
 ['e : bains &gt; botanique','+3,50 points','0,038 / 0,048','Association présente'],
 ['k : botanique &gt; bains','+0,56 point','0,380 / 0,397','Pas d’appui net'],
 ['o : astral &gt; botanique','Non estimable','-','Pas de strate comparable']
],[W*.30,W*.16,W*.26,W*.28])
p('Procédure : 1 999 permutations des feuilles, séparément dans les strates main / classification Currier; test unilatéral; correction de Holm sur les trois affirmations fixées. Une affirmation non estimable reçoit p = 1 pour cette correction. Les chiffres sont exploratoires, sans validation confirmatoire indépendante.','small')
p('La limite qui empêche d’en faire une traduction','h2')
p('Les feuilles de bains appartiennent toutes au même cahier M. L’effet de section ne peut donc pas être séparé proprement d’un effet de cahier ou de pratique rédactionnelle. La permutation des feuilles suppose une échangeabilité discutable dans ce contexte; ses p ne doivent pas être considérés comme des preuves calibrées de signification.')
p('Les deux transcriptions portent sur les mêmes pages : leur accord vérifie la robustesse à la lecture, pas une réplication sur deux manuscrits. Le signal e pourrait marquer une construction, une convention, un thème, ou un effet de production. Il ne permet pas d’identifier le mot « eau », encore moins une recette.')

newpage();heading(6,'Un chiffrement positif, puis une clé testée')
p('L’article Naibbe de Michael A. Greshko propose un chiffrement homophonique à groupes, capable de produire des statistiques proches de certaines propriétés du Voynich. Il s’agit d’un modèle de compatibilité et non d’un déchiffrement du manuscrit. [S7-S8]')
p('Contrôle effectivement exécuté','h2')
p('L’implémentation et les tables publiées ont chiffré un texte latin de Pline fourni dans le même dépôt. Graine fixée; découpage aléatoire standard 17/36; jeu de 52 cartes; codage non ambigu; mécanismes optionnels de réutilisation désactivés. Aucune table n’a été ajustée au Voynich.')
table([
 ['Résultat du contrôle','Mesure'],
 ['Lettres de latin normalisé','52 641'],
 ['Lignes récupérées à l’identique','1 063 sur 1 063'],
 ['Tokens chiffrés / lettres EVA','34 809 / 182 844'],
 ['Récupération du texte normalisé','100 %, avec les tables et espaces de codage connus']
],[W*.55,W*.45])
table([
 ['Mesure descriptive','Latin source','Naibbe généré','Voynich ZL','Voynich IT'],
 ['H0 (sans espaces)',fmt(CONTROL['H_within_word_latin'][0],3),fmt(CONTROL['H_within_word_cipher'][0],3),fmt(ZL['full']['H0_no_spaces'],3),fmt(IT['full']['H0_no_spaces'],3)],
 ['H(lettre | précédente)',fmt(CONTROL['H_within_word_latin'][1],3),fmt(CONTROL['H_within_word_cipher'][1],3),fmt(ZL['full']['H_within_word'][1],3),fmt(IT['full']['H_within_word'][1],3)]
],[W*.32,W*.17,W*.17,W*.17,W*.17])
p('Ces entropies empiriques sont calculées dans les mots, sans espaces, et ne sont pas les scores prédictifs de la page 4. Les frontières des mots latins et celles des groupes chiffrés diffèrent par construction. Le contrôle démontre qu’un contenu récupérable peut coexister avec une faible entropie; il ne reproduit pas toutes les propriétés du manuscrit.','small')
p('Tentative de lecture du Voynich avec la clé publiée','h2')
p('Dans une extension exploratoire documentée avant son exécution, la clé Naibbe publiée a été appliquée aux tokens du Voynich sans modification et sans décomposition en mots composés. Pour ZL, 29 247 tokens sur 38 614 ont une lecture mécanique unique (75,74 %), 8 544 n’ont pas de lecture et 823 sont ambigus. Le résultat IT est de 76,65 % de lectures uniques.')
p('<b>Ce pourcentage n’est pas un taux de déchiffrement.</b> Il mesure seulement la possibilité de découper un token avec une table construite pour ressembler au Voynich. La couverture est incomplète et aucun message n’est validé. L’échec concerne cette clé inchangée et ces frontières de tokens, pas l’ensemble des chiffrements à groupes.')
p('Le contrôle restitue les lettres normalisées, après retrait des espaces et ponctuations et normalisations de l’auteur. Il ne reconstitue pas la typographie originale du latin. Les clés étaient connues : aucune récupération de clé inconnue n’a été démontrée.','small')

newpage();heading(7,'Une suite précise pour chercher une lecture')
p('L’étude fournit maintenant une base exploitable et un contrôle positif. La prochaine phase pertinente consiste à rechercher une transformation réversible limitée et à la confronter à des informations extérieures. Les noms de signes et les paraphrases libres ne peuvent pas jouer ce rôle.')
table([
 ['Travail à poursuivre','Condition d’un résultat utile'],
 ['1. Stabiliser les unités graphiques','Comparer les signes et ligatures sur les images de Yale avec plusieurs transcriptions. Vérifier si ch, sh ou les suites de minims doivent être traités comme unités. Conserver l’incertitude au lieu de la convertir en sens.'],
 ['2. Tester une famille bornée de codes','Définir les tables, opérations permises et règles de segmentation avant l’essai. Un décodage doit réencoder exactement le texte dans la marge d’incertitude de transcription documentée.'],
 ['3. Utiliser de vrais contrôles positifs','La méthode doit retrouver une lecture dans des textes chiffrés dont la clé est cachée à l’algorithme. Le contrôle Naibbe de cette reprise est à clé connue; ce prochain critère reste à satisfaire.'],
 ['4. Fixer une ancre externe','Associer un groupe de signes à une information attestée indépendamment : légende d’un objet identifié, parallèle textuel vérifiable, ou annotation datée. Une plante seulement supposée reconnaissable ne suffit pas.'],
 ['5. Garder un test indépendant','Réserver des cahiers et des mains avant d’ajuster les règles. Faire annoter les illustrations sans montrer le décodage. Comparer à des clés permutées et à des modèles de même complexité.'],
 ['6. Publier une lecture vérifiable','Produire les formes originales, la translittération, la segmentation, la clé et une traduction dont chaque ajout est justifié. Prédire un contenu inédit vérifié par une source indépendante.']
],[W*.32,W*.68])
p('Décision sur les pistes','h2')
p('<b>À abandonner comme résultat acquis :</b> la table eau / soleil / terre et ses traductions rituelles. <b>À conserver comme objet de test :</b> le signal de section de e, les contraintes de position et les familles de chiffrement réversible. <b>À ne pas conclure :</b> « c’est du latin », « c’est un faux » ou « c’est nécessairement alchimique ».')
p('Le manuscrit reste présenté comme non déchiffré par Yale. [S1] Cette reprise n’annonce pas une solution et ne fournit aucun mot dont le sens soit nouvellement établi. Elle corrige une preuve erronée, établit des résultats reproductibles et définit les épreuves qui permettraient de reconnaître un véritable progrès.')

newpage();heading(8,'Sources et reproduction')
p('Sources primaires consultées au 28 octobre 2026. Revue ciblée, non exhaustive. Les nouvelles mesures de ce rapport proviennent des scripts et sorties joints, pas des chiffres de l’article de Grok.','small')
refs=[
 ('S1','Yale University Library. The Beinecke Cipher (Voynich) Manuscript.','https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript'),
 ('S2','René Zandbergen. Transliteration of the Text; définition d’EVA et inventaire des transcriptions.','https://www.voynich.nu/transcr.html'),
 ('S3','Zandbergen-Landini, fichier ZL3b-n, version 3b du 13/05/2025.','https://www.voynich.nu/data/ZL3b-n.txt'),
 ('S4','Takahashi, extraction Landini-Stolfi IT2a-n, modifiée le 25/06/2025.','https://www.voynich.nu/data/IT2a-n.txt'),
 ('S5','René Zandbergen. IVTFF, document 2.0.2 du 08/07/2025.','https://www.voynich.nu/software/ivtt/IVTFF_format.pdf'),
 ('S6','Lindemann et Bowern (2021). Character Entropy in Modern and Historical Texts. Cadre comparatif, non répliqué intégralement ici.','https://arxiv.org/abs/2010.14697'),
 ('S7','Greshko (2025). The Naibbe cipher. Cryptologia. DOI : 10.1080/01611194.2025.2566408.','https://doi.org/10.1080/01611194.2025.2566408'),
 ('S8','Michael A. Greshko. Implémentations, tables et texte latin de contrôle. Code et jeux de données sous licence MIT modifiée, jointe.','https://github.com/greshko/naibbe-cipher')]
for code,title,url in refs:
    p(f'<b>[{code}]</b> {title}<br/><link href="{url}" color="{TEAL}">{url}</link>','small')
p('Empreintes des données','h2')
for item in INTEGRITY:
    p(f'<b>{item["file"]}</b><br/>{item["sha256"]}','small')
p('Rejouer les essais','h2')
p('Le dossier contient les fichiers sources conservés, les scripts Python, les licences, le protocole, l’extension exploratoire et les sorties JSON/CSV. Depuis le dossier décompressé, installer requirements.txt, puis exécuter : <b>python analyse.py</b>, <b>python models.py</b>, <b>python naibbe_control.py</b> et <b>python key_probe.py</b>. Le rapport se régénère avec <b>python make_report.py</b>; les contrôles finaux avec <b>python verify_study.py</b>.','small')
p('Le protocole a été écrit après inspection du format des données et avant les nouveaux calculs. Ce n’est ni un préenregistrement externe, ni une réplication en aveugle. Les analyses et les limites sont conservées, y compris les résultats négatifs.','small')

doc=SimpleDocTemplate(str(REPORT),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=43,bottomMargin=52,
                      title='Voynich : reprise expérimentale, 28 octobre 2026',author='Étude préparée pour Alex avec ChatGPT',
                      subject='Audit reproductible et tests de structure; aucun déchiffrement revendiqué')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(REPORT)
