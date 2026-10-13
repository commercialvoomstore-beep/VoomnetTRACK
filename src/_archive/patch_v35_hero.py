#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.5 — En-tête de tableau de bord « mobilité corporate » : typographie éditoriale,
bandeau de données raffiné et illustration de véhicule vectorielle."""
import re

# ---------------------------------------------------------------- 1. le véhicule
svgh = open('test/vehicule.html', encoding='utf-8').read()
svg = svgh[svgh.index('<svg'):svgh.index('</svg>') + 6]
# portée des identifiants + animation du trajet
svg = (svg.replace('id="bp"', 'id="hv-bp"').replace('url(#bp)', 'url(#hv-bp)')
          .replace('id="wash"', 'id="hv-wash"').replace('url(#wash)', 'url(#hv-wash)')
          .replace('id="under"', 'id="hv-under"').replace('url(#under)', 'url(#hv-under)')
          .replace('id="rt"', 'class="hv-route"')
          .replace('viewBox="0 0 560 250"', 'viewBox="0 0 560 238" role="img" aria-label="Suivi des déplacements"'))
svg = svg.replace('  <rect x="0" y="8" width="560" height="204" rx="16" fill="url(#hv-bp)" opacity=".9"/>\n'
                  '  <rect x="0" y="8" width="560" height="204" rx="16" fill="url(#hv-wash)"/>\n', '')
svg = re.sub(r'\n\s*', ' ', svg).replace('> <', '><').strip()
svg = svg.replace('font-family="system-ui"', 'font-family="inherit"')

# ---------------------------------------------------------------- 2. structure
p2 = 'src/part2_body.html'
b = open(p2, encoding='utf-8').read()
start = b.index('        <!-- 1. EN-TÊTE RH -->')
end = b.index('        <!-- 2. FILTRES GLOBAUX')
NEW = '''        <!-- 1. EN-TÊTE RH — identité « mobilité corporate » -->
        <div class="hero reveal" style="--i:0">
          <div class="hero-l">
            <div class="hero-eyebrow"><i></i> Espace RH — contrôle de la mobilité</div>
            <h2 class="hero-title" id="welcomeTitle">Pilotage de la mobilité et des dépenses</h2>
            <p class="hero-sub" id="welcomeSub">Synthèse consolidée des déplacements de l'organisation.</p>
            <div class="hero-stats" id="heroStats"></div>
          </div>
          <div class="hero-r">
            <div class="hero-actions">
              <button class="btn btn-gold" id="qaPdf"><span class="ic" data-ico="pdf"></span> Télécharger le PDF</button>
              <button class="btn btn-primary" data-goto="new"><span class="ic" data-ico="plus"></span> Nouveau déplacement</button>
            </div>
            <div class="hero-art" aria-hidden="true">''' + svg + '''</div>
          </div>
        </div>

'''
b = b[:start] + NEW + b[end:]
open(p2, 'w', encoding='utf-8').write(b)
print("✓ nouvelle structure d'en-tête (hero + illustration)")

# ---------------------------------------------------------------- 3. styles
p1 = 'src/part1_head.html'
h = open(p1, encoding='utf-8').read()
old_start = h.index('.welcome{')
old_end = h.index('@media(max-width:900px){.welcome{grid-template-columns:1fr}.welcome .actions{justify-content:flex-start}}')
old_end = h.index('\n', old_end) + 1
CSS = r'''/* ================= EN-TÊTE ÉDITORIAL (mobilité corporate) ================= */
.hero{
  position:relative;display:grid;grid-template-columns:minmax(0,1fr) clamp(250px,31%,420px);
  gap:26px;align-items:end;padding:30px 34px 24px;border-radius:var(--r-xl);border:1px solid var(--line);
  overflow:hidden;
  background:
    radial-gradient(760px 280px at 4% -10%, #F4EEFB 0%, rgba(244,238,251,0) 62%),
    radial-gradient(560px 220px at 98% 116%, #FBF5E2 0%, rgba(251,245,226,0) 58%),
    var(--surface);
}
.hero::after{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--secondary),var(--accent))}
.hero-eyebrow{
  display:flex;align-items:center;gap:10px;font-size:10.5px;font-weight:750;
  letter-spacing:.18em;text-transform:uppercase;color:var(--secondary)
}
.hero-eyebrow i{display:block;width:26px;height:2px;border-radius:2px;background:linear-gradient(90deg,var(--accent),rgba(201,162,39,.12))}
.hero-title{
  margin:14px 0 0;font-size:clamp(23px,2.1vw,32px);font-weight:790;letter-spacing:-.038em;
  line-height:1.07;color:var(--ink);text-wrap:balance
}
.hero-sub{margin:11px 0 0;font-size:13.3px;line-height:1.62;color:var(--muted);max-width:64ch}
.hero-sub b{color:var(--ink-2);font-weight:640}
.hero-stats{display:flex;flex-wrap:wrap;margin-top:22px;padding-top:16px;border-top:1px solid var(--line)}
.hs{padding:0 22px;border-left:1px solid var(--line);min-width:98px}
.hs:first-child{padding-left:0;border-left:0}
.hs b{display:block;font-size:21px;font-weight:760;letter-spacing:-.032em;line-height:1.1;color:var(--ink);font-variant-numeric:tabular-nums}
.hs b s{text-decoration:none;font-size:11px;font-weight:650;letter-spacing:.06em;color:var(--muted);margin-left:3px}
.hs span{display:block;margin-top:5px;font-size:10.3px;font-weight:680;letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.hs.gold b{color:var(--accent-600)}
.hs.ok b{color:#2F7D5B}
.hero-r{display:flex;flex-direction:column;align-items:flex-end;gap:16px;min-width:0}
.hero-actions{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.hero-art{width:100%;max-width:420px}
.hero-art svg{display:block;width:100%;height:auto;overflow:visible}
.hv-route{animation:hvDash 7s linear infinite}
@keyframes hvDash{to{stroke-dashoffset:-132}}
@media(prefers-reduced-motion:reduce){.hv-route{animation:none}}
@media(max-width:1080px){
  .hero{grid-template-columns:1fr;gap:20px}
  .hero-r{align-items:flex-start}
  .hero-actions{justify-content:flex-start}
  .hero-art{max-width:360px}
}
@media(max-width:760px){
  .hero{padding:24px 20px 20px}
  .hero-art{display:none}
  .hs{padding:0 15px;min-width:0;flex:1 1 44%}
  .hs:nth-child(odd){padding-left:0;border-left:0}
}
'''
h = h[:old_start] + CSS + h[old_end:]
# micro-typographie des cartes KPI (cohérence éditoriale)
h = h.replace('.kpi .lbl{font-size:11.5px;font-weight:650;color:var(--muted);letter-spacing:.02em}',
              '.kpi .lbl{font-size:10.5px;font-weight:720;color:var(--muted);letter-spacing:.13em;text-transform:uppercase}')
h = h.replace('.kpi .val{font-size:25px;font-weight:750;letter-spacing:-.035em;margin-top:14px;color:var(--ink);line-height:1.1}',
              '.kpi .val{font-size:26px;font-weight:760;letter-spacing:-.038em;margin-top:14px;color:var(--ink);line-height:1.08;font-variant-numeric:tabular-nums}')
open(p1, 'w', encoding='utf-8').write(h)
print("✓ styles d'en-tête + micro-typographie KPI")

# ---------------------------------------------------------------- 4. rendu JS
p3 = 'src/part3b_dash.js.html'
d = open(p3, encoding='utf-8').read()
old = d[d.index('  $("#welcomeTitle").innerHTML'):d.index('\n', d.index('$("#welcomePills").innerHTML'))]
old = old[:old.rindex('$("#welcomePills").innerHTML')]
new = '''  $("#welcomeTitle").innerHTML="Pilotage de la mobilité et des dépenses";
  $("#welcomeSub").innerHTML="Synthèse consolidée de <b>"+esc(monthLabel(m))+"</b> — "+
    fmtN(n)+" déplacement"+(n>1?"s":"")+" enregistré"+(n>1?"s":"")+" par "+
    fmtN(agentsActifs.length)+" collaborateur"+(agentsActifs.length>1?"s":"")+", tous services confondus.";
  const hs=function(l,v,u,cls,tip){ return '<div class="hs'+(cls? " "+cls:"")+'"'+(tip? ' title="'+esc(tip)+'"':'')+'>'+
      '<b>'+v+(u? ' <s>'+esc(u)+'</s>':'')+'</b><span>'+l+'</span></div>'; };
  $("#heroStats").innerHTML=
    hs("Déplacements", fmtN(n), "", "", "Nombre de déplacements enregistrés sur la période")+
    hs("Dépenses", fmtN(total), DB.params.devise, "", "Total des dépenses de mobilité de la période")+
    (openList.length
      ? hs("En attente", fmtN(openList.length), "", "gold", fmtN(sum(openList))+" "+DB.params.devise+" à régler")
      : hs("Règlement", "À jour", "", "ok", "Tous les déplacements de la période sont réglés"))+
    hs("Validés", fmtN(okList.length), "", "", "Déplacements réglés sur la période")+
    hs("Distance", fmtN(km), "km", "", "Distance cumulée des trajets renseignés");
'''
d = d.replace(old, new, 1)
d = d.replace('$("#welcomePills").innerHTML', '/* #welcomePills remplacé par #heroStats (v3.5) */ $("#heroStats").innerHTML')
open(p3, 'w', encoding='utf-8').write(d)
print("✓ en-tête dynamique (titre, synthèse, bandeau de 5 indicateurs)")
