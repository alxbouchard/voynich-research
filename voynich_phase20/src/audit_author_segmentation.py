#!/usr/bin/env python3
"""Audit greedy segmentation versus exact dictionary segmentation at fixed keys.

Uses the original published English models and interpolation constants.
No key is fitted here. The README fixture is development data, not a holdout.
CC BY-SA 4.0; see ../README.md for Hauer, Hayward and Kondrak attribution.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT/'tmp/authors_models'
WL = (0.129793302623898, 0.226872659329747, 0.643334038046355)
CL = (0.0950848948641174, 0.229797965264228, 0.675117139871655)
X = 0.05


def edges_for(text, vocabulary):
    return [[(j, text[i:j]) for j in range(i+1, len(text)+1)
             if text[i:j] in vocabulary] for i in range(len(text))] + [[]]


def greedy(text, vocabulary):
    if not text or text in vocabulary:
        return text
    for length in range(len(text), 0, -1):
        for offset in range(len(text)-length+1):
            word = text[offset:offset+length]
            if word in vocabulary:
                return ' '.join(x for x in (
                    greedy(text[:offset], vocabulary), word,
                    greedy(text[offset+length:], vocabulary)) if x)
    return text


def needed_ngrams(edges):
    wanted = {1: set(), 2: set(), 3: set()}
    for outgoing in edges:
        for j, a in outgoing:
            wanted[1].add((a,))
            for k, b in edges[j]:
                wanted[2].add((a, b))
                for _, c in edges[k]:
                    wanted[3].add((a, b, c))
    return wanted


def read_models(wanted):
    tables = {}
    for unit, suffix in [('word','unk.wlm'), ('char','chr.clm')]:
        for n in (1, 2, 3):
            table = {}
            with (MODELS/f'lmtrain_nyt_word.{suffix}{n}').open() as f:
                for line in f:
                    parts = line.rstrip().split('\t')
                    key = tuple(parts[:n])
                    if unit == 'char' or key in wanted[n] or key == ('<u>',):
                        table[key] = float(parts[n])
            tables[unit, n] = table
    return tables


def token_score(history, token, unit, tables):
    coefficients = WL if unit == 'word' else CL
    context = tuple(history) + (token,)
    prob = sum(coefficients[n-1] * tables[unit, n].get(context[-n:], 0.)
               for n in (1, 2, 3) if len(context) >= n)
    if not prob:
        raise ValueError(f'Zero probability for {unit} {context!r}')
    return math.log(prob)


def full_score(segmented, tables):
    total = {}
    for unit, sequence in [('word', segmented.split()),
                           ('char', list(segmented.replace(' ', '_')))]:
        if any((x,) not in tables[unit, 1] for x in sequence):
            raise ValueError('This audit is restricted to dictionary tokens.')
        total[unit+'_score_ln'] = sum(token_score(sequence[max(0,i-2):i], token, unit, tables)
                                      for i, token in enumerate(sequence))
    total['combined_score_ln'] = X*total['char_score_ln']+(1-X)*total['word_score_ln']
    return total


def transition(history, word, tables):
    word_score = token_score(history, word, 'word', tables)
    # At a word boundary, the last two characters are determined by the last
    # two words. Spaces are scored when the next word is appended, as upstream.
    char_history = list('_'.join(history)[-2:])
    addition = ('_' if history else '') + word
    char_score = 0.
    for char in addition:
        char_score += token_score(char_history, char, 'char', tables)
        char_history = (char_history+[char])[-2:]
    return (1-X)*word_score + X*char_score


def exact_segment(text, edges, tables):
    # Complete dynamic program: future scores depend only on position and the
    # previous two words. No beam pruning, use of plaintext, or fitted threshold.
    states = [dict() for _ in range(len(text)+1)]
    states[0][()] = (0., ())
    states_visited = 0
    for position in range(len(text)):
        states_visited += len(states[position])
        for history, (score, path) in states[position].items():
            for end, word in edges[position]:
                next_history = (history+(word,))[-2:]
                candidate = score + transition(history, word, tables)
                previous = states[end].get(next_history)
                if previous is None or candidate > previous[0]:
                    states[end][next_history] = (candidate, path+(word,))
    if not states[-1]:
        raise ValueError('No dictionary segmentation.')
    score, path = max(states[-1].values(), key=lambda x: x[0])
    segmented = ' '.join(path)
    assert abs(score-full_score(segmented, tables)['combined_score_ln']) < 1e-9
    return {'segmentation':segmented, 'score_ln':score,
            'states_visited':states_visited, 'final_states':len(states[-1])}


def exhaustive_check(edges, tables):
    best = (-math.inf, '')
    visited = 0
    def walk(position, path):
        nonlocal best, visited
        if position == len(edges)-1:
            visited += 1
            text = ' '.join(path)
            score = full_score(text, tables)['combined_score_ln']
            if score > best[0]:
                best = score, text
            return
        for end, word in edges[position]:
            walk(end, path+(word,))
    walk(0, ())
    return {'paths_enumerated':visited, 'best_score_ln':best[0], 'best_segmentation':best[1]}


def main():
    for row in json.loads((ROOT/'data/authors_model_sources.json').read_text())['extracted']:
        assert hashlib.sha256((MODELS/row['file']).read_bytes()).hexdigest() == row['sha256']
    vocabulary = set()
    with (MODELS/'lmtrain_nyt_word.patlst').open() as f:
        for line in f:
            parts = line.rstrip().split('\t')
            if parts[0] == '1':
                vocabulary.update(parts[2:])
    candidates = [('true_key','thisisatopsecretmessage'),
                  ('returned_key','thisisatulsecretmessage')]
    edge_sets = {name:edges_for(text,vocabulary) for name,text in candidates}
    wanted = {n:set() for n in (1,2,3)}
    for edges in edge_sets.values():
        needed = needed_ngrams(edges)
        for n in wanted:
            wanted[n].update(needed[n])
    tables = read_models(wanted)
    result = {'scope':'Fixed-key development diagnostic only; not decipherment, held-out calibration, or a complete reproduction of the article.',
              'language':'English, original NYT-derived published models',
              'candidate_plaintext_known_to_auditor':True,
              'algorithm_sees':'Decoded letter string, dictionary and probability tables only; no true boundaries.',
              'vocabulary_size':len(vocabulary), 'rows':[]}
    for name, text in candidates:
        old = greedy(text, vocabulary)
        optimal = exact_segment(text, edge_sets[name], tables)
        exhaustive = exhaustive_check(edge_sets[name], tables)
        assert abs(exhaustive['best_score_ln']-optimal['score_ln']) < 1e-9
        result['rows'].append({'candidate':name, 'letters':text,
            'greedy_segmentation':old, 'greedy_scores':full_score(old,tables),
            'exact':optimal, 'exhaustive_check':exhaustive})
    result['known_correct_boundaries_score'] = full_score('this is a top secret message',tables)
    (ROOT/'results/authors_exact_segmentation_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'tmp/reduced_model_tables.json').write_text(json.dumps({
        unit+str(n):[['\t'.join(key),value] for key,value in table.items()]
        for (unit,n),table in tables.items()}))
    print(json.dumps(result,indent=2),flush=True)


if __name__ == '__main__':
    main()
