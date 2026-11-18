"""Generate the complete f67r2 alignment table, preserving IVTFF alternatives."""
import argparse
import csv
import math
import re
from pathlib import Path

from prepare_cards import CENTER, RUBRICS
from prepare_sectors import BLACK_CODES, DIVIDERS, FACES

PARAGRAPHS=[(13,14),(16,18),(19,21),(23,25),(26,27),(29,30),(32,33),(35,36),(38,40),(41,43),(44,46),(48,51)]
ISOLATED={1:15,3:22,5:28,6:31,7:34,8:37,11:47}
PAINT=["rouge","ocre","rouge","ocre","rouge","ocre","ocre","rouge","rouge","ocre","rouge","ocre"]
def load(path):
    text=path.read_text(encoding="utf-8-sig")
    matches=re.findall(r"^<f67r2\.(\d+),[^>]+>\s+([^\n]+)",text,re.M)
    result={int(num):value.rstrip() for num,value in matches}
    if set(result)!=set(range(1,75)):
        raise ValueError(f"Source incomplete: {path}")
    return result
def write(data,out):
    editions=[load(data/name) for name in ("IT2a-n.txt","ZL3b-n.txt")]
    with out.open("w",newline="",encoding="utf8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        head=["secteur","angle_bord_debut_degres","angle_bord_fin_degres","x_rouge_repere_px","y_rouge_repere_px","x_visage_repere_px","y_visage_repere_px","pigment_lateral_visage","carte_rouge","carte_noire","locus_rouge","loci_paragraphe","locus_isole","locus_visage"]
        for e in ("H","ZL"):
            head.extend(e+"_"+role for role in ("rouge","paragraphe_dans_ordre","isole","visage"))
        writer.writerow(head)
        for k,(card,num,left,right) in enumerate(RUBRICS):
            t=math.radians((left+right)/2)
            face=math.radians(FACES[k])
            lo,hi=PARAGRAPHS[k]
            loc=ISOLATED.get(num)
            line=[num,DIVIDERS[k],DIVIDERS[k+1],round(CENTER[0]+1090*math.sin(t)),round(CENTER[1]-1090*math.cos(t)),round(CENTER[0]+535*math.sin(face)),round(CENTER[1]-535*math.cos(face)),PAINT[k],card,BLACK_CODES[k],num,f"{lo}–{hi}",loc or "",52+k]
            for edit in editions:
                line.extend([edit[num]," | ".join(edit[i] for i in range(lo,hi+1)),edit[loc] if loc else "",edit[52+k]])
            writer.writerow(line)
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("data",type=Path)
    p.add_argument("output",type=Path)
    args=p.parse_args()
    write(args.data,args.output)
