#!/usr/bin/env python3
"""Explicit opt-in installation from pinned official sources; never invoked by lint."""
import argparse
import hashlib
import io
from pathlib import Path
import platform
import subprocess
import tarfile
import urllib.request

ROOT=Path(__file__).resolve().parents[1]/'assets/lint'
URL='https://github.com/vale-cli/vale/releases/download/v3.25.1/vale_3.25.1_Linux_64-bit.tar.gz'
SHA='4bf5c5176b682b1da0830f471584d3494f1c2e27ee3029e1ad6f6661d4962182'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--install',action='store_true',required=True)
    p.parse_args()
    if platform.system()!='Linux' or platform.machine() not in ['x86_64','AMD64']:
        raise SystemExit('Only the reviewed Linux x86_64 Vale distribution is supported')
    subprocess.run(['npm','ci','--ignore-scripts','--no-audit','--no-fund','--registry=https://registry.npmjs.org/'],cwd=ROOT,check=True)
    with urllib.request.urlopen(URL,timeout=60) as response:raw=response.read(30_000_001)
    if len(raw)>30_000_000 or hashlib.sha256(raw).hexdigest()!=SHA:raise SystemExit('Vale archive integrity mismatch')
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        entry=archive.getmember('vale')
        if not entry.isfile():raise SystemExit('Expected a regular Vale executable')
        content=archive.extractfile(entry).read()
    target=ROOT/'.tools/vale';target.parent.mkdir(exist_ok=True)
    target.write_bytes(content);target.chmod(0o755)
    subprocess.run([str(target),'--version'],check=True)

if __name__=='__main__':main()
