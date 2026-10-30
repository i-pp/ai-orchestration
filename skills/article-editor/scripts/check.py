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
NOSLOP_VERSION = '26.10.114'
NOSLOP_BINARY_SHA256 = 'bd5c48be69d9bc1bfdf024ad1731b21db312dfcf527df44ba031cec667727711'

def utf16_index(text, column):
    units=column-1
    for i,ch in enumerate(text):
        if units==0:return i
        units-=2 if ord(ch)>0xffff else 1
        if units<0:raise ValueError('Position splits a surrogate pair')
    if units==0:return len(text)
    raise ValueError('Position outside source')

def textlint_position(source, message):
    line=message.get('line',1);column=message.get('column',1);span=''
    lines=source.splitlines()
    if 1<=line<=len(lines):
        start=utf16_index(lines[line-1],column);column=start+1
        end=message.get('loc',{}).get('end',{})
        end_line=end.get('line',message.get('endLine',line));end_column=end.get('column',message.get('endColumn'))
        if end_line==line and end_column:
            span=lines[line-1][start:utf16_index(lines[line-1],end_column)]
    return line,column,span

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
    """Evidence projection only. Never feed whitespace-masked prose back as Markdown."""
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

def without_frontmatter(text):
    lines=text.splitlines(keepends=True)
    if not lines or lines[0].strip() not in ('---','+++'):return text
    delimiter=lines[0].strip()
    for i in range(1,len(lines)):
        if lines[i].strip() in (delimiter,'...' if delimiter=='---' else delimiter):
            return ''.join(blank(line) for line in lines[:i+1])+''.join(lines[i+1:])
    raise ValueError('Unterminated frontmatter')

def config_hash():
    paths = ['package.json', 'package-lock.json', '.textlintrc.json', '.vale.ini',
             'styles/config/vocabularies/Project/accept.txt', 'styles/config/vocabularies/Project/reject.txt']
    return digest(json.dumps({p:digest((CONFIG/p).read_bytes()) for p in paths},sort_keys=True))

def aggregate_findings(rows):
    merged={}
    for row in rows:
        if row.get('category')=='AI_HYPE' and row.get('span_text'):
            key=('AI_HYPE',row.get('line'),row.get('column'),row['span_text'].removesuffix('な'))
        else:key=('exact',row.get('line'),row.get('column'),row.get('severity'),re.sub(r'\s+',' ',row['message']).strip())
        source={k:row.get(k) for k in ['tool','rule','message','severity','original_severity','span_text']}
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
                line,column,span=textlint_position(masked,m)
                rule=m.get('ruleId','textlint')
                record['findings'].append({'rule':rule,'line':line,'column':column,'message':m['message'],'severity':'MINOR',
                    'span_text':span,'category':'AI_HYPE' if rule.endswith('/no-ai-hype-expressions') else None})
        else:
            for entries in data.values():
                for m in entries:
                    record['findings'].append({'rule':m['Check'],'line':m['Line'],'column':m.get('Span',[1])[0],'message':m['Message'],'severity':'MINOR'})
        if result.returncode == 1 and not record['findings']:
            record['status'] = 'TOOL_ERROR'
        else: record['status'] = 'COMPLETED'
        return record
    except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired):
        record['status'] = 'TOOL_ERROR'
        return record

def run_noslop(text, lang, enabled=False):
    record={'name':'noslop','version':None,'optional':True,'requested':enabled,'executed':False,'exit_code':None,'status':'NOT_RUN','findings':[]}
    if lang!='ja':record['status']='NOT_APPLICABLE';return record
    if not enabled:return record
    source=CONFIG/'.tools/noslop-v26.10.114/noslop'
    try:
        if not source.is_file():record['status']='NOT_INSTALLED';return record
        binary_bytes=source.read_bytes()
    except OSError:
        record['status']='TOOL_ERROR';return record
    if digest(binary_bytes)!=NOSLOP_BINARY_SHA256:record['status']='DIGEST_MISMATCH';return record
    record.update(binary_sha256=NOSLOP_BINARY_SHA256,sanitized_sha256=digest(text),input_mode='sanitized-copy',
        command=['noslop','check','--no-config','--dict','bundled','--genre','tech','--format','json','--fail-on','never','article.md'])
    try:
        with tempfile.TemporaryDirectory(prefix='noslop-runtime-') as directory:
            root=Path(directory);binary=root/'noslop';binary.write_bytes(binary_bytes);binary.chmod(0o700)
            article=root/'article.md';article.write_bytes(text.encode());article.chmod(0o400)
            version=subprocess.run([str(binary),'--version'],capture_output=True,text=True,timeout=10)
            record['version']=version.stdout.strip().removeprefix('noslop ')
            if version.returncode or record['version']!=NOSLOP_VERSION:record['status']='VERSION_MISMATCH';return record
            record['executed']=True
            result=subprocess.run([str(binary),*record['command'][1:]],cwd=root,capture_output=True,text=True,timeout=45)
            record['exit_code']=result.returncode
            if article.read_bytes()!=text.encode():raise ValueError('Input changed')
            data=json.loads(result.stdout)
        if result.returncode!=0 or data.get('errors') or data.get('columnUnit')!='unicode-scalar' or data.get('summary',{}).get('files')!=1 or len(data.get('files',[]))!=1:
            raise ValueError('Unexpected noslop result')
        observed=0;raw=text.encode()
        for item in data['files']:
            if item.get('path')!='article.md':raise ValueError('Unexpected noslop input')
            for f in item['diagnostics']:
                observed+=1
                if f.get('suppressed'):raise ValueError('Unexpected hidden suppression')
                start=f['range']['start'];end=f['range']['end'];left=start['offset'];right=end['offset']
                if type(left) is not int or type(right) is not int or not 0<=left<=right<=len(raw):raise ValueError('Invalid source range')
                prefix=raw[:left].decode();span=raw[left:right].decode();line=prefix.count('\n')+1;column=len(prefix.rsplit('\n',1)[-1])+1
                if (line,column)!=(start['line'],start['column']):raise ValueError('Inconsistent source position')
                record['findings'].append({'tool':'noslop','rule':f['ruleId'],'line':line,'column':column,'message':f['message'],
                    'severity':'MINOR','original_severity':f['severity'],'span_text':span,
                    'category':'AI_HYPE' if f['ruleId']=='P19' and f.get('ruleName')=='HYPE' else None})
        if observed!=data['summary']['diagnostics']:raise ValueError('Incomplete diagnostics')
        record['status']='COMPLETED'
    except (OSError,ValueError,KeyError,TypeError,AttributeError,subprocess.TimeoutExpired):
        record['status']='TOOL_ERROR';record['findings']=[]
    return record

