"""Package validated downloads only; never include staging files or credentials."""
import hashlib, json, zipfile, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
OUT.mkdir(exist_ok=True)
LIMIT=490_000_000
selected=json.loads((ROOT/'msi/selected_files.json').read_text())
downloaded=[]
for f in selected:
    p=ROOT/'msi'/f['group']/f.get('folio','')/f['title']
    meta=Path(str(p)+'.json')
    assert p.exists() and meta.exists(), f['title']
    record=json.loads(meta.read_text())
    assert p.stat().st_size==int(f['size']), f['title']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'], f['title']
    record['path']=str(p.relative_to(ROOT))
    downloaded.append(record)

yale=json.loads((ROOT/'yale/image_index.json').read_text())
assert len(yale)==213
for r in yale:
    p=ROOT/r['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']

materials=json.loads((ROOT/'materials/source_index.json').read_text())
manifest={'retrieved_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
    'yale':yale,'msi':downloaded,'materials':materials,
    'scope':{'yale_images':213,'yale_pdf_pages':214,'processed_jpegs':25,
             'processed_tiffs':1,'true_color_jpegs':6,'raw_f116v':22,'raw_f1r':3},
    'note':'Selected raw files only. Yale full-size JPEG derivatives are not the original TIFF masters.'}
(ROOT/'DOWNLOAD_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

readme='''VOYNICH : RESSOURCES NUMERIQUES POUR LA RECHERCHE

Ces fichiers sont des sources de travail. Ils ne constituent pas un déchiffrement.

CONTENU TELECHARGE ET VERIFIE
- Yale : les 213 images du manifeste officiel, dans leurs dimensions natives JPEG.
  Ce nombre inclut les couvertures, les tranches et les dépliants ; il ne désigne
  pas 213 feuillets. PDF officiel séparé : 214 pages, dont une notice initiale.
- Multispectral : les 25 JPEG du dossier Processed_Images pour les dix pages
  1r, 8r, 17r, 26r, 47r, 70v1, 71r, 93r, 102v1 et 116v ; ajout d'un TIFF
  traité en couleur pour f116v. Six JPEG de référence en couleur naturelle.
- Données brutes : 22 TIFF de f116v, numéros de capture 001 à 022, et trois
  TIFF de f1r (006, 007, 011). Ce sont des images 16 bits conservées sans
  retouche. Les 22 captures ne correspondent pas à 22 longueurs d'onde distinctes.
- Rapport McCrone du 1 avril 2009, publié par Yale : 8 pages.
- Résumé de communication de Zyats, Hodgins et Barabe (2012) : 1 page.
- README original des données multispectrales ; catalogue public et index local.

CE QUI N'EST PAS TELECHARGE DANS CET ENSEMBLE
Le lot brut public contient davantage de fichiers : 46 pour f116v et 38 pour
f1r lors de notre consultation. Les autres captures de ces deux pages, les
TIFF bruts des huit autres pages, les autres TIFF traités et les TIFF maîtres
de Yale restent consultables aux liens du catalogue. Ne pas confondre cette
sélection ciblée avec une copie exhaustive de toutes les données publiques.

UTILISATION
Ouvrir le PDF pour parcourir le manuscrit. Utiliser les JPEG pleine dimension
pour les comparaisons de glyphes et les TIFF bruts pour de nouveaux traitements.
Conserver les noms originaux et l'orientation EXIF. Les fichiers bruts et les
images traitées peuvent avoir des orientations et cadrages différents.
Les TIFF nécessitent un logiciel acceptant des niveaux de gris 16 bits.
Avant une comparaison spectrale : lire les métadonnées et le README original,
vérifier l'alignement, la calibration, les différences d'exposition et les
images témoins. Une couleur artificielle ou une forme visible sur un seul
traitement ne démontre pas la présence d'un caractère.

PORTEE
Ces téléchargements rendent possible une étude numérique à distance ; ils ne
permettent pas de nouvelles mesures physiques sur l'encre ou le parchemin.
Le rapport chimique restitue des analyses déjà réalisées sur l'original.
Aucune nouvelle lecture, traduction ou attribution linguistique n'est validée
par la constitution de ce dossier.

PROVENANCE ET CREDITS
Fac-similé : Cipher manuscript (Voynich manuscript), General Collection,
Beinecke Rare Book and Manuscript Library, Yale University, MS 408.
https://collections.library.yale.edu/catalog/2002046
https://collections.library.yale.edu/manifests/2002046

Imagerie multispectrale : The Lazarus Project and The Chester F. Carlson Center
for Imaging Science at Rochester Institute of Technology.
Beinecke Rare Book & Manuscript Library MS 408, folio indiqué dans le fichier.
Prises de vue en 2014 ; diffusion publique annoncée par Lisa Fagin Davis en 2024.
https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/
https://drive.google.com/drive/folders/1mNQGKQDSCR4M_c2M2JrsU5soghvYwMig

Rapport McCrone, adresse actuelle liée par Yale :
https://library.yale.edu/sites/default/files/2026-06/voynich_analysis.pdf
Résumé de communication de 2012 :
https://cool.culturalheritage.org/coolaic/sg/bpg/annual/v31/bpga31-15.pdf

INTEGRITE
Les fichiers sources sont conservés sans recompression d'image. La compression
ZIP est réversible et conserve les octets. DOWNLOAD_MANIFEST.json contient les
tailles et SHA-256 ; les ZIP sont testés après création. Chaque partie est une
archive ZIP autonome. Extraire les archives dans un même dossier conserve les
sous-dossiers. Les notices de provenance communes peuvent être identiques.
Le PDF officiel est fourni séparément.
'''
(ROOT/'LISEZ_MOI.txt').write_text(readme)

common=[ROOT/'LISEZ_MOI.txt',ROOT/'DOWNLOAD_MANIFEST.json']
outputs=[]

def pack(name,paths):
    parts=[];z=None
    try:
        for p in paths:
            if z is None or (z.fp.tell()+p.stat().st_size+20000>LIMIT):
                if z:z.close()
                out=OUT/f'{name}_{len(parts)+1:02d}.zip'
                z=zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=1)
                parts.append(out)
                for c in common:z.write(c,c.relative_to(ROOT))
            z.write(p,p.relative_to(ROOT))
        if z:z.close();z=None
    finally:
        if z:z.close()
    for out in parts:
        with zipfile.ZipFile(out) as test:
            assert test.testzip() is None,out.name
            assert not any(any(v.startswith('.') for v in Path(n).parts) for n in test.namelist())
        outputs.append({'path':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
        print('Archive validated:',out.name,out.stat().st_size,flush=True)

pack('Voynich_Yale_images',[ROOT/r['path'] for r in yale]+[ROOT/'yale/yale_manifest.json',ROOT/'yale/image_index.json',ROOT/'src/download_yale.py'])
msi_paths=[ROOT/r['path'] for r in downloaded if r['group']!='raw']
msi_paths += [ROOT/'msi/public_catalogue.json',ROOT/'msi/selected_files.json',ROOT/'src/download_drive.py']
msi_paths += [ROOT/'materials'/r['filename'] for r in materials]
msi_paths += [ROOT/'materials/source_index.json']
pack('Voynich_multispectral_et_analyses',msi_paths)
raw=sorted((r for r in downloaded if r['group']=='raw'),key=lambda r:(r['folio'],r['title']))
pack('Voynich_TIFF_bruts',[ROOT/r['path'] for r in raw])
pdf=ROOT/'Voynich_Yale_facsimile_complet.pdf'
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==json.loads((ROOT/'yale/download_summary.json').read_text())['pdf_sha256']
outputs.insert(0,{'path':str(pdf),'bytes':pdf.stat().st_size,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()})
(ROOT/'deliverables.json').write_text(json.dumps(outputs,indent=2))
print(json.dumps({'delivered_files':len(outputs),'total_bytes':sum(r['bytes'] for r in outputs),'scope':manifest['scope']}),flush=True)
