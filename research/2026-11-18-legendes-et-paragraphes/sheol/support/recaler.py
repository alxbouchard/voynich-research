"""Reporte la silhouette du recto après un recalage affine sur le support."""
import hashlib
import json
from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / 'REPERES.json').read_text())
WINDOW = [930, 150, 3010, 1010]


def read_image(path, key):
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == DATA[key]['sha256']
    im = cv2.imread(str(path))
    assert list(im.shape[1::-1]) == DATA[key]['size']
    return im


def project(points, affine):
    points = np.atleast_2d(points)
    return np.column_stack((points, np.ones(len(points)))) @ affine


def point_errors(items, transform):
    result = []
    for item in items:
        prediction = project(item['recto_miroir'], transform)[0]
        delta = prediction - item['verso']
        result.append({'nom': item['nom'], 'prediction': prediction.tolist(), 'ecart_px': float(np.linalg.norm(delta))})
    return result


def green_mask(im, box, amax):
    x, y, right, bottom = box
    a = cv2.cvtColor(im[y:bottom, x:right], cv2.COLOR_BGR2LAB)[:, :, 1]
    # Le filtre médian supprime le grain du JPEG et les variations isolées de la peau.
    return (cv2.medianBlur(a, 11) <= amax).astype('uint8')


def full_green_front(front, threshold, bbox):
    x, y, right, bottom = bbox
    small = green_mask(front, bbox, threshold)
    n, ids, stats, _ = cv2.connectedComponentsWithStats(small, 8)
    assert n > 1
    largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    mask = np.zeros(front.shape[:2], 'uint8')
    mask[y:bottom, x:right] = (ids == largest).astype('uint8')
    return mask


def scores(front, back, fit, box_front, box_back):
    x, y, right, bottom = box_back
    h, w = bottom-y, right-x
    rows = []
    predicted = None
    for forward_level, reverse_level in [(123, 124), (125, 126), (127, 128)]:
        src = full_green_front(front, forward_level, box_front)
        target = green_mask(back, (x, y, right, bottom), reverse_level)
        if forward_level == 125:
            predicted = cv2.warpAffine(src, fit.T, back.shape[1::-1], flags=cv2.INTER_NEAREST)
        comparisons = {}
        for displacement in (-500, -250, 0, 250, 500):
            shift = fit.copy()
            shift[2] += [displacement-x, -y]
            predicted_roi = cv2.warpAffine(src, shift.T, (w, h), flags=cv2.INTER_NEAREST)
            count = int(predicted_roi.sum())
            overlap = int((predicted_roi & target).sum())
            comparisons[str(displacement)] = {'pixels_predits': count, 'pixels_communs': overlap,
                                               'couverture': overlap / count}
        rows.append({'seuil_a_recto': forward_level, 'seuil_a_verso': reverse_level,
                     'pixels_verts_region_verso': int(target.sum()), 'deplacements_x': comparisons})
    return rows, predicted


def font_for_figure(size):
    for name in ('DejaVuSans.ttf', 'Arial.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def landmarks_figure(front, back):
    points = DATA['training'] + DATA['reserve']
    n = len(points)
    out = Image.new('RGB', (8*122, 2*145+30), '#f5f1ec')
    d = ImageDraw.Draw(out)
    font = font_for_figure(13)
    for i, (im, key) in enumerate(((front, 'recto_miroir'), (back, 'verso'))):
        for j, row in enumerate(points):
            x,y = row[key]
            crop = im[y-55:y+56,x-55:x+56]
            ox,oy = j*122+4,i*145+22
            out.paste(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)),(ox,oy))
            cx,cy = ox+55,oy+55
            for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
                d.line((cx+7*dx,cy+7*dy,cx+15*dx,cy+15*dy),fill='red',width=2)
            d.text((ox,oy+112), f'{x}, {y}',font=font,fill='#24211d')
            prefix = 'Calage' if j<4 else 'Réserve'
            d.text((ox,2),f'{prefix} {j%4+1}',font=font,fill='#24211d')
    d.text((4,297),'Haut : recto en miroir. Bas : verso. Coordonnées en pixels natifs.',font=font,fill='#24211d')
    out.save(HERE/'points-du-parchemin.jpg',quality=93)


def figure(front, back, predicted, extra_masks, fit):
    x, y, right, bottom = WINDOW
    # Tous les panneaux sont présentés dans les coordonnées du verso.
    warped = cv2.warpAffine(front, fit.T, back.shape[1::-1])
    contour, _ = cv2.findContours(predicted.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    overlay = back[y:bottom,x:right].copy()
    cv2.drawContours(overlay, contour, -1, (25,30,215), 5, offset=(-x,-y))
    panels = [warped[y:bottom,x:right], back[y:bottom,x:right], overlay]
    for secondary in extra_masks:
        other, _ = cv2.findContours(secondary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(overlay, other, -1, (150,75,5), 4, offset=(-x,-y))
    font = font_for_figure(20)
    out = Image.new('RGB', (940, 3*430), '#f7f4ee')
    d = ImageDraw.Draw(out)
    for i, (im, title) in enumerate(zip(panels, ['Recto retourné et recalé', 'Verso du même feuillet',
                                                   'Contours du recto sur le verso. Couronne en rouge, deux feuilles en bleu'])):
        pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        pil.thumbnail((920,386),Image.Resampling.LANCZOS)
        out.paste(pil,(10,35+430*i))
        d.text((10,6+430*i), title, fill='#25221e',font=font)
    out.save(HERE/'superposition.jpg',quality=92)


def main():
    front = cv2.flip(read_image(sys.argv[1], 'recto'), 1)
    back = read_image(sys.argv[2], 'verso')
    train = DATA['training']
    source = np.array([p['recto_miroir'] for p in train])
    dest = np.array([p['verso'] for p in train])
    fit = np.linalg.lstsq(np.c_[source, np.ones(len(source))], dest, rcond=None)[0]
    frontiers = []
    for ref in DATA['bord_superieur']:
        pred = project(ref['recto_miroir'], fit)[0]
        frontiers.append(dict(ref, prediction=pred.tolist(), erreur_y_px=float(pred[1]-ref['y_verso_lu'])))
    metrics, predicted = scores(front, back, fit, DATA['region_grande_couronne_recto_miroir'],
                                DATA['region_recherche_verso'])
    secondary_metrics = {}
    extra_masks = []
    for name, box in DATA['apres_inspection_petites_feuilles_recto_miroir'].items():
        more, mask = scores(front, back, fit, box, DATA['region_recherche_feuilles_verso'])
        secondary_metrics[name] = more
        extra_masks.append(mask)
    figure(front, back, predicted, extra_masks, fit)
    landmarks_figure(front, back)
    result = {'matrice_affine_recto_miroir_vers_verso': fit.tolist(),
              'calage': point_errors(train, fit), 'reserve': point_errors(DATA['reserve'], fit),
              'bord_superieur': frontiers, 'vert': metrics, 'complement_suggere_apres_inspection': secondary_metrics}
    (HERE/'RESULTATS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('Réserves', result['reserve'])
    print('Bord',[(r['recto_miroir'][0],round(r['erreur_y_px'],1)) for r in frontiers])
    for row in metrics:
        print(row['seuil_a_recto'],[(x,round(row['deplacements_x'][str(x)]['couverture'],3)) for x in [-500,-250,0,250,500]])


if __name__=='__main__':
    main()
