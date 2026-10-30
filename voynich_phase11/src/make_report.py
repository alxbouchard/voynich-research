import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCustom',fontName='DVB',fontSize=23,leading=28,textColor=HexColor('#133642'),spaceAfter=13))
styles.add(ParagraphStyle(name='BodyCustom',fontName='DV',fontSize=10,leading=15,spaceAfter=9))
styles.add(ParagraphStyle(name='SubCustom',fontName='DVB',fontSize=13,leading=17,textColor=HexColor('#133642'),spaceBefore=11,spaceAfter=7))
styles.add(ParagraphStyle(name='SmallCustom',fontName='DV',fontSize=8,leading=11,spaceAfter=7))
styles.add(ParagraphStyle(name='CellCustom',fontName='DV',fontSize=8.5,leading=12))
story=[]
def p(t,style='BodyCustom'):story.append(Paragraph(t,styles[style]))
def sub(t):p(t,'SubCustom')
def table(rows,widths):
 data=[[Paragraph(str(c),styles['CellCustom']) for c in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dcebee')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.7,HexColor('#548291')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f3f6f7')])]))
 story.extend([t,Spacer(1,10)])
def load(n):return json.loads((ROOT/'results'/n).read_text())
s=load('scott_audit.json');z=load('zfd_canonical_semantic.json');v=load('zfd_v3_semantic.json')

p('VOYNICH · PHASE 11','SmallCustom')
p('Deux décodeurs à l’épreuve','TitleCustom')
p('<b>Résultat : aucune traduction validée.</b> Les programmes publics de Scott Schechter et de ZFD ont été exécutés. Leurs mesures de couverture et de confiance ne permettent pas de choisir les sens corrects parmi les attributions testées.')
table([['Essai effectué','Résultat observé'],['Scott : corpus complet, 225 folios selon son parseur','33 785 occurrences reconnues sur 37 886 : <b>89,18 %</b>.'],['Scott : 100 tables témoins de significations','Chaque occurrence reconnue change de mot proposé. Couverture, vocabulaire unique et profil de fréquences triées restent identiques.'],['ZFD : reproduction du test statistique v3','Les résultats des deux configurations, cinq folios et 30 répétitions par témoin sont reproduits sans différence.'],['ZFD actuel : huit folios, 20 permutations des sens','1 946 occurrences. Entre 1 708 et 1 899 gloses changent par permutation ; scores et statistiques identiques.']],[205,298])
sub('Une lecture candidate n’est pas encore un déchiffrement')
p('Exemple réellement calculé : pour le mot transcrit <b>daiin</b>, Scott propose <b>OLEUM</b> (huile). ZFD donne une glose de l’ordre de <b>donner</b>, avec un résidu non résolu. Ce désaccord ne tranche pas entre les deux projets ; il montre pourquoi il faut une preuve indépendante du sens.')
p('Une permutation témoin n’est pas une nouvelle traduction plausible. Elle échange volontairement les significations tout en conservant les formes reconnues. Si un score reste identique, il ne peut, à lui seul, valider l’attribution initiale. La grammaticalité et l’histoire des langues demandent d’autres vérifications.')
sub('Ce que l’essai permet de conclure')
p('Les forts taux affichés par ces métriques mesurent principalement la reconnaissance de formes ou leur décomposition. Les essais reproduits ne justifient donc pas de présenter ces taux comme un pourcentage du manuscrit traduit correctement. Cela ne réfute pas automatiquement tous les arguments linguistiques, historiques ou iconographiques des auteurs.')
p('Données, scripts, versions et contrôles : archive de reproduction jointe. Exécutions du 29 octobre 2026 UTC. Aucun nouveau mot du Voynich n’est déclaré déchiffré dans cette étude.','SmallCustom')
story.append(PageBreak())

p('Mesures et contrôles','TitleCustom')
sub('Scott : le chiffre dépend de la version du glossaire')
p('Le commit exécuté contient 4 063 clés EVA et 947 valeurs distinctes. Son programme original affiche 89,2 % après arrondi, alors que le README annonce 87,8 %. Le chiffre de cet audit provient de l’exécution : 33 785 / 37 886. L’original a d’abord été exécuté tel quel ; une copie exposant ses fonctions a servi aux contrôles.')
p('Les 100 permutations sont des cycles sans point fixe sur les valeurs distinctes : elles conservent les regroupements de mots associés à une même valeur. Toutes les sorties reconnues changent de sens proposé. La couverture reste à 89,18 % dans les 100 cas. Le vocabulaire unique reste identique ; un test limité à la présence de termes dans ce vocabulaire conserve donc aussi son résultat. Les arguments syntaxiques et les identifications d’images du dépôt ne sont pas audités ici.')
sub('ZFD : reproduction fidèle, sens non identifiés par le score')
p('Le test v3 compare le texte à des témoins dont les caractères sont mélangés, à de l’EVA synthétique et à des mots latins aléatoires. Les 900 témoins et les dix lectures de référence reproduisent exactement les résultats numériques publiés. Les deux configurations classent les cinq folios comme discriminants selon leurs propres critères.')
table([['Folio','Ancienne config.','Config. étendue','Après permutation des sens'],['f10r','0,7011','0,9058','Identique dans 20/20 essais'],['f23v','0,7778','0,9060','Identique dans 20/20 essais'],['f47r','0,7073','0,9037','Identique dans 20/20 essais'],['f89r','0,6955','0,9059','Identique dans 20/20 essais'],['f101v','0,7585','0,9012','Identique dans 20/20 essais']],[55,105,110,233])
p('Chaque ligne montre le score de « cohérence » original. Les 20 tables de significations sont appliquées dans chacune des deux configurations : <b>200 comparaisons au total</b> (20 × 2 × 5). Les couvertures et confiances moyennes restent aussi identiques. Sur les 849 éléments du parseur, 368 à 398 gloses changent dans l’ancienne configuration ; 774 à 827 dans la configuration étendue.')
p('Le score combine couverture (30 %), diversité d’opérateurs (25 %), diversité de catégories (25 %) et confiance moyenne (20 %). La diversité est plafonnée à cinq catégories. Les tables modifiées en produisent six ou sept : la composante sémantique reste saturée. Ce score n’évalue ni la justesse des objets nommés ni la syntaxe des phrases.','SmallCustom')
story.append(PageBreak())

p('Décodeur actuel et reproductibilité','TitleCustom')
p('Le décodeur canonique <b>06_Pipelines/zfd_decoder_v2.py</b>, avec le lexique v3, est distinct du programme de validation v3. Il a été appliqué aux cinq folios du test et à trois folios supplémentaires. Ces derniers peuvent avoir été utilisés par l’auteur ; ce ne sont pas des pages indépendantes tenues secrètes.')
rows=[['Folio','Mots','Classés ≥ 0,7','Classés 0,3-0,7','Autres','Gloses changées*']]
for f,b in z['baseline'].items():
 stats=b['stats']; changed=[t['folios'][f]['changed_glosses'] for t in z['trials']]
 rows.append([f,stats['total_words'],stats['fully_resolved'],stats['partially_resolved'],stats['unknown'],f'{min(changed)} à {max(changed)}'])
table(rows,[52,42,95,112,56,146])
p('* Minimum et maximum parmi les 20 permutations. La colonne 0,3-0,7 exclut 0,7. Les classes reprennent les seuils de confiance du programme ; elles ne signifient pas traduction correcte. Les 160 comparaisons conservent les statistiques et les confiances de chaque mot, ligne et folio. Les différences de décompte avec le test v3 viennent des parseurs distincts.','SmallCustom')
sub('Protocole et limites')
p('Les formes reconnues restent fixes. Les paquets de sens sont permutés à l’intérieur de chaque section du lexique. Une correction technique, documentée séparément, conserve aussi le type et la présence des champs : le premier essai rencontrait une valeur nulle incompatible avec une fonction de mise en majuscules. Aucune permutation n’a été sélectionnée en fonction de son score.')
p('Ce test établit une limite des métriques inspectées, pas une impossibilité de déchiffrer le manuscrit. Une prochaine hypothèse devra imposer une règle applicable sans réattribution libre des mots, puis réussir des prédictions de sens ou de syntaxe sur des passages réservés. Une telle règle n’a pas été obtenue ici.')
sub('Sources figées et reproduction')
p('Scott Schechter : commit <font size="7">71f2f3c91e9113d285ab21e024f1dd70c1f43c44</font>.<br/>ZFD : commit <font size="7">3f030a9293b8db15dc2c7b0d0e7c703e71711f62</font>.<br/>Le manifeste conserve les chemins, empreintes Git et SHA256 des 45 fichiers utilisés. Le vérificateur contrôle les décomptes, reconstruit la formule de cohérence et vérifie les empreintes.','SmallCustom')
p('<link href="https://github.com/scott-schechter/voynich-decoded">github.com/scott-schechter/voynich-decoded</link><br/><link href="https://github.com/denoflore/ZFD">github.com/denoflore/ZFD</link><br/>Fichiers clés : decode.js ; tools/glossary-export.js ; publication/29-negative-domain-tests.md ; validation/blind_decode_test/run_test_v3.py et decoder.py ; 06_Pipelines/zfd_decoder_v2.py.','SmallCustom')

def footer(c,doc):
 c.setStrokeColor(HexColor('#c4d6db'));c.line(46,43,549,43)
 c.setFont('DV',8);c.setFillColor(HexColor('#53707a'));c.drawString(46,29,'Voynich · Phase 11 · Audit expérimental');c.drawRightString(549,29,str(doc.page))
doc=SimpleDocTemplate(str(OUT/'Voynich_phase11_audit_des_decodeurs.pdf'),pagesize=(595,842),leftMargin=46,rightMargin=46,topMargin=44,bottomMargin=57,title='Voynich phase 11 - Audit de deux décodeurs',author='Analyse réalisée avec ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT/'Voynich_phase11_audit_des_decodeurs.pdf')
