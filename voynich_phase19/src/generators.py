"""Structured random strings and retained-span conditional permutations.

No plaintext input, lexicon lookup, cipher or held-out symbol fitting.
The Markov model intentionally inherits local statistics from training words.
It is a diagnostic surrogate, not a proposed historical generator.
"""
import collections
import copy
import random


def active_slots(lines):
    """Known word slots participating in a span of at least four characters."""
    active = set()
    for ri, row in enumerate(lines):
        run = []
        for wi in range(len(row['words'])+1):
            word = row['words'][wi] if wi < len(row['words']) else None
            if word is None:
                if sum(len(row['words'][j]) for j in run) + max(0, len(run)-1) >= 4:
                    active.update((ri, j) for j in run)
                run = []
            else:
                run.append(wi)
    return active


def role(length, index):
    if length == 1:
        return 'singleton'
    if index == 0:
        return 'initial'
    if index == length-1:
        return 'final'
    return 'interior'


def shuffle_retained(lines, seed):
    """Shuffle only scored slots within (leaf, role); excluded words are fixed."""
    rng = random.Random(seed)
    active = active_slots(lines)
    result = copy.deepcopy(lines)
    positions = collections.defaultdict(list)
    for ri, row in enumerate(result):
        row['words'] = [list(w) if w is not None else None for w in row['words']]
        for wi, word in enumerate(row['words']):
            if (ri, wi) in active:
                for ci in range(len(word)):
                    positions[(row['physical_leaf'], role(len(word), ci))].append((ri, wi, ci))
    for group in sorted(positions):
        locations = positions[group]
        values = [result[r]['words'][w][c] for r, w, c in locations]
        rng.shuffle(values)
        for (r, w, c), value in zip(locations, values):
            result[r]['words'][w][c] = value
    for row in result:
        row['words'] = [''.join(w) if w is not None else None for w in row['words']]
    return result


def train_markov(lines, order=2, alpha=1.0):
    """Count within-word contexts in retained TRAINING words only.

    Recursively smoothed by the next shorter context, with pseudocount alpha.
    At order zero the role distribution is empirical (global fallback if a
    role is entirely absent). Word lengths are supplied by an external layout.
    """
    counts = collections.defaultdict(collections.Counter)
    global_counts = collections.Counter()
    for ri, wi in sorted(active_slots(lines)):
        word = lines[ri]['words'][wi]
        for i, ch in enumerate(word):
            r = role(len(word), i)
            global_counts[ch] += 1
            for k in range(min(order, i)+1):
                context = word[i-k:i] if k else ''
                counts[(r, context)][ch] += 1
    return {'order': order, 'alpha': alpha, 'alphabet': sorted(global_counts),
            'global_counts': dict(sorted(global_counts.items())),
            'counts': [{'role': r, 'context': ctx, 'letters': dict(sorted(c.items()))}
                       for (r, ctx), c in sorted(counts.items())]}


def generate(layout, model, seed):
    """Uses only lengths/barriers/metadata from layout, never its letters."""
    rng = random.Random(seed)
    alphabet = model['alphabet']
    counts = {(r['role'], r['context']): r['letters'] for r in model['counts']}
    cache = {}
    def probabilities(r, context):
        index = (r, context)
        if index in cache:
            return cache[index]
        c = counts.get(index, {})
        n = sum(c.values())
        if not context:
            if not n:
                c = model['global_counts']
                n = sum(c.values())
            probabilities_ = [c.get(ch, 0)/n for ch in alphabet]
        else:
            lower = probabilities(r, context[1:])
            alpha = model['alpha']
            probabilities_ = [(c.get(ch, 0)+alpha*b)/(n+alpha) for ch, b in zip(alphabet, lower)]
        cache[index] = probabilities_
        return probabilities_
    result = copy.deepcopy(layout)
    for row in result:
        output = []
        for original in row['words']:
            if original is None:
                output.append(None)
                continue
            length = len(original)
            word = ''
            for i in range(length):
                context = word[-model['order']:] if model['order'] else ''
                weights = probabilities(role(length, i), context)
                word += rng.choices(alphabet, weights=weights, k=1)[0]
            output.append(word)
        row['words'] = output
    return result
