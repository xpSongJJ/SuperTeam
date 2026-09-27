"""Validate the team skill inventory or export three self-contained role bundles."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from urllib.parse import unquote

ROLES = ('planner', 'frontend', 'backend')
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
LINK = re.compile(r"""\[[^\]]*\]\(((?:<[^>
]+>|[^\s)]+)(?:[ 	]+(?:"[^"]*"|'[^']*'))?[ 	]*)\)""")




def strip_inline_code(text):
    runs = list(re.finditer(r'`+', text))
    result, cursor = [], 0
    for index, opening in enumerate(runs):
        if opening.start() < cursor:
            continue
        closing = next((r for r in runs[index + 1:] if len(r[0]) == len(opening[0])), None)
        if closing is not None:
            result.append(text[cursor:opening.start()])
            cursor = closing.end()
    result.append(text[cursor:])
    return ''.join(result)


def markdown_links(text):
    """Read the documented inline/reference link subset, excluding code examples."""
    lines, fence = [], None
    for line in text.splitlines():
        if fence is not None:
            if re.fullmatch(r'\s{0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}[ \t]*', line):
                fence = None
            continue
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if marker:
            fence = marker[1]
            continue
        lines.append(line)
    prose = strip_inline_code('\n'.join(lines))
    definitions = dict(re.findall(r'^\s{0,3}\[([^\]]+)\]:\s*(.+)$', prose, re.M))
    definitions = {' '.join(k.lower().split()): v for k, v in definitions.items()}
    inline = LINK.findall(prose)
    if len(inline) != len(re.findall(r'\[[^\]]*\]\(', prose)):
        raise ValueError('Unsupported inline link syntax; encode spaces and parentheses in destinations')
    destinations = list(definitions.values()) + inline
    for label, reference in re.findall(r'\[([^\]]+)\]\[([^\]]*)\]', prose):
        key = ' '.join((reference or label).lower().split())
        if key not in definitions:
            raise ValueError(f'Undefined Markdown reference: {reference or label}')
    for raw in destinations:
        match = re.fullmatch(r"(?:<([^>]+)>|(\S+))(?:\s+(?:\"[^\"]*\"|'[^']*'))?", raw.strip())
        if not match:
            raise ValueError(f'Unsupported link syntax: {raw}; use a relative URL with an optional quoted title')
        yield match[1] or match[2]


def validate_links(item, boundary=None):
    for link in markdown_links(item.read_text(encoding='utf-8-sig')):
        if re.match(r'^(https?://|mailto:|#)', link, re.I):
            continue
        relative = unquote(link.split('#', 1)[0])
        if not relative or relative.startswith('/') or '\\' in relative or ':' in relative:
            raise ValueError(f'Absolute or invalid local link in {item}: {link}')
        if boundary is None:
            raise ValueError(f'Instructions must be self-contained; put local resources in a skill: {item}: {link}')
        target = (item.parent / relative).resolve()
        if not target.is_relative_to(boundary.resolve()) or not target.is_file():
            raise ValueError(f'Nonportable or missing link in {item}: {link}')


def source(root, relative):
    if not isinstance(relative, str) or '\\' in relative or ':' in relative:
        raise ValueError(f'Expected a relative POSIX path: {relative!r}')
    parts = PurePosixPath(relative)
    if parts.is_absolute() or '..' in parts.parts or not parts.parts:
        raise ValueError(f'Path escapes source: {relative}')
    path = root.joinpath(*parts.parts)
    if not path.resolve().is_relative_to(root.resolve()) or not path.exists():
        raise ValueError(f'Missing or external source: {relative}')
    if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
        raise ValueError(f'Symlink source not supported: {relative}')
    return path


def metadata(path):
    text = path.read_text(encoding='utf-8-sig')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError(f'Missing skill frontmatter: {path}')
    fields = {}
    for line in match[1].splitlines():
        key, sep, value = line.partition(':')
        if not sep or key not in ('name', 'description') or key in fields:
            raise ValueError(f'Use unique name/description frontmatter fields: {path}')
        fields[key] = value.strip().strip('"\'')
    name = fields.get('name', '')
    description = fields.get('description', '')
    if not NAME.fullmatch(name) or len(name) > 64 or name != path.parent.name:
        raise ValueError(f'Invalid skill name: {path}')
    if not description.startswith('Use when ') or len(description) > 1024:
        raise ValueError(f'Invalid trigger description: {path}')
    return fields


def check(root):
    root = Path(root).resolve()
    try:
        manifest = json.loads((root / 'team.json').read_text(encoding='utf-8-sig'))
        if manifest['schema_version'] != 1 or set(manifest['roles']) != set(ROLES):
            raise ValueError('team.json must declare schema 1 and exactly three roles')
        if not source(root, manifest['common_instructions']).is_file():
            raise ValueError('Common instructions must be a file')
        validate_links(source(root, manifest['common_instructions']))
        shared = manifest['shared_skills']
        if not isinstance(shared, list) or not shared:
            raise ValueError('Shared skills must be a nonempty list')
        inventory = []
        for path in shared:
            if not path.startswith('skills/shared/'):
                raise ValueError('Shared skills belong under skills/shared')
            inventory.append(path)
        for role, config in manifest['roles'].items():
            if not source(root, config['instructions']).is_file():
                raise ValueError(f'Missing instructions for {role}')
            validate_links(source(root, config['instructions']))
            if not isinstance(config['skills'], list) or not config['skills']:
                raise ValueError(f'Missing skills for {role}')
            for path in config['skills']:
                if not path.startswith(f'skills/{role}/'):
                    raise ValueError(f'Wrong skill binding for {role}: {path}')
                inventory.append(path)
        if len(inventory) != len(set(inventory)):
            raise ValueError('Duplicate skill binding')
        names = set()
        for relative in inventory:
            folder = source(root, relative)
            entry = source(root, relative + '/SKILL.md')
            name = metadata(entry)['name']
            if name in names:
                raise ValueError(f'Duplicate flattened skill name: {name}')
            names.add(name)
            for item in folder.rglob('*'):
                if item.is_symlink():
                    raise ValueError(f'Symlink in skill: {item}')
                if item.is_file() and item.suffix == '.md':
                    validate_links(item, folder)

        discovered = {p.parent.relative_to(root).as_posix() for p in (root / 'skills').rglob('SKILL.md')}
        if discovered != set(inventory):
            raise ValueError(f'Unbound or missing skills: {sorted(discovered ^ set(inventory))}')
    except (KeyError, TypeError, AttributeError, OSError, json.JSONDecodeError) as exc:
        raise ValueError(f'Invalid team sources: {exc}') from exc
    return manifest


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(root, out):
    root, out = Path(root).resolve(), Path(out).resolve()
    manifest = check(root)
    if out == root or any(out.is_relative_to(root / p) for p in ('agents', 'skills', 'scripts', 'tests', 'docs', 'evals', '.git')):
        raise ValueError('Output must be outside source directories, e.g. dist/team-v1')
    if out.exists():
        raise ValueError(f'Refusing to overwrite {out}; choose a new output directory')
    common = source(root, manifest['common_instructions']).read_text(encoding='utf-8-sig')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.team-build-', dir=out.parent) as temporary:
        staging = Path(temporary) / 'payload'
        for role in ROLES:
            config = manifest['roles'][role]
            selected = manifest['shared_skills'] + config['skills']
            bundle = staging / role
            (bundle / 'skills').mkdir(parents=True)
            instructions = common + '\n\n' + source(root, config['instructions']).read_text(encoding='utf-8-sig')
            instructions += '\n\n## Bound skills\n\n' + '\n'.join('- ' + Path(p).name for p in selected) + '\n'
            (bundle / 'instructions.md').write_text(instructions, encoding='utf-8')
            for relative in selected:
                folder = source(root, relative)
                shutil.copytree(folder, bundle / 'skills' / folder.name)
            checksums = {p.relative_to(bundle).as_posix(): digest(p) for p in sorted(bundle.rglob('*')) if p.is_file()}
            (bundle / 'bundle.json').write_text(json.dumps({'schema_version': 1, 'role': role, 'skills': [Path(p).name for p in selected], 'sha256': checksums}, indent=2) + '\n', encoding='utf-8')
        if out.exists():
            raise ValueError(f'Output appeared during build: {out}')
        staging.rename(out)

    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['check', 'build'])
    p.add_argument('--out', type=Path, default=Path('dist/team-v1'))
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        if args.command == 'build':
            print(build(root, args.out))
        else:
            manifest = check(root)
            count = len(manifest['shared_skills']) + sum(len(r['skills']) for r in manifest['roles'].values())
            print(f'Validated {len(manifest["roles"])} roles and {count} self-contained skills')
    except (ValueError, OSError) as exc:
        p.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
