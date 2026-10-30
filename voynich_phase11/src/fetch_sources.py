"""Download pinned upstream files, preserving bytes; verify every Git blob and SHA256."""
import hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
for item in json.loads((ROOT/'data/source_manifest.json').read_text()):
    target=ROOT/item['local_path']
    if target.exists():
        data=target.read_bytes()
    else:
        url=f"https://raw.githubusercontent.com/{item['repository']}/{item['commit']}/{item['path']}"
        request=urllib.request.Request(url,headers={'User-Agent':'Voynich-phase11-reproduction'})
        with urllib.request.urlopen(request,timeout=60) as response:
            data=response.read()
    assert len(data)==item['expected_bytes'],item['path']
    assert hashlib.sha256(data).hexdigest()==item['sha256'],item['path']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['blob_sha'],item['path']
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
print('45 pinned source files verified. No upstream code was executed.')
