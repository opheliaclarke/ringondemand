#!/usr/bin/env python3
"""Regenerate negatives.html from NEGATIVES.md.
Run after adding a new dated block: `python3 adcopy/build-negatives-page.py`
Source of truth = NEGATIVES.md. The HTML is just a copy-button view of it."""
import re, html, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

md = open('NEGATIVES.md').read()
base = re.search(r'## 📋 BASELINE BLOCK.*?```\n(.*?)```', md, re.S).group(1).strip('\n')
rounds_section = re.search(r'## 📌 Dated optimization rounds(.*?)\n## ⚠️', md, re.S).group(1)
rounds = []
for m in re.finditer(r'### 🗓️ (.+?)\n(.*?)```\n(.*?)```', rounds_section, re.S):
    desc = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', m.group(2).strip())
    desc = re.sub(r'`(.+?)`', r'<code>\1</code>', desc)
    body = m.group(3).strip('\n')
    rounds.append((m.group(1).strip(), desc, body, len(body.strip().splitlines())))
base_n = len(base.strip().splitlines())

def card(idx, title, desc, body, n, frozen=False):
    tag = '<span class="frozen">frozen baseline</span>' if frozen else '<span class="new">new</span>'
    return f'''
  <section class="card">
    <div class="head">
      <h2>{html.escape(title)} <span class="badge">{n} terms</span> {tag}</h2>
      <button class="copy" data-target="blk{idx}">📋 Copy</button>
    </div>
    <p class="desc">{desc}</p>
    <pre id="blk{idx}">{html.escape(body)}</pre>
  </section>'''

cards = [card(0, 'Baseline — initial load', 'Already pasted into the account. Leave it frozen. Only copy this if you ever rebuild the list from scratch.', base, base_n, frozen=True)]
for i,(t,d,b,n) in enumerate(rounds, 1): cards.append(card(i,t,d,b,n))

STYLE = ''':root{--bg:#0f1420;--card:#1a2130;--line:#2b3447;--txt:#e6ebf2;--mut:#9aa6b8;--acc:#3b82f6;--grn:#22c55e}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}.wrap{max-width:820px;margin:0 auto;padding:24px 16px 80px}header h1{font-size:22px;margin:0 0 4px}header p{color:var(--mut);margin:0 0 24px}.how{background:#16203a;border:1px solid #284067;border-radius:10px;padding:12px 16px;margin-bottom:28px;color:#cdd9ee;font-size:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:20px}.head{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}.head h2{font-size:16px;margin:0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}.badge{background:#243049;color:var(--mut);font-size:12px;padding:2px 8px;border-radius:20px;font-weight:600}.new{background:#10331f;color:#5be08a;font-size:11px;padding:2px 8px;border-radius:20px}.frozen{background:#33240f;color:#e0b35b;font-size:11px;padding:2px 8px;border-radius:20px}.desc{color:var(--mut);font-size:13px;margin:8px 0 12px}.desc code{background:#0c1120;padding:1px 5px;border-radius:4px;color:#cdd9ee}.copy{background:var(--acc);color:#fff;border:0;padding:8px 16px;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;white-space:nowrap}.copy:hover{filter:brightness(1.1)}.copy.done{background:var(--grn)}pre{background:#0c1120;border:1px solid var(--line);border-radius:8px;padding:12px;max-height:300px;overflow:auto;font:12px/1.45 ui-monospace,Menlo,Consolas,monospace;color:#cdd9ee;margin:0}footer{color:var(--mut);font-size:12px;text-align:center;margin-top:30px}'''
SCRIPT = '''document.querySelectorAll('.copy').forEach(function(b){b.addEventListener('click',function(){var x=document.getElementById(b.dataset.target).innerText;var d=function(){b.textContent='\\u2705 Copied!';b.classList.add('done');setTimeout(function(){b.textContent='\\ud83d\\udccb Copy';b.classList.remove('done')},1800)};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(x).then(d,function(){f(x,d)})}else{f(x,d)}})});function f(x,d){var t=document.createElement('textarea');t.value=x;document.body.appendChild(t);t.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(t);d()}'''

page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>RingOnDemand — Negative Keywords (by date)</title><style>{STYLE}</style></head>
<body><div class="wrap">
  <header><h1>\U0001f6b0 RingOnDemand — Negative Keywords</h1>
  <p>Shared list <code style="color:#cdd9ee">Plumbing_Master_Negs</code> · applied to all campaigns · one copy button per date</p></header>
  <div class="how"><b>How to use:</b> each date below is one optimization round. Hit <b>\U0001f4cb Copy</b> → in Google Ads open
  <b>Tools → Shared library → Negative keyword lists → Plumbing_Master_Negs → Edit</b> → paste → Save.
  Match types are already built in. Newest round is at the top.</div>
  {''.join(cards)}
  <footer>Generated from <code>NEGATIVES.md</code> · keep the source of truth in git</footer>
</div><script>{SCRIPT}</script></body></html>'''
open('negatives.html','w').write(page)
print(f"negatives.html rebuilt — baseline {base_n}, {len(rounds)} dated round(s)")
