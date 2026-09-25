#!/usr/bin/env python3
"""Regenerate skills/issue-triage/references/sop.md from index.html (the source of truth).

Usage: python3 scripts/html_to_md.py      (requires pandoc)
"""
import re, subprocess, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
html = (root / 'index.html').read_text(encoding='utf-8')
version = re.search(r'作業指南 v([\d.]+)', html)
version = version.group(1) if version else '?'
body = html[html.index('<main'):html.index('<footer')]
body = re.sub(r'<aside class="sidebar">.*?</aside>', '', body, flags=re.S)
body = re.sub(r'<div class="mobile-nav">.*?</div>', '', body, flags=re.S)
def svg_to_note(m):
    t = re.search(r'<title[^>]*>(.*?)</title>', m.group(0), flags=re.S)
    return f'<p><em>[圖：{t.group(1).strip() if t else "流程圖"}]</em></p>'
body = re.sub(r'<svg.*?</svg>', svg_to_note, body, flags=re.S)
body = re.sub(r'<button[^>]*>.*?</button>', '', body, flags=re.S)
body = re.sub(r'<details([^>]*)><summary>(.*?)</summary>', r'<section\1><h2>\2</h2>', body, flags=re.S)
body = body.replace('</details>', '</section>')
body = re.sub(r'<h4[^>]*>', '<h4>', body)
body = re.sub(r'<div class="page-head">.*?</div>\s*</div>', '', body, flags=re.S)
body = re.sub(r'<dt>(.*?)</dt>\s*<dd>', r'<p><strong>\1</strong>：', body, flags=re.S)
body = body.replace('</dd>', '</p>').replace('<dl class="task task-head">', '').replace('<dl class="task">', '').replace('</dl>', '')
body = re.sub(r'</?div[^>]*>', '', body)
md = subprocess.run(['pandoc', '-f', 'html', '-t', 'gfm', '--wrap=none'], input=body, text=True, capture_output=True, check=True).stdout
md = re.sub(r'^</?div[^>]*>\s*$', '', md, flags=re.M)
md = re.sub(r'^## 定級速查', '**定級速查**', md, flags=re.M)
md = re.sub(r'\n{3,}', '\n\n', md).strip()
head = f'# Issue Triage 與交付流程 — SOP v{version}\n\n此檔由 `scripts/html_to_md.py` 從 `index.html` 產生；改內容請改 HTML 再重跑，不要直接改這裡。\n\n'
out = root / 'skills' / 'issue-triage' / 'references' / 'sop.md'
out.write_text(head + md + '\n', encoding='utf-8')
print(f'{out.relative_to(root)} regenerated (v{version})')
