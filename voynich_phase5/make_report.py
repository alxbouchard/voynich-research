#!/usr/bin/env python3
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from matplotlib.font_manager import findfont,FontProperties
ROOT=Path(__file__).resolve().parent
S=json.loads((ROOT/'results/summary.json').read_text());T=json.loads((ROOT/'results/transcription_sensitivity.json').read_text());assert S['verification']=='PASS'
for n,w in [('DV','normal'),('DVB','bold')]:pdfmetrics.registerFont(TTFont(n,findfont(FontProperties(family='DejaVu Sans',weight=w))))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
INK=colors.HexColor('#17313D');TEAL=colors.HexColor('#176F75');MUTED=colors.HexColor('#566A72')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=24,leading=29,textColor=INK,spaceAfter=14),
 'kicker':ParagraphStyle('kicker',fontName='DVB',fontSize=9,leading=13,textColor=TEAL,spaceAfter=10),
 'body':ParagraphStyle('body',fontName='DV',fontSize=10,leading=14.7,textColor=INK,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8.4,leading=12,textColor=MUTED,spaceAfter=8),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=13,leading=17,textColor=TEAL,spaceBefore=7,spaceAfter=8),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.2,leading=11.2,textColor=INK),
 'head':ParagraphStyle('head',fontName='DVB',fontSize=8.2,leading=11.2,textColor=colors.white),
 'sample':ParagraphStyle('sample',fontName='DV',fontSize=9,leading=13,textColor=INK,wordWrap='CJK',backColor=colors.HexColor('#EEF5F4'),borderPadding=8,spaceBefore=7,spaceAfter=13)
};story=[]
def p(s,style='body'):story.append(Paragraph(s,styles[style]))
def page(k,title):
 if story:story.append(PageBreak())
 p(k,'kicker');p(title,'title')
