"""Run text-only decision probes in fresh Codex CLI sessions; not an E2E harness."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


def run(root, out, phase, sample, timeout, cases):
    prompt = (root / 'evals/scenarios.txt').read_text(encoding='utf-8-sig')
    if cases:
        lines = prompt.splitlines()
        prompt = '\n'.join(line for line in lines if ':' not in line or line.split(':', 1)[0] in cases)
    if phase == 'guided':
        parts = []
        for folder in ('agents', 'skills'):
            for p in sorted((root / folder).rglob('*.md')):
                parts.append(f'FILE: {p.relative_to(root).as_posix()}\n{p.read_text(encoding="utf-8")}')
        prompt = 'Apply the following team instructions and skills to the exercise.\n' + '\n\n'.join(parts) + '\n\n' + prompt
    label = phase + ('-' + '-'.join(cases) if cases else '')
    target = out / f'{label}-{sample}'
    prompt_path = target.with_suffix('.prompt.txt')
    prompt_path.write_text(prompt, encoding='utf-8')
    started = time.time()
    command = [shutil.which('codex') or 'codex', 'exec', '--ephemeral', '--skip-git-repo-check', '--sandbox', 'read-only', '--color', 'never', '--json', '-o', str(target.with_suffix('.txt')), '-']
    try:
        with tempfile.TemporaryDirectory(prefix='team-probe-') as workspace:
            result = subprocess.run(command, input=prompt, cwd=workspace, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=timeout)
        target.with_suffix('.events.jsonl').write_text(result.stdout, encoding='utf-8')
        target.with_suffix('.stderr.txt').write_text(result.stderr, encoding='utf-8')
        record = {'phase': phase, 'sample': sample, 'exit_code': result.returncode, 'seconds': round(time.time()-started, 2), 'response_present': target.with_suffix('.txt').exists() and target.with_suffix('.txt').stat().st_size > 0}
    except (subprocess.TimeoutExpired, OSError) as exc:
        record = {'phase': phase, 'sample': sample, 'error': str(exc), 'seconds': round(time.time()-started, 2)}
    target.with_suffix('.meta.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps(record), flush=True)
    return record.get('exit_code') == 0 and record.get('response_present', False)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase', choices=['baseline', 'guided'])
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--samples', type=int, default=5)
    p.add_argument('--start', type=int, default=1)
    p.add_argument('--timeout', type=int, default=240)
    p.add_argument('--cases', nargs='+', choices=['P1', 'P2', 'C1', 'D1', 'F1', 'B1', 'R1', 'I1', 'V1'])
    args = p.parse_args()
    if args.samples < 1 or args.samples > 10:
        p.error('samples must be 1..10')
    root = Path(__file__).resolve().parents[1]
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda n: run(root, args.out, args.phase, n, args.timeout, args.cases), range(args.start, args.start + args.samples)))
    return 0 if all(results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
