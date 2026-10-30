import platform,shutil,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent.parent
(root/'tmp').mkdir(exist_ok=True)
compiler=shutil.which('g++') or shutil.which('clang++')
if not compiler:raise SystemExit('Install a C++ compiler. On macOS: xcode-select --install')
cmd=[compiler,'-O3','-std=c++17','-dynamiclib' if sys.platform=='darwin' else '-shared','-fPIC',str(root/'src/cost.cpp'),'-o',str(root/'tmp/libcost.so')]
subprocess.run(cmd,check=True)
print('CPU kernel compiled on',platform.platform())