def check(path, lang, suppressions=None, noslop=False, sanitized_sha256=None):
    raw = Path(path).read_bytes()
    if len(raw)>2_000_000: raise ValueError('Article exceeds the bounded prose-check size')
    text=raw.decode();masked=prose_only(text)
    if noslop and lang=='ja':
        if sanitized_sha256!=digest(raw):raise ValueError('Noslop needs an explicit sanitized-copy SHA256 matching this input')
        if re.search(r'/(?:home|Users|run/media)/|https://chatgpt\.com/c/|\b(?:ghp_|github_pat_|sk-)[A-Za-z0-9_-]{20,}',text):
            raise ValueError('Sanitize private paths/references/credentials before noslop')
    primary_text=without_frontmatter(text)
    primary=run_tool('textlint' if lang=='ja' else 'vale',primary_text)
    secondary=run_noslop(text,lang,noslop)
    findings=[]
    if primary['status']!='COMPLETED':
        findings.append({'id':'primary-tool','severity':'MAJOR','rule':primary['name'],'line':1,'message':'Primary tool '+primary['status'],'status':'OPEN'})
    rows=[dict(f,tool=primary['name']) for f in primary['findings']]+secondary['findings']
    if noslop and lang=='ja' and secondary['status']!='COMPLETED':
        findings.append({'id':'optional-noslop','severity':'MINOR','rule':'noslop','line':1,'message':'Optional noslop '+secondary['status'],'status':'OPEN'})
    for i,f in enumerate(aggregate_findings(rows)):
        findings.append({'id':f'lint-{i+1}',**f,'status':'OPEN'})
    for f in findings:
        f['fingerprint']=digest(json.dumps({k:f.get(k) for k in ['rule','line','column','message','severity','sources']},sort_keys=True))
    used=[]
    for item in suppressions or []:
        if (item.get('article_sha256')!=digest(raw) or not item.get('reason') or not item.get('rule')
                or not re.fullmatch(r'[0-9a-f]{64}',item.get('fingerprint',''))): raise ValueError('Suppression needs exact article/finding fingerprint/rule/reason')
        matches=[f for f in findings if f['severity']=='MINOR' and f['rule']==item['rule'] and f['fingerprint']==item['fingerprint']]
        if len(matches)!=1: raise ValueError('Stale, ambiguous or unmatched suppression')
        for f in matches: f.update(status='SUPPRESSED',reason=item['reason'])
        used.append(item)
    lt_jar=CONFIG/'.tools/languagetool-6.8/lib/languagetool-commandline-6.8.jar'
    lt_available=lt_jar.is_file() and bool(shutil.which('java'))
    return {'schema_version':1,'checker_version':'1.0.0','checker_sha256':digest(Path(__file__).read_bytes()),'article_sha256':digest(raw),'masked_sha256':digest(masked),
            'config_sha256':config_hash(),'language':lang,'network':'NONE','input_modified':False,
            'primary_input_sha256':digest(primary_text),'primary_exclusion':'native Markdown plus AST/config exclusions; frontmatter lines blanked only',
            'tools':[primary,{'name':'languagetool','version':'6.8' if lt_available else None,'executed':False,'exit_code':None,
                            'status':'NOT_RUN' if lt_available else 'NOT_INSTALLED','optional':True,'available':lt_available,'java_available':bool(shutil.which('java')),
                            'note':'Separate optional local CLI per Skill; not executed by this checker. No cloud fallback. JA has no spellcheck.'},secondary],
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
    parser.add_argument('--noslop',action='store_true',help='Explicit optional Japanese check on a sanitized copy only')
    parser.add_argument('--sanitized-sha256',help='SHA256 of the authorized sanitized input, not automatic confidentiality approval')
    args=parser.parse_args()
    data=check(args.article,args.lang,None if not args.suppressions else json.loads(Path(args.suppressions).read_text()),args.noslop,args.sanitized_sha256)
    write_report(args.output,data,args.article)
    print(json.dumps({'article_sha256':data['article_sha256'],'primary_tool':data['tools'][0]['status'],'findings':len(data['findings']),
        'optional_languagetool':data['tools'][1]['status'],'optional_noslop':data['tools'][2]['status']}))
    return 0 if data['tools'][0]['status']=='COMPLETED' else 2

if __name__=='__main__':raise SystemExit(main())
