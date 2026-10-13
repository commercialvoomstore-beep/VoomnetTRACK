#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.4 — rendu du suivi transport (chaîne, flux, réseau) + trajets visuels dans le tableau."""
import re

# ------------------------------------------------------------------ 1. routeViz (noyau)
p = 'src/part3_core.js.html'
s = open(p, encoding='utf-8').read()

ROUTE = r'''/* Visualisation de trajet (suivi transport) : départ ● — pointillé — ◉ arrivée */
function routeViz(from,to,opts){
  opts=opts||{};
  const a=esc(from||"—"), b=esc(to||"—");
  return '<span class="route-viz'+(opts.mini?" mini":"")+'">'+
    '<span class="rv-a"></span>'+
    '<span class="rv-pt" title="'+a+'">'+a+'</span>'+
    '<svg class="rv-line" viewBox="0 0 60 10" preserveAspectRatio="none" aria-hidden="true">'+
      '<path d="M1 5 H59"/><circle cx="30" cy="5" r="2.1"/></svg>'+
    '<span class="rv-pt" title="'+b+'">'+b+'</span>'+
    '<span class="rv-b"></span></span>';
}
'''
anchor = 'function tableHTML(list,opts){'
assert anchor in s
s = s.replace(anchor, ROUTE + anchor, 1)

# trajet visuel dans le tableau (colonne Trajet)
old_cell = '''      (opts.compact? "" : '<td class="cell-route">'+esc((t.from||"—")+" → "+(t.to||"—"))+
        (Number(t.km)? ' <span class="small">· '+fmtN(t.km)+' km</span>':'')+'</td>')+'''
new_cell = '''      (opts.compact? "" : '<td class="cell-route">'+routeViz(t.from,t.to,{mini:true})+
        (Number(t.km)? ' <span class="small">· '+fmtN(t.km)+' km</span>':'')+'</td>')+'''
assert old_cell in s, 'cellule trajet introuvable'
s = s.replace(old_cell, new_cell, 1)
open(p, 'w', encoding='utf-8').write(s)
print("✓ routeViz + colonne Trajet visuelle")

# ------------------------------------------------------------------ 2. rendu du suivi
p2 = 'src/part3b_dash.js.html'
d = open(p2, encoding='utf-8').read()

