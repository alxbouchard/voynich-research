"""Prépare les deux cartes pour lecteurs et la comparaison des inscriptions au fac-similé."""
from hashlib import sha256
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
RECTO = (5820,130,9000,1070)
VERSO = (500,120,4040,1330)


def plate(recto, verso):
    front = recto.crop(RECTO).resize((1200,355), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(front)
    # Seul le troisième fragment du recto est interrogé. Son inscription chevauche le pli.
    draw.rectangle((455,161,599,200), fill='#dddddd')
    draw.rectangle((135,137,227,181), fill='#dddddd')
    ref = front.crop((193,0,679,341))
    back = verso.crop(VERSO).resize((1216,416), Image.Resampling.LANCZOS)
    draws = ImageDraw.Draw(back)
    for box in [(0,208,134,263),(210,274,291,320),(434,260,519,303),(581,256,674,299),(709,256,774,300),(807,251,892,296)]:
        draws.rectangle(box, fill='#dddddd')
    # Le texte courant est recouvert sous les dessins sans retrancher la longue racine à droite.
    draws.rectangle((10,333,1014,415), fill='#dddddd')
    frame = Image.new('RGB',(1244,850),'white')
    frame.paste(ref,(379,30))
    frame.paste(back,(14,402))
    d = ImageDraw.Draw(frame)
    try:
        f = ImageFont.truetype('DejaVuSans.ttf',21)
    except OSError:
        f = ImageFont.load_default(size=21)
    d.text((15,15),'Fragment A', font=f, fill='black')
    d.text((15,366),'Candidats 1, 2, 3, 4, 5',font=f,fill='black')
    for i,x in enumerate((163,369,618,761,1046),1):
        d.text((x,821),str(i),font=f,fill='black')
    frame.save(HERE/'dessins-masques.jpg', quality=94)


def inscriptions(recto, verso):
    records = [
        ('f89r2.22', 'Texte, mot 2', recto, (6080,2342,6280,2470)),
        ('f89v2.7', 'Texte, mot 2', verso, (830,1125,1030,1253)),
        ('f89v2.5', 'Fragment 53', verso, (2550,867,2750,995)),
    ]
    frame = Image.new('RGB', (656,207), 'white')
    draw = ImageDraw.Draw(frame)
    font = ImageFont.load_default(size=17)
    for i, (loc, title, im, box) in enumerate(records):
        left = 12 + i*217
        draw.text((left, 8), loc, fill='black', font=font)
        draw.text((left, 32), title, fill='black', font=font)
        frame.paste(im.crop(box), (left,61))
    frame.save(HERE/'trois-inscriptions.png')


if __name__ == '__main__':
    r, v = (Path(a) for a in sys.argv[1:])
    hashes = [sha256(p.read_bytes()).hexdigest() for p in (r, v)]
    assert hashes[0] == '3b553c70d0c068cb39a276d391127165c5d9d868ec08e7f5eb2e73b32bb95d1e'
    assert hashes[1] == 'b6b0dd8ba7cd316f3b09a8b156d1eed0eb36ad8ec9086b975969f4f8f7dd5406'
    with Image.open(r) as recto, Image.open(v) as verso:
        assert recto.size == (9078,3777) and verso.size == (4204,3809)
        plate(recto, verso)
        inscriptions(recto, verso)
