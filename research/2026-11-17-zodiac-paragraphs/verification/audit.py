"""Independent, stdlib-only upper bound for literal whole-label prefix reuse.

No model or prior analysis output is imported. First-token compatibility is
necessary, not sufficient, for a whole zodiac label to begin a stars paragraph.
"""
from collections import Counter
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DEFAULT_SOURCES = ROOT.parents[2] / 'voynich_phase46' / 'sources'


def first_regex(body, commas):
    body = re.sub(r'<![^>]*>', '', body)
    body = body.replace('<%>', '').replace('<$>', '').strip()
    body = body.replace(',', '.' if commas == 'split' else '')
    token = body.split('.')[0]
    return token, token if re.fullmatch('[a-z]+', token) else None


def parse_regex(text, commas):
    metadata = None
    current_page = None
    rows = {'labels': [], 'starts': []}
    exclusions = []
    for line_number, line in enumerate(text.splitlines(), 1):
        header = re.match(r'^<(f\d+[rv]\d*)>\s*(.*)$', line)
        if header:
            current_page = header[1]
            metadata = dict(re.findall(r'\$([A-Z])=([^\s>]+)', header[2]))
            continue
        locus = re.match(r'^<(f\d+[rv]\d*\.\d+),([^>]+)>\s*(.*)$', line)
        if not locus:
            continue
        assert locus[1].split('.')[0] == current_page
        code = locus[2]
        assert len(code) == 3, code
        cleaned = re.sub(r'<![^>]*>', '', locus[3]).strip()
        group = None
        if metadata.get('I') == 'Z' and code[1:] == 'Lz':
            group = 'labels'
        if (metadata.get('Q') == 'T' and metadata.get('I') == 'S'
                and code[1:] == 'P0' and cleaned.startswith('<%>')):
            group = 'starts'
        if group is None:
            continue
        if code[0] == '!':
            exclusions.append({'line': line_number, 'locus': locus[1], 'group': group})
            continue
        raw_token, token = first_regex(locus[3], commas)
        rows[group].append({'locus': locus[1], 'line': line_number,
                            'raw_first_token': raw_token, 'certain_token': token})
    return rows, exclusions


def without_comments(body):
    """Separate character-scanning implementation, no regular expressions."""
    out = []
    i = 0
    while i < len(body):
        if body[i:i+2] == '<!':
            close = body.find('>', i + 2)
            assert close >= 0, 'Unterminated editorial comment'
            i = close + 1
        else:
            out.append(body[i])
            i += 1
    return ''.join(out)


def first_scanner(body, commas):
    clean = without_comments(body)
    out = []
    i = 0
    while i < len(clean):
        if clean[i:i+3] in ('<%>', '<$>'):
            i += 3
        else:
            out.append(clean[i])
            i += 1
    clean = ''.join(out).strip()
    first = []
    for char in clean:
        if char == '.' or (char == ',' and commas == 'split'):
            break
        if char != ',':
            first.append(char)
    token = ''.join(first)
    return token, token if token and all('a' <= c <= 'z' for c in token) else None


def parse_scanner(text, commas):
    # First pass: metadata indexed by the page explicitly named in each locus.
    pages = {}
    for line in text.splitlines():
        if not line.startswith('<'):
            continue
        stop = line.find('>')
        assert stop > 0
        identifier = line[1:stop]
        if ',' in identifier or '.' in identifier:
            continue
        fields = {}
        for bit in line[stop+1:].replace('>', ' ').split():
            if bit.startswith('$') and '=' in bit:
                key, value = bit[1:].split('=', 1)
                fields[key] = value
        assert identifier not in pages
        pages[identifier] = fields
    rows = {'labels': [], 'starts': []}
    exclusions = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.startswith('<'):
            continue
        stop = line.find('>')
        identifier = line[1:stop]
        if ',' not in identifier:
            continue
        locus, code = identifier.split(',')
        page, index = locus.rsplit('.', 1)
        assert index.isdecimal() and len(code) == 3
        fields = pages[page]
        body = line[stop+1:].strip()
        group = None
        if fields.get('I') == 'Z' and code[1:] == 'Lz':
            group = 'labels'
        if (fields.get('Q') == 'T' and fields.get('I') == 'S'
                and code[1:] == 'P0' and without_comments(body).strip().startswith('<%>')):
            group = 'starts'
        if group is None:
            continue
        if code[0] == '!':
            exclusions.append({'line': line_number, 'locus': locus, 'group': group})
            continue
        raw_token, token = first_scanner(body, commas)
        rows[group].append({'locus': locus, 'line': line_number,
                            'raw_first_token': raw_token, 'certain_token': token})
    return rows, exclusions


