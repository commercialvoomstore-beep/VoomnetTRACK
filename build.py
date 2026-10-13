#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble la plateforme VOOMNET en un seul fichier index.html autonome."""
import base64, os, re, sys

ROOT = "/home/user"
SRC  = os.path.join(ROOT, "src")
ASSETS = os.path.join(ROOT, "assets")

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- logos (dimensions réelles après conversion) --------------------------
from PIL import Image
def dims(p):
    with Image.open(p) as im:
        return im.size

logos = {
    "TECH":  ("logo-voomnet-technology.jpg", "tech"),
    "DIR":   ("logo-direction.jpg",          "direction"),  # photo de M. WILFRIED GADOU (service Direction)
    "ENCACI": ("logo-encaci.jpg",            "encaci"),
    "FORM":  ("logo-voomnet-formation.jpg",  "form"),
    "HEAD":  ("logo-track-pdf.jpg",          "head"),   # logo officiel VOOMNET Track (fond blanc, pour le PDF)
}

full_w, full_h = dims(os.path.join(ASSETS, "logo-track.webp"))

repl = {}
for key, (fname, _) in logos.items():
    p = os.path.join(ASSETS, fname)
    w, h = dims(p)
    repl["__LOGO_%s__" % key] = "data:image/jpeg;base64," + b64(p)
    repl["__W_%s__" % key] = str(w)
    repl["__H_%s__" % key] = str(h)

# --- police Inter + kit de marque VOOMNET Track (logo officiel) -------------
repl["__FONT_INTER__"] = b64(os.path.join(ASSETS, "inter-latin.woff2"))
repl["__LOGO_TRACK__"]   = "data:image/webp;base64," + b64(os.path.join(ASSETS, "logo-track.webp"))
repl["__W_LOGO_TRACK__"] = str(full_w); repl["__H_LOGO_TRACK__"] = str(full_h)
repl["__SYMBOL_TRACK__"] = "data:image/webp;base64," + b64(os.path.join(ASSETS, "symbol.webp"))
repl["__FAVICON_TRACK__"]= "data:image/png;base64,"  + b64(os.path.join(ASSETS, "favicon-128.png"))
repl["__APPLE_ICON__"]   = "data:image/png;base64,"  + b64(os.path.join(ASSETS, "favicon-180.png"))

parts = [open(os.path.join(SRC, f), encoding="utf-8").read()
         for f in ("part1_head.html", "part2_body.html", "part3_core.js.html",
                   "part3c_api.js.html", "part3b_dash.js.html", "part4_pdf.js.html")]

html = "\n".join(parts)

missing = set(re.findall(r"__[A-Z_]+__", html))
for k, v in repl.items():
    html = html.replace(k, v)
missing -= set(repl.keys())
if missing:
    print("!! Placeholders non remplacés :", missing, file=sys.stderr)

out = os.path.join(ROOT, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html écrit : %.1f Ko" % (os.path.getsize(out) / 1024))
print("Placeholders remplacés :", len(repl))
