"""Relever les deux lieux dans les éditions de la collection IVTFF et dans l'original v101."""
import argparse
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FILES = ["CD2a-n.txt","FG2a-n.txt","GC2a-n.txt","IT2a-n.txt","RF1b-e.txt","RF1b-er.txt","VT0e-n.txt","ZL3b-n.txt"]
ORIGINAL_PAIR = b"ok179.okoe89"
URL_BASE = "https://www.voynich.nu/data/"


def read_file(path, source_name, grab):
    data = path.read_bytes()
    rows = [{"ligne":n, "texte":row.decode("latin1")} for n,row in enumerate(data.splitlines(),1) if grab(row)]
    return {"url":URL_BASE+source_name,"sha256":sha256(data).hexdigest(),"lignes":rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection", type=Path, help="Dossier des huit éditions nommées dans TEMOINS.json")
    parser.add_argument("original", type=Path, help="Fichier original de Glen Claston, voyn_101.txt")
    parser.add_argument("--sortie",type=Path,default=HERE/"TEMOINS.json")
    args = parser.parse_args()
    def loci(row):
        return row.startswith((b"<f48v.9,",b"<fRos.45,"))
    report = {name:read_file(args.collection/name,name,loci) for name in FILES}
    def shape_controls(row):
        return row.startswith((b"<fRos.50,", b"<fRos.63,"))
    report["deux_témoins_de_forme_de_la_même_face"] = {
        name:read_file(args.collection/name, name, shape_controls) for name in ("ZL3b-n.txt", "GC2a-n.txt")
    }
    def has_pair(row):
        return ORIGINAL_PAIR in row.partition(b">")[2]
    report["voyn_101.txt"] = read_file(args.original,"voyn_101.txt",has_pair)
    args.sortie.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")


if __name__ == "__main__":
    main()
