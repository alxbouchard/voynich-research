import collections
import copy
import unittest

import generators as g


def histogram(lines):
    c = collections.Counter()
    for ri, wi in g.active_slots(lines):
        row = lines[ri]
        word = row['words'][wi]
        for i, ch in enumerate(word):
            c[row['physical_leaf'], g.role(len(word), i), ch] += 1
    return c


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.rows = [dict(physical_leaf='f1', words=['ab', None, 'c', None, 'abcd', 'efghi', 'j']),
                     dict(physical_leaf='f1', words=['klmn', 'opq', None, 'xy']),
                     dict(physical_leaf='f2', words=['abcde', 'fgh', 'i'])]

    def test_retention_at_barriers(self):
        self.assertEqual(g.active_slots(self.rows), {(0,4), (0,5), (0,6), (1,0), (1,1), (2,0), (2,1), (2,2)})
        self.assertEqual(g.active_slots([dict(words=['a','b']), dict(words=['a','bc'])]), {(1,0),(1,1)})

    def test_shuffle_preserves_scored_marginals_and_excluded_words(self):
        result = g.shuffle_retained(self.rows, 73)
        self.assertNotEqual(result, self.rows)
        self.assertEqual(histogram(result), histogram(self.rows))
        active = g.active_slots(self.rows)
        for ri, (before, after) in enumerate(zip(self.rows, result)):
            for wi, (a, b) in enumerate(zip(before['words'], after['words'])):
                self.assertEqual(None if a is None else len(a), None if b is None else len(b))
                if (ri, wi) not in active:
                    self.assertEqual(a, b)
        self.assertEqual(result, g.shuffle_retained(self.rows, 73))

    def test_training_ignores_excluded_words(self):
        changed = copy.deepcopy(self.rows)
        changed[0]['words'][0] = 'zz'
        changed[0]['words'][2] = 'z'
        changed[1]['words'][-1] = 'zz'
        self.assertEqual(g.train_markov(self.rows), g.train_markov(changed))

    def test_generator_uses_layout_not_heldout_letters(self):
        model = g.train_markov(self.rows)
        layout = copy.deepcopy(self.rows)
        for row in layout:
            row['words'] = ['z'*len(w) if w is not None else None for w in row['words']]
        a, b = g.generate(self.rows, model, 89), g.generate(layout, model, 89)
        self.assertEqual(a, b)
        self.assertNotEqual(a, self.rows)
        self.assertEqual(g.active_slots(a), g.active_slots(self.rows))
        self.assertNotEqual(a, g.generate(layout, model, 90))

    def test_markov_counts_are_exact_and_do_not_cross_words(self):
        model = g.train_markov([dict(words=['abca', 'bca', 'a'])])
        counts = {(r['role'], r['context']): r['letters'] for r in model['counts']}
        self.assertEqual(counts['final','bc'], {'a': 2})
        self.assertEqual(counts['final','c'], {'a': 2})
        self.assertEqual(counts['singleton',''], {'a': 1})
        self.assertNotIn(('initial','a'), counts)
        self.assertEqual(sum(model['global_counts'].values()), 8)

    def test_no_mutation_of_training_or_model(self):
        original = copy.deepcopy(self.rows)
        model = g.train_markov(self.rows)
        frozen = copy.deepcopy(model)
        g.generate(self.rows, model, 3)
        g.shuffle_retained(self.rows, 3)
        self.assertEqual(model, frozen)
        self.assertEqual(self.rows, original)


if __name__ == '__main__':
    unittest.main()
