"""Comparer les positions annoncées aux positions mesurées dans le dessin, à la même échelle relative."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
import numpy as np

HERE=Path(__file__).resolve().parent
def read(path):
    return json.loads(path.read_text())


def panel(ax,title,subtitle,anchors,result):
    points=np.array(anchors,dtype=float)
    center=points.mean(axis=0)
    size=result['diametre_calage_pixels']
    points=(points-center)/size
    observed=np.array([r['coord_observee'] for r in result['etoiles']])
    observed=(observed-center)/size
    predicted=(np.array([r['coord_pred'] for r in result['etoiles']])-center)/size
    ax.set_aspect('equal');ax.set_xlim(-.9,1.02);ax.set_ylim(.72,-.88)
    ax.axhline(0,color='#dcd8d0',lw=.65,zorder=0);ax.axvline(0,color='#dcd8d0',lw=.65,zorder=0)
    ax.scatter(*points.T,s=45,facecolor='#484d52',edgecolor='white',linewidth=.8,zorder=4)
    for q,r in zip(predicted,observed):
        ax.add_patch(Circle(q,.1,facecolor='#faf0e7',edgecolor='#ac5930',alpha=.65,lw=1))
        ax.plot([q[0],r[0]],[q[1],r[1]],color='#867a72',lw=1.2,zorder=2)
    ax.scatter(*predicted.T,marker='x',s=63,lw=2,color='#aa4c22',zorder=4)
    ax.scatter(*observed.T,marker='D',s=40,facecolor='#166c71',edgecolor='white',lw=.6,zorder=5)
    ax.text(0,1.16,title,transform=ax.transAxes,fontsize=16,fontweight='bold',color='#21282c')
    ax.text(0,1.07,subtitle,transform=ax.transAxes,fontsize=11,color='#41484b')
    ax.set_xticks([]);ax.set_yticks([])
    for spine in ax.spines.values():spine.set_edgecolor('#d4d0ca')


def main():
    p=HERE.parent
    result=read(HERE/'RESULTATS.json')['resultats']['voynich']['pleiades_bright7']
    gal=read(HERE/'GALILEE-RESULTATS.json')['reserve']['pleiades_bright7']
    train=read(HERE/'apprentissage.json')['voynich']['xy']
    rows=sorted(read(p/'etalons/galilee1610_pleiades_six_points.json')['points'],key=lambda r:(r['x'],r['y']))
    fig,axes=plt.subplots(1,2,figsize=(9.3,5.45))
    fig.subplots_adjust(left=.045,right=.975,top=.77,bottom=.16,wspace=.15)
    panel(axes[0],'Manuscrit Voynich','Sept points, dont trois réservés',train,result)
    panel(axes[1],'Carte de Galilée, 1610','Six points, dont deux réservés',[[rows[i]['x'],rows[i]['y']] for i in (0,2,3,5)],gal)
    fig.suptitle('Où la carte des Pléiades place-t-elle les étoiles cachées ?',fontsize=17,fontweight='bold',y=.965)
    handles=[Line2D([],[],marker=m,color=c,linestyle='None',markersize=7,label=t) for m,c,t in [
        ('o','#484d52','Point de calage'),('x','#aa4c22','Position prédite'),('D','#166c71','Position observée en réserve')]]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.064),ncol=3,frameon=False,fontsize=10)
    fig.text(.5,.038,'Chaque cercle a pour rayon 10 % du diamètre des quatre points de calage.',ha='center',fontsize=10,color='#444')
    fig.savefig(HERE/'positions-predites.png',dpi=160,facecolor='white')
    plt.close(fig)


if __name__=='__main__':
    main()
