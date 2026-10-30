"""Small invariants for the scientific experiment, separate from calibration."""
import collections
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import experiment as e


class EncodingTests(unittest.TestCase):
    def setUp(self):
        self.lines = [dict(physical_leaf='f1', words=['ab', 'c', None, 'defg']),
                      dict(physical_leaf='f2', words=['hi', 'jkl'])]

    def test_positions_and_breaks(self):
        self.assertEqual(e.encode(self.lines, 'initial'), [[26, 1, 52, 28], [29, 4, 5, 6], [33, 8, 52, 35, 10, 11]])
        self.assertEqual(e.encode(self.lines, 'final'), [[0, 27, 52, 28], [3, 4, 5, 32], [7, 34, 52, 9, 10, 37]])
        self.assertEqual(e.encode(self.lines, 'single'), [[0, 1, 26, 2], [3, 4, 5, 6], [7, 8, 26, 9, 10, 11]])

    def test_encryption_round_trip_both_families(self):
        for family in ['initial', 'final']:
            encrypted, tables = e.encrypt(self.lines, family, 17)
            keys = [''.join(e.ALPHABET[t.index(c)] for c in e.ALPHABET) for t in tables]
            key = ''.join(keys)+' '
            decoded = [''.join(key[i] for i in seq) for seq in e.encode(encrypted, family)]
            self.assertEqual(decoded, ['ab c', 'defg', 'hi jkl'])

    def test_null_keeps_structure_and_position_totals(self):
        lines = [dict(physical_leaf=f'f{i//2}', words=['abcd', 'efghi', 'j', None, 'klmn', 'opq']) for i in range(6)]
        def histogram(rows):
            result = collections.Counter()
            for r in rows:
                for w in r['words']:
                    if w:
                        for i, c in enumerate(w):
                            result[(r['physical_leaf'], e.role(w, i), c)] += 1
            return result
        mixed = e.shuffle_letters(lines, 31)
        self.assertEqual(histogram(lines), histogram(mixed))
        self.assertNotEqual(lines, mixed)
        self.assertEqual(mixed, e.shuffle_letters(lines, 31))
        self.assertEqual([[None if w is None else len(w) for w in r['words']] for r in lines],
                         [[None if w is None else len(w) for w in r['words']] for r in mixed])
        self.assertEqual(lines[0]['words'][0], 'abcd')

    def test_short_spans_never_bridge_unknowns_or_lines(self):
        self.assertEqual(e.encode([dict(words=['a', None, 'b']), dict(words=['cd'])], 'initial'), [])
        with self.assertRaises(ValueError):
            e.encode([dict(words=['ab?c'])], 'initial')

    def test_absent_alphabet_slots_are_retained(self):
        with tempfile.TemporaryDirectory() as folder:
            inp = Path(folder)/'input.txt'
            inp.write_text('0 1 2 3\n')  # No spaces and no position-table slots observed.
            cmd = [str(e.TMP/'position_permutation'), str(e.TMP/'latin_lm.bin'),
                   str(e.TMP/'latin_freq.txt'), str(inp), '1', '10', '17', '4', '.002', '52']
            result = json.loads(subprocess.check_output(cmd, text=True))
            self.assertEqual(len(result['key']), 53)
            self.assertEqual(sorted(result['key'][:26]), list(e.ALPHABET))
            self.assertEqual(sorted(result['key'][26:52]), list(e.ALPHABET))
            self.assertEqual(result['key'][52], '{')


if __name__ == '__main__':
    unittest.main()
