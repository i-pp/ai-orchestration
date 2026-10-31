"""Check an accepted B identity before comparing A. Local/read-only; no writer invocation."""
import argparse
from datetime import datetime
import difflib
import hashlib
import json
from pathlib import Path


def compare(b_path, a_path, record, policy_path):
    b = Path(b_path).read_bytes()
    a = Path(a_path).read_bytes()
    sha = lambda raw: hashlib.sha256(raw).hexdigest()
    if (record.get('accepted_b') is not True or not record.get('acceptance_ref')
            or record.get('policy_version') != '2.0'
            or record.get('policy_sha256') != sha(Path(policy_path).read_bytes())
            or record.get('face_b_sha256') != sha(b)
            or record.get('face_a_source_b_sha256') != sha(b)):
        raise ValueError('Accepted frozen B and exact policy identity required before A comparison')
    # Optional timestamps supplement the accepted-revision record, not a new
    # human approval on each cosmetic edit. Equal recorded seconds are valid.
    if record.get('b_frozen_at') is not None or record.get('a_created_at') is not None:
        frozen = datetime.fromisoformat(record.get('b_frozen_at', ''))
        created = datetime.fromisoformat(record.get('a_created_at', ''))
        if frozen.tzinfo is None or created.tzinfo is None or frozen > created:
            raise ValueError('Recorded B freeze must not be later than A creation')
    return {'face_b_sha256': sha(b), 'face_a_sha256': sha(a), 'policy_version': '2.0',
            'diff': ''.join(difflib.unified_diff(b.decode().splitlines(True), a.decode().splitlines(True), fromfile='frozen-B', tofile='A')),
            'substantive_change_review': 'PENDING_HUMAN_JUDGMENT',
            'editorial_acceptance': 'NOT_ASSESSED', 'publication_authorized': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('b'); p.add_argument('a'); p.add_argument('--record', required=True); p.add_argument('--policy', required=True)
    args = p.parse_args()
    print(json.dumps(compare(args.b, args.a, json.loads(Path(args.record).read_text()), args.policy), ensure_ascii=False, indent=2))
