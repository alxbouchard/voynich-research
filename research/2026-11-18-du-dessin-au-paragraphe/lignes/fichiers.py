"""Écriture déterministe des registres de l'expérience."""
from pathlib import Path
from hashlib import sha256
import gzip
import json

HERE=Path(__file__).resolve().parent
PASSAGES=HERE.parent/'passages'


def save(name,data):
    raw=(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    (HERE/name).write_bytes(gzip.compress(raw,mtime=0) if name.endswith('.gz') else raw)


def load(name):
    raw=(HERE/name).read_bytes()
    return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()
