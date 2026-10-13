#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planche de contrôle : rend tous les symboles en grand."""
import asyncio, re, sys
from playwright.async_api import async_playwright

OUT = sys.argv[1] if len(sys.argv) > 1 else "test/diag/v36-icones.png"

async def main():
    src = open("src/part3_core.js.html", encoding='utf-8').read()
    icons = re.search(r'const ICONS = \{[\s\S]*?\n\};', src).group(0)
    names = re.findall(r"^\s*([a-zA-Z0-9_]+): '", icons, re.M)
    page = """<!doctype html><meta charset=utf-8><style>
    :root{--accent:#C9A227;--primary:#4A2A63}
    body{font-family:system-ui;background:#F8F7FA;margin:0;padding:24px}
    .g{display:flex;flex-wrap:wrap;gap:14px}
    .c{width:134px;background:#fff;border:1px solid #EBE6F0;border-radius:14px;padding:12px 10px 9px;text-align:center}
    .b{width:66px;height:66px;border-radius:20px;margin:0 auto 9px;display:grid;place-items:center;
       background:linear-gradient(155deg,#fff 8%,#F1ECF5 100%);border:1px solid #DFD2E9;color:#6B4A82;
       box-shadow:0 1px 2px rgba(74,42,99,.08),0 5px 12px -7px rgba(74,42,99,.28),inset 0 1px 0 #fff}
    svg.ic{width:34px;height:34px}
    .n{font:600 10.5px/1.3 ui-monospace;color:#6B7280;word-break:break-all}</style>
    <div class=g>""" + "".join(
        '<div class=c><div class=b><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></svg></div><div class=n>' + n + '</div></div>'
        for n in names) + """</div>
    <script>""" + icons + """
    const ks=""" + str(names).replace("'", '"') + """;
    document.querySelectorAll('svg.ic').forEach((s,i)=>{ s.innerHTML=ICONS[ks[i]]||''; });
    </script>"""
    open("/tmp/icons2.html", "w", encoding='utf-8').write(page)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await (await b.new_context(viewport={"width": 1000, "height": 1000}, device_scale_factor=2)).new_page()
        await pg.goto("file:///tmp/icons2.html")
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=OUT, full_page=True)
        print("symboles rendus :", len(names), "→", OUT)
        await b.close()

asyncio.run(main())
