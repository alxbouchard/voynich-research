#!/usr/bin/env python3
"""Produce the phase-2 report from saved, verified results."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from matplotlib.font_manager import FontProperties, findfont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
PDF=OUT/'Voynich_phase2_2026-10-28.pdf'
for name,weight in [('DV','normal'),('DVB','bold')]:
    pdfmetrics.registerFont(TTFont(name,findfont(FontProperties(family='DejaVu Sans',weight=weight))))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
INK=colors.HexColor('#162D3D');TEAL=colors.HexColor('#146B71');GRAY=colors.HexColor('#536572')
styles={
 'kicker':ParagraphStyle('kicker',fontName='DVB',fontSize=9,leading=13,textColor=TEAL,spaceAfter=12),
 'title':ParagraphStyle('title',fontName='DVB',fontSize=25,leading=30,textColor=INK,spaceAfter=16),
 'heading':ParagraphStyle('heading',fontName='DVB',fontSize=13,leading=18,textColor=TEAL,spaceBefore=12,spaceAfter=8),
 'body':ParagraphStyle('body',fontName='DV',fontSize=10,leading=15,textColor=INK,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8.2,leading=12,textColor=GRAY,spaceAfter=7),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.8,leading=12,textColor=INK),
 'header':ParagraphStyle('header',fontName='DVB',fontSize=8.5,leading=12,textColor=colors.white),
}
story=[]
def p(s,style='body'):
    story.append(Paragraph(s,styles[style]))
def heading(s):p(s,'heading')
def table(rows,widths):
    cells=[[Paragraph(escape(str(x)),styles['header' if i==0 else 'cell']) for x in row] for i,row in enumerate(rows)]
    t=Table(cells,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),
       ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
       ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
       ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EFF5F5'),colors.white]),
       ('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#CAD8DB'))]))
    story.append(t);story.append(Spacer(1,10))
def page(kicker,title):
    if story:story.append(PageBreak())
    p(kicker,'kicker');p(title,'title')
def result(name):return json.loads((ROOT/'results'/(name+'.json')).read_text())
lat=result('latin_hidden_key_control');ita=result('italian_hidden_key_control')
ext=json.loads((ROOT/'results/extended_summary.json').read_text())
best={lang:min((r for r in ext if r['case'].startswith('extended_'+lang+'_')),key=lambda r:r['heldout_cross_entropy_bits']) for lang in ['latin','italian']}
anchors=result('anchors_summary')

page('ÉTUDE VOYNICH · PHASE 2 · 28 OCTOBRE 2026','Chercher une clé,\nexiger une preuve'.replace('\n','<br/>'))
p('<b>Aucune traduction du manuscrit n’a été validée.</b> Cette phase ajoute une recherche de clés inconnues, deux contrôles linguistiques et un index de légendes. Les programmes produisent des candidats statistiques, mais aucun texte clair suffisamment cohérent et confirmé par des éléments indépendants.')
heading('Ce qui a effectivement progressé')
table([
 ['Travail réalisé','Résultat vérifié'],
 ['Contrôle latin à clé cachée','28 639 / 28 641 lettres correctes sur la partie réservée, soit 99,993 %'],
 ['Contrôle italien à clé cachée','109 933 / 109 933 lettres correctes sur la partie réservée, soit 100 %'],
 ['Essais sur le Voynich','30 configurations exécutées ; aucune traduction validée'],
 ['Légendes illustrées','729 loci inventoriés ; 497 accords exacts entre ZL et IT'],
 ],[207,292])
p('La réussite des contrôles montre que le solveur peut retrouver une substitution simple lorsqu’un texte du type attendu est effectivement présent. Elle ne donne aucun pourcentage de déchiffrement du Voynich.')
heading('Deux tâches distinctes')
p('<b>Cryptanalyse :</b> chercher une règle de transformation reproductible, puis appliquer la clé sans l’ajuster aux passages d’évaluation. <b>Lecture du manuscrit :</b> établir les signes et leurs liens avec les illustrations avant d’assigner des noms de plantes, d’astres ou d’ingrédients.')
p('La phase 1, également incluse dans l’archive, vérifiait les transcriptions, les comptages, les modèles de structure et le contrôle Naibbe. Le présent rapport porte sur les nouveaux essais. Il ne prétend pas couvrir toutes les langues, tous les chiffres ou toutes les analyses possibles.','small')

page('01 · CONTRÔLES POSITIFS','Le solveur retrouve-t-il\nune clé cachée ?'.replace('\n','<br/>'))
p('Le programme reçoit un texte chiffré par permutation de l’alphabet et un modèle statistique de langue. La clé et le texte original sont conservés pour l’évaluation, sans être fournis au solveur. Chaque essai optimise une clé sur 24 000 lettres, puis l’applique à une autre partie du message.')
table([
 ['Contrôle','Modèle de langue','Message à retrouver','Erreurs réservées'],
 ['Latin','César, De Bello Gallico','Pline, Histoire naturelle XVI','2 / 28 641'],
 ['Italien','Dante : Inferno et Purgatorio','Dante : Paradiso','0 / 109 933'],
 ],[63,147,176,113])
p('Le latin utilise deux auteurs distincts. Le contrôle italien sépare les parties du poème, mais garde le même auteur. Les deux contrôles ne représentent donc pas le même degré de difficulté ou de diversité linguistique.')
heading('Calibration documentée')
p('La première fonction de score, fondée sur des probabilités conditionnelles de quatre lettres, a échoué sur le contrôle. Elle a été remplacée par les probabilités conjointes de groupes de quatre lettres. Ce choix a été fait à partir du contrôle ; l’échec initial est conservé dans les résultats.')
p('Le fichier source de Dante contenait deux copies intégrales du poème. La seconde a été retirée. Le contrôle final utilise exclusivement le premier Paradiso, sans copie d’Inferno ou de Purgatorio dans sa partie d’évaluation.')
heading('Algorithme et portée')
p('Recherche par recuit simulé : huit redémarrages, jusqu’à 40 000 propositions d’échange par redémarrage, puis amélioration locale. La clé reste une bijection entre 26 symboles et 26 lettres. Cette classe de modèles ne couvre ni les homophones, ni des syllabaires arbitraires, ni une clé variable selon la position.')
p('Le contrôle Naibbe avec permutation globale se réduit au contrôle latin une fois les tables morphologiques publiées fournies. Il ne constitue pas un troisième contrôle indépendant et ne résout pas le problème des tables Naibbe entièrement inconnues.','small')

page('02 · ESSAIS SUR LE MANUSCRIT','30 configurations,\naucun texte clair validé'.replace('\n','<br/>'))
p('Six essais initiaux portent sur l’EVA brut et la sortie des tables Naibbe connues. Vingt-quatre essais supplémentaires croisent deux langues de référence, trois sous-ensembles du manuscrit (ensemble, Currier A, Currier B), deux unités de transcription et deux sens de lecture.')
p('Les unités expérimentales regroupent notamment ch, sh et certains groupes en i. Elles ne constituent pas un alphabet établi. Les essais étendus répartissent les données entre 78 feuillets pour l’apprentissage et 20 pour l’évaluation, en gardant les deux faces ensemble. La recherche de clé utilise au plus 24 000 lettres du groupe d’apprentissage par variante.')
heading('Scores sur les passages réservés')
table([
 ['Modèle','Contrôle connu','Meilleur essai Voynich¹','EVA mélangé²'],
 ['Latin',f"{lat['heldout_cross_entropy_bits']:.3f}",f"{best['latin']['heldout_cross_entropy_bits']:.3f}",f"{result('shuffled_null_latin')['heldout_cross_entropy_bits']:.3f}"],
 ['Italien',f"{ita['heldout_cross_entropy_bits']:.3f}",f"{best['italian']['heldout_cross_entropy_bits']:.3f}",f"{result('shuffled_null_italian')['heldout_cross_entropy_bits']:.3f}"],
 ],[91,119,170,119])
p('Unité : moyenne de −log₂ p(groupe de quatre lettres), en bits par fenêtre de quatre lettres. Plus petit signifie plus compatible avec ce modèle statistique. Ce n’est ni une entropie par caractère, ni un taux de traduction, ni une mesure directement comparable entre langues.','small')
p('¹ Dans les deux langues, le minimum parmi les variantes étendues est obtenu sur Currier B, unités regroupées, sens inverse. Ce minimum est choisi après examen de plusieurs variantes, sans troisième jeu de confirmation. ² Caractères mélangés à l’intérieur de chaque segment EVA ; ce témoin conserve des fréquences, mais n’est pas apparié à chaque variante regroupée.','small')
p('Les sorties Voynich conservent des répétitions et ne forment pas un passage interprétable de façon stable. Battre le texte mélangé montre une structure exploitable par le score ; cela ne suffit pas à établir une langue ou un contenu.')
heading('Ce que l’échec ne permet pas de conclure')
p('Ces essais n’écartent ni tout latin ou italien, ni toute substitution, ni l’hypothèse d’une langue naturelle. Les corpus de César et de Dante représentent mal certains vocabulaires techniques médiévaux. Le budget de recherche est borné et les transcriptions demeurent incertaines. Les résultats complets, clés comprises, restent accessibles pour examiner ces limites.')

page('03 · LIENS ENTRE IMAGES ET TEXTE','Des points de comparaison\nconcrets, sans sens inventé'.replace('\n','<br/>'))
p('L’index aligne les lectures ZL et IT de chaque locus de légende, puis recherche les mêmes formes dans le texte courant. L’accord entre transcriptions facilite la sélection des passages ; il ne garantit pas la bonne lecture du manuscrit.')
table([
 ['Inventaire','Nombre'],
 ['Loci de légendes illustrées','729'],
 ['Lectures exactement concordantes ZL / IT','497'],
 ['Loci concordants avec une forme retrouvée dans le texte courant','258'],
 ['Légendes zodiacales, dont concordantes','299, dont 190'],
 ],[389,110])
heading('Quatre correspondances à vérifier sur les originaux')
table([
 ['Forme EVA','Légende','Ligne correspondante'],
 ['okols','f100r.21','f89v2.21'],
 ['okcheor','f100v.10','f93r.12'],
 ['otcheody','f68r1.10','f114v.31'],
 ['otald','f70v2.10','f47v.13'],
 ],[110,194,195])
p('Ces quatre formes concordent entre les deux transcriptions et apparaissent chacune dans une seule ligne de texte courant dans ce comptage. Elles ne sont pas traduites. L’index compte les lignes contenant une forme, pas ses répétitions éventuelles dans une même ligne. Le nombre 258 ne désigne pas 258 mots distincts.','small')
heading('Les images ne fournissent pas encore de clé bilingue')
p('La vignette du folio 71r a été inspectée pour sa disposition circulaire, mais ses 337 × 480 pixels ne permettent pas de valider les glyphes. Les noms de mois lisibles en alphabet latin sont des annotations ajoutées par une autre main plus tardive [3]. Leur présence n’aligne pas automatiquement les légendes voynich sur des noms de mois, de plantes ou d’étoiles.')
p('Une prochaine lecture utile devra identifier exactement le signe, l’objet désigné et la portée de la légende. L’interprétation devra ensuite expliquer les occurrences de la même forme sur d’autres feuillets, sans changer de règle.','small')

page('04 · TRANSPARENCE ET SUITE','Un dossier réutilisable')
p('L’archive rassemble les sources utilisées, les transcriptions, les scripts Python et C++, les paramètres, les trente clés candidates, les contrôles réussis et l’échec de calibration conservé. Le fichier README décrit la reproduction et les limites de chaque champ.')
heading('Vérifications effectuées')
p('Empreintes des sources contrôlées ; récupération des deux messages tests recalculée depuis les clés enregistrées ; scores d’apprentissage des trente configurations recalculés ; séparation des feuillets vérifiée ; dédoublement de Dante et effectifs de l’index contrôlés. Ces vérifications valident l’exécution, pas le déchiffrement.')
heading('Les trois prolongements les mieux définis')
p('<b>1. Vérifier les signes sur des images de haute résolution.</b> Commencer par les correspondances de la page précédente et noter explicitement les lectures concurrentes.')
p('<b>2. Élargir la famille de clés.</b> Tester des substitutions homophoniques ou des tables syllabiques variables, avec un contrôle à clé cachée de même difficulté avant d’interpréter un échec sur le manuscrit.')
p('<b>3. Élargir les corpus comparatifs.</b> Introduire des textes médicaux et botaniques médiévaux, puis réserver de nouveaux feuillets pour confirmer une hypothèse sélectionnée. Tout sens proposé doit produire des prédictions vérifiables sur ces passages.')
heading('Sources principales et attribution')
sources=[
 ('[1] Transcriptions complètes ZL3b et IT2a, format IVTFF, René Zandbergen et transcripteurs crédités dans les fichiers.', 'https://www.voynich.nu/transcr.html'),
 ('[2] César, De Bello Gallico, Perseus Digital Library, canonical-latinLit. XML et normalisation : CC BY-SA 4.0.', 'https://github.com/PerseusDL/canonical-latinLit'),
 ('[3] René Zandbergen, écriture et annotations plus tardives ; étude des légendes ; description du folio 71r.', 'https://www.voynich.nu/writing.html'),
 ('[4] Michael A. Greshko (2025), Naibbe cipher, Cryptologia. Code, tables, textes de contrôle et licence conservés.', 'https://doi.org/10.1080/01611194.2025.2566408'),
 ]
for label,url in sources:
    p(escape(label)+'<br/><link href="'+url+'" color="#146B71">'+escape(url)+'</link>','small')
p('URL fixées aux révisions, empreintes SHA-256 et autres références : SOURCES_AND_LIMITS.json et sources de la phase 1. Les lectures de travail ne sont pas présentées comme une découverte historique ou une traduction.','small')

def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#CAD8DB'));canvas.line(48,43,547,43)
    canvas.setFont('DV',8);canvas.setFillColor(GRAY)
    canvas.drawString(48,29,'VOYNICH · Étude exploratoire · Aucun déchiffrement validé')
    canvas.drawRightString(547,29,str(doc.page))

doc=SimpleDocTemplate(str(PDF),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=43,bottomMargin=59,
    title='Voynich : recherche de clés et index des légendes, phase 2',author='Étude réalisée avec ChatGPT',subject='Analyses exploratoires reproductibles ; aucune traduction validée')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(PDF)
