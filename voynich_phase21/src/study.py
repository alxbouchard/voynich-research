#!/usr/bin/env python3
"""Phase-21 fresh unknown-key controls with a locally frozen protocol. CC BY-SA 4.0."""
import argparse
import bisect
import json
import random
import subprocess
import time
from pathlib import Path
import common as c

PFILE=c.ROOT/'PROTOCOL.json'
CLOSED_EXE=c.TMP/'closed_solver'


def protocol():
    p=c.read(PFILE)
    for path,digest in p['sha256'].items():assert c.sha(c.REPO/path)==digest, f'Changed input: {path}'
    return p


def prepare():
    p=protocol();c.compile_solver()
    subprocess.run(['c++','-O3','-std=c++17',str(c.OLD/'src/joint_solver.cpp'),'-o',str(CLOSED_EXE)],check=True)
    models=[c.build_model(lang) for lang in p['languages']]
    c.save(c.DATA/'models.json',models)
    source={x['case']:x for x in c.read(c.REPO/'voynich_phase10/data/source_inputs.json')}
    old_by_language={lang:[] for lang in p['languages']};old_keys=set()
    for old in c.read(c.OLD/'data/calibration/cases.json'):
        truth=c.read(c.OLD/'data/calibration'/old['case']/'truth.json')
        old_by_language[old['language']].extend(truth['source_word_ranges'].values());old_keys.add(truth['encryption_key'])
    cases=[];new_keys=set()
    for li,(language,name) in enumerate(p['languages'].items()):
        words=[w for line in source[name]['lines'] for w in line['words'] if w]
        assert all(set(w)<=set(c.ALPHABET) for w in words)
        prefixes=[0]
        for w in words:prefixes.append(prefixes[-1]+len(w))
        binsize=len(words)//6
        for trial,length in enumerate(p['fit_letters']*2):
            eligible=[]
            for start in range(trial*binsize,(trial+1)*binsize):
                fit_end=bisect.bisect_left(prefixes,prefixes[start]+length)
                test_start=fit_end+p['gap_words']
                if test_start>=len(words):continue
                end=bisect.bisect_left(prefixes,prefixes[test_start]+p['transfer_letters'])
                if end>(trial+1)*binsize:continue
                buffer=p['old_passage_buffer_words']
                if any(start<b+buffer and end>a-buffer for a,b in old_by_language[language]):continue
                eligible.append((start,fit_end,test_start,end))
            assert eligible,'No disjoint passage; do not weaken exclusion.'
            selected=random.Random(p['selection_seed']+100*li+trial).choice(eligible)
            start,fit_end,test_start,end=selected
            plain_fit=' '.join(words[start:fit_end]);plain_test=' '.join(words[test_start:end])
            key=list(c.ALPHABET);random.Random(p['encryption_seed']+100*li+trial).shuffle(key);key=''.join(key)
            assert key not in old_keys|new_keys;new_keys.add(key)
            name=f'{language}_{length}_{trial//3+1}';folder=c.DATA/'controls'/name;folder.mkdir(parents=True,exist_ok=True)
            table=str.maketrans(c.ALPHABET,key)
            (folder/'fit.txt').write_text(plain_fit.replace(' ','').translate(table)+'\n')
            (folder/'transfer.txt').write_text(plain_test.replace(' ','').translate(table)+'\n')
            c.save(folder/'truth.json',{'plaintext_fit':plain_fit,'plaintext_transfer':plain_test,
                   'encryption_key':key,'source':p['languages'][language],
                   'source_word_ranges':{'fit':[start,fit_end],'transfer':[test_start,end]},
                   'evaluation_only':True,'never_passed_to_key_search':True})
            cases.append({'case':name,'language':language,'fit_letters':len(plain_fit.replace(' ','')),
                          'transfer_letters':len(plain_test.replace(' ','')),
                          'eligible_start_count':len(eligible),
                          'sha256':{f.name:c.sha(f) for f in folder.iterdir()}})
    c.save(c.DATA/'cases.json',cases)
    c.save(c.DATA/'environment.json',{'run_base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.REPO,text=True).strip(),
        'protocol_sha256':c.sha(PFILE),'open_solver_sha256':c.sha(c.EXE),'closed_solver_sha256':c.sha(CLOSED_EXE),
        'compiler':subprocess.check_output(['c++','--version'],text=True),'python':subprocess.check_output(['python3','--version'],text=True).strip(),'numpy':c.np.__version__})
    print(json.dumps({'prepared':len(cases),'new_keys':len(new_keys)}),flush=True)


def check_inputs():
    p=protocol();env=c.read(c.DATA/'environment.json')
    assert c.sha(c.EXE)==env['open_solver_sha256'] and c.sha(CLOSED_EXE)==env['closed_solver_sha256']
    for model in c.read(c.DATA/'models.json'):
        for kind,files in (('open',model['open_files']),('closed',model['closed']['files'])):
            for name,digest in files.items():assert c.sha(c.TMP/kind/model['language']/name)==digest
    for case in c.read(c.DATA/'cases.json'):
        for name,digest in case['sha256'].items():assert c.sha(c.DATA/'controls'/case['case']/name)==digest
    return p


