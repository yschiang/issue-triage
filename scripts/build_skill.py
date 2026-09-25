#!/usr/bin/env python3
"""Build the Claude skill from the repo.

Copies the three HTML pages into skills/issue-triage/assets/, regenerates
references/sop.md, and writes dist/issue-triage-v<version>.skill (a zip).

Usage: python3 scripts/build_skill.py
"""
import shutil, subprocess, sys, zipfile, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
skill = root / 'skills' / 'issue-triage'
assets = skill / 'assets'
assets.mkdir(exist_ok=True)
for name in ['index.html', 'executive-summary.html', 'triage-wizard.html']:
    shutil.copy2(root / name, assets / name)
subprocess.run([sys.executable, str(root / 'scripts' / 'html_to_md.py')], check=True)
version = (root / 'VERSION').read_text(encoding='utf-8').strip()
dist = root / 'dist'; dist.mkdir(exist_ok=True)
out = dist / f'issue-triage-v{version}.skill'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(skill.rglob('*')):
        if p.is_file() and p.name != '.DS_Store':
            z.write(p, pathlib.Path('issue-triage') / p.relative_to(skill))
print(f'built {out.relative_to(root)}')
