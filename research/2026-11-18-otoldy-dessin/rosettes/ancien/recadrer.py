"""Reconstruire les deux fenêtres 2004 à partir des tuiles publiques du Voyager."""
from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image

HERE = Path(__file__).resolve().parent


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('sortie', type=Path)
    parser.add_argument('--cache', type=Path,
                        help='cache local facultatif ayant la structure Ros/6/ligne/col.webp, f48v/5/ligne/col.webp')
    args = parser.parse_args()
    args.sortie.mkdir(parents=True, exist_ok=True)
    for row in json.loads((HERE/'SOURCES.json').read_text()):
        left, top, right, bottom = row['cadre_2004']
        crop = Image.new('RGB',(right-left,bottom-top))
        for tile in row['tuiles']:
            if args.cache:
                name = tile['url'].split('jasondavies.com/', 1)[1]
                raw = (args.cache/name).read_bytes()
            else:
                request = Request(tile['url'],headers={'User-Agent':'Voynich research: image provenance'})
                with urlopen(request, timeout=30) as response:
                    raw = response.read()
            if sha256(raw).hexdigest() != tile['sha256']:
                raise ValueError('Empreinte inattendue pour '+tile['url'])
            with Image.open(BytesIO(raw)) as part:
                crop.paste(part.convert('RGB'),(256*tile['col']-left,256*tile['ligne']-top))
        if row['rotation']==180:
            crop = crop.transpose(Image.Transpose.ROTATE_180)
        if sha256(crop.tobytes()).hexdigest() != row['sha256_pixels_RGB_2004']:
            raise ValueError('Décodage ou assemblage différent pour '+row['lieu'])
        crop.save(args.sortie/(row['lieu']+'.png'))


if __name__=='__main__':
    main()
