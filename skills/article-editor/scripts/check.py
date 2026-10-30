#!/usr/bin/env python3
"""Local-only prose checks; no auto-fix, dependency download or remote API."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'assets/lint'
VERSIONS = {'textlint': '15.8.0', 'vale': '3.25.1'}

def digest(raw):
    return hashlib.sha256(raw if isinstance(raw, bytes) else raw.encode()).hexdigest()

def blank(value):
    return ''.join('\n' if c == '\n' else ' ' for c in value)

def mask_destinations(line):
    start=0
    while True:
        match=re.search(r'\]\(',line[start:])
        if not match:break
        left=start+match.end()-1;right=left+1;depth=1
        while right<len(line) and line[right]!='\n' and depth:
            if line[right]=='\\':right+=2;continue
            if line[right]=='(':depth+=1
            elif line[right]==')':depth-=1
            right+=1
        if depth:start=left+1;continue
        line=line[:left]+blank(line[left:right])+line[right:];start=right
    return line

def mask_inline(text):
    runs=list(re.finditer(r'`+',text));i=0
    while i<len(runs):
        left=runs[i];before=text[:left.start()]
        if (len(before)-len(before.rstrip('\\')))%2:
            i+=1;continue
        barrier=re.search(r'\n[ \t]*\n',text[left.end():])
        limit=len(text) if not barrier else left.end()+barrier.start()
        right=next((j for j in range(i+1,len(runs)) if runs[j].start()<limit and len(runs[j][0])==len(left[0])),None)
        if right is None:i+=1;continue
        end=runs[right].end();text=text[:left.start()]+blank(text[left.start():end])+text[end:];i=right+1
    return text

def prose_only(text):
    """Keep line positions; exclude metadata/code/URL targets without touching input."""
    lines = text.splitlines(keepends=True)
    metadata = bool(lines and lines[0].strip() == '---')
    fence = None
    output = []
    for i, line in enumerate(lines):
        if metadata:
            output.append(blank(line))
            if i and line.strip() in ('---', '...'): metadata = False
            continue
        match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            output.append(blank(line))
            if re.match(r'^ {0,3}'+re.escape(fence[0])+'{'+str(len(fence))+r',}[ \t]*\r?\n?$',line): fence = None
            continue
        if match:
            fence = match[1]
            output.append(blank(line))
            continue
        if line.startswith(('    ', '\t')):
            output.append(blank(line))
            continue
        output.append(line)
    text=mask_inline(''.join(output))
    output=[]
    for line in text.splitlines(keepends=True):
        line=mask_destinations(line)
        line=re.sub(r'https?://[^\s<>]+',lambda m:blank(m[0]),line)
        line=re.sub(r'^ {0,3}\[[^\]]+\]:[^\n]*',lambda m:blank(m[0]),line)
        output.append(line)
    return ''.join(output)

def config_hash():
    paths = ['package.json', 'package-lock.json', '.textlintrc.json', '.vale.ini',
             'styles/config/vocabularies/Project/accept.txt', 'styles/config/vocabularies/Project/reject.txt']
    return digest(json.dumps({p:digest((CONFIG/p).read_bytes()) for p in paths},sort_keys=True))

def aggregate_findings(rows):
    merged={}
    for row in rows:
        key=(row.get('line'),row.get('column'),row.get('severity'),re.sub(r'\s+',' ',row['message']).strip())
        source={'tool':row.get('tool'),'rule':row.get('rule')}
        if key not in merged:merged[key]={**row,'sources':[]}
        if source not in merged[key]['sources']:merged[key]['sources'].append(source)
    return list(merged.values())

def run_tool(name, masked):
    if name == 'textlint':
        binary = CONFIG / 'node_modules/.bin/textlint'
        args = ['--config', str(CONFIG/'.textlintrc.json'), '--format', 'json']
    else:
        binary = CONFIG / '.tools/vale'
        args = ['--no-global', '--config', str(CONFIG/'.vale.ini'), '--output=JSON']
    record = {'name':name,'version':None,'executed':False,'exit_code':None,'status':'NOT_INSTALLED','findings':[]}
    if not binary.is_file(): return record
    try:
        version = subprocess.run([str(binary),'--version'],capture_output=True,text=True,timeout=10)
        found = re.search(r'\b(?:v|version )?([0-9]+\.[0-9]+\.[0-9]+)\b',version.stdout)
        record['version'] = found[1] if found else None
        if version.returncode or record['version'] != VERSIONS[name]:
            record['status'] = 'VERSION_MISMATCH'
            return record
        with tempfile.TemporaryDirectory(prefix='editorial-prose-') as directory:
            article = Path(directory)/'article.md'
            article.write_text(masked)
            record['executed']=True
            result = subprocess.run([str(binary),*args,str(article)],cwd=CONFIG,capture_output=True,text=True,timeout=45)
        record.update(executed=True,exit_code=result.returncode)
        try: data = json.loads(result.stdout)
        except ValueError:
            record['status'] = 'TOOL_ERROR'
            return record
        if result.returncode not in (0,1):
            record['status'] = 'TOOL_ERROR'
            return record
        if name == 'textlint':
            messages = [m for item in data for m in item.get('messages',[])]
            for m in messages:
                record['findings'].append({'rule':m.get('ruleId','textlint'),'line':m.get('line',1),'column':m.get('column',1),'message':m['message'],'severity':'MINOR'})
        else:
            for entries in data.values():
                for m in entries:
                    record['findings'].append({'rule':m['Check'],'line':m['Line'],'column':m.get('Span',[1])[0],'message':m['Message'],'severity':'MINOR'})
        if result.returncode == 1 and not record['findings']:
            record['status'] = 'TOOL_ERROR'
        else: record['status'] = 'COMPLETED'
        return record
    except (OSError,subprocess.TimeoutExpired):
        record['status'] = 'TOOL_ERROR'
        return record

def check(path, lang, suppressions=None):
    raw = Path(path).read_bytes()
    if len(raw)>2_000_000: raise ValueError('Article exceeds the bounded prose-check size')
    text=raw.decode();masked=prose_only(text)
    primary=run_tool('textlint' if lang=='ja' else 'vale',masked)
    findings=[]
    if primary['status']!='COMPLETED':
        findings.append({'id':'primary-tool','severity':'MAJOR','rule':primary['name'],'line':1,'message':'Primary tool '+primary['status'],'status':'OPEN'})
    for i,f in enumerate(aggregate_findings([dict(f,tool=primary['name']) for f in primary['findings']])):
        findings.append({'id':f'lint-{i+1}',**f,'status':'OPEN'})
    for f in findings:
        f['fingerprint']=digest(json.dumps({k:f.get(k) for k in ['rule','line','column','message','severity']},sort_keys=True))
    used=[]
    for item in suppressions or []:
        if (item.get('article_sha256')!=digest(raw) or not item.get('reason') or not item.get('rule')
                or not re.fullmatch(r'[0-9a-f]{64}',item.get('fingerprint',''))): raise ValueError('Suppression needs exact article/finding fingerprint/rule/reason')
        matches=[f for f in findings if f['severity']=='MINOR' and f['rule']==item['rule'] and f['fingerprint']==item['fingerprint']]
        if len(matches)!=1: raise ValueError('Stale, ambiguous or unmatched suppression')
        for f in matches: f.update(status='SUPPRESSED',reason=item['reason'])
        used.append(item)
    return {'schema_version':1,'checker_version':'1.0.0','checker_sha256':digest(Path(__file__).read_bytes()),'article_sha256':digest(raw),'masked_sha256':digest(masked),
            'config_sha256':config_hash(),'language':lang,'network':'NONE','input_modified':False,
            'tools':[primary,{'name':'languagetool','version':None,'executed':False,'exit_code':None,
                            'status':'NOT_INSTALLED','optional':True,'java_available':bool(shutil.which('java')),
                            'note':'LanguageTool jar is not provisioned; no cloud fallback. Japanese is supported, without JA spellcheck.'}],
            'findings':findings,'suppressions':used}

def write_report(path, value, input_path):
    target=Path(path);source=Path(input_path)
    if target.suffix!='.json' or target.resolve()==source.resolve() or (target.exists() and os.path.samefile(target,source)):
        raise ValueError('Report must be a JSON file distinct from the source article')
    if target.exists() or target.is_symlink():raise ValueError('Reports are immutable; choose a new output path')
    target.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.editorial-',dir=target.parent)
    try:
        with os.fdopen(fd,'w') as out:
            json.dump(value,out,ensure_ascii=False,indent=2);out.write('\n');out.flush();os.fsync(out.fileno())
        # Same-directory hard link is atomic and fails if another writer won the name.
        os.link(name,target)
    finally:
        if os.path.exists(name):os.unlink(name)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('article');parser.add_argument('--lang',required=True,choices=['ja','en'])
    parser.add_argument('--output',required=True);parser.add_argument('--suppressions')
    args=parser.parse_args()
    data=check(args.article,args.lang,None if not args.suppressions else json.loads(Path(args.suppressions).read_text()))
    write_report(args.output,data,args.article)
    print(json.dumps({'article_sha256':data['article_sha256'],'primary_tool':data['tools'][0]['status'],'findings':len(data['findings']),'optional_languagetool':'NOT_INSTALLED'}))
    return 0 if data['tools'][0]['status']=='COMPLETED' else 2

if __name__=='__main__':raise SystemExit(main())
