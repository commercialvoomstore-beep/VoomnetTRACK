#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.9b — Intégration : véhicule qui rebondit sur le train avant + symboles or royal / argent."""
import re

# ---------------------------------------------------------------- 1. le SVG
src = open('test/vehicule-v5.html', encoding='utf-8').read()
svg = src[src.index('<svg'):src.index('</svg>') + 6]
svg = svg.replace('viewBox="0 0 560 250"', 'viewBox="16 92 502 136"')
svg = re.sub(r'\n\s*', ' ', svg)
svg = svg.replace('> <', '><').strip()

p2 = 'src/part2_body.html'
b = open(p2, encoding='utf-8').read()
i = b.index('<svg viewBox="16 94 502 130"')
j = b.index('</svg>', i) + 6
b = b[:i] + svg + b[j:]
open(p2, 'w', encoding='utf-8').write(b)
print("✓ véhicule animé intégré dans l'en-tête")

# ---------------------------------------------------------------- 2. animations CSS
p1 = 'src/part1_head.html'
h = open(p1, encoding='utf-8').read()
old = h[h.index('.hv-route{animation:hvDash 7s linear infinite}'):h.index('@media(prefers-reduced-motion:reduce){.hv-route{animation:none}}')]
new = '''/* ---- véhicule : la caisse rebondit sur le train avant, le pneu s'écrase ---- */
.hv-body{animation:hvBounce 1.6s cubic-bezier(.33,0,.35,1) infinite;transform-origin:396px 190px;transform-box:view-box}
@keyframes hvBounce{
  0%   {transform:translateY(0)     rotate(0deg)}
  14%  {transform:translateY(-6.4px) rotate(-.52deg)}
  30%  {transform:translateY(1.1px)  rotate(.10deg)}
  44%  {transform:translateY(-2.6px) rotate(-.24deg)}
  58%  {transform:translateY(.5px)   rotate(.04deg)}
  72%  {transform:translateY(-1px)   rotate(-.09deg)}
  86%  {transform:translateY(.15px)  rotate(.01deg)}
  100% {transform:translateY(0)     rotate(0deg)}
}
.hv-tyre{animation:hvTyre 1.6s cubic-bezier(.33,0,.35,1) infinite;transform-box:fill-box;transform-origin:center}
@keyframes hvTyre{
  0%,100%{transform:scale(1,1)}
  14%{transform:scale(1.035,.925)}
  30%{transform:scale(.995,1.02)}
  44%{transform:scale(1.012,.985)}
  58%{transform:scale(1,1)}
}
.hv-shadow{animation:hvShadow 1.6s cubic-bezier(.33,0,.35,1) infinite;transform-box:view-box;transform-origin:264px 196px}
@keyframes hvShadow{
  0%,100%{transform:scaleX(1);opacity:.055}
  14%{transform:scaleX(.955);opacity:.036}
  30%{transform:scaleX(1.012);opacity:.062}
}
.hv-route{animation:hvDash 6.5s linear infinite}
@keyframes hvDash{to{stroke-dashoffset:-132}}
'''
h = h.replace(old, new, 1)
h = h.replace('@media(prefers-reduced-motion:reduce){.hv-route{animation:none}}',
              '@media(prefers-reduced-motion:reduce){.hv-route,.hv-body,.hv-tyre,.hv-shadow{animation:none}}')
open(p1, 'w', encoding='utf-8').write(h)
print("✓ animations du véhicule installées (rebond 1,6 s)")

# ---------------------------------------------------------------- 3. or royal / argent
h = open(p1, encoding='utf-8').read()
def gild(old, new, label):
    global h
    assert old in h, "introuvable : " + label
    h = h.replace(old, new, 1); print("  ✓", label)

# les icônes des cartes de données passent à l'or royal (les remplissages d'accent restent dorés)
gild('.kpi .ic-wrap .ic{width:22px;height:22px;stroke-width:1.5}',
     '.kpi .ic-wrap .ic{width:22px;height:22px;stroke-width:1.5;color:var(--gold-real)}', "icônes KPI → or royal")
gild('.card-h .ic-chip .ic{width:20px;height:20px;stroke-width:1.5}',
     '.card-h .ic-chip .ic{width:20px;height:20px;stroke-width:1.5;color:var(--gold-real)}', "icônes de titres → or royal")
gild('.stat-tile .ic-wrap .ic{width:21px;height:21px;stroke-width:1.5}',
     '.stat-tile .ic-wrap .ic{width:21px;height:21px;stroke-width:1.5;color:var(--gold-real)}', "tuiles d'analyse → or royal")
# les détails secondaires passent à l'argent (hiérarchie visuelle)
gild('.chip .ic{width:14px;height:14px;color:var(--faint)}',
     '.chip .ic{width:14px;height:14px;color:var(--silver)}', "puces de filtre → argent")
gild('.tl-meta .ic{width:13px;height:13px;color:var(--faint)}',
     '.tl-meta .ic{width:13px;height:13px;color:var(--silver)}', "détails du flux → argent")
open(p1, 'w', encoding='utf-8').write(h)
print("✓ palette appliquée : or royal pour les données, argent pour les détails")

# ---------------------------------------------------------------- 4. version
b = open(p2, encoding='utf-8').read()
b = b.replace('VOOMNET Track · v3.8', 'VOOMNET Track · v3.9').replace('VOOMNET Track v3.8', 'VOOMNET Track v3.9')
open(p2, 'w', encoding='utf-8').write(b)
print("✓ version → v3.9")
