#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.6b — Corrections ciblées : voiture, trajet, jauge, carburant, portefeuille."""
import re

FIX = {
# voiture : roues réellement sous la caisse, vitrage, phare
"car": '<path d="M4.6 14.8v-.8c0-.8.4-1.5 1.1-1.9l1.8-.9 1.8-3.3A2.6 2.6 0 0 1 11.6 6.6h3.2a2.6 2.6 0 0 1 2.3 1.3l1.8 3.3 1.8.9c.7.4 1.1 1.1 1.1 1.9v.8z" fill="currentColor" fill-opacity=".16"/><path d="M4.6 14.8v-.8c0-.8.4-1.5 1.1-1.9l1.8-.9 1.8-3.3A2.6 2.6 0 0 1 11.6 6.6h3.2a2.6 2.6 0 0 1 2.3 1.3l1.8 3.3 1.8.9c.7.4 1.1 1.1 1.1 1.9v.8"/><path d="M7.9 9.4h5.4l1.5 3H6.6z" fill="currentColor" fill-opacity=".3" stroke="none"/><path d="M4.4 14.8h1.2M18.4 14.8h1.2" stroke-width="1.6"/><circle cx="8.6" cy="15.6" r="2.3" fill="#fff"/><circle cx="15.4" cy="15.6" r="2.3" fill="#fff"/><circle cx="8.6" cy="15.6" r="2.3"/><circle cx="15.4" cy="15.6" r="2.3"/><circle cx="8.6" cy="15.6" r=".85" fill="currentColor" stroke="none"/><circle cx="15.4" cy="15.6" r=".85" fill="currentColor" stroke="none"/>',
# trajet : route balisée + épingle de destination dorée
"route": '<path d="M5.4 20.4c3.4-.8 4.6-3.8 4.6-7 0-3.2 1.4-5.4 4.2-5.4" fill="none" stroke-width="3.6" stroke-opacity=".16"/><path d="M5.4 20.4c3.4-.8 4.6-3.8 4.6-7 0-3.2 1.4-5.4 4.2-5.4" fill="none" stroke-width="1.6" stroke-dasharray="2.6 2.6"/><circle cx="4.4" cy="20.8" r="2" fill="currentColor"/><path d="M17.4 11.8c-2.1 0-3.8-1.7-3.8-3.8s1.7-3.8 3.8-3.8 3.8 1.7 3.8 3.8c0 2.5-2.6 5.1-3.8 6.3z" fill="var(--accent)" fill-opacity=".22" stroke="var(--accent)" stroke-width="1.5"/><circle cx="17.4" cy="8" r="1.3" fill="var(--accent)" stroke="none"/>',
# jauge : cadran gradué + aiguille dorée
"gauge": '<path d="M3.6 18.6a8.4 8.4 0 0 1 16.8 0z" fill="currentColor" fill-opacity=".14"/><path d="M3.6 18.6a8.4 8.4 0 0 1 16.8 0"/><path d="M5.2 18.6H3.6M6.6 14.2l-1.1-1.1M12 11.8V10.2M17.4 14.2l1.1-1.1M18.8 18.6h1.6" stroke-width="1.4" stroke-opacity=".7"/><path d="M12 18.6l3.6-5.2" stroke="var(--accent)" stroke-width="2"/><circle cx="12" cy="18.6" r="1.6" fill="currentColor" stroke="none"/><path d="M3 21h18" stroke-width="1.5" stroke-opacity=".45"/>',
# carburant : pompe avec vitre, tuyau et pistolet
"fuel": '<path d="M4.8 20.6V5.4a2 2 0 0 1 2-2h5.6a2 2 0 0 1 2 2v15.2z" fill="currentColor" fill-opacity=".14"/><path d="M4.8 20.6V5.4a2 2 0 0 1 2-2h5.6a2 2 0 0 1 2 2v15.2"/><path d="M3.2 20.6h13.2" stroke-width="1.9"/><rect x="7" y="6.6" width="5.2" height="4.6" rx="1.2" fill="currentColor" fill-opacity=".38" stroke="none"/><path d="M14.4 8.6h1.8a2.4 2.4 0 0 1 2.4 2.4v4.6a1.8 1.8 0 0 0 3.6 0v-3.2" stroke-width="1.7"/><path d="M20.6 12.4h1.8" stroke-width="1.7"/>',
# portefeuille : rabat + poche à carte + fermoir doré
"wallet": '<path d="M4.6 8.2h14.8v10.4a1.8 1.8 0 0 1-1.8 1.8H6.4a1.8 1.8 0 0 1-1.8-1.8z" fill="currentColor" fill-opacity=".16"/><path d="M4.6 8.2 15 5a1.7 1.7 0 0 1 2.1 1.2l.3 2" fill="currentColor" fill-opacity=".3"/><path d="M4.6 8.2 15 5a1.7 1.7 0 0 1 2.1 1.2l.3 2"/><path d="M4.6 8.2h14.8v10.4a1.8 1.8 0 0 1-1.8 1.8H6.4a1.8 1.8 0 0 1-1.8-1.8z"/><rect x="13" y="11.4" width="7.6" height="4.6" rx="1.7" fill="currentColor" fill-opacity=".3"/><circle cx="16.8" cy="13.7" r="1.15" fill="currentColor" stroke="none"/><path d="M7.4 13.7h3.4" stroke-width="1.5" stroke-opacity=".6"/>',
}

p = 'src/part3_core.js.html'
s = open(p, encoding='utf-8').read()
for name, svg in FIX.items():
    m = re.search(r"(\n  %s: ')(.*?)('\n|\n)" % re.escape(name), s, re.S)
    if not m:
        m = re.search(r"(\n  %s: ')(.*?)(',\n)" % re.escape(name), s, re.S)
    assert m, "icône introuvable : " + name
    s = s[:m.start(2)] + svg + s[m.end(2):]
    print("  ✓", name, "corrigée")
open(p, 'w', encoding='utf-8').write(s)
print("✓ corrections appliquées")
