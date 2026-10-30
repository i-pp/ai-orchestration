#!/usr/bin/env python3
"""Validate source-bound independent review data; never authorize publication."""
import argparse
import hashlib
import json
from pathlib import Path
import re

SEVERITIES={'BLOCKER','MAJOR','MINOR','SUGGESTION'}

def final_state(article, mechanical, record):
    sha=hashlib.sha256(Path(article).read_bytes()).hexdigest()
    if mechanical.get('article_sha256')!=sha or record.get('article_sha256')!=sha:
        raise ValueError('Review or mechanical report belongs to different article bytes')
    if (mechanical.get('schema_version')!=1 or mechanical.get('checker_version')!='1.0.0'
            or mechanical.get('checker_sha256')!=hashlib.sha256(Path(__file__).with_name('check.py').read_bytes()).hexdigest()
            or mechanical.get('network')!='NONE' or mechanical.get('input_modified') is not False
            or mechanical.get('language') not in ['ja','en']
            or not re.fullmatch(r'[0-9a-f]{64}',mechanical.get('config_sha256',''))
            or not re.fullmatch(r'[0-9a-f]{64}',mechanical.get('masked_sha256',''))):
        raise ValueError('Incomplete mechanical execution report')
    tools=mechanical.get('tools',[])
    primary='textlint' if mechanical['language']=='ja' else 'vale'
    if len(tools)!=2 or tools[0].get('name')!=primary or tools[1].get('name')!='languagetool':
        raise ValueError('Mechanical report must identify primary and optional tool')
    if tools[0].get('status')=='COMPLETED':
        if (tools[0].get('executed') is not True or type(tools[0].get('exit_code')) is not int
                or tools[0]['exit_code'] not in [0,1] or tools[0].get('version')!={'textlint':'15.8.0','vale':'3.25.1'}[primary]):
            raise ValueError('Completed tool needs actual pinned execution')
    elif not any(f.get('id')=='primary-tool' and f.get('severity')=='MAJOR' for f in mechanical.get('findings',[])):
        raise ValueError('Missing primary tool limitation')
    report_sha=hashlib.sha256(json.dumps(mechanical,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    if record.get('mechanical_sha256')!=report_sha:raise ValueError('Review must bind the exact mechanical report')
    if type(record.get('cycle')) is not int or not 1<=record['cycle']<=2:
        raise ValueError('At most two review/revision cycles; record a new evidence decision separately')
    roles=record.get('roles',{})
    if set(roles)!={'writer','editor','technical'} or any(not isinstance(x,str) or not x.strip() for x in roles.values()) or len(set(roles.values()))!=3:
        raise ValueError('Writer, Editor and Technical Reviewer must be distinct assignments')
    for role in ['editor','technical']:
        review=record.get(role,{})
        if review.get('article_sha256')!=sha or review.get('reviewed') is not True or not review.get('evidence'):
            raise ValueError('Both independent reviews must identify the final article and evidence')
    checks=record.get('final_verification',{})
    required=['sources_checked','meaning_preserved','protected_spans_reviewed','disclosure_checked','confidentiality_checked']
    if any(checks.get(k) is not True for k in required): raise ValueError('Final verification incomplete')
    dispositions={f['id']:f for f in record.get('findings',[])}
    if len(dispositions)!=len(record.get('findings',[])):raise ValueError('Duplicate finding id')
    for f in mechanical.get('findings',[]):
        d=dispositions.get(f['id'])
        if d is None:raise ValueError('Mechanical finding missing disposition')
        if d.get('severity')!=f['severity']:raise ValueError('Mechanical severity changed without a new evidence record')
        if d.get('status')=='FIXED':raise ValueError('A still-present final lint finding cannot be marked fixed')
    blockers=[];residuals=[]
    for f in dispositions.values():
        if f.get('severity') not in SEVERITIES or f.get('status') not in ['OPEN','FIXED','ACCEPTED','SUPPRESSED']:
            raise ValueError('Unknown severity/disposition')
        if f['severity']=='BLOCKER' and f['status']!='FIXED':blockers.append(f['id'])
        elif f['severity']=='MAJOR' and f['status']!='FIXED':
            if f['status']!='ACCEPTED' or not all(f.get(k) for k in ['reason','impact','reconsider_when']):blockers.append(f['id'])
        if f['status'] in ['ACCEPTED','SUPPRESSED'] and not f.get('reason'):raise ValueError('Disposition needs a rationale')
        if f['status']!='FIXED':residuals.append(f['id'])
    return {'state':'BLOCKED' if blockers else 'READY_FOR_HUMAN_REVIEW','article_sha256':sha,
            'cycle':record['cycle'],'blockers':blockers,'residuals':residuals,'merge_authorized':False,'publication_authorized':False}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('article');parser.add_argument('--mechanical',required=True);parser.add_argument('--review',required=True)
    args=parser.parse_args()
    result=final_state(args.article,json.loads(Path(args.mechanical).read_text()),json.loads(Path(args.review).read_text()))
    print(json.dumps(result,indent=2));return 2 if result['blockers'] else 0

if __name__=='__main__':raise SystemExit(main())
