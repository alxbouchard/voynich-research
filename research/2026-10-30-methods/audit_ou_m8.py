#!/usr/bin/env python3
"""Recount archived outputs; does not train or rerun any external generator."""
import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = 'f3c79b12eecfec87bfa9373f083ed5067c9c995cce8e456871863deb2e1e7019'
SOURCE = ('https://github.com/yangou2012/voynich_stt/blob/'
          '6d061eb959b1053b35d12a689aa764a8d22930f4/results/stt_battery_results.json')


def audit(raw):
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError('Source changed: use the pinned input, not a newer version.')
    results = json.loads(raw)
    rows = []
    for name, result in results.items():
        metrics = result['metrics']
        count = sum(m['pass'] for m in metrics.values())
        assert len(metrics) == 8 and count == result['n_metrics_passed']
        delta = metrics['M8']['delta_acc_mean']
        one_sided = delta < 0.05
        assert one_sided == metrics['M8']['pass']
        bilateral = abs(delta) < 0.05
        rows.append({
            'model': name, 'archived_runs': result['n_runs'],
            'archived_criteria_passed': count,
            'baseline_accuracy': metrics['M8']['voynich_acc'],
            'synthetic_accuracy_mean': metrics['M8']['voynich_acc'] - delta,
            'baseline_minus_synthetic_mean': delta,
            'archived_m8_pass': one_sided,
            'm8_bilateral_on_archived_mean': bilateral,
            'criteria_if_only_m8_changed': count - int(one_sided) + int(bilateral),
        })
    return {
        'date': '2026-10-30', 'source_url': SOURCE, 'sha256': digest,
        'scope': 'Arithmetic check on archived means. No generator or classifier rerun; other seven flags kept as reported. Not the per-run majority rule of the paper.',
        'discovery': 'Lead from https://beyond-any-doubt.org/posts/voynich-harness/; checked against primary code, results and preprint section 3.2.0.8.',
        'models_checked': len(rows),
        'm8_flags_changed': sum(r['archived_m8_pass'] != r['m8_bilateral_on_archived_mean'] for r in rows),
        'rows': rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.input.read_bytes())
    text = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
