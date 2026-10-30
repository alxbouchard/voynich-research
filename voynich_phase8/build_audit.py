#!/usr/bin/env python3
import json,hashlib,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent

def load(p):return json.loads(p.read_text())
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def main():
 targets=load(ROOT/'data/image_targets.json')
 specs=[
  ('1006076',(1310,2825,1590,2955),1460,'ok,chey','okchey','La hampe et la boucle du signe transcrit k occupent des hauteurs différentes. Un intervalle est visible avant ch ; sa largeur dépend de la bande verticale examinée.'),
  ('1006076',(1770,2825,2080,2990),1930,'keey,dal','keey.dal','L’encre est pâle. La fin y et le signe suivant d se distinguent, mais cette image seule ne décide pas du statut de mot.'),
  ('1006208',(1735,2115,1950,2240),1816,'o,kalol','okalol','L’ovale o est distinct de la hampe suivante. Un blanc graphique peut aussi apparaître à l’intérieur d’un groupe transcrit sans espace.'),
  ('1006208',(2010,1000,2320,1130),2122,'dy,olshedy','dy.ol.shedy','Les prolongements inférieurs sont proches. IT ajoute aussi une séparation après ol ; ce deuxième choix n’est pas la cible ici.'),
  ('1006254',(630,2710,865,2810),771,'okeeo,l,lchey','okeeol.lchey','Deux signes transcrits l se suivent. IT joint le premier au groupe précédent et sépare le second ; les deux virgules ZL doivent rester distinctes.'),
  ('1006254',(1650,1585,1935,1710),1772,'tchey,qokeey','tchey.qokchy','La frontière est localisée entre y et q. IT lit aussi ch là où ZL lit ee dans le groupe suivant : cette divergence de signes est conservée.')
 ]
 out=[]
 source_map={r['oid']:r for r in load(ROOT/'data/image_sources.json')}
 for idx,(t,spec) in enumerate(zip(targets,specs),1):
  oid,box,center,z,it,note=spec
  orig=BASE/'voynich_phase3/images'/f'{oid}.jpg';dest=ROOT/'data'/f'{oid}.jpg'
  if not dest.exists():shutil.copy2(orig,dest)
  source=source_map[oid];assert hashlib.sha256(dest.read_bytes()).hexdigest()==source['sha256']
  crop=Image.open(dest).crop(box);cp=ROOT/'results'/f'crop_{idx:02}.png';crop.save(cp)
  out.append(dict(t,id=f'I{idx}',oid=oid,crop_file=cp.relative_to(ROOT).as_posix(),bbox_xyxy=list(box),boundary_x_approx=center,ZL_local=z,IT_local=it,IT_target_split=t['selection']=='maximum',observation_fr=note,source_sha256=source['sha256'],source_url=source['url'],status='LOCALISATION_VISUELLE_NON_AVEUGLE_VARIANTES_CONSERVEES'))
 rows=load(ROOT/'data/paired_uncertain.json');bad=[r for r in rows if (r['p4']<=.1 or r['p4']>=.9) and ((r['p4']>=.5)!=r['IT_label'])];bad.sort(key=lambda r:(min(r['p4'],1-r['p4']),r['locus'],r['offset']))
 t=bad[0];assert t['locus']=='f113v.43,+P0' and t['offset']==48
 box=(1990,2710,2370,2800);Image.open(ROOT/'data/1006271.jpg').crop(box).save(ROOT/'results/crop_07.png');source=load(ROOT/'data/additional_source.json')
 out.append(dict(t,id='I7',selection='supplementary_posthoc_strongest_IT_disagreement',oid='1006271',crop_file='results/crop_07.png',bbox_xyxy=list(box),boundary_x_approx=2153,ZL_local='qok,aiinos',IT_local='qok.aiin.os',IT_target_split=True,observation_fr='Un intervalle est visible entre la fin du groupe qok et le début aiin. Le score très faible du modèle ne suffit pas à supprimer la virgule ZL. IT introduit aussi un espace avant os, hors de la cible.',source_sha256=source['sha256'],source_url=source['url'],status='LOCALISATION_VISUELLE_NON_AVEUGLE_VARIANTES_CONSERVEES'))
 save(ROOT/'results/image_audit.json',{'reviewer':'assistant, image inspection assisted by existing transcriptions and scores, not an independent expert','coordinates':'Native Yale JPEG pixels, top-left origin, boxes [x0,y0,x1,y1); boundary x approximate for visual arrows only','image_processing':'Exact pixel crops only, no enhancement, no synthetic restoration; report scales display without changing sources','claims':'Locations and visible graphical intervals only. No measured physical gap widths, no word-boundary adjudication, no language reading. Six extreme cases chosen on three cached pages, plus one posthoc disagreement; no population accuracy can be inferred.','items':out})
 save(ROOT/'results/extreme_disagreements.json',bad)
 print('Created',len(out),'audit records and exact crops;',len(bad),'extreme disagreements retained.')
if __name__=='__main__':main()