def table(rows,widths):
 t=Table([[Paragraph(escape(str(c)),styles['head' if i==0 else 'cell']) for c in row] for i,row in enumerate(rows)],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EEF5F4'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.append(t);story.append(Spacer(1,9))
def dec(x,n=3):return f'{x:.{n}f}'.replace('.',',')
def pct(x,n=2):return dec(x*100,n)+' %'
def num(x):return f'{x:,}'.replace(',',' ')
def label(k):return k.replace('latin','Latin').replace('italian','Italien').replace('_',' / ')

page('VOYNICH · PHASE 5 · 28 OCTOBRE 2026','Un signe peut-il coder<br/>plusieurs lettres ?')
p('<b>Aucune traduction validée.</b> Cette phase autorise une clé à transformer chaque unité du manuscrit en une lettre ou un groupe de deux lettres. Elle compare deux inventaires : consonne-voyelle (CV), par exemple ta, et voyelle-consonne (VC), par exemple an. Plusieurs signes peuvent partager la même sortie.')
p('Les contrôles fonctionnent, les candidats échouent','h')
data=[['Modèle de contrôle','Unités exactes*','Erreurs / unités évaluées']]
for lang in ['latin','italian']:
 for kind in ['CV','VC']:
  r=next(x for x in S['controls'] if x['language']==lang and x['kind']==kind and x['trial']==1)
  data.append([label(lang+'_'+kind),pct(r['heldout_unit_accuracy'],3),num(r['heldout_unit_errors'])+' / '+num(r['test_metrics']['units'])])
table(data,[180,130,189])
p('* Deux clés cachées différentes par ligne du tableau, avec les mêmes résultats. Il s’agit de huit essais sur deux textes sources, pas de huit textes indépendants. Une unité exacte peut représenter une ou deux lettres ; ces pourcentages ne se comparent donc pas directement aux pourcentages de lettres de la phase 4.','small')
p(f"<b>{S['real_count']} configurations Voynich et {S['null_count']} témoins mélangés</b> ont ensuite été calculés. Parmi les 32 clés retenues par le score, {S['real_full_canonical_count']} respecte entièrement la règle de redécoupage sur les segments réservés. Chaque candidat présente donc une contradiction avec le mécanisme précis qu’il est censé représenter.")
p('Les quatre meilleurs scores, sélectionnés après comparaison au sein de chaque inventaire, ont aussi été évalués sur la transcription de Takahashi (IT), avec les mêmes clés. Les scores restent proches de ceux obtenus sur ZL ; les incohérences de découpage subsistent.','small')
p('Cette conclusion porte sur les clés obtenues par cette recherche limitée. Elle ne démontre pas que toute autre clé ou tout autre chiffre syllabique est impossible.','small')

page('MÉTHODE','Quatre inventaires limités')
p('Chaque inventaire contient les 23 lettres normalisées et neuf groupes de deux lettres. Ces neuf groupes sont sélectionnés uniquement dans le corpus servant au modèle de langue. La lettre y est ici classée comme consonne par convention. Le texte sans espaces est découpé de gauche à droite en privilégiant un groupe disponible, puis une lettre isolée.')
table([['Inventaire','Neuf groupes retenus']]+[[label(k),' · '.join(v['pairs'])] for k,v in S['models'].items()],[116,383])
p('Ce sont des unités orthographiques expérimentales. Elles ne constituent pas une analyse phonologique : par exemple, he est retenu statistiquement dans le modèle italien. Le dictionnaire n’inclut pas toutes les syllabes possibles et ne dépasse pas deux lettres. Des chiffres historiques à éléments CV et VC ont été étudiés par Lasry [1] ; ce travail ne reproduit pas son algorithme.','small')
p('Corpus et contrôle à clé cachée','h')
p('Le modèle latin utilise César, et le texte chiffré de contrôle Pline. Le modèle italien utilise l’Enfer et le Purgatoire de Dante ; le contrôle utilise le Paradis. La copie répétée présente dans la source Dante est supprimée avant ces séparations. Les deux textes italiens restent du même auteur.','small')
p('Pour chaque contrôle, 48 signes chiffrés sont affectés aléatoirement aux unités claires. Le solveur ignore cette clé. Il utilise les 24 000 premières unités pour l’ajustement, puis la suite pour l’évaluation. Le seuil prévu était de 95 % d’unités exactes pour chacune des deux clés de chaque inventaire. Aucun paramètre n’a été modifié après observation des résultats.','small')
p('La recherche sur le manuscrit','h')
p('Deux langues × deux inventaires CV/VC × Currier A/B × unités EVA/composées × sens direct/inverse donnent 32 cas. Une clé distincte est ajustée pour chaque cas. Une feuille physique sur cinq, dans l’ordre trié des identifiants, est réservée ; la clé ne voit pas ses lignes pendant l’ajustement. Les anciens travaux ont néanmoins déjà utilisé ce corpus.','small')
p('Chaque recherche emploie huit départs et 60 000 propositions par départ, puis une amélioration locale. Le score combine les fréquences de groupes de quatre unités et une pénalité sur les fréquences des unités. Les variantes explicites, signes illisibles ou rares et interruptions coupent les séquences. Les virgules incertaines restent des frontières avant la construction des unités composées.','small')

for lang in ['latin','italian']:
 page('RÉSULTATS · '+('LATIN' if lang=='latin' else 'ITALIEN'),'Les 16 essais '+('latins' if lang=='latin' else 'italiens'))
 p('Évaluation sur les segments réservés. Le score non pénalisé est exprimé en bits par fenêtre de quatre unités, et non par lettre. Plus bas signifie plus conforme au modèle local. Comparer les chiffres uniquement à l’intérieur d’un même inventaire ; ils ne sont pas directement comparables à ceux de la phase 4.','small')
 data=[['Groupe / unités','Type','Sens','Score','Mélangé','2 lettres*','Conformes*']]
 for r in [x for x in S['real'] if x['language']==lang]:
  data.append([r['subset']+' / '+('EVA' if r['units']=='EVA' else 'composées'),r['kind'],'direct' if r['direction']=='forward' else 'inverse',dec(r['test_metrics']['bits_per_four_units']),dec(r['matched_null_bits']),pct(r['segmentation_diagnostics']['two_letter_unit_fraction'],1),pct(r['test_metrics']['canonical_segment_fraction'],1)])
 table(data,[120,35,52,68,70,77,77])
 p('* « 2 lettres » : part des unités décodées en un groupe de deux lettres. « Conformes » : part des segments dont le texte décodé redonne exactement les mêmes unités après application de la règle de découpage. Ce dernier taux n’est pas une exactitude de traduction ; il dépend aussi de la longueur des segments.','small')
 p('Le témoin mélangé conserve exactement les signes et les longueurs de chaque segment, mais change leur ordre. Un seul mélange est réalisé par configuration, avec le même budget de recherche. Tous les candidats battent leur témoin sur le score local ; cela ne leur donne ni une syntaxe ni un sens vérifiés.','small')

page('DIAGNOSTIC','Pourquoi ces clés<br/>ne sont pas acceptables')
p('Si ta appartient à l’inventaire CV, la règle donne priorité à ta. Une clé qui produit deux unités successives t puis a se contredit : en redécoupant le texte obtenu, ces deux unités deviennent ta. Une suite peut donc sembler plausible au modèle statistique tout en violant le chiffrement supposé.')
table([['Meilleur score par inventaire*','Unités à 2 lettres','Segments conformes','Jonctions interdites']]+[[label(k),pct(r['segmentation_diagnostics']['two_letter_unit_fraction']),pct(r['test_metrics']['canonical_segment_fraction']),num(r['segmentation_diagnostics']['illegal_singleton_joins'])] for k,r in S['best_post_hoc_within_inventory'].items()],[191,100,105,103])
p('* Meilleur score réservé, non pénalisé, choisi après comparaison des huit cas de l’inventaire. Les jonctions interdites sont des erreurs de cohérence avec la règle choisie, pas des preuves d’une langue ou d’un sens. La cohérence a été vérifiée de deux façons : redécoupage complet et détection des jonctions de lettres qui auraient dû fusionner.','small')
p('Les clés utilisent peu la possibilité syllabique','h')
p('Sur les 32 sorties, les unités à deux lettres représentent de '+pct(S['real_two_letter_fraction_min'])+' à '+pct(S['real_two_letter_fraction_max'])+'. Le candidat italien CV au meilleur score n’utilise aucun groupe de deux lettres. Autoriser des syllabes ne suffit donc pas à obtenir une solution syllabique pertinente.')
for k in ['latin_CV','italian_CV']:
 r=S['best_post_hoc_within_inventory'][k]
 p(label(k)+' : extrait automatique, aucune traduction','small')
 p(escape('\n'.join(r['candidate_preview_NOT_TRANSLATION'].splitlines()[1:3])).replace('\n','<br/>'),'sample')
p('Le contrôle de cohérence intervient ici après l’optimisation ; il n’est pas une contrainte dure du solveur. Cette limite explique pourquoi celui-ci peut proposer des clés incompatibles avec la règle. L’intégrer directement à la recherche constitue une amélioration méthodologique prioritaire, qui reste à tester.','small')

page('TRANSCRIPTIONS ET LIMITES','Vérifier sans changer la clé')
p('Diagnostic complémentaire après comparaison des variantes : les quatre clés retenues sont appliquées telles quelles aux passages correspondants d’IT2a. Les métadonnées ZL définissent les groupes et les feuilles réservées. Aucune réoptimisation n’est effectuée.')
data=[['Inventaire','Loci communs','Séquences égales*','Score ZL','Score IT','Conformes IT']]
for r in T['cases']:
 data.append([label(r['model']),r['matched_loci'],r['equal_encoded_unit_sequences'],dec(r['ZL_metrics_matched_loci']['bits_per_four_units']),dec(r['IT_metrics_matched_loci']['bits_per_four_units']),pct(r['IT_metrics_matched_loci']['canonical_segment_fraction'],1)])
table(data,[105,68,95,71,71,89])
p('* Égalité après encodage, pouvant inclure des coupures pour signes inconnus. Les mêmes 340 ou 560 loci sont réutilisés pour deux modèles. Les transcriptions peuvent modifier les longueurs et les fenêtres évaluées ; les écarts sont descriptifs. ZL et IT ne constituent pas deux expertises totalement indépendantes. Aucun nouveau glyphe n’a été certifié sur photographie pendant cette phase.','small')
p('Ce qui demeure inconnu','h')
p('La langue, les valeurs des signes et le mécanisme du manuscrit restent inconnus. Les correspondances okcheor, otcheody et otald du pilote précédent gardent un sens inconnu. Leur répétition ne fournit pas du texte clair connu. Le cas okols reste dépendant d’un espace incertain.','small')
p('Cette expérience ne couvre pas les unités de trois lettres ou plus, tous les inventaires CV/VC, les décompositions non systématiques, les signes nuls, les changements de clé, ni toutes les langues médiévales. Elle ne réfute pas la famille des chiffres syllabiques.','small')
p('Sources et dossier reproductible','h')
p('[1] George Lasry, <link href="https://dspace.ut.ee/items/76b22b8e-5ae1-41a6-8b15-8b2527b9762e" color="#176F75">Deciphering Historical Syllabic Ciphers</link>, HistoCrypt 2024, doi:10.58009/aere-perennius0106. Référence de contexte, pas une réplication.<br/>[2] René Zandbergen / Gabriel Landini, ZL3b ; Takeshi Takahashi et extraction Landini-Stolfi, IT2a ; <link href="https://www.voynich.nu/transcr.html" color="#176F75">transcriptions et format IVTFF</link>. Sources et crédits conservés.<br/>[3] Perseus Digital Library, César, De Bello Gallico : XML et texte normalisé sous CC BY-SA 4.0.<br/>[4] Corpus Pline et Dante fournis par Michael A. Greshko ; licence conservée. Citation requise : The Naibbe cipher, 2025, <link href="https://doi.org/10.1080/01611194.2025.2566408" color="#176F75">doi:10.1080/01611194.2025.2566408</link>. Les tables Naibbe ne sont pas utilisées ici.','small')
p('L’archive contient le protocole, les dictionnaires, les graines, les entrées, les clés, les sorties non traduites, les programmes, les sources et un manifeste SHA-256. Les 72 objectifs C++ ont été recalculés en Python, ainsi que les exactitudes, les mélanges et les diagnostics de découpage.','small')

def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#D5E2E5'));c.line(48,40,547,40)
 c.setFont('DV',8);c.setFillColor(MUTED);c.drawString(48,27,'VOYNICH · PHASE 5 · AUCUNE TRADUCTION VALIDÉE');c.drawRightString(547,27,str(doc.page))
out=ROOT/'output/pdf/Voynich_phase5_syllabes_2026-10-28.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=42,bottomMargin=52,title='Voynich, phase 5 : lettres et unités syllabiques',author='Étude assistée par ChatGPT').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
