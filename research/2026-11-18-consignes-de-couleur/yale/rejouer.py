"""Vérifier les photos natives, refaire les mesures et les 14 présentations anonymes."""
from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from statistics import median

from PIL import Image, ImageCms, ImageDraw, ImageOps

BASE = Path(__file__).resolve().parent
POINT_KEYS = {
    'T': 'trace_or_box_center_xy',
    'I': 'same_anatomical_region_xy',
    'P': 'adjacent_parchment_xy',
    'H': 'homologous_organ_xy',
}


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


def rgb_disk(image, center, radius):
    cx, cy = center
    pixels = [
        image.getpixel((cx + dx, cy + dy))
        for dy in range(-radius, radius + 1)
        for dx in range(-radius, radius + 1)
        if dx * dx + dy * dy <= radius * radius
    ]
    return {'n': len(pixels), 'sRGB': [median(channel) for channel in zip(*pixels)]}


def make_card(crop, angle):
    panels = []
    for panel in (crop.copy(), ImageOps.autocontrast(crop, cutoff=0.3)):
        if angle:
            background = int(median(panel.tobytes()))
            panel = panel.rotate(angle, Image.Resampling.BICUBIC, expand=True, fillcolor=background)
        width, height = panel.size
        factor = min(680 / width, 335 / height, 4.5)
        panels.append(panel.resize((round(width * factor), round(height * factor)), Image.Resampling.LANCZOS))
    width, height = panels[0].size
    card = Image.new('RGB', (width + 56, 2 * height + 96), '#f0f0f0')
    draw = ImageDraw.Draw(card)
    for index, panel in enumerate(panels):
        top = 28 + index * (height + 44)
        card.paste(panel, (28, top))
        cy = top + height // 2
        draw.polygon([(12, cy - 5), (12, cy + 5), (24, cy)], fill='#303030')
        draw.polygon([(width + 44, cy - 5), (width + 44, cy + 5), (width + 32, cy)], fill='#303030')
    return card


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='Répertoire de sortie pour le rejeu')
    parser.add_argument('--sources', type=Path, default=BASE / 'originaux')
    args = parser.parse_args()
    registry = json.loads((BASE / 'sites-et-temoins.json').read_text())
    keys = json.loads((BASE / 'cle-cartes.json').read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    card_folder = args.output / 'cartes-Q'
    card_folder.mkdir(exist_ok=True)
    (card_folder / 'LIRE.md').write_bytes((BASE / 'cartes-Q' / 'LIRE.md').read_bytes())
    measurements = {}
    source_info = {}
    for folio, source in registry['sources'].items():
        path = args.sources / (folio + '.jpg')
        if file_digest(path) != source['sha256']:
            raise ValueError(f'Image source différente pour {folio}')
        with Image.open(path) as image:
            if list(image.size) != source['size'] or image.mode != 'RGB':
                raise ValueError(f'Dimensions ou mode couleur inattendus pour {folio}')
            profile = image.info['icc_profile']
            icc = ImageCms.getOpenProfile(BytesIO(profile))
            description = ImageCms.getProfileName(icc).strip()
            if 'srgb' not in description.lower():
                raise ValueError(f'Profil source inattendu pour {folio}: {description}')
            source_info[folio] = {
                'sha256': source['sha256'], 'iiif': source['iiif'],
                'size': source['size'], 'embedded_icc_name': description,
                'embedded_icc_sha256': sha256(profile).hexdigest(),
            }
            at = registry['sites'][folio]
            measurements[folio] = {
                role: {
                    'xy': at[key],
                    'disk': {r: rgb_disk(image, at[key], r) for r in (4, 7, 11)},
                }
                for role, key in POINT_KEYS.items() if at[key] is not None
            }
            for row in (item for item in keys if item['folio'] == folio):
                crop = image.convert('L').crop(row['crop_xyxy'])
                for letter, angle in [('A', 0), ('B', -24)]:
                    target = card_folder / (row['id'] + '-' + letter + '.png')
                    make_card(crop, angle).save(target)
                    if file_digest(target) != row['cards'][target.name]:
                        # PNG compression can differ across versions. Compare decoded pixels.
                        with Image.open(BASE / 'cartes-Q' / target.name) as original, Image.open(target) as replay:
                            if original.mode != replay.mode or original.size != replay.size or original.tobytes() != replay.tobytes():
                                raise ValueError(f'Carte différente : {target}')
    result = {
        'method': 'Médiane par canal des pixels sRGB natifs, disques de rayon euclidien 4, 7, 11. Aucun éclaircissement ni étirement du contraste. La mesure porte sur la photographie encodée et ne détermine pas la composition matérielle.',
        'source': source_info, 'measurements': measurements,
    }
    (args.output / 'mesures-srgb.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
