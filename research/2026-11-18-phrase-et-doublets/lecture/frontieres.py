"""Sensibilité ajoutée après lecture des deux fac-similés du XVe siècle."""
from argparse import ArgumentParser
from pathlib import Path
import json

from lectures_contextuelles import HERE, dictionary_index, readback, run, save
from corpus_sources import celsus


def main():
    cli = ArgumentParser()
    cli.add_argument("xml",type=Path)
    args = cli.parse_args()
    german = json.loads((HERE/"RIDGES.json").read_text())
    site = "BuchDerNatur-Canamellis_1482_vonMegenberg:3456-3488"
    assert german[site][:5] == ["der","lactucken","lactuca","heyst","lactucken"]
    heading, body = german[site][:2], german[site][2:]
    del german[site]
    german[site+":rubrique"] = heading
    german[site+":corps"] = body
    result = {}
    for name,data in [("RIDGES_frontiere_laitue",german),("Celse_points",celsus(args.xml,r"[.!?]")),
                      ("Celse_points_et_point_virgule",celsus(args.xml,r"[.!?;]"))]:
        lex = {w for line in data.values() for w in line}
        index = dictionary_index(lex)
        for mute in (False,True):
            summary = run(data,"position",mute,lex,index)
            hits = readback({"essais":{name:{"m":summary}}},{name:data})[name]["m"]
            result[name+str(mute)] = {"fenetres":summary["fenetres"],"triplets":len(hits["sites"]),
                                     "mesures":hits["mesures"],"sites":hits["sites"]}
            print(name,mute,summary["fenetres"],len(hits["sites"]),hits["mesures"]["attendu"])
    save(HERE/"FRONTIERES.json",result)


if __name__=="__main__":
    main()
