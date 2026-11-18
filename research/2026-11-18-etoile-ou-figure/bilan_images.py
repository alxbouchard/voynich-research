"""Croiser les lectures aveugles avec les mots déjà enregistrés."""
import json
from combiner import HERE, write


def read(name):
    return json.loads((HERE/name).read_bytes())


def main():
    a = read('images/VOTES.json')
    b = {x['id']:x for x in read('images/LECTEUR-2.json')['cartes']}
    rows = read('RESULTATS.json')['releve']
    cards = []
    for x in a:
        key=x['carte']
        loc=x['lieu']
        word=rows[loc]['mot']
        first = ('etoile' if x['etoile_reconnaissable'] else
                 'personne' if x['figure_humaine_reconnaissable'] else 'incertain')
        second = b[key]['classe']
        cards.append({'carte':key,'lieu':loc,'lecteur_1':first,'lecteur_2':second,'mot':word,
                      'debut_ot':word.startswith('ot') if word else None,
                      'fin_edy':word.endswith('edy') if word else None})
    data=read('RESULTATS.json')['par_face']
    faces=sorted(f for f in data['figures'].keys() & data['objets'].keys() if
                 all(data[v][f]['lisibles'] for v in ('figures','objets')))
    mixed={v:{'sites':sum(data[v][f]['lisibles'] for f in faces),
              'fin_edy':sum(data[v][f]['tous']['ot_edy']['fin'] for f in faces),
              'debut_ot':sum(data[v][f]['tous']['ot_edy']['debut'] for f in faces)} for v in ('figures','objets')}
    write('LECTURES-ET-MOTS.json',{'cartes':cards,'bains_faces_comparables':faces,'bains_memes_faces':mixed})


if __name__=='__main__': main()