def count_bound(left, right):
    lc = Counter(x for x in left if x is not None)
    rc = Counter(x for x in right if x is not None)
    common = {x: min(lc[x], rc[x]) for x in sorted(lc.keys() & rc.keys())}
    uleft, uright = left.count(None), right.count(None)
    bound = min(len(left), len(right), sum(common.values()) + uleft + uright)
    return bound, common, uleft, uright


def matching(left, right):
    """Maximum bipartite matching via augmenting paths on occurrence vertices."""
    adjacency = [[j for j, b in enumerate(right) if a is None or b is None or a == b]
                 for a in left]
    owner = [-1] * len(right)
    def augment(i, seen):
        for j in adjacency[i]:
            if j in seen:
                continue
            seen.add(j)
            if owner[j] == -1 or augment(owner[j], seen):
                owner[j] = i
                return True
        return False
    for i in range(len(left)):
        augment(i, set())
    pairs = sorted((i, j) for j, i in enumerate(owner) if i != -1)
    assert len({i for i, j in pairs}) == len(pairs)
    assert all(left[i] is None or right[j] is None or left[i] == right[j] for i, j in pairs)
    return pairs


def tests():
    examples = [
        (' <!clock> <%>abc,def.ghi<$> ', 'join', 'abcdef', 'abcdef'),
        (' <!clock> <%>abc,def.ghi<$> ', 'split', 'abc', 'abc'),
        ('<%>a<!note>b.c', 'join', 'ab', 'ab'),
        ('<%>a[b:c].d', 'join', 'a[b:c]', None),
        ('<%>a<->b.c', 'join', 'a<->b', None),
        ('<%>?.abc', 'split', '?', None),
        ('<%>.abc', 'join', '', None),
        ('<%>abc def.ghi', 'join', 'abc def', None),
    ]
    for body, mode, raw, token in examples:
        assert first_regex(body, mode) == first_scanner(body, mode) == (raw, token)
    toy = ('<f1r> <! $I=Z>\n<f1r.1,@Lz>abc\n<f1r.2,!Lz>def\n'
           '<f2r> <! $Q=T $I=S>\n<f2r.1,@P0><!note><%>abc.def\n'
           '<f2r.2,+P0>def<%>ghi\n<f2r.3,!P0><%>abc\n')
    for mode in ('join', 'split'):
        a, excluded = parse_regex(toy, mode)
        assert (a, excluded) == parse_scanner(toy, mode)
        assert len(a['labels']) == len(a['starts']) == 1 and len(excluded) == 2
    arrays = [list(x) for n in range(4) for x in itertools.product(('a', 'b', None), repeat=n)]
    cases = 0
    for left in arrays:
        for right in arrays:
            assert count_bound(left, right)[0] == len(matching(left, right)), (left, right)
            cases += 1
    return {'first_token_cases': len(examples), 'parser_fixture_modes': 2,
            'exhaustive_count_formula_vs_matching_cases': cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, default=DEFAULT_SOURCES,
                        help='Directory containing ZL.txt and IT.txt (default: repository phase46 sources).')
    source_directory = parser.parse_args().sources.resolve()
    result = {
        'scope': 'Maximum possible injective whole-label-to-paragraph-start literal prefix copies, bounded by first-token compatibility only.',
        'no_prior_result_read': True,
        'sources': {}, 'checks': tests(), 'cases': [],
        'formula': 'min(n_labels,n_starts,sum_token min(c_labels,c_starts)+uncertain_labels+uncertain_starts)',
        'rules': {
            'labels': 'Real Lz loci on pages with I=Z',
            'starts': 'Real P0 loci beginning with <%> after removal of <! comments, on pages Q=T and I=S',
            'real': 'Locator ! excluded',
            'first_token': 'Remove <!…>, <%>, <$>; strip exterior whitespace; comma join/split; first dot-delimited piece; certainty requires nonempty ASCII [a-z]+',
            'uncertainty': 'Any other first token, including empty, is an unrestricted wildcard',
            'unit': 'Each label and paragraph-start occurrence is a distinct vertex, with multiplicity preserved'
        },
        'limitations': [
            'An accepted first-token edge does not establish equality of the whole label or a historical relation.',
            'No order, semantic, phonetic, morphological, synonym or spelling-variant equivalence is assumed.',
            'The bound addresses literal copies beginning at the first token in these selected extant transcription loci only.',
            'Both transcriptions describe the same manuscript and are sensitivity configurations, not independent replications.',
            'The editorial frequency observation uses RF1b with paragraph markers adopted from ZL, so its reported totals are not silently substituted for ZL/IT totals here.'
        ]
    }
    for corpus in ('ZL', 'IT'):
        source = source_directory / (corpus + '.txt')
        raw = source.read_bytes()
        result['sources'][corpus] = {'path': os.path.relpath(source, ROOT), 'sha256': hashlib.sha256(raw).hexdigest()}
        text = raw.decode('utf-8')
        for mode in ('join', 'split'):
            rows, excluded = parse_regex(text, mode)
            independent_rows, independent_excluded = parse_scanner(text, mode)
            assert rows == independent_rows and excluded == independent_excluded
            for group in rows.values():
                assert len({r['locus'] for r in group}) == len(group)
            left = [r['certain_token'] for r in rows['labels']]
            right = [r['certain_token'] for r in rows['starts']]
            upper, certain_common, ul, us = count_bound(left, right)
            # Matching uses the independently extracted rows, never counts.
            pairs = matching([r['certain_token'] for r in independent_rows['labels']],
                             [r['certain_token'] for r in independent_rows['starts']])
            assert len(pairs) == upper
            case = {'corpus': corpus, 'commas': mode,
                    'n_labels': len(left), 'n_starts': len(right),
                    'uncertain_labels': ul, 'uncertain_starts': us,
                    'certain_intersection_capacity': sum(certain_common.values()),
                    'certain_intersection_by_token': certain_common,
                    'upper_bound': upper, 'bipartite_matching_size': len(pairs),
                    'maximum_fraction_of_labels': upper / len(left),
                    'maximum_fraction_of_starts': upper / len(right),
                    'at_least_labels_without_injective_literal_prefix_copy': len(left) - upper,
                    'at_least_starts_without_injective_literal_prefix_copy': len(right) - upper,
                    'excluded_nonexistent_loci': excluded,
                    'parsed_records': rows,
                    'first_token_matching_witness_not_whole_label_matches': [
                        {'label': rows['labels'][i]['locus'], 'start': rows['starts'][j]['locus'],
                         'label_first': left[i], 'start_first': right[j]}
                        for i, j in pairs]}
            result['cases'].append(case)
    result['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['status'] = 'VERIFIED_FIRST_TOKEN_UPPER_BOUND_NOT_TRANSLATION'
    (ROOT / 'AUDIT.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'status': result['status'], 'checks': result['checks'], 'cases': [
        {k: v for k, v in c.items() if k not in ('parsed_records', 'first_token_matching_witness_not_whole_label_matches')}
        for c in result['cases']]}, indent=2))


if __name__ == '__main__':
    main()
