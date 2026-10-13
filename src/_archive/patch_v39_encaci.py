#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.9 — 1) VOOMSTORE supprimé, remplacé par ENCACI (nouveau logo fourni)
          2) Vraie couleur or pour les icônes de navigation + support argent."""
import re, os, shutil

# =============================================================== 1. build.py
p = 'build.py'
s = open(p, encoding='utf-8').read()
old = '    "STORE": ("logo-voomstore.jpg",          "store"),'
new = '    "ENCACI": ("logo-encaci.jpg",            "encaci"),   # remplace VOOMSTORE (service inactif)'
assert old in s, "ligne STORE introuvable dans build.py"
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(s)
print("✓ build.py : logo ENCACI embarqué à la place de VOOMSTORE")

# =============================================================== 2. noyau
p = 'src/part3_core.js.html'
c = open(p, encoding='utf-8').read()

# 2.a — table des logos embarqués
c = c.replace('  store: { uri:"__LOGO_STORE__",  w:__W_STORE__,  h:__H_STORE__  },',
              '  encaci:{ uri:"__LOGO_ENCACI__", w:__W_ENCACI__, h:__H_ENCACI__ },   /* ex-VOOMSTORE */')

# 2.b — définition du service (couleur or royal pour rester dans l\'identité)
old_svc = '''  { id:"VOOMSTORE", code:"COM", name:"VOOMSTORE", short:"Voomstore",
    role:"Service Commercial", color:"#5A93B8", color2:"#5A93B8", logo:"store", icon:"briefcase" },'''
new_svc = '''  { id:"ENCACI", code:"ENC", name:"ENCACI", short:"ENCACI",
    role:"Service Partenaire", color:"#9A7A15", color2:"#C9A227", logo:"encaci", icon:"building" },'''
assert old_svc in c, "définition VOOMSTORE introuvable"
c = c.replace(old_svc, new_svc, 1)

# 2.c — collaborateurs & véhicules rattachés à l\'ancien service
c = c.replace('{ nom:"Mme BAMBA Aïcha", service:"VOOMSTORE", actif:true }',
              '{ nom:"Mme BAMBA Aïcha", service:"ENCACI", actif:true }')
c = c.replace('service:"VOOMSTORE"', 'service:"ENCACI"')

open(p, 'w', encoding='utf-8').write(c)
print("✓ noyau : service ENCACI + collaborateurs + véhicules mis à jour")

# =============================================================== 3. PDF
p = 'src/part4_pdf.js.html'
d = open(p, encoding='utf-8').read()
old = 'tech:"VOOMNET TECHNOLOGY", store:"VOOMSTORE", form:"VOOMNET FORMATION", head:"VOOMNET"'
new = 'tech:"VOOMNET TECHNOLOGY", encaci:"ENCACI", form:"VOOMNET FORMATION", head:"VOOMNET"'
assert old in d, "table PDF introuvable"
d = d.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(d)
print("✓ moteur PDF : ENCACI référencé")

# =============================================================== 4. contrôle
restes = []
for f in ('src/part1_head.html','src/part2_body.html','src/part3_core.js.html',
          'src/part3b_dash.js.html','src/part4_pdf.js.html','build.py'):
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'VOOMSTORE|Voomstore|logo-voomstore|"store"|__LOGO_STORE__', t):
        restes.append(f + " → " + t[max(0,m.start()-40):m.end()+40].replace("\n"," "))
print("✓ contrôle :", "aucune référence VOOMSTORE restante" if not restes else "À NETTOYER :\n  " + "\n  ".join(restes))

# =============================================================== 5. couleurs « or » et « argent »
p = 'src/part1_head.html'
h = open(p, encoding='utf-8').read()
if '--gold-real' not in h:
    h = h.replace('--accent:#C9A227;', '''--accent:#C9A227;          /* or principal (identité) */
  --gold-real:#B58A2B;        /* OR ROYAL : icônes décoratives */
  --gold-real-2:#E3C05C;
  --silver:#8E93A1;           /* ARGENT : variante sobre */
  --silver-2:#C6CAD4;''', 1)
    open(p, 'w', encoding='utf-8').write(h)
    print("✓ palette : or royal + argent ajoutés")
else:
    print("· palette déjà complétée")
