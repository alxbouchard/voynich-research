"""Calage des similitudes à partir de quatre centres sans nom. Aucune lecture de la réserve."""
from itertools import permutations
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
PRIMARY = ('pleiades_bright7','grande_ourse','petite_ourse')
ORDERS = np.array(list(permutations(range(7),4)))
LIMIT_FIT = .075
LIMIT_HIDDEN = .1


def project(stars):
    ra,dec = np.radians(np.array([(s['ra_deg'],s['dec_deg']) for s in stars]).T)
    v = np.array([np.cos(ra)*np.cos(dec),np.sin(ra)*np.cos(dec),np.sin(dec)]).T
    center = v.mean(axis=0)
    center /= np.linalg.norm(center)
    east = np.cross([0.,0.,1.],center)
    east /= np.linalg.norm(east)
    north = np.cross(center,east)
    return ((v@east)+1j*(v@north))/(v@center)


def complex_xy(xy):
    a=np.asarray(xy)
    return a[:,0]+1j*a[:,1]


def xy(z):
    return [float(z.real),float(z.imag)]


class Chart:
    def __init__(self,stars):
        self.names = [s['name'] for s in stars]
        self.sky = project(stars)
        options = self.sky[ORDERS]
        self.means = options.mean(axis=1)
        centered = options-self.means[:,None]
        self.coeffs = np.concatenate((centered.conj(),centered))
        self.energy = np.tile(np.sum(abs(centered)**2,axis=1),2)
        self.variance_inv = 1/self.energy

    def fit(self,points):
        """Minimiser la perte de Procrustes par une régression complexe après centrage."""
        centered=points-points.mean()
        # Produit scalaire des quatre points, en parallèle pour les 1 680 affectations.
        correlation = sum(self.coeffs[:,j]*v for j,v in enumerate(centered))
        score = abs(correlation)**2*self.variance_inv
        best=int(np.argmax(score))
        return best,score,correlation

    def transform(self,idx,correlation,points):
        perm_idx = idx % len(ORDERS)
        mirror = idx>=len(ORDERS)
        sky = self.sky.conj() if mirror else self.sky
        alpha = correlation[idx]*self.variance_inv[idx]
        order = ORDERS[perm_idx]
        estimate = (sky-sky[order].mean())*alpha+points.mean()
        dia = max(abs(points[:,None]-points).ravel())
        er = abs(estimate[order]-points)
        return estimate,order,mirror,float(np.sqrt(np.mean(er**2))/dia)

    def predictions(self,points):
        idx,scores,corr = self.fit(points)
        runner=int(np.argsort(-scores,kind='stable')[1])
        options=[]
        for pos in (idx,runner):
            estimate,order,mirror,rms=self.transform(pos,corr,points)
            unseen=sorted(set(range(7))-set(order))
            options.append({'ordre_calage':[self.names[i] for i in order],'miroir':mirror,
                    'rms_relatif':rms,'previsions':[{'nom':self.names[i],'xy':xy(estimate[i])} for i in unseen]})
        return options


def charts():
    source=json.loads((HERE.parent/'catalogue/modeles.json').read_text())['models']
    return {tag:Chart(rows) for tag,rows in source.items()}


def main():
    training=json.loads((HERE/'apprentissage.json').read_text())
    models=charts()
    output={}
    for tag,data in training.items():
        points=complex_xy(data['xy'])
        fits = {name:model.predictions(points) for name,model in models.items()}
        winner=min(PRIMARY,key=lambda n:fits[n][0]['rms_relatif'])
        output[tag]={'diametre_calage':float(np.max(abs(points[:,None]-points))),
                     'source_sha256':data['empreinte'],'choix_primaire':winner,'calages':fits}
    (HERE/'PREDICTIONS.json').write_text(json.dumps(output,indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
