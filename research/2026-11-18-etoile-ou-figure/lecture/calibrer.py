"""Seconde calibration avec une ancre secrète de cinq unités distinctes."""
from comparer_hygin import encode, forecast, read, write

table_cachee = dict(o='s', t='t', e='e', d='ll', y='a', ch='q', p='u', k='r')
phrase = ('quarta','stella','est')
texte = [encode(w,table_cachee)[0] for w in phrase]
# stella peut aussi s'encoder avec deux l seulement si l est disponible. Ici il ne l'est pas.
_, predictions = forecast(texte[1],phrase[1],texte[0],'droite',read('HYGIN.json')['ancres']['stella']['contextes'])
write('CALIBRATION.json',{'phrase':phrase,'recodage':texte,'annonces':predictions,
                          'correct':texte[2] in {v[0] for v in predictions}})