TRACK = r'''
/* ============ SUIVI TRANSPORT (design technologique) ============ */
function renderTracking(m){
  const base=dashTrips(m), n=base.length, tot=sum(base);
  const just=base.filter(t=>t.justif==="OUI"), reg=base.filter(t=>t.statut==="REGLE");
  const att=base.filter(t=>t.statut==="A_REGLE"), attTot=sum(att);
  const pct=x=> n? Math.round(x/n*100) : 0;

  /* --- 1. Chaîne de traitement --- */
  const steps=[
    {ico:"list",  l:"Enregistrés",  v:n,               s:"sortie(s) sur la période", p:pct(n),        gold:false},
    {ico:"shield",l:"Justifiés",    v:just.length,     s:pct(just.length)+"% avec justificatif", p:pct(just.length), gold:false},
    {ico:"check", l:"Réglés",       v:reg.length,      s:fmtN(sum(reg))+" "+DB.params.devise, p:pct(reg.length), gold:false},
    {ico:"clock", l:"À régler",     v:att.length,      s:fmtN(attTot)+" "+DB.params.devise, p:pct(att.length), gold:true,
      clic:{vue:"registre",statut:"A_REGLE"}}
  ];
  const elF=$("#flowTrack");
  if(elF){
    elF.innerHTML = steps.map((st,i)=>
      '<div class="fnode'+(st.gold? " gold":"")+(st.v?"":" dim")+'"'+(st.clic? ' data-clic="1" data-go-vue="'+st.clic.vue+'" data-go-statut="'+st.clic.statut+'"':'')+'>'+
        '<div class="fh"><span class="fico">'+ic(st.ico)+'</span><span class="fl">'+st.l+'</span></div>'+
        '<div class="fv">'+fmtN(st.v)+'</div><div class="fs">'+esc(st.s)+'</div>'+
        '<div class="fbar"><i style="width:'+st.p+'%"></i></div>'+
      '</div>' + (i<steps.length-1? '<div class="fconn"></div>' : "")
    ).join("");
    /* clic : ouvre le registre pré-filtré (filtre global, jamais un écran séparé) */
    $$("#flowTrack [data-clic]").forEach(el=>{
      el.onclick=()=>{
        const st=el.dataset.goStatut;
        const sel=$("#fStatut"); if(sel && st) sel.value=st;
        go("registre");
        if(typeof applyRegistreFilters==="function"){ try{ applyRegistreFilters(); }catch(e){} }
        toast("Registre filtré", st==="A_REGLE"? "Déplacements en attente de règlement." : "Déplacements réglés.","info");
      };
    });
  }

  /* --- 2. Flux de mobilité récent --- */
  const elT=$("#mobTimeline");
  if(elT){
    const last=base.slice().sort((a,b)=>(b.date||"").localeCompare(a.date||"")).slice(0,6);
    elT.innerHTML = last.length? last.map(t=>{
      const s=svc(t.service);
      const cls = t.statut==="REGLE"? " is-ok" : (t.justif==="NON"? " is-gold":"");
      const ico = t.statut==="REGLE"? "check" : (t.justif==="NON"? "alert":"clock");
      return '<div class="tl-item'+cls+'">'+
        '<div class="tl-rail"><span class="tl-dot">'+ic(ico)+'</span></div>'+
        '<div class="tl-body">'+
          '<div class="tl-top">'+
            '<span class="tl-date">'+esc(dateFR(t.date))+'</span>'+
            serviceTag(t.service)+statusTag(t.statut)+
            (t.justif==="NON"? '<span class="tag" style="background:var(--warn-bg);color:#8A6F14">'+ic("alert")+'Justificatif à fournir</span>':"")+
          '</div>'+
          '<div class="route-viz" style="width:100%">'+
            '<span class="rv-a"></span><span class="rv-pt" title="'+esc(t.from||"")+'">'+esc(t.from||"—")+'</span>'+
            '<svg class="rv-line" viewBox="0 0 60 10" preserveAspectRatio="none" aria-hidden="true"><path d="M1 5 H59"/><circle cx="30" cy="5" r="2.1"/></svg>'+
            '<span class="rv-pt" title="'+esc(t.to||"")+'">'+esc(t.to||"—")+'</span><span class="rv-b"></span>'+
          '</div>'+
          '<div class="tl-motif" title="'+esc(t.motif)+'">'+esc(t.motif)+'</div>'+
          '<div class="tl-meta">'+
            '<span>'+ic("user")+'</span>'+esc(t.agent||"—")+
            '<span class="sep"></span><span>'+ic("fuel")+'</span>'+esc(t.transport||"—")+
            (Number(t.km)? '<span class="sep"></span>'+fmtN(t.km)+' km':'')+
            '<span class="tl-amt">'+fmtN(t.montant)+' '+esc(DB.params.devise)+'</span>'+
          '</div>'+
        '</div></div>';
    }).join("") : emptyState("route","Aucun mouvement sur la période","Ajustez la période ou les filtres.");
    hydrateIcons(elT);
  }

  /* --- 3. Réseau & trajets --- */
  const elN=$("#netStats");
  if(elN){
    const parTrajet={}, parTrans={};
    base.forEach(t=>{
      const k=(t.from&&t.to)? (t.from+" → "+t.to) : null;
      if(k){ parTrajet[k]=parTrajet[k]||{n:0,m:0}; parTrajet[k].n++; parTrajet[k].m+=Number(t.montant)||0; }
      const tr=t.transport||"—"; parTrans[tr]=parTrans[tr]||{n:0,m:0}; parTrans[tr].n++; parTrans[tr].m+=Number(t.montant)||0;
    });
    const topT=Object.entries(parTrajet).sort((a,b)=>b[1].n-a[1].n).slice(0,3);
    const topM=Object.entries(parTrans).sort((a,b)=>b[1].n-a[1].n).slice(0,3);
    const maxN=topT.length? topT[0][1].n : 1, maxM=topM.length? topM[0][1].n : 1;
    const rowsT=topT.map(([k,v])=>
      '<div class="net-row"><div class="net-top"><span class="ic" style="width:14px;height:14px;color:var(--secondary)">'+ic("route")+'</span>'+
      '<span class="route-viz mini" style="gap:5px"><span class="rv-a"></span>'+
      '<span class="rv-pt" style="max-width:96px">'+esc(k.split(" → ")[0])+'</span>'+
      '<svg class="rv-line" viewBox="0 0 60 10" preserveAspectRatio="none"><path d="M1 5 H59"/><circle cx="30" cy="5" r="2.1"/></svg>'+
      '<span class="rv-pt" style="max-width:96px">'+esc(k.split(" → ")[1]||"")+'</span><span class="rv-b"></span></span>'+
      '<span class="nb">'+v.n+'× · '+fmtN(v.m)+'</span></div>'+
      '<div class="net-bar"><i style="width:'+(v.n/maxN*100).toFixed(0)+'%;background:linear-gradient(90deg,var(--primary),var(--secondary))"></i></div></div>').join("");
    const rowsM=topM.map(([k,v])=>
      '<div class="net-row"><div class="net-top"><span class="ic" style="width:14px;height:14px;color:var(--accent-600)">'+ic("fuel")+'</span>'+
      '<span>'+esc(k)+'</span><span class="nb">'+v.n+'× · '+fmtN(v.m)+'</span></div>'+
      '<div class="net-bar"><i style="width:'+(v.n/maxM*100).toFixed(0)+'%;background:linear-gradient(90deg,var(--accent),var(--accent-300))"></i></div></div>').join("");
    elN.innerHTML = (topT.length? rowsT + '<div style="height:4px"></div>' : "") + (topM.length? rowsM : "") +
      '<div class="net-legend">'+
        '<span>Distance cumulée : <b>'+fmtN(sumKm(base))+' km</b></span>'+
        '<span>Coût moyen : <b>'+fmtN(n? tot/n:0)+' '+esc(DB.params.devise)+'</b></span>'+
        '<span>Trajets distincts : <b>'+Object.keys(parTrajet).length+'</b></span>'+
      '</div>';
    if(!topT.length && !topM.length) elN.innerHTML = emptyState("gauge","Aucune liaison enregistrée","Renseignez les lieux de départ et d'arrivée des déplacements.");
    hydrateIcons(elN);
  }
}
'''

anchor2 = 'function renderDashboard(){'
assert anchor2 in d
d = d.replace(anchor2, TRACK + '\n' + anchor2, 1)

# appel depuis renderDashboard : après les KPI
anchor3 = '  /* --- 8. Derniers déplacements --- */'
assert anchor3 in d
d = d.replace(anchor3, '  /* --- 7bis. Suivi transport (chaîne, flux, réseau) --- */\n  renderTracking(m);\n\n' + anchor3, 1)
open(p2, 'w', encoding='utf-8').write(d)
print("✓ renderTracking() + appel dans renderDashboard()")
