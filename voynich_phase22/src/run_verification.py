#!/usr/bin/env python3
"""Post-freeze import-only launcher for the unchanged frozen audit. CC BY-SA 4.0.

phase22lib imports phase21 dependencies by prepending phase21/src to sys.path.
Consequently the frozen verify.py's `import study` otherwise resolves to phase21.
Load the correct phase22 study module explicitly before executing the frozen audit.
This launcher does not change models, controls, fitting, scores or audit assertions.
"""
import importlib.util
from pathlib import Path
import sys
import phase22lib


def local_module(name,filename):
    path=Path(__file__).resolve().parent/filename
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    spec.loader.exec_module(module)
    assert Path(module.__file__).resolve()==path
    return module


if __name__=='__main__':
    local_module('study','study.py')
    audit=local_module('phase22_frozen_verify','verify.py')
    audit.main()
