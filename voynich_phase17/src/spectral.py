"""Transparent, non-generative processing of an explicitly bounded f116v region."""
from pathlib import Path
import hashlib, json, re, warnings, io, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage, fft

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT.parent/'voynich_resources/msi/raw/f116v'
BOX=(2400,550,6050,1570)
SEED=20261030

def savegray(a,p,percentiles=(1,99)):
    lo,hi=np.percentile(a,percentiles)
    assert hi>lo
    im=Image.fromarray(np.uint8(np.clip((a-lo)/(hi-lo),0,1)*255))
    buf=io.BytesIO();im.save(buf,format='PNG')
    temp=Path(str(p)+'.writing')
    with temp.open('wb') as out:
        out.write(buf.getvalue());out.flush();os.fsync(out.fileno())
    temp.replace(p)
    with Image.open(p) as check:check.load()
    return [float(lo),float(hi)]

def contrast(a):
    f=ndimage.median_filter(a.astype(np.float32),size=3)
    b=ndimage.uniform_filter(f,size=101,mode='reflect')
    return -np.log((f+1)/(b+1))

def shift_estimate(a,b,limit=6):
    a=a.astype(np.float32)-np.mean(a);b=b.astype(np.float32)-np.mean(b)
    window=np.outer(np.hanning(a.shape[0]),np.hanning(a.shape[1])).astype(np.float32)
    fa=fft.rfft2(a*window,workers=1);fb=fft.rfft2(b*window,workers=1)
    cc=fft.irfft2(fa*np.conj(fb),s=a.shape,workers=1)
    best=max((float(cc[dy%len(cc),dx%cc.shape[1]]),dy,dx) for dy in range(-limit,limit+1) for dx in range(-limit,limit+1))
    return [int(best[1]),int(best[2])]

def corr(a,b):
    return float(np.corrcoef(a.ravel(),b.ravel())[0,1])

def main():
    for d in ['data','results','figures']: (ROOT/d).mkdir(exist_ok=True)
    entries=[];arrays=[]
    roi=ROOT/'data/f116v_native_roi_22bands.npz'
    if roi.exists():
        stack=np.load(roi)['pixels']
        meta=json.loads((ROOT/'data/raw_roi_sources.json').read_text());entries=meta['bands']
        assert list(BOX)==meta['box_xyxy'] and stack.shape==(22,1020,3650) and stack.dtype==np.uint16
        for i,e in enumerate(entries):
            if 'crop_sha256' in e:assert hashlib.sha256(stack[i].tobytes()).hexdigest()==e['crop_sha256']
    else:
        manifest=json.loads((ROOT.parent/'voynich_resources/DOWNLOAD_MANIFEST.json').read_text())
        source={r['title']:r for r in manifest['msi'] if r['group']=='raw' and r['folio']=='f116v'}
        for band in range(1,23):
            p=next(RAW.glob(f'*_{band:03d}_F.tif'))
            digest=hashlib.sha256(p.read_bytes()).hexdigest()
            assert digest==source[p.name]['sha256'],p.name
            with Image.open(p) as im:
                assert im.mode=='I;16'
                camera=str(im.getexif().get(272,''))
                a=np.rot90(np.array(im),1)
            a=a[BOX[1]:BOX[3],BOX[0]:BOX[2]].copy()
            arrays.append(a)
            entries.append({'band':band,'filename':p.name,'source_sha256':digest,'camera':camera,
                            'shape':list(a.shape),'min':int(a.min()),'max':int(a.max()),'clip65535_pixels':int((a==65535).sum()),
                            'crop_sha256':hashlib.sha256(a.tobytes()).hexdigest()})
        stack=np.stack(arrays);del arrays
        np.savez_compressed(roi,pixels=stack)
        (ROOT/'data/raw_roi_sources.json').write_text(json.dumps({'orientation':'np.rot90(array,1)','box_xyxy':BOX,'bands':entries},indent=2))
    print('22 raw crops verified and saved',flush=True)
    X=np.stack([contrast(a) for a in stack]);del stack
    reference=X[5]
    aligned=[];audit=[]
    for i,a in enumerate(X):
        shift=[0,0] if i==5 else shift_estimate(reference,a)
        b=np.roll(a,shift,axis=(0,1))
        patch=[]
        # Disjoint left, middle, right areas; retained in the audit even when weak.
        for x1,x2 in [(20,1100),(1200,2300),(2400,3600)]:
            patch.append(shift_estimate(reference[20:-20,x1:x2],b[20:-20,x1:x2],3))
        audit.append({'band':i+1,'translation_dy_dx':shift,'corr_before':corr(reference[8:-8,8:-8],a[8:-8,8:-8]),
                      'corr_after':corr(reference[8:-8,8:-8],b[8:-8,8:-8]),'residual_patch_shifts':patch,
                      'at_search_boundary':max(map(abs,shift))==6})
        aligned.append(b[8:-8,8:-8])
    X=np.stack(aligned);del aligned
    h,w=X.shape[1:]
    rng=np.random.default_rng(SEED);sample=rng.choice(h*w,size=50000,replace=False)
    pcas={}
    for family,indices in [('all',list(range(22))),('reflection',list(range(12))),('fluorescence',list(range(12,22)))]:
        small=X[indices].reshape(len(indices),-1)[:,sample].T.astype(np.float64)
        means=small.mean(axis=0);std=small.std(axis=0);std=np.maximum(std,1e-9)
        train=(small-means)/std
        cov=np.cov(train,rowvar=False);eig,vectors=np.linalg.eigh(cov);order=np.argsort(eig)[::-1]
        eig=eig[order];vectors=vectors[:,order]
        for k in range(3):
            if vectors[np.argmax(np.abs(vectors[:,k])),k]<0:vectors[:,k]*=-1
        coeff=vectors[:,:3]/std[:,None]
        offset=means@coeff
        limits=[]
        for k in range(3):
            y=np.einsum('i,ihw->hw',coeff[:,k].astype(np.float32),X[indices],optimize=False)-offset[k]
            limits.append(savegray(y,ROOT/'figures'/f'pca_{family}_{k+1}.png'))
        pcas[family]={'bands':[i+1 for i in indices],'sample_size':50000,'sample_seed':SEED,
                      'means':means.tolist(),'stds':std.tolist(),'eigenvalues':eig.tolist(),
                      'explained_variance_ratio':(eig/eig.sum()).tolist(),'coefficients':coeff.tolist(),
                      'offset':offset.tolist(),'display_percentiles':limits}
        print('PCA',family,'first three variance fractions',np.round(eig[:3]/eig.sum(),4).tolist(),flush=True)
    bandlimits=[]
    for i,a in enumerate(X):
        bandlimits.append(savegray(-a,ROOT/'figures'/f'band_{i+1:02d}_contrast.png'))
    result={'source_box_xyxy':BOX,'final_box_xyxy':[BOX[0]+8,BOX[1]+8,BOX[2]-8,BOX[3]-8],
            'registration':audit,'pca':pcas,'native_relative_contrast_display':bandlimits,
            'limitations':['Local normalization is not a reflectance or chemical calibration.',
                          'PCA transforms can amplify noise, stains, misalignment and show-through.',
                          'Neither repeated acquisitions nor derived components are independent historical evidence.']}
    (ROOT/'results/spectral.json').write_text(json.dumps(result,indent=2))
    for a in audit:print(a,flush=True)

if __name__=='__main__':main()