def run(command,output):
    identity={'command':list(map(str,command)),'protocol_sha256':c.sha(PFILE),
              'executable_sha256':c.sha(command[0]),'models_sha256':c.sha(c.DATA/'models.json'),
              'argument_files':{str(v):c.sha(v) for v in command[1:] if isinstance(v,Path) and v.is_file()}}
    if output.exists():
        old=c.read(output);assert old['identity']==identity,'Stale result'
        return old['result']
    start=time.monotonic()
    process=subprocess.run(list(map(str,command)),capture_output=True,text=True,check=True)
    if process.stderr:raise RuntimeError(process.stderr)
    result=json.loads(process.stdout)
    c.save(output,{'identity':identity,'seconds':time.monotonic()-start,'result':result})
    return result


def fit():
    p=check_inputs()
    for i,case in enumerate(c.read(c.DATA/'cases.json')):
        name=case['case'];lang=case['language'];folder=c.OUT/'controls'/name;folder.mkdir(parents=True,exist_ok=True)
        cipher=c.DATA/'controls'/name/'fit.txt'
        print(json.dumps({'case':name,'stage':'initializer'}),flush=True)
        initial=run([CLOSED_EXE,c.TMP/'closed'/lang,'init',cipher,p['optimizer_seed']+i,p['restarts'],p['steps']],folder/'initializer.json')
        observed=sorted(set(cipher.read_text().strip()));signatures=set();keys=[]
        for row in initial['restarts']:
            signature=''.join(row['key'][ord(ch)-97] for ch in observed)
            if signature not in signatures:keys.append(row['key']);signatures.add(signature)
            if len(keys)==p['refinement_starts']:break
        keyfile=c.TMP/(name+'_starts.txt');keyfile.write_text('\n'.join(keys)+'\n')
        for mode in ('closed','open'):
            print(json.dumps({'case':name,'stage':mode,'starts':len(keys)}),flush=True)
            if mode=='closed':command=[CLOSED_EXE,c.TMP/'closed'/lang,'exact',cipher,keyfile,p['refinement_passes']]
            else:command=[c.EXE,c.TMP/'open'/lang,'refine',cipher,keyfile,p['beta'],p['penalty'],p['refinement_passes']]
            result=run(command,folder/(mode+'.json'))
            print(json.dumps({'case':name,'finished':mode,'evaluations':result['evaluations']}),flush=True)


def evaluate():
    p=check_inputs();cases=c.read(c.DATA/'cases.json')
    for case in cases:
        for mode in ('closed','open'):assert (c.OUT/'controls'/case['case']/(mode+'.json')).exists()
    rows=[]
    for case in cases:
        name=case['case'];lang=case['language'];folder=c.OUT/'controls'/name
        truth=c.read(c.DATA/'controls'/name/'truth.json')
        inverse=''.join(c.ALPHABET[truth['encryption_key'].index(ch)] for ch in c.ALPHABET)
        initial=c.read(folder/'initializer.json')['result']['restarts'][0]['key']
        results={}
        for mode in ('initializer','closed','open','oracle_open','oracle_closed'):
            key=inverse if mode.startswith('oracle') else initial if mode=='initializer' else c.read(folder/(mode+'.json'))['result']['key']
            assert len(key)==26 and set(key)==set(c.ALPHABET)
            row={'key':key,'evaluation_only':mode.startswith('oracle')}
            for split in ('fit','transfer'):
                cipher=(c.DATA/'controls'/name/(split+'.txt')).read_text().strip()
                decoded=cipher.translate(str.maketrans(c.ALPHABET,key));target=c.TMP/(name+'_'+mode+'_'+split+'.txt');target.write_text(decoded+'\n')
                if mode in ('closed','oracle_closed'):command=[CLOSED_EXE,c.TMP/'closed'/lang,'segment',target,'exact']
                else:command=[c.EXE,c.TMP/'open'/lang,'segment',target,p['beta'],p['penalty']]
                out=run(command,folder/(mode+'_'+split+'_segmentation.json'))
                row[split]=dict(c.previous.metrics(out['segmentation'],truth['plaintext_'+split]),score=out['score'],segmentation=out['segmentation'])
            if mode in ('closed','open'):assert abs(row['fit']['score']-c.read(folder/(mode+'.json'))['result']['fit']['score'])<1e-8
            results[mode]=row
        transfer=results['open']['transfer']
        passed=transfer['character_accuracy']>=p['gate']['character_accuracy'] and transfer['boundary_f1']>=p['gate']['boundary_f1']
        record={'case':name,'language':lang,'rows':results,'passes_gate':passed,'NOT_TRANSLATION':True}
        c.save(folder/'evaluation.json',record);rows.append(record)
        print(json.dumps({'case':name,'passed':passed,'letters':transfer['character_accuracy'],'boundary_f1':transfer['boundary_f1']}),flush=True)
    c.save(c.OUT/'summary.json',{'cases':rows,'passed':sum(x['passes_gate'] for x in rows),'total':len(rows),
        'voynich_gate_open':all(x['passes_gate'] for x in rows),'NOT_TRANSLATION':True})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['prepare','fit','evaluate'])
    args=parser.parse_args();{'prepare':prepare,'fit':fit,'evaluate':evaluate}[args.action]()
