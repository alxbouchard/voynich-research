"""Rapprocher les lectures transcrites des observations iconographiques du Gart."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE.parents[1] / '2026-11-18-mots-et-dessins' / 'herbier_1485' / 'corpus.json'
EXTRA_VUE32 = 'e62177b329e348ef075c9da896fc48a1ad1ee0af11313410748070fbdbee706c'


def tables(path):
    with path.open() as stream:
        return {int(row['chapitre']): row for row in csv.DictReader(stream, delimiter='\t')}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def counts(rows, window):
    result = {}
    for status in ('oui', 'non'):
        subset = [row for row in rows if row[window] == status and row['masse_renflee'] != 'sans image']
        result[status] = {
            'chapitres_avec_image': [row['chapitre'] for row in subset],
            'renflement': [row['chapitre'] for row in subset if row['masse_renflee'] == 'oui'],
            'base_distincte': [row['chapitre'] for row in subset if row['partie_basale_distincte'] == 'oui'],
            'renflement_indetermine': [row['chapitre'] for row in subset if row['masse_renflee'] == 'indéterminé'],
        }
    return result


def make_images(images, output, sources, vue32):
    from PIL import Image, ImageDraw, ImageFont
    files = {no: images / f'{sources[no]["view"]}.jpg' for no in (10, 11)}
    for no, file in files.items():
        assert digest(file) == sources[no]['image_sha256']
    assert digest(vue32) == EXTRA_VUE32
    board = Image.new('RGB', (1240, 610), 'white')
    draw = ImageDraw.Draw(board)
    title = ImageFont.load_default(size=19)
    for i, (no, file) in enumerate(files.items()):
        x = 10 + 620 * i
        draw.text((x, 4), f"Chapitre {no}, vue {sources[no]['view']}", font=title, fill='black')
        crop = Image.open(file).crop((217, 920, 1034, 1518))
        crop.thumbnail((600, 440), Image.Resampling.LANCZOS)
        board.paste(crop, (x, 35))
    draw.text((10, 480), 'Suite du chapitre 10, vue 32', font=title, fill='black')
    crop = Image.open(vue32).crop((308, 235, 1175, 332))
    board.paste(crop, (10, 508))
    board.save(output, quality=90)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sortie', type=Path, default=HERE / 'resultats.json')
    parser.add_argument('--photos', type=Path, help='Dossier contenant notamment 31.jpg et 33.jpg')
    parser.add_argument('--vue32', type=Path)
    parser.add_argument('--planche', type=Path, default=HERE / 'deux-aristoloches.jpg')
    args = parser.parse_args()
    dessins = tables(HERE / 'dessins.tsv')
    mentions = tables(HERE / 'mentions.tsv')
    sources = {item['number']: item for item in json.loads(CORPUS.read_text())['items']}
    assert list(dessins) == list(mentions) == list(sources) == list(range(1, 13))
    rows = []
    for no, src in sources.items():
        assert len(src['body'].split()) == 24 and int(dessins[no]['vue']) == int(mentions[no]['vue']) == src['view']
        rows.append(dict(dessins[no], **{k:v for k,v in mentions[no].items() if k not in ('chapitre','vue')},
                         titre=src['title'], url=src['image_url'], sha256=src['image_sha256']))
    result = {'corpus_sha256':digest(CORPUS), 'lectures':rows,
              'partie_basale_et_renflement_par_mention':{w:counts(rows, w) for w in ('positions24','page_ouverture')},
              'suite_du_chapitre_10':{'vue':32, 'source':'https://api.digitale-sammlungen.de/iiif/image/v2/bsb00032739_00032/full/1400,/0/default.jpg','sha256':EXTRA_VUE32}}
    args.sortie.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    if args.photos or args.vue32:
        if not (args.photos and args.vue32):
            parser.error('Indiquer --photos et --vue32 ensemble.')
        make_images(args.photos, args.planche, sources, args.vue32)


if __name__ == '__main__':
    main()
