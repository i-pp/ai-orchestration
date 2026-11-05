#!/usr/bin/env python3
"""Load local editorial instructions and hash-bound user examples; never execute them."""
import argparse
import hashlib
import json
from pathlib import Path
import re

PINNED = (
    'docs/ai/editorial-policy.md',
    'docs/ai/example/before_ryzen-ai-max-395-ubuntu-2604-npu-ja.md',
    'docs/ai/example/after_ryzen-ai-max-395-ubuntu-2604-npu-ja.md',
)
CONTEXT = (
    'docs/ai/orchestration.md', 'docs/ai/policies.md', 'policies/editorial.md',
    'agents/README.md', 'skills/technical-writing/SKILL.md',
    'skills/article-editor/SKILL.md',
    'skills/article-editor/references/editorial.md',
    'skills/article-editor/references/voice-style.md',
    'skills/article-editor/references/technical-review.md',
    'skills/article-editor/references/engineering-example.md',
    'skills/article-editor/references/faces.md',
)
MANIFEST = 'skills/article-editor/references/engineering-example.json'


def read_file(root, name):
    path = root / name
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError('Context must be an in-repository regular file: ' + name)
    if not path.is_file():
        raise ValueError('Required editorial context unavailable: ' + name)
    return path.read_bytes()


def load_context(root, show=False):
    root = Path(root).expanduser().resolve()
    raw_manifest = read_file(root, MANIFEST)
    manifest = json.loads(raw_manifest)
    if (not isinstance(manifest, dict) or manifest.get('schema_version') != 1 or manifest.get('policy_version') != '2.0'
            or not isinstance(manifest.get('files'), dict)
            or set(manifest['files']) != set(PINNED)):
        raise ValueError('Incomplete engineering-policy/example manifest')
    documents = []
    for name in (*PINNED, *CONTEXT):
        raw = read_file(root, name)
        actual = hashlib.sha256(raw).hexdigest()
        if name in PINNED:
            expected = manifest['files'][name]
            if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected):
                raise ValueError('Invalid content pin: ' + name)
            if actual != expected:
                raise ValueError('Policy/example changed; review and repin explicitly: ' + name)
        entry = {'path': name, 'sha256': actual, 'bytes': len(raw),
                 'role': 'authoritative_editorial_standard' if name == PINNED[0]
                 else 'style_example_not_factual_authority' if name in PINNED[1:]
                 else 'operating_context'}
        if show:
            entry['content'] = raw.decode('utf-8')
        documents.append(entry)
    # Each entry reports the exact bytes read. No mutable-file set is claimed
    # to be an atomic Git snapshot, and no media pin is silently rewritten.
    return {'state': 'LOCAL_CONTEXT_LOADED', 'schema_version': 1,
            'source': 'local working files; not a remote Git pin',
            'manifest_sha256': hashlib.sha256(raw_manifest).hexdigest(),
            'remote_activation': False, 'article_acceptance': 'NOT_ASSESSED',
            'documents': documents}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument('--show', action='store_true', help='Emit the documents for the author/reviewers to read')
    args = parser.parse_args()
    try:
        result = load_context(args.root, args.show)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'state': 'CONTEXT_UNAVAILABLE', 'reason': str(error)}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
