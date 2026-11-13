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
    def test_optional_read_failure_is_visible_and_nonblocking(self):
        original=c.Path.read_bytes
        def inaccessible(path):
            if path.name=='noslop':raise PermissionError('Fixture read failure')
            return original(path)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);binary=root/'.tools/noslop-v26.10.114/noslop';binary.parent.mkdir(parents=True);binary.write_bytes(b'Fixture')
            with patch.object(c,'CONFIG',root),patch.object(c.Path,'read_bytes',inaccessible),patch.object(c.subprocess,'run') as run:
                result=c.run_noslop('\u516c\u958b\u691c\u8a3c\u6587\u3002','ja',True)
        self.assertEqual(result['status'],'TOOL_ERROR');self.assertFalse(result['executed']);run.assert_not_called()
    def test_native_markdown_preserves_prose_after_inline_code(self):
        for lang,prose in [('ja','\u3053\u308c\u306f\u9769\u547d\u7684\u306a\u6280\u8853\u3067\u3059\u3002'),('en','The the mispeling word.')]:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'fixture.md';p.write_text('`code` '+prose+'\n')
                result=c.check(p,lang)
            self.assertEqual(result['tools'][0]['status'],'COMPLETED');self.assertTrue(result['findings'])
    def test_private_link_and_metadata_exclusions_do_not_hide_following_prose(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.md';p.write_text('---\ntitle: \u9769\u547d\u7684\u306a\n---\n[\u9769\u547d\u7684\u306a](https://example.test/a) \u3053\u308c\u306f\u9769\u547d\u7684\u306a\u6280\u8853\u3067\u3059\u3002\n')
            report=c.check(p,'ja')
            hype=[f for f in report['findings'] if (f.get('category')=='AI_HYPE')]
            self.assertEqual(len(hype),1);self.assertEqual((hype[0]['line'],hype[0]['column']),(4,35))
    def test_noslop_not_requested_and_english_do_not_execute(self):
        with patch.object(c.subprocess,'run') as run:
            self.assertEqual(c.run_noslop('Fixture','ja')['status'],'NOT_RUN')
            self.assertEqual(c.run_noslop('Fixture','en',True)['status'],'NOT_APPLICABLE')
        run.assert_not_called()
    def test_noslop_requires_explicit_matching_sanitized_copy(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.md';p.write_text('\u516c\u958b\u691c\u8a3c\u6587\u3002')
            with patch.object(c,'run_noslop') as run:
                with self.assertRaises(ValueError):c.check(p,'ja',noslop=True)
            run.assert_not_called()
    def test_noslop_digest_mismatch_never_executes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);binary=root/'.tools/noslop-v26.10.114/noslop';binary.parent.mkdir(parents=True);binary.write_bytes(b'Untrusted fixture')
            with patch.object(c,'CONFIG',root),patch.object(c.subprocess,'run') as run:
                result=c.run_noslop('\u516c\u958b\u691c\u8a3c\u6587\u3002','ja',True)
            self.assertEqual(result['status'],'DIGEST_MISMATCH');self.assertFalse(result['executed']);run.assert_not_called()
    def test_unicode_position_and_semantic_merge_keep_both_ranges(self):
        line,col,span=c.textlint_position('\U0001f9ea\u9769\u547d\u7684\u306a',{'line':1,'column':3,'loc':{'end':{'line':1,'column':7}}})
        self.assertEqual((line,col,span),(1,2,'\u9769\u547d\u7684\u306a'))
        a={'tool':'textlint','rule':'ai-hype','category':'AI_HYPE','line':line,'column':col,'span_text':span,'message':'Candidate A','severity':'MINOR'}
        b=dict(a,tool='noslop',rule='P19',span_text='\u9769\u547d\u7684',message='Candidate B',original_severity='info')
        result=c.aggregate_findings([a,b,dict(b,span_text='\u5225\u8a9e')]);self.assertEqual(len(result),2)
        self.assertEqual({x['span_text'] for x in result[0]['sources']},{'\u9769\u547d\u7684\u306a','\u9769\u547d\u7684'})
    @unittest.skipUnless((c.CONFIG/'.tools/noslop-v26.10.114/noslop').is_file(),'Optional noslop is not installed in this environment')
    def test_real_noslop_local_merge_and_markdown_protection(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.md';p.write_text('\u3053\u308c\u306f\u9769\u547d\u7684\u306a\u6280\u8853\u3067\u3059\u3002\n\n- **\u91cd\u8981**: \u3059\u3079\u3066\u306e\u554f\u984c\u3092\u5b8c\u5168\u306b\u89e3\u6c7a\u3057\u307e\u3059\u3002\n\n```text\n\u3053\u308c\u306f\u9769\u547d\u7684\u306a\u6280\u8853\u3067\u3059\u3002\n```\n')
            before=p.read_bytes();report=c.check(p,'ja',noslop=True,sanitized_sha256=hashlib.sha256(before).hexdigest())
            self.assertEqual(report['tools'][2]['status'],'COMPLETED')
            self.assertEqual(len(report['tools'][0]['findings']),3);self.assertEqual(len(report['tools'][2]['findings']),1)
            self.assertEqual(len(report['findings']),3);self.assertEqual(len(report['findings'][0]['sources']),2)
            self.assertTrue(all(f['line']<5 for f in report['findings']));self.assertEqual(before,p.read_bytes())
    def test_duplicate_aggregation_keeps_all_sources_and_separate_issues(self):
        a={'tool':'textlint','rule':'one','line':1,'column':2,'message':'Same warning','severity':'MINOR'}
        b=dict(a,tool='optional-fixture-only',rule='two',message='Same  warning')
        other=dict(b,column=9)
        result=c.aggregate_findings([a,b,other]);self.assertEqual(len(result),2)
        self.assertEqual(len(result[0]['sources']),2);self.assertEqual(len(result[1]['sources']),1)
    def test_real_ai_writing_rule_is_advisory(self):
        result=c.run_tool('textlint','\u3053\u308c\u306f\u9769\u547d\u7684\u306a\u6280\u8853\u3067\u3059\u3002\n\n- **\u91cd\u8981**: \u554f\u984c\u3092\u5b8c\u5168\u306b\u89e3\u6c7a\u3057\u307e\u3059\u3002\n')
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
            rejected=self.record(sha);rejected['mechanical_sha256']=report_sha
            rejected['technical']['verdict']='PASS';rejected['editor']['verdict']='FAIL'
            self.assertEqual(r.final_state(p,m,rejected)['state'],'BLOCKED')
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
        for lang,word in [('ja','\u3053\u3053\u3067\u306f\u8a66\u9a13\u3067\u306f\u4e0d\u5177\u5408\u3092\u8abf\u3079\u305f\u3002'),('en','The the mispeling word.')]:
            tool='textlint' if lang=='ja' else 'vale'
            live=c.run_tool(tool,word+'\n')
            self.assertEqual(live['status'],'COMPLETED');self.assertTrue(live['executed']);self.assertTrue(live['findings'])
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'a.md';p.write_text('---\ntitle: '+word+'\n---\n```\n'+word+'\n```\n`'+word+'`\n')
                report=c.check(p,lang);self.assertEqual(report['tools'][0]['status'],'COMPLETED');self.assertEqual(report['findings'],[])

if __name__=='__main__':unittest.main()
