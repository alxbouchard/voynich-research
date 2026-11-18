"""Vérifier l’ingrédient annoncé dans le corps d’une recette dentaire."""
from pathlib import Path
from hashlib import sha256
from xml.etree import ElementTree as ET
import re
import sys
from recettes import HERE, SOURCE, save

source=Path(sys.argv[1]); prediction=HERE/'REMEDE-PREDICTION.md'
assert sha256(source.read_bytes()).hexdigest()==SOURCE
pattern=re.compile('p[iy]r(?:e|ae)t(?:h)?r(?:i|o|um|a|is|orum)')
occurrences={}; target=None; length=0
for chapter in ET.parse(source).iter():
    if chapter.get('subtype')!='compositio':continue
    n=chapter.get('n'); text=' '.join(''.join(chapter.itertext()).split())
    words=re.findall(r'[^\W\d_]+',text.lower()); hits=[(i+1,w) for i,w in enumerate(words) if pattern.fullmatch(w)]
    length+=len(words)
    if hits:occurrences[n]=dict(mots=len(words),positions=hits)
    if n=='60': target=dict(extrait=' '.join(text.split()[:25]),mots=len(words),positions=hits)
assert target is not None
save('REMEDE-RESULTAT.json',dict(annonce=sha256(prediction.read_bytes()).hexdigest(),xml=SOURCE,
      notice_60=target,occurrences=occurrences,total_mots=length,
      nombre_recettes=271,nombre_recettes_avec_nom=len(occurrences)))
