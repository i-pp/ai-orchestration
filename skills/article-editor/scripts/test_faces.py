import hashlib
import tempfile
import unittest
from pathlib import Path
from faces import compare


class FaceTests(unittest.TestCase):
    def test_changed_or_unaccepted_b_and_wrong_policy_cannot_be_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            b, a, policy = [Path(tmp)/n for n in ('B.md','A.md','policy.md')]
            b.write_text('Measured result\n');a.write_text('Reader-first result\n');policy.write_text('v2 fixture\n')
            sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
            record={'accepted_b':True,'acceptance_ref':'fixture-author-acceptance','face_b_sha256':sha(b),'policy_version':'2.0','policy_sha256':sha(policy),'face_a_source_b_sha256':sha(b),'b_frozen_at':'2026-10-31T00:00:00+00:00','a_created_at':'2026-10-31T00:01:00+00:00'}
            result=compare(b,a,record,policy)
            self.assertIn('-Measured result',result['diff']);self.assertFalse(result['publication_authorized'])
            self.assertEqual(result['substantive_change_review'],'PENDING_HUMAN_JUDGMENT')
            for key,value in [('accepted_b',False),('face_b_sha256','0'*64),('policy_sha256','0'*64),('acceptance_ref',''),('face_a_source_b_sha256','0'*64),('b_frozen_at','2026-11-01T00:00:00+00:00')]:
                with self.subTest(key=key),self.assertRaises(ValueError):compare(b,a,dict(record,**{key:value}),policy)
            untimed={k:v for k,v in record.items() if k not in ('a_created_at','b_frozen_at')}
            self.assertEqual(compare(b,a,untimed,policy)['face_b_sha256'],sha(b))
            equal=dict(record,a_created_at=record['b_frozen_at'])
            self.assertEqual(compare(b,a,equal,policy)['face_b_sha256'],sha(b))
            b.write_text('Changed after acceptance\n')
            with self.assertRaises(ValueError):compare(b,a,record,policy)
