#!/usr/bin/env python3
"""Known-key positive control. Does NOT decode the Voynich manuscript.

Uses Michael A. Greshko's published implementation and published cipher tables.
See controls/LICENSE_GRESHKO and DOI 10.1080/01611194.2025.2566408.
"""
import collections
import importlib.util
import json
import os
import random
import sys

from analyse import ROOT, SEED, conditional_entropy, write_json


def main():
    os.chdir(ROOT/'controls')
    sys.path.insert(0,str(ROOT/'controls'))
    import naibbe_cv_vc_reuse as cipher
    import decrypt_naibbe as decoder
    random.seed(SEED)
    # Fixed example and default respacing ratio. Disable optional recent reuse
    # mechanisms, retain unambiguous coding. No parameter fitted to Voynich.
    cipher.RESPACING_MODE='random'
    cipher.ENABLE_SHORT_RANGE_REUSE=False
    cipher.ENABLE_LONG_RANGE_REUSE=False
    cipher.UNAMBIGUOUS=True
    plaintext=(ROOT/'controls/input/nathist_book16.txt').read_text()
    clean_lines=[cipher.clean_line(line) for line in plaintext.splitlines() if cipher.clean_line(line)]
    u,p,s,w=decoder.build_reverse_mappings(cipher.glyph_df)
    ciphertext=[]; decoded=[]; failures=[]
    for index,line in enumerate(clean_lines):
        toks=cipher.encrypt_naibbe(line,cipher.naibbe_tables,cipher.placeholder_to_glyph,use_78=False)
        reads=[decoder.decrypt_naibbe_token(t,u,p,s,w,basic=True,compound=False) for t in toks]
        recovered=''.join(reads)
        target=line.replace(' ','')
        if recovered!=target:
            failures.append(dict(line=index,expected_chars=len(target),recovered_chars=len(recovered),ambiguous_tokens=sum('|' in r or '?' in r for r in reads)))
        ciphertext.append(' '.join(toks));decoded.append(recovered)
    out=ROOT/'controls/generated';out.mkdir(exist_ok=True)
    (out/'naibbe_ciphertext.txt').write_text('\n'.join(ciphertext)+'\n')
    (out/'normalized_plaintext.txt').write_text('\n'.join(l.replace(' ','') for l in clean_lines)+'\n')
    (out/'recovered_plaintext.txt').write_text('\n'.join(decoded)+'\n')
    tokens=' '.join(ciphertext).split()
    # Preserve the original Latin word boundaries for the plain-language
    # comparison. clean_line deliberately removes all spacing for encryption.
    latin_words=[cipher.clean_line(w) for w in plaintext.split() if cipher.clean_line(w)]
    result=dict(seed=SEED,source='Pliny, Naturalis Historia book 16, supplied in the Greshko repository',
                settings=dict(respacing_mode='random',respacing=cipher.RESPACING,use_78=False,unambiguous=True,short_range_reuse=False,long_range_reuse=False),
                lines=len(clean_lines),plaintext_characters=sum(len(l.replace(' ','')) for l in clean_lines),
                ciphertext_tokens=len(tokens),ciphertext_EVA_characters=sum(map(len,tokens)),
                fully_recovered_lines=len(clean_lines)-len(failures),failures=failures,
                exact_plaintext_recovery=not failures,
                unambiguous_retry_count=cipher.ambiguity_retries,
                H_within_word_cipher=[conditional_entropy(tokens,o) for o in range(4)],
                H_within_word_latin=[conditional_entropy(latin_words,o) for o in range(4)],
                semantic_Grok_tags='The fixed alchemical map would output ritual tags here as well, despite the known Latin plaintext.',
                limitation='Known tables and original ciphertext spaces are provided. This demonstrates compatibility, not key recovery, historical authenticity or an actual decipherment.')
    write_json('naibbe_control.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
