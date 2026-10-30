from pathlib import Path
import json,hashlib
from PIL import Image,ImageOps
R=Path(__file__).resolve().parent.parent
specs=[
 ('f116v_MSI_BW.jpg',(2470,1190,4550,1510),'f116v_BW_lastline.png','Last mixed-script line; processed PCA derivative. No new palaeographic reading asserted.'),
 ('f116v_MSI_PSC.jpg',(2470,1190,4550,1510),'f116v_visible_lastline.png','Natural-color reference, EXIF orientation corrected before cropping.'),
 ('f116v_MSI_BW.jpg',(2470,1220,2990,1500),'f116v_BW_pair.png','Candidate oror/aror followed by sheey; first glyph remains uncertain here.'),
 ('f116v_MSI_PSC.jpg',(2470,1220,2990,1500),'f116v_visible_pair.png','Same area in natural color; views are not independent specimens.'),
 ('f104r_Yale.jpg',(340,1890,2520,2160),'f104r_paragraph8.png','Includes f104r.27-29 and some adjacent writing. Comparison located with existing transcripts; not blind.'),
 ('f104r_Yale.jpg',(875,1980,1250,2085),'f104r_pair.png','Candidate aror,sheey (ZL) / arorsheey (IT), f104r.28.'),
]
out=[]
for source,box,name,note in specs:
 p=R/'data'/source;im=ImageOps.exif_transpose(Image.open(p));cut=im.crop(box);dest=R/'audit'/name;cut.save(dest)
 check=Image.open(dest)
 assert check.size==cut.size and check.tobytes()==cut.tobytes()
 out.append(dict(source='data/'+source,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                 original_exif_orientation=Image.open(p).getexif().get(274,1),
                 crop_xyxy_after_exif=box,crop='audit/'+name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
                 note=note,exact_pixel_match=True))
(R/'results/image_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print('Verified',len(out),'native-pixel crops after EXIF orientation handling.')
