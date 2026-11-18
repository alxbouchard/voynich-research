"""Deux régions de Yale en pixels natifs, pour vérifier l'étiquette et son support."""
from hashlib import sha256
from pathlib import Path
import sys
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
CASES = [("f77r","9ad387ccea37cd8a25ce9602817eb19af5105c545a238203715efe454e5b24ad",
          (1050,130,1910,815), (1451,300,1558,376)),
         ("f77v","e2e2f629753bfe6a9c111d8157ac63cfc4524966cbf367ddaaffece07cffdab2",
          (540,185,1410,905), (904,395,1149,478))]
for name, required, extent, inscription in CASES:
    path=Path(sys.argv[1])/(name+".jpg")
    assert sha256(path.read_bytes()).hexdigest()==required
    region=Image.open(path).crop(extent)
    x,y=extent[:2]
    a,b,c,d=inscription
    ImageDraw.Draw(region).rectangle((a-x-6,b-y-7,c-x+6,d-y+7),outline="#92385e",width=3)
    region.save(HERE/(name+".jpg"),quality=94)
