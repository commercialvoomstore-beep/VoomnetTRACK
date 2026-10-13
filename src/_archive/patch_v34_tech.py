#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.4 — Design technologique « gestion & suivi transport »."""
p = 'src/part1_head.html'
s = open(p, encoding='utf-8').read()

CSS = r'''
/* ===================== v3.4 · SUIVI TRANSPORT (design tech) ===================== */
.tech-live{
  display:inline-flex;align-items:center;gap:7px;font-size:11.6px;font-weight:650;letter-spacing:.02em;
  color:#2F7D5B;background:#EEF8F2;border:1px solid #D5EBDD;border-radius:var(--pill);padding:5px 11px;white-space:nowrap;
}
.tech-live .pulse{width:7px;height:7px;border-radius:50%;background:#39A06F;box-shadow:0 0 0 0 rgba(57,160,111,.5);animation:ptPulse 2.1s var(--ease) infinite}
@keyframes ptPulse{0%{box-shadow:0 0 0 0 rgba(57,160,111,.42)}70%{box-shadow:0 0 0 7px rgba(57,160,111,0)}100%{box-shadow:0 0 0 0 rgba(57,160,111,0)}}

/* --- chaîne de traitement --- */
.flow{display:flex;align-items:stretch;gap:0;margin-top:4px;flex-wrap:wrap}
.fnode{
  flex:1 1 148px;min-width:132px;background:var(--surface);border:1px solid var(--line-2);border-radius:var(--r-md);
  padding:13px 14px 12px;position:relative;cursor:default;transition:border-color .18s var(--ease),box-shadow .18s var(--ease),transform .18s var(--ease);
}
.fnode[data-clic]{cursor:pointer}
.fnode[data-clic]:hover{border-color:var(--primary-200);box-shadow:var(--sh-xs);transform:translateY(-1px)}
.fnode .fh{display:flex;align-items:center;gap:9px;margin-bottom:9px}
.fnode .fico{
  width:30px;height:30px;flex:0 0 30px;border-radius:9px;display:grid;place-items:center;
  background:linear-gradient(150deg,#fff,var(--surface-3));border:1px solid var(--line-2);color:var(--secondary);
}
.fnode .fico .ic{width:16px;height:16px;stroke-width:1.8}
.fnode .fl{font-size:11.4px;font-weight:660;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.fnode .fv{font-size:25px;font-weight:760;letter-spacing:-.02em;color:var(--ink);font-variant-numeric:tabular-nums;line-height:1.05}
.fnode .fs{font-size:11.6px;color:var(--muted);margin-top:3px;font-variant-numeric:tabular-nums}
.fnode .fbar{height:5px;border-radius:3px;background:var(--surface-3);overflow:hidden;margin-top:10px}
.fnode .fbar i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,var(--primary),var(--secondary));transition:width .7s var(--ease-out)}
.fnode.gold{background:linear-gradient(160deg,#FFFDF6,#FFF9E9);border-color:#EBD9A6}
.fnode.gold .fico{background:linear-gradient(150deg,#fff,var(--accent-50));border-color:#EBD9A6;color:var(--accent-600)}
.fnode.gold .fbar i{background:linear-gradient(90deg,var(--accent),var(--accent-300))}
.fnode.dim{opacity:.72}
.fconn{
  flex:0 0 34px;align-self:center;height:2px;margin:0 2px;position:relative;
  background-image:linear-gradient(90deg,var(--line-2) 0 6px,transparent 6px 11px);background-size:11px 2px;background-repeat:repeat-x;
}
.fconn::after{
  content:"";position:absolute;right:-3px;top:50%;width:6px;height:6px;margin-top:-3px;
  border-top:1.6px solid var(--line-2);border-right:1.6px solid var(--line-2);transform:rotate(45deg);
}
@media(max-width:860px){.fconn{display:none}.fnode{flex:1 1 100%}}

/* --- trajet (visualisation) --- */
.route-viz{display:inline-flex;align-items:center;gap:7px;max-width:100%;vertical-align:middle}
.route-viz .rv-pt{
  font-size:12.4px;font-weight:600;color:var(--ink-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:132px;
}
.route-viz .rv-a{width:6px;height:6px;border-radius:50%;background:var(--surface);border:2px solid var(--secondary);flex:0 0 6px}
.route-viz .rv-b{width:7px;height:7px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 3px var(--accent-50);flex:0 0 7px}
.route-viz .rv-line{flex:1 1 34px;min-width:26px;height:10px}
.route-viz .rv-line path{stroke:var(--primary-200);stroke-width:1.6;fill:none;stroke-dasharray:3 3;stroke-linecap:round}
.route-viz .rv-line circle{fill:var(--accent)}
.route-viz.mini .rv-pt{font-size:12.1px;max-width:104px}
.cell-route .route-viz{width:100%}

/* --- flux de mobilité (timeline) --- */
.timeline{position:relative;margin-top:2px}
.tl-item{position:relative;display:flex;gap:13px;padding:0 0 15px}
.tl-item:last-child{padding-bottom:0}
.tl-rail{position:relative;flex:0 0 26px;display:flex;justify-content:center}
.tl-rail::before{
  content:"";position:absolute;top:24px;bottom:-15px;width:2px;
  background-image:linear-gradient(180deg,var(--line-2) 0 5px,transparent 5px 10px);background-size:2px 10px;
}
.tl-item:last-child .tl-rail::before{display:none}
.tl-dot{
  width:26px;height:26px;border-radius:9px;display:grid;place-items:center;z-index:1;
  background:linear-gradient(150deg,#fff,var(--surface-3));border:1px solid var(--line-2);color:var(--secondary);
}
.tl-dot .ic{width:14px;height:14px;stroke-width:1.9}
.tl-item.is-gold .tl-dot{background:linear-gradient(150deg,#fff,var(--accent-50));border-color:#EBD9A6;color:var(--accent-600)}
.tl-item.is-ok .tl-dot{background:#EEF8F2;border-color:#D5EBDD;color:#2F7D5B}
.tl-body{
  flex:1;min-width:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);
  padding:11px 13px;transition:border-color .18s var(--ease),box-shadow .18s var(--ease);
}
.tl-body:hover{border-color:var(--line-2);box-shadow:var(--sh-xs)}
.tl-top{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:7px}
.tl-date{font-size:11.8px;font-weight:700;color:var(--primary);font-variant-numeric:tabular-nums;letter-spacing:.01em}
.tl-meta{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-top:7px;font-size:12.1px;color:var(--muted)}
.tl-meta b{color:var(--ink);font-weight:650;font-variant-numeric:tabular-nums}
.tl-meta .sep{width:3px;height:3px;border-radius:50%;background:var(--line-2);flex:0 0 3px}
.tl-motif{font-size:12.4px;color:var(--ink-2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tl-amt{margin-left:auto;font-weight:750;color:var(--ink);font-variant-numeric:tabular-nums}

/* --- statistiques réseau --- */
.net-stats{display:flex;flex-direction:column;gap:12px}
.net-row{display:flex;flex-direction:column;gap:6px}
.net-top{display:flex;align-items:center;gap:9px;font-size:12.6px}
.net-top .nb{font-weight:700;font-variant-numeric:tabular-nums;margin-left:auto;color:var(--ink)}
.net-bar{height:7px;border-radius:4px;background:var(--surface-3);overflow:hidden}
.net-bar i{display:block;height:100%;border-radius:4px;transition:width .7s var(--ease-out)}
.net-legend{display:flex;gap:14px;flex-wrap:wrap;margin-top:14px;padding-top:13px;border-top:1px dashed var(--line-2);font-size:11.8px;color:var(--muted)}
.net-legend b{color:var(--ink);font-variant-numeric:tabular-nums}

/* --- boîte d'aide « enregistrer sur l'appareil » --- */
.save-steps{display:flex;flex-direction:column;gap:12px}
.sstep{display:flex;gap:12px;align-items:flex-start;background:var(--surface-2);border:1px solid var(--line);border-radius:var(--r-md);padding:13px 15px}
.sstep .n{
  width:24px;height:24px;flex:0 0 24px;border-radius:50%;display:grid;place-items:center;
  background:var(--primary);color:#fff;font-size:12.4px;font-weight:750;
}
.sstep b{display:block;font-size:13.4px;margin-bottom:3px}
.sstep .tx{font-size:12.2px;color:var(--muted);line-height:1.5}
.save-url{
  display:flex;align-items:center;gap:9px;margin-top:13px;background:var(--surface-2);
  border:1px dashed var(--line-2);border-radius:var(--r-md);padding:9px 12px;flex-wrap:wrap;
}
.save-url .ic{width:15px;height:15px;color:var(--accent-600);flex:0 0 15px}
.save-url code{font-size:11.6px;color:var(--ink-2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1 1 180px;min-width:0}
'''
s = s.replace('</style>', CSS + '</style>', 1)
open(p, 'w', encoding='utf-8').write(s)
print("✓ CSS v3.4 (suivi transport + boîte d'aide)")

