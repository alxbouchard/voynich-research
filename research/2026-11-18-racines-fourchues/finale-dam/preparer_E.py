"""Isole les dessins sur le cliché Yale par polygones de présentation."""
from pathlib import Path
from hashlib import sha256
import json
import sys
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
NATIF = Path(sys.argv[1])
DIGEST = '111f6dfc34b8ecb9230cb5a0d144afef4cbd788048ddda2f440108941c91d5e5'
assert sha256(NATIF.read_bytes()).hexdigest() == DIGEST
im = Image.open(NATIF).convert('RGB')
assert im.size == (2802, 3697)
# Polygones relevés dans une fenêtre de travail provenant du natif.
poly = {
 109: [(151,94),(158,82),(168,74),(184,72),(185,84),(172,94),(173,160),(199,173),(205,226),(190,260),(203,271),(248,277),(252,293),(223,298),(190,290),(213,311),(198,317),(174,299),(148,312),(126,316),(126,301),(142,292),(86,304),(79,298),(86,287),(125,265),(141,245),(132,219),(123,197),(124,173),(147,158),(151,154)],
 110: [(249,78),(289,76),(301,92),(296,105),(277,114),(291,142),(299,174),(301,207),(324,219),(360,222),(386,213),(401,216),(410,231),(405,251),(388,284),(386,309),(376,313),(366,304),(370,266),(357,279),(347,304),(350,315),(332,314),(326,303),(337,269),(335,266),(304,252),(286,233),(279,270),(270,291),(262,293),(254,275),(255,248),(232,271),(218,279),(217,265),(236,228),(244,210),(238,196),(235,171),(244,154),(261,150),(262,131),(247,111)],
 111: [(481,88),(495,80),(507,79),(510,88),(501,100),(504,141),(513,171),(553,168),(576,164),(595,183),(596,224),(587,251),(573,273),(582,301),(570,304),(548,282),(535,264),(513,255),(505,277),(486,299),(465,305),(466,292),(397,329),(385,327),(387,314),(403,291),(417,259),(417,202),(416,180),(425,175),(487,175),(488,159),(480,124)],
 112: [(749,34),(757,27),(770,27),(788,45),(790,78),(780,110),(765,142),(776,160),(786,190),(794,192),(793,204),(785,231),(773,273),(751,302),(743,323),(751,337),(769,343),(770,351),(751,349),(739,347),(723,340),(702,337),(686,339),(671,351),(656,351),(649,337),(638,340),(621,350),(608,353),(604,344),(609,326),(625,290),(632,266),(628,238),(622,213),(626,186),(640,165),(674,146),(705,130),(726,114),(741,85),(751,54)],
 113: [(838,111),(848,85),(869,68),(896,58),(910,55),(916,44),(936,37),(968,35),(995,45),(1002,53),(993,59),(971,51),(937,54),(922,64),(915,78),(913,132),(945,131),(976,143),(998,151),(1004,162),(994,174),(982,185),(978,210),(967,225),(947,248),(923,266),(910,277),(913,296),(922,324),(936,344),(960,357),(973,357),(978,364),(965,369),(939,359),(924,348),(909,328),(898,299),(894,275),(869,293),(849,321),(828,350),(825,365),(833,373),(850,373),(865,370),(873,371),(877,378),(862,384),(839,385),(824,381),(815,371),(811,359),(814,321),(824,289),(830,259),(825,232),(826,206),(810,198),(805,178),(810,156),(841,143),(878,133),(883,77),(870,80),(859,98),(857,116),(848,121)],
}
order = [111, 113, 109, 112, 110]  # Mélange fixe, avant toute cotation.
picks = {}
for k,n in enumerate(order,1):
    pts = [(round((x+285)*im.width/1360), round((y+725)*im.height/1794)) for x,y in poly[n]]
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    bbox = mask.getbbox()
    pict = Image.new('RGB', im.size, '#e8e4d9')
    pict.paste(im,mask=mask)
    sel = pict.crop(bbox)
    code = 'E'+str(k)
    picks[code]={'fragment':n, 'coordonnees_natives':pts, 'cadre':bbox}
    if k==1:
        board=Image.new('RGB',(1164,1280),'#e8e4d9')
    # Même échelle native pour les 5 cartes, et même hauteur de l'aire de dessin.
    thumb=sel.resize((round(sel.width * .63),round(sel.height * .63)),Image.Resampling.LANCZOS)
    xbase, ybase = (k-1)%3*388, (k-1)//3*625
    board.paste(thumb,(xbase+(388-thumb.width)//2,ybase+66+(540-thumb.height)//2))
    draw=ImageDraw.Draw(board)
    try: font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',30)
    except OSError: font=ImageFont.load_default(size=30)
    draw.text((xbase+25,ybase+22),code,fill='#26221f',font=font)
board.save(BASE/'E'/'PLANCHE.jpg',quality=93,optimize=True)
context = im.crop((660, 1530, 2720, 2320))
context.thumbnail((1270,520), Image.Resampling.LANCZOS)
context.save(BASE/'RANGEE-E-CONTEXTE.jpg',quality=91,optimize=True)
details={'photo':'https://collections.library.yale.edu/iiif/2/1006247/full/full/0/default.jpg',
         'sha256':DIGEST,'dimensions':im.size,'folio':'f99v','rangee':3,'codes':picks}
(BASE/'CLE-E.json').write_text(json.dumps(details,indent=1)+'\n')
