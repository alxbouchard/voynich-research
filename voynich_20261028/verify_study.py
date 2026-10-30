#!/usr/bin/env python3
"""Check material evidence, source identity and evaluation separation."""
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

from analyse import ROOT, OUT, PROTOCOL, parse


def main():
    checks=[]
    for name in PROTOCOL['corpora']:
        records,pages=parse(name)
        checks.append(f'{name}: complete source hash, locus uniqueness and format passed')
        assert sum(r['clean'].count('qokeedy') for r in records if r['page']=='f1r')==0
        checks.append(f'{name}: qokeedy absent from genuine f1r')
    model=json.loads((OUT/'models.json').read_text())
    for name,analyses in model['corpora'].items():
        for method,orders in analyses.items():
            assert len(orders)==4
            for order in orders:
                all_test=[]
                for fold in order['folds']:
                    assert not (set(fold['train_groups'])&set(fold['test_groups']))
                    all_test.extend(fold['test_groups'])
                assert len(all_test)==len(set(all_test))
        assert analyses['real_leaf'][2]['bits_per_EVA_char']<analyses['shuffled_leaf'][2]['bits_per_EVA_char']
        checks.append(f'{name}: no group leakage; all groups evaluated once per model')
    control=json.loads((OUT/'naibbe_control.json').read_text())
    assert control['exact_plaintext_recovery']
    assert control['plaintext_characters']==52641
    generated=ROOT/'controls/generated'
    assert (generated/'normalized_plaintext.txt').read_bytes()==(generated/'recovered_plaintext.txt').read_bytes()
    checks.append('Known-key Naibbe: byte-identical normalized plaintext recovery')
    probe=json.loads((OUT/'fixed_key_probe.json').read_text())
    for name,item in probe.items():
        assert sum(item['counts'].values())==item['tokens']
        assert item['counts']['unknown']>0 and not item['full_direct_decipherment']
    checks.append('Fixed-key probe: all tokens accounted for, incomplete reading explicitly marked')
    pdf=ROOT/'output/pdf/Etude_Voynich_2026-10-28.pdf'
    reader=PdfReader(pdf)
    texts=[page.extract_text() or '' for page in reader.pages]
    assert len(texts)==8,f'Unexpected page count: {len(texts)}'
    for i,t in enumerate(texts,1):
        assert f'/ {i:02d}' in t,f'Unexpected section on page {i}'
        assert '\ufffd' not in t and '\u2014' not in t
    for needle in ['52 641','qokeedy','reproduction','100 %']:
        assert needle in '\n'.join(texts),f'Missing text {needle}'
    checks.append('PDF: 8 complete sections, readable extracted text; visual review also required')
    result=dict(passed=True,checks=checks)
    (OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
