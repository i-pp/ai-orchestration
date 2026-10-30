"""Context integrity tests; no article command is executed and no quality verdict is inferred."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('editorial_context', Path(__file__).with_name('load_policy.py'))
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repository'
        pins = {}
        for name in (*context.PINNED, *context.CONTEXT):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            raw = ('Fixture ' + name + '\n').encode()
            path.write_bytes(raw)
            if name in context.PINNED:
                pins[name] = hashlib.sha256(raw).hexdigest()
        self.manifest = self.root / context.MANIFEST
        self.manifest.write_text(json.dumps({'schema_version': 1, 'policy_version': '1.0', 'files': pins}))

    def test_loaded_bytes_and_roles_without_quality_or_remote_claim(self):
        result = context.load_context(self.root, show=True)
        self.assertFalse(result['remote_activation'])
        self.assertEqual(result['article_acceptance'], 'NOT_ASSESSED')
        for entry in result['documents']:
            self.assertEqual(entry['content'].encode(), (self.root / entry['path']).read_bytes())
        self.assertEqual(result['documents'][0]['role'], 'authoritative_editorial_standard')
        self.assertEqual(result['documents'][1]['role'], 'style_example_not_factual_authority')

    def test_missing_canonical_policy_does_not_fall_back(self):
        (self.root / context.PINNED[0]).unlink()
        with self.assertRaisesRegex(ValueError, 'unavailable'):
            context.load_context(self.root)

    def test_modified_standard_or_example_needs_new_review(self):
        for name in context.PINNED:
            with self.subTest(name=name):
                path = self.root / name
                raw = path.read_bytes()
                path.write_bytes(raw + b'changed')
                with self.assertRaisesRegex(ValueError, 'changed'):
                    context.load_context(self.root)
                path.write_bytes(raw)

    def test_incomplete_or_additional_pin_rejected(self):
        data = json.loads(self.manifest.read_text())
        data['files']['../external'] = '0' * 64
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            context.load_context(self.root)

    def test_symlink_cannot_substitute_external_policy(self):
        path = self.root / context.PINNED[0]
        outside = Path(self.tmp.name) / 'outside.md'
        outside.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'in-repository'):
            context.load_context(self.root)

    def test_missing_operating_context_does_not_claim_complete_load(self):
        (self.root / context.CONTEXT[3]).unlink()
        with self.assertRaisesRegex(ValueError, 'unavailable'):
            context.load_context(self.root)


if __name__ == '__main__':
    unittest.main()
