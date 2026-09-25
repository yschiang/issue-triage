#!/usr/bin/env python3
"""Bump the shared version: three HTML pages, VERSION, SKILL.md, CHANGELOG.

Usage: python3 scripts/bump_version.py 1.13 "一句話說明改了什麼"
Then run: python3 scripts/build_skill.py
"""
import sys, pathlib, datetime
root = pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv) < 3:
    sys.exit('usage: bump_version.py <new-version> "<summary>"')
new, summary = sys.argv[1], sys.argv[2]
old = (root / 'VERSION').read_text(encoding='utf-8').strip()
if old == new:
    sys.exit(f'version already {new}')
edits = {
    'index.html': [(f'作業指南 v{old}', f'作業指南 v{new}')],
    'executive-summary.html': [(f'Executive Summary · v{old}', f'Executive Summary · v{new}')],
    'triage-wizard.html': [(f'Triage Wizard v{old} · 規則同《Issue Triage 與交付流程》v{old}',
                            f'Triage Wizard v{new} · 規則同《Issue Triage 與交付流程》v{new}')],
    'skills/issue-triage/SKILL.md': [(f'version: "{old}"', f'version: "{new}"'),
                                     (f'SOP（v{old}）', f'SOP（v{new}）'),
                                     (f'現為 {old}', f'現為 {new}')],
}
for rel, reps in edits.items():
    p = root / rel; s = p.read_text(encoding='utf-8')
    for a, b in reps:
        if a not in s:
            sys.exit(f'{rel}: "{a}" not found; fix the file before bumping')
        s = s.replace(a, b, 1)
    p.write_text(s, encoding='utf-8')
(root / 'VERSION').write_text(new + '\n', encoding='utf-8')
cl = root / 'CHANGELOG.md'; c = cl.read_text(encoding='utf-8')
c = c.replace('# Changelog\n\n', f'# Changelog\n\n## v{new} — {datetime.date.today().isoformat()}\n\n- {summary}\n\n', 1)
cl.write_text(c, encoding='utf-8')
print(f'{old} → {new}. Next: python3 scripts/build_skill.py, then commit and git tag v{new}')