# ---------------------------------------------------------------- structure HTML
p2 = 'src/part2_body.html'
b = open(p2, encoding='utf-8').read()

anchor = '        <!-- 4. GRAPHIQUES -->'
NEW = '''        <!-- 3bis. SUIVI TRANSPORT — chaîne de traitement (design technologique) -->
        <div class="section reveal" style="--i:2">
          <div class="card pad-lg">
            <div class="card-h">
              <div class="t">
                <h3><span class="ic-chip"><span class="ic" data-ico="route"></span></span> Suivi transport — chaîne de traitement</h3>
                <div class="desc">De l'enregistrement au règlement. Cliquez sur une étape pour ouvrir le registre correspondant.</div>
              </div>
              <span class="tech-live"><span class="pulse"></span> SUIVI ACTIF</span>
            </div>
            <div class="flow" id="flowTrack"></div>
          </div>
        </div>

        <!-- 3ter. FLUX DE MOBILITÉ — trajets suivis en continu -->
        <div class="section reveal" style="--i:3">
          <div class="grid g-32">
            <div class="card pad-lg">
              <div class="card-h">
                <div class="t">
                  <h3><span class="ic-chip"><span class="ic" data-ico="bolt"></span></span> Flux de mobilité récent</h3>
                  <div class="desc">Trajet, moyen de transport, montant et statut — les derniers mouvements enregistrés</div>
                </div>
                <button class="btn btn-ghost btn-sm" data-goto="registre"><span class="ic" data-ico="arrowRight"></span> Tout le registre</button>
              </div>
              <div class="timeline" id="mobTimeline"></div>
            </div>

            <div class="card pad-lg">
              <div class="card-h">
                <div class="t">
                  <h3><span class="ic-chip"><span class="ic" data-ico="gauge"></span></span> Réseau &amp; trajets</h3>
                  <div class="desc">Intensité des liaisons et moyens de transport de la période</div>
                </div>
              </div>
              <div class="net-stats" id="netStats"></div>
            </div>
          </div>
        </div>

'''
assert anchor in b
b = b.replace(anchor, NEW + anchor, 1)
open(p2, 'w', encoding='utf-8').write(b)
print("✓ structure : « Suivi transport » + « Flux de mobilité » + « Réseau & trajets »")
