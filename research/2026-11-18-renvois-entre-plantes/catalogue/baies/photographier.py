"""Cadrer trois débuts de ligne dans les images natives de Yale."""
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]
sys.path.insert(0, str(RESEARCH / '2026-11-18-d-initial-et-formules/deux-lignes/photos'))
from planche import entries, font

CASES = [
    ('f17v', 2, 'H, ZL   ycheey   keeor', 'Apprentissage'),
    ('f96v', 8, 'H   ycheey   ckheol        ZL   ycheey   ckheal', 'Seconde plante de départ'),
    ('f87v', 5, 'H, ZL   ycheey   keeo', 'Autre page botanique'),
]


def create(cache):
    index_path = RESEARCH.parent / 'voynich_resources/yale/image_index.json'
    index = {r['label']: r for r in json.loads(index_path.read_bytes())}
    board = Image.new('RGB', (1130, 670), '#faf7ef')
    draw = ImageDraw.Draw(board)
    geometry = {}
    for row_index, (page, n, readings, role) in enumerate(CASES):
        line = entries(page, n, cache, index)
        first, second, third = [r['boite'] for r in line['groupes'][:3]]
        assert first[0] < second[0] < third[0] and line['groupes'][0]['mot'] == 'ycheey'
        # Préserver le blanc à gauche et le début du troisième groupe.
        crop = [first[0]-48, min(first[1], second[1], third[1])-6,
                third[2]+10, max(first[3], second[3], third[3])+4]
        native = Image.open(cache / (page+'-n.jpg')).convert('RGB')
        thumb = native.copy()
        thumb.thumbnail((135, 180))
        offset = row_index*222
        x0, y0 = 8, offset+24
        board.paste(thumb, (x0, y0))
        scale = thumb.width / native.width
        draw.rectangle([x0+crop[0]*scale-1, y0+crop[1]*scale-1,
                        x0+crop[2]*scale+1, y0+crop[3]*scale+1], outline='#b11a12', width=2)
        fragment = native.crop(crop)
        ratio = min(944 / fragment.width, 147 / fragment.height)
        fragment = fragment.resize((round(fragment.width*ratio), round(fragment.height*ratio)), Image.Resampling.LANCZOS)
        board.paste(fragment, (161, offset+34))
        draw.text((160, offset+4), f'{page}.{n}     {role}', fill='#2d271e', font=font(23))
        draw.text((160, offset+184), readings, fill='#2d271e', font=font(23))
        line['cadre_debut'] = crop
        geometry[page] = line
    (HERE/'SOURCES-IMAGES.json').write_text(json.dumps(geometry, ensure_ascii=False, indent=1)+'\n')
    board.save(HERE/'trois-debuts.jpg', quality=92, subsampling=0)


if __name__ == '__main__':
    create(Path(sys.argv[1]))
