import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import subprocess
import unittest
from unittest.mock import patch

def module(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

c=module('check');r=module('review')

class EditorialTests(unittest.TestCase):
    def test_duplicate_aggregation_keeps_all_sources_and_separate_issues(self):
        a={'tool':'textlint','rule':'one','line':1,'column':2,'message':'Same warning','severity':'MINOR'}
        b=dict(a,tool='optional-fixture-only',rule='two',message='Same  warning')
        other=dict(b,column=9)
        result=c.aggregate_findings([a,b,other]);self.assertEqual(len(result),2)
        self.assertEqual(len(result[0]['sources']),2);self.assertEqual(len(result[1]['sources']),1)
    def test_real_ai_writing_rule_is_advisory(self):
        result=c.run_tool('textlint','これは革命的な技術です。\n\n- **重要**: 問題を完全に解決します。\n')
        self.assertEqual(result['status'],'COMPLETED')
        self.assertTrue(any('no-ai-hype-expressions' in f['rule'] for f in result['findings']))
        self.assertTrue(all(f['severity']=='MINOR' for f in result['findings']))
    def test_link_tail_and_multibacktick_inline_code(self):
        text='[docs](https://example.test/a(b)) The the result (important).\n``a ` b``\n'
        masked=c.prose_only(text)
        self.assertIn('The the result (important).',masked);self.assertNotIn('a ` b',masked)
    def test_invalid_fence_close_does_not_hide_later_prose(self):
        text='```\ncode\n``` trailing text\ncode\n```\nVisible prose.\n'
        masked=c.prose_only(text)
        self.assertNotIn('trailing text',masked);self.assertIn('Visible prose.',masked)
    def test_report_cannot_replace_article_or_hardlink(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.json';p.write_text('original');other=Path(d)/'report.json';other.hardlink_to(p)
            for target in [p,other]:
                with self.assertRaises(ValueError):c.write_report(target,{},p)
            config=Path(d)/'config.json';config.write_text('{"user_owned":"PRESERVE"}')
            with self.assertRaises(ValueError):c.write_report(config,{},p)
            self.assertEqual(config.read_text(),'{"user_owned":"PRESERVE"}')
            self.assertEqual(p.read_text(),'original')
    def test_timeout_records_actual_main_process_start(self):
        version=subprocess.CompletedProcess([],0,stdout='15.8.0',stderr='')
        with patch.object(c.subprocess,'run',side_effect=[version,subprocess.TimeoutExpired('textlint',45)]):
            result=c.run_tool('textlint','Prose')
        self.assertTrue(result['executed']);self.assertIsNone(result['exit_code']);self.assertEqual(result['status'],'TOOL_ERROR')
    def test_fingerprint_suppresses_only_one_same_line_finding(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.md';p.write_text('Prose')
            fake={'name':'textlint','status':'COMPLETED','findings':[{'rule':'fixture','line':1,'column':i,'message':str(i),'severity':'MINOR'} for i in [1,2]]}
            with patch.object(c,'run_tool',return_value=fake):
                initial=c.check(p,'ja');s={'article_sha256':initial['article_sha256'],'rule':'fixture','fingerprint':initial['findings'][0]['fingerprint'],'reason':'one exact instance'}
                result=c.check(p,'ja',[s]);self.assertEqual([f['status'] for f in result['findings']],['SUPPRESSED','OPEN'])
    def test_metadata_code_and_destinations_masked_labels_preserved(self):
        text='---\ntitle: mispeling\n---\nRead [label](https://example.test/mispeling).\n`mispeling`\n```c\nmispeling\n```\n    mispeling\nhttps://example.test/mispeling\nVisible prose.\n'
        masked=c.prose_only(text)
        self.assertNotIn('mispeling',masked);self.assertIn('[label]',masked);self.assertIn('Visible prose.',masked)
        self.assertEqual(text.count('\n'),masked.count('\n'))
    def test_suppression_is_bound_and_no_input_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.md';p.write_text('Original prose.\n');raw=p.read_bytes()
            fake={'name':'textlint','version':'15.8.0','executed':True,'exit_code':0,'status':'COMPLETED','findings':[{'rule':'fixture','line':1,'column':1,'message':'candidate','severity':'MINOR'}]}
            with patch.object(c,'run_tool',return_value=fake):
                initial=c.check(p,'ja');suppression={'article_sha256':hashlib.sha256(raw).hexdigest(),'rule':'fixture','fingerprint':initial['findings'][0]['fingerprint'],'reason':'Reviewed fixture false positive'}
                result=c.check(p,'ja',[suppression]);self.assertEqual(result['findings'][0]['status'],'SUPPRESSED')
                with self.assertRaises(ValueError):c.check(p,'ja',[dict(suppression,article_sha256='0'*64)])
            self.assertEqual(raw,p.read_bytes())
    def test_unavailable_primary_tool_is_not_success(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.md';p.write_text('Prose')
            with patch.object(c,'run_tool',return_value={'name':'vale','status':'NOT_INSTALLED','findings':[]}):
                report=c.check(p,'en')
            self.assertEqual(report['findings'][0]['severity'],'MAJOR')
            self.assertFalse(report['tools'][1]['executed'])
    def record(self,sha):
        return {'article_sha256':sha,'cycle':2,'roles':{'writer':'Writer','editor':'Editor','technical':'Technical'},
                'editor':{'article_sha256':sha,'reviewed':True,'evidence':'Fixture read'},
                'technical':{'article_sha256':sha,'reviewed':True,'evidence':'Fixture sources'},'findings':[],
                'final_verification':{k:True for k in ['sources_checked','meaning_preserved','protected_spans_reviewed','disclosure_checked','confidentiality_checked']}}
    def test_review_blockers_major_rationale_role_and_two_cycle_limit(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.md';p.write_text('Prose');sha=hashlib.sha256(p.read_bytes()).hexdigest()
            m={'schema_version':1,'checker_version':'1.0.0','article_sha256':sha,'masked_sha256':sha,'config_sha256':sha,'network':'NONE','input_modified':False,'language':'en','tools':[{'name':'vale','version':'3.25.1','status':'COMPLETED','executed':True,'exit_code':0},{'name':'languagetool'}],'findings':[]};v=self.record(sha)
            m['checker_sha256']=hashlib.sha256(Path(c.__file__).read_bytes()).hexdigest()
            report_sha=hashlib.sha256(__import__('json').dumps(m,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            v['mechanical_sha256']=report_sha
            with self.assertRaises(ValueError):r.final_state(p,{'article_sha256':sha,'findings':[]},v)
            self.assertEqual(r.final_state(p,m,v)['state'],'READY_FOR_HUMAN_REVIEW')
            v['cycle']=3
            with self.assertRaises(ValueError):r.final_state(p,m,v)
            v=self.record(sha);v['mechanical_sha256']=report_sha;v['roles']['editor']='Writer'
            with self.assertRaises(ValueError):r.final_state(p,m,v)
            v=self.record(sha);v['mechanical_sha256']=report_sha;v['findings']=[{'id':'b','severity':'BLOCKER','status':'ACCEPTED','reason':'Cannot waive'}]
            self.assertEqual(r.final_state(p,m,v)['state'],'BLOCKED')
            v['findings']=[{'id':'m','severity':'MAJOR','status':'ACCEPTED','reason':'Specific reason'}]
            self.assertEqual(r.final_state(p,m,v)['state'],'BLOCKED')
            v['findings'][0].update(impact='Known bounded limitation',reconsider_when='New evidence')
            self.assertEqual(r.final_state(p,m,v)['state'],'READY_FOR_HUMAN_REVIEW')
            p.write_text('Changed')
            with self.assertRaises(ValueError):r.final_state(p,m,v)
    def test_real_tools_detect_errors_and_exclude_protected_content(self):
        for lang,word in [('ja','ここでは試験では不具合を調べた。'),('en','The the mispeling word.')]:
            tool='textlint' if lang=='ja' else 'vale'
            live=c.run_tool(tool,word+'\n')
            self.assertEqual(live['status'],'COMPLETED');self.assertTrue(live['executed']);self.assertTrue(live['findings'])
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'a.md';p.write_text('---\ntitle: '+word+'\n---\n```\n'+word+'\n```\n`'+word+'`\n')
                report=c.check(p,lang);self.assertEqual(report['tools'][0]['status'],'COMPLETED');self.assertEqual(report['findings'],[])

if __name__=='__main__':unittest.main()
