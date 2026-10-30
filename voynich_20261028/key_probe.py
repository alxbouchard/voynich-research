#!/usr/bin/env python3
"""Exploratory use of an existing fixed cipher key, with no fitting to Voynich."""
import collections
import os
import sys
from analyse import ROOT, PROTOCOL, parse, write_json


def main():
    os.chdir(ROOT/'controls')
    sys.path.insert(0,str(ROOT/'controls'))
    import pandas as pd
    import decrypt_naibbe as decoder
    u,p,s,w=decoder.build_reverse_mappings(pd.read_csv('references/naibbe_tables.csv'))
    result={}
    for name in PROTOCOL['corpora']:
        recs,_=parse(name)
        tokens=[tok for r in recs if r['type']!='Lx' and r['locator']!='!' for tok in r['clean']]
        readings={tok:decoder.decrypt_naibbe_token(tok,u,p,s,w,basic=True,compound=False) for tok in set(tokens)}
        counts=collections.Counter()
        for tok in tokens:
            r=readings[tok]
            counts['unknown' if '?' in r else 'ambiguous' if '|' in r else 'unique']+=1
        result[name]=dict(tokens=len(tokens),counts=dict(counts),unique_percent=100*counts['unique']/len(tokens),
                          unknown_examples=sorted((t for t,r in readings.items() if '?' in r),key=lambda t:(len(t),t))[:20],
                          full_direct_decipherment=False,
                          limitation='No key search. Fails only this unchanged published key with the original token boundaries, not the general verbose-cipher hypothesis.')
    write_json('fixed_key_probe.json',result)
    print(result)


if __name__=='__main__':main()
