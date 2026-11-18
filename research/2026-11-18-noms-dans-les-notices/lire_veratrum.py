"""Rejoue la comparaison exploratoire avec la table de Bax de l'étude précédente."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '2026-11-18-bax'))
from recherche_bax import match, word_info

if __name__ == '__main__':
    projection = word_info('otoldy')
    skeleton = list('vrtrm')
    result = {'repere':'f99v.2', 'hypothese':'veratrum', 'consonnes':skeleton,
              'projection':projection, 'compatibilite_selon_le_modele':match(projection,skeleton)}
    (HERE/'BAX_VERATRUM.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
