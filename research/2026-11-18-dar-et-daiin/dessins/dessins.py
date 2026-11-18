"""Régénérer les deux planches à partir des 13 JPEG Yale et publier les codages visuels."""
import json
from hashlib import sha256
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
# Les deux colonnes codent la présence des colliers doubles et la présence des dents.
CASES = {
    "f18v": ((780,2535,2640,3690), False, True, "Dents dessinées sur le bord supérieur de la masse ocre."),
    "f23r": ((340,2750,2530,3410), True, False, "Plusieurs profils ovales emboîtés à travers le corps, radicelles vers le bas."),
    "f14r": ((850,2960,2440,3580), False, False, "Sections incurvées simples, croissants d’ocre. Axe en boucle presque fermée."),
    "f9r": ((580,2610,2600,3680), False, None, "Sur le bout mince, plusieurs petites paires de crochets. Le détail ne permet pas de les assimiler avec certitude à des lobes à double contour."),
    "f9v": ((1560,2920,2420,3770), False, False, "Racines fines descendantes en faisceau."),
    "f10r": ((70,3000,2400,3730), False, False, "Corps jointif prolongé par deux renflements rouges terminaux."),
    "f10v": ((1250,2900,2839,3740), False, True, "Trois pointes libres au-dessus du prolongement horizontal droit. Le départ est terminal, critère pris dans son acception large."),
    "f13r": ((760,2420,2250,3710), False, False, "Masse brun rouge, petits corps juxtaposés autour du col."),
    "f13v": ((1420,2860,2610,3730), False, False, "Racines partant de la base vers le bas ou vers la droite."),
    "f15r": ((430,2940,2210,3620), False, False, "Petites pointes principalement sous l’axe rouge horizontal. Forme centrale reliée à la tige."),
    "f15v": ((960,2820,2830,3700), False, False, "Deux bosses sur chacune des deux extrémités renflées, sans série de trois sur le même bord."),
    "f16r": ((720,2490,2400,3730), False, False, "Plusieurs bras arrondis bordés de poils à trait simple."),
    "f16v": ((1250,2770,2580,3660), False, None, "Les pointes en forme de griffe remontent. Leurs bases sont superposées ; leur implantation sur un même bord supérieur horizontal est incertaine."),
}
LINES = {"f18v": ((1913,923,2620,1046), "qokol  daiin  qokol  dar"),
         "f23r": ((886,820,1516,927), "qokchol  dar  qokchol"),
         "f14r": ((430,750,1340,895), "qokchol  dar  dala/dalo  qotolo")}


def font(size, bold=False):
    names = [Path("/System/Library/Fonts/Supplemental")/("Arial Bold.ttf" if bold else "Arial.ttf"),
             Path("/usr/share/fonts/truetype/dejavu")/("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")]
    return next((ImageFont.truetype(str(p),size) for p in names if p.exists()), ImageFont.load_default(size=size))


def paste(canvas, im, x, y, w, h):
    im = im.copy()
    im.thumbnail((w, h), Image.Resampling.LANCZOS)
    canvas.paste(im, (x+(w-im.width)//2,y+(h-im.height)//2))


def main(folder):
    index=json.loads((ROOT/"voynich_resources/yale/image_index.json").read_text())
    sources,images={},{}
    for page,(box,p,d,note) in CASES.items():
        rec,=(row for row in index if row["label"]==page[1:])
        file=folder/(page+".jpg")
        if sha256(file.read_bytes()).hexdigest()!=rec["sha256"]:
            raise ValueError(f"Empreinte différente de la source Yale : {page}")
        images[page]=Image.open(file).convert("RGB")
        sources[page]={k:rec[k] for k in ("url","sha256","width","height")}
        sources[page].update(racine_xyxy=box,colliers=p,dents=d,observation=note)
        if page in LINES: sources[page]["texte_xyxy"]=LINES[page][0]
    board=Image.new("RGB",(1480,1240),"white")
    pen=ImageDraw.Draw(board)
    pen.text((22,17),"Les passages et la racine sur les trois pages",font=font(37,True),fill="#25271f")
    pen.text((25,84),"Page entière",font=font(23,True),fill="black")
    pen.text((305,84),"Passage",font=font(23,True),fill="black")
    pen.text((905,84),"Détail de la racine",font=font(23,True),fill="black")
    for idx, (pg,(line,reading)) in enumerate(LINES.items()):
        y=135+idx*350
        pen.line((20,y-7,1460,y-7),fill="#c8c8c3",width=2)
        pen.text((23,y),pg+(".5" if pg=="f14r" else ".7"),font=font(23,True),fill="black")
        overview=images[pg].copy()
        d=ImageDraw.Draw(overview)
        d.rectangle(line,outline="#a62242",width=13);d.rectangle(CASES[pg][0],outline="#3d5c68",width=13)
        paste(board,overview,20,y+33,242,290)
        paste(board,images[pg].crop(line),305,y+58,545,145)
        pen.text((310,y+213),reading,font=font(22),fill="black")
        paste(board,images[pg].crop(CASES[pg][0]),893,y+37,564,278)
    pen.text((24,1191),"Yale, Beinecke MS 408. Les recadrages gardent les proportions. Les trois racines sont à des échelles différentes.",font=font(19),fill="#444a44")
    board.save(HERE/"trois-racines.jpg",quality=94)

    controls=[pg for pg in CASES if pg not in LINES]
    out=Image.new("RGB",(1380,1330),"white"); pen=ImageDraw.Draw(out)
    pen.text((22,18),"Les dix faces témoins du cahier 2",font=font(34,True),fill="black")
    for i,pg in enumerate(controls):
        x=18+(i%3)*455;y=83+(i//3)*306
        pen.text((x+4,y),pg,font=font(22,True),fill="black")
        paste(out,images[pg].crop(CASES[pg][0]),x,y+35,443,245)
    out.save(HERE/"dix-temoins.jpg",quality=92)
    tally=lambda i,val:sum(CASES[pg][i] is val for pg in controls)
    res={"sources":sources,"coordonnees":"pixels xyxy, origine en haut à gauche, fin exclue",
         "temoins":controls,"temoins_colliers_presents":tally(1,True),"temoins_dents_presentes":tally(2,True),
         "temoins_dents_absentes":tally(2,False),"temoins_dents_incertaines":tally(2,None)}
    (HERE/"LECTURES.json").write_text(json.dumps(res,ensure_ascii=False,indent=2)+"\n")


if __name__=="__main__":
    main(Path(sys.argv[1]))
