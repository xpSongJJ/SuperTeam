import importlib.util
import json
import hashlib
from unittest.mock import patch
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('team', ROOT / 'scripts/team.py')
team = importlib.util.module_from_spec(spec)
spec.loader.exec_module(team)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'source'
        self.root.mkdir()
        (self.root / 'agents').mkdir()
        (self.root / 'agents/common.md').write_text('Shared instruction', encoding='utf-8')
        self.manifest = {'schema_version': 1, 'common_instructions': 'agents/common.md', 'shared_skills': ['skills/shared/evidence'], 'roles': {}}
        for role in ('planner', 'frontend', 'backend'):
            (self.root / f'agents/{role}.md').write_text(f'{role} instruction', encoding='utf-8')
            self.manifest['roles'][role] = {'instructions': f'agents/{role}.md', 'skills': [f'skills/{role}/{role}-work']}
            self.skill(f'skills/{role}/{role}-work')
        self.skill('skills/shared/evidence')
        self.save()

    def skill(self, path):
        folder = self.root / path
        folder.mkdir(parents=True)
        (folder / 'SKILL.md').write_text(f'---\nname: {folder.name}\ndescription: Use when work needs {folder.name}.\n---\n\n# Work\n', encoding='utf-8')

    def save(self):
        (self.root / 'team.json').write_text(json.dumps(self.manifest), encoding='utf-8')

    def test_exports_three_self_contained_packages_and_shared_instructions(self):
        assets = self.root / 'skills/shared/evidence/references'
        assets.mkdir()
        (assets / 'record.md').write_text('Proof', encoding='utf-8')
        skill = self.root / 'skills/shared/evidence/SKILL.md'
        skill.write_text(skill.read_text() + '\n[Record](references/record.md)\n', encoding='utf-8')
        out = Path(self.tmp.name) / 'out'
        team.build(self.root, out)
        for role in ('planner', 'frontend', 'backend'):
            bundle = out / role
            text = (bundle / 'instructions.md').read_text(encoding='utf-8')
            self.assertIn('Shared instruction', text)
            self.assertIn(f'{role} instruction', text)
            self.assertTrue((bundle / 'skills/evidence/references/record.md').exists())
            self.assertTrue((bundle / f'skills/{role}-work/SKILL.md').exists())
            self.assertEqual(len(list((bundle / 'skills').iterdir())), 2)
            inventory = json.loads((bundle / 'bundle.json').read_text())
            self.assertEqual(inventory['role'], role)
            self.assertIn('instructions.md', inventory['sha256'])
            self.assertEqual(inventory['sha256']['instructions.md'], hashlib.sha256((bundle / 'instructions.md').read_bytes()).hexdigest())

    def test_rejects_missing_skill(self):
        (self.root / 'skills/backend/backend-work/SKILL.md').unlink()
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_rejects_path_escape(self):
        self.manifest['common_instructions'] = '../secret.md'
        self.save()
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_rejects_wrong_role_binding(self):
        self.manifest['roles']['frontend']['skills'] = ['skills/backend/backend-work']
        self.save()
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_rejects_unbound_skill(self):
        self.skill('skills/planner/forgotten')
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_rejects_broken_local_reference(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        p.write_text(p.read_text() + '\n[Template](missing.md)\n')
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_rejects_cross_skill_reference_that_would_break_import(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        p.write_text(p.read_text() + '\n[Other](../../planner/planner-work/SKILL.md)\n')
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_refuses_to_overwrite_existing_output(self):
        out = Path(self.tmp.name) / 'out'
        out.mkdir()
        sentinel = out / 'user-file.txt'
        sentinel.write_text('keep')
        with self.assertRaises(ValueError):
            team.build(self.root, out)
        self.assertEqual(sentinel.read_text(), 'keep')

    def test_validates_before_writing(self):
        (self.root / 'agents/frontend.md').unlink()
        out = Path(self.tmp.name) / 'out'
        with self.assertRaises(ValueError):
            team.build(self.root, out)
        self.assertFalse(out.exists())

    def test_rejects_output_inside_sources(self):
        with self.assertRaises(ValueError):
            team.build(self.root, self.root / 'skills/export')

    def test_names_are_unique_after_flattening(self):
        self.skill('skills/planner/evidence')
        self.manifest['roles']['planner']['skills'].append('skills/planner/evidence')
        self.save()
        with self.assertRaises(ValueError):
            team.check(self.root)



    def test_rejects_absolute_skill_reference(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        p.write_text(p.read_text() + f'\n[Self]({p.as_posix()})\n')
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_rejects_broken_reference_style_link(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        p.write_text(p.read_text() + '\n[Record][record]\n\n[record]: missing.md\n')
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_accepts_titles_and_ignores_code_examples(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        (p.parent / 'record.md').write_text('record')
        p.write_text(p.read_text() + '\n[Record](record.md "Proof")\n```markdown\n[Example](missing.md)\n```\n`[Example](also-missing.md)`\n')
        team.check(self.root)

    def test_rejects_instruction_file_dependency(self):
        p = self.root / 'agents/planner.md'
        p.write_text('[Guide](common.md)')
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_invalid_encoding_fails_before_output_is_created(self):
        (self.root / 'agents/backend.md').write_bytes(bytes([255]))
        out = Path(self.tmp.name) / 'out'
        with self.assertRaises(ValueError):
            team.build(self.root, out)
        self.assertFalse(out.exists())

    def test_failed_copy_leaves_no_partial_output_and_can_retry(self):
        out = Path(self.tmp.name) / 'out'
        with patch.object(team.shutil, 'copytree', side_effect=OSError('simulated copy failure')):
            with self.assertRaises(OSError):
                team.build(self.root, out)
        self.assertFalse(out.exists())
        team.build(self.root, out)
        self.assertTrue((out / 'backend/bundle.json').exists())



    def test_backtick_runs_do_not_hide_real_broken_links(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        p.write_text(p.read_text() + '\n``a```b`` [Broken](missing.md) `x`\n')
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_parentheses_in_quoted_link_title(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        (p.parent / 'record.md').write_text('record')
        p.write_text(p.read_text() + '\n[Record](record.md "Proof (v1)")\n')
        team.check(self.root)

    def test_fence_with_info_string_does_not_close_code_block(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        p.write_text(p.read_text() + '\n```markdown\n```python\n[Example](missing.md)\n```\n')
        team.check(self.root)



    def test_apostrophe_in_destination_cannot_hide_missing_file(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        p.write_text(p.read_text() + "\n[Broken](missing's.md)\n")
        with self.assertRaises(ValueError):
            team.check(self.root)

    def test_unsupported_link_syntax_is_rejected_not_ignored(self):
        p = self.root / 'skills/shared/evidence/SKILL.md'
        p.write_text(p.read_text() + '\n[Broken](missing file.md)\n')
        with self.assertRaises(ValueError):
            team.check(self.root)


if __name__ == '__main__':
    unittest.main()
