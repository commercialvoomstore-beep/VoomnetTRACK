# -*- coding: utf-8 -*-
"""Patch affichage : graphique violet+or, dashboard RH centralisé avec filtres globaux, retrait de Véhicules."""
p = 'src/part3b_dash.js.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  ✓", label)

# ============================================================ 1. GRAPHIQUE ÉVOLUTION
a0 = s.index('/* ---- Graphique d\'évolution (aire lissée + points + tooltips + animation) ---- */')
a1 = s.index('/* ---- Barres groupées par entité (Analyse) ---- */')
new_chart = '''/* ---- Graphique d'évolution : violet doux + or, grille subtile, tooltip, légende ---- */
function areaChart(series, opts){
  opts=opts||{};
  const W=800, H=310, L=66, R=28, T=26, B=48;
  const iw=W-L-R, ih=H-T-B;
  const VIOLET="#6B4A82", VIOLET_D="#4A2A63", GOLD="#C9A227";
  const max = Math.max(1, ...series.map(s=>s.value));
  const pow = Math.pow(10, Math.floor(Math.log10(max)));
  const nice = pow * (max/pow>5?10:5);
  const step = series.length>1? iw/(series.length-1) : iw;
  const x = i => L + (series.length>1? i*step : iw/2);
  const y = v => T + ih - (v/nice)*ih;
  const pts = series.map((s,i)=>[x(i), y(s.value)]);
  const line = smoothPath(pts);
  const area = line + " L"+x(series.length-1).toFixed(1)+" "+(T+ih)+" L"+L+" "+(T+ih)+" Z";
  const total = series.reduce((a,b)=>a+b.value,0);
  const average = series.length? total/series.length : 0;
  const avgY = y(average);

  let grid="", labels="", dots="", hit="";
  for(let g=0; g<=4; g++){
    const gy = T + ih*g/4, val = nice*(1-g/4);
    grid += '<line x1="'+L+'" y1="'+gy.toFixed(1)+'" x2="'+(W-R)+'" y2="'+gy.toFixed(1)+'" stroke="'+
      (g===4? "#E4DEE9":"#F0EBF4")+'" stroke-width="1"'+(g===4?"":' stroke-dasharray="3 6"')+'/>';
    labels += '<text x="'+(L-14)+'" y="'+(gy+4).toFixed(1)+'" text-anchor="end" font-size="11" font-weight="600" fill="#9A95A0">'+esc(fmtShort(val))+'</text>';
  }
  series.forEach((s,i)=>{
    const px=x(i);
    labels += '<text x="'+px.toFixed(1)+'" y="'+(H-16)+'" text-anchor="middle" font-size="11" font-weight="'+(s.current?"700":"600")+
      '" fill="'+(s.current? VIOLET_D:"#9A95A0")+'">'+esc(s.label)+'</text>';
    hit += '<rect x="'+(px-step/2).toFixed(1)+'" y="'+T+'" width="'+step.toFixed(1)+'" height="'+ih+'" fill="transparent" style="cursor:pointer" '+
      'data-tip="'+esc(s.tipLabel||s.label)+'" data-tipv="'+esc(fmtN(s.value)+" "+DB.params.devise)+'" data-tips="'+
      esc((s.count||0)+" déplacement"+(s.count>1?"s":""))+' + (s.nb? " · "+s.nb+" collab." : "")+'" data-x="'+px.toFixed(1)+'" data-y="'+y(s.value).toFixed(1)+'"/>';
  });
  series.forEach((s,i)=>{
    if(!s.value) return;
    const px=x(i), py=y(s.value);
    dots += '<circle class="vt-pt" cx="'+px.toFixed(1)+'" cy="'+py.toFixed(1)+'" r="'+(s.current?5.5:3.8)+'" fill="#fff" stroke="'+
      (s.current? GOLD:VIOLET)+'" stroke-width="'+(s.current?3:2.2)+'"/>';
    if(s.current){
      dots += '<circle cx="'+px.toFixed(1)+'" cy="'+py.toFixed(1)+'" r="11" fill="none" stroke="'+GOLD+'" stroke-width="1.2" opacity=".38"/>'+
        '<text x="'+px.toFixed(1)+'" y="'+(py-20).toFixed(1)+'" text-anchor="end" font-size="12" font-weight="750" fill="'+VIOLET_D+'">'+esc(fmtN(s.value))+'</text>';
    }
  });
  /* ligne de moyenne — repère doré discret */
  const avgLine = '<line x1="'+L+'" y1="'+avgY.toFixed(1)+'" x2="'+(W-R)+'" y2="'+avgY.toFixed(1)+'" stroke="'+GOLD+'" stroke-width="1.4" stroke-dasharray="6 6" opacity=".55"/>';

  return '<svg class="chart" viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Évolution des dépenses">'+
    SVG_STYLE+
    '<defs><linearGradient id="vtArea" x1="0" y1="0" x2="0" y2="1">'+
      '<stop offset="0" stop-color="'+VIOLET+'" stop-opacity=".18"/><stop offset="1" stop-color="'+VIOLET+'" stop-opacity="0"/></linearGradient></defs>'+
    grid+avgLine+labels+
    '<path class="vt-area" d="'+area+'" fill="url(#vtArea)"/>'+
    '<path class="vt-line" d="'+line+'" fill="none" stroke="'+VIOLET+'" stroke-width="2.8" stroke-linecap="round" pathLength="1"/>'+
    dots+hit+
    '</svg>'+
    '<div class="chart-legend">'+
      '<span class="lg-item"><span class="sw line" style="background:'+VIOLET+'"></span> Dépenses mensuelles</span>'+
      '<span class="lg-item"><span class="sw" style="background:'+GOLD+'"></span> Mois analysé</span>'+
      '<span class="lg-item"><span class="sw dash"></span> Moyenne '+esc(fmtN(average))+' '+esc(DB.params.devise)+'/mois</span>'+
    '</div>'+
    '<div class="flex-between" style="margin-top:12px">'+
      '<span class="small">Cumul de la période : <b style="color:var(--primary)">'+fmtN(total)+' '+esc(DB.params.devise)+'</b></span>'+
      '<span class="small">'+(series.length)+' mois analysés</span>'+
    '</div>';
}

'''
s = s[:a0] + new_chart + s[a1:]
print("  ✓ graphique Évolution (violet doux + or)")

# ============================================================ 2. DASHBOARD RH
d0 = s.index('/* ------------------------------ 3. DASHBOARD ------------------------------ */')
d1 = s.index('/* ------------------------------ 4. ANALYSE ------------------------------ */')
new_dash = r'''/* ------------------------------ 3. TABLEAU DE BORD RH CENTRALISÉ ------------------------------
   Un seul espace de pilotage : les filtres s'appliquent à l'ensemble du tableau de bord.
   Les services et les collaborateurs sont des DONNÉES (jamais des espaces indépendants).
   ---------------------------------------------------------------------------------------------- */
let evoRange=6;
let dashFilters = { service:"", agent:"", type:"" };

/* trajets correspondant aux filtres globaux (période + service + collaborateur + type) */
function dashTrips(month){
  const m = month || $("#dashMonth").value || currentMonth();
  const f = dashFilters;
  return DB.trips.filter(t=>{
    if(monthOf(t.date)!==m) return false;
    if(f.service && t.service!==f.service) return false;
    if(f.agent && t.agent!==f.agent) return false;
    if(f.type && t.transport!==f.type) return false;
    return true;
  });
}
function dashMonthPrev(month){
  const pm = shiftMonth(month,-1);
  const f = dashFilters;
  return DB.trips.filter(t=>{
    if(monthOf(t.date)!==pm) return false;
    if(f.service && t.service!==f.service) return false;
    if(f.agent && t.agent!==f.agent) return false;
    if(f.type && t.transport!==f.type) return false;
    return true;
  });
}
function renderFilterChips(){
  const m=$("#dashMonth").value||currentMonth();
  const chips=[
    '<span class="chip violet">'+ic("calendar")+'<b>'+esc(monthLabel(m))+'</b></span>'
  ];
  if(dashFilters.service) chips.push('<span class="chip">'+ic("building")+esc(svc(dashFilters.service).name)+'</span>');
  if(dashFilters.agent)   chips.push('<span class="chip">'+ic("users")+esc(dashFilters.agent)+'</span>');
  if(dashFilters.type)    chips.push('<span class="chip">'+ic("route")+esc(dashFilters.type)+'</span>');
  const active = (dashFilters.service||dashFilters.agent||dashFilters.type);
  chips.push(active? '<span class="chip ok">'+ic("check")+'Filtres actifs</span>' : '<span class="chip">'+ic("info")+'Toute l\'organisation</span>');
  $("#filterChips").innerHTML = chips.join("");
}
function renderDashboard(){
  const m=$("#dashMonth").value||currentMonth();
  const list=dashTrips(m), prev=dashMonthPrev(m);
  const n=list.length, total=sum(list), km=sumKm(list);
  const avg = n? total/n : 0;
  const pn=prev.length, ptotal=sum(prev);
  const openList=list.filter(t=>t.statut==="A_REGLE"), okList=list.filter(t=>t.statut==="REGLE");
  const agentsActifs = Array.from(new Set(list.map(t=>t.agent)));

  /* --- 1. En-tête RH --- */
  $("#welcomeTitle").innerHTML="Bonjour, RH 👋";
  $("#welcomeSub").innerHTML="Pilotez les déplacements, les collaborateurs et les coûts de mobilité depuis cet espace centralisé. Situation de <b>"+esc(monthLabel(m))+"</b>.";
  $("#welcomePills").innerHTML=
    '<span class="chip violet">'+ic("calendar")+esc(monthLabel(m))+'</span>'+
    '<span class="chip">'+ic("list")+fmtN(n)+' déplacement(s)</span>'+
    '<span class="chip">'+ic("wallet")+fmtN(total)+' '+esc(DB.params.devise)+'</span>'+
    (openList.length? '<span class="chip gold">'+ic("clock")+openList.length+' en attente</span>' : '<span class="chip ok">'+ic("check")+'Tout est réglé</span>')+
    '<span class="chip">'+ic("route")+fmtN(km)+' km</span>';

  /* --- 2. Filtres globaux --- */
  const sSel=$("#gService"); if(sSel && !sSel.options.length) sSel.innerHTML='<option value="">Tous les services</option>'+SERVICES.map(x=>'<option value="'+x.id+'">'+esc(x.name)+'</option>').join("");
  const aSel=$("#gAgent");
  if(aSel){
    const cur=aSel.value;
    const noms=Array.from(new Set(DB.agents.map(a=>a.nom))).sort((x,y)=>x.localeCompare(y,"fr"));
    aSel.innerHTML='<option value="">Tous les collaborateurs</option>'+noms.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join("");
    aSel.value = dashFilters.agent || cur || "";
  }
  const tSel=$("#gType"); if(tSel && tSel.options.length<2) tSel.innerHTML='<option value="">Tous les types</option>'+DB.transports.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join("");
  if(sSel) sSel.value=dashFilters.service;
  if(tSel) tSel.value=dashFilters.type;
  renderFilterChips();

  /* --- 3. KPI (6 cartes) --- */
  const sparkTotals=monthRange(m,6).map(x=>sum(tripsOf(x)));
  const sparkCounts=monthRange(m,6).map(x=>tripsOf(x).length);
  $("#kpiRow").innerHTML=[
    kpiCard({i:0, label:"Total des déplacements", icon:"list", value:fmtN(n),
      foot:"vs "+fmtN(pn)+" le mois précédent", delta:deltaPct(n,pn), spark:sparkline(sparkCounts,"#6B4A82"),
      tip:"Nombre de déplacements enregistrés sur la période"}),
    kpiCard({i:1, label:"Dépenses de mobilité", icon:"wallet", value:fmtN(total), unit:DB.params.devise, tone:"gold",
      foot:"mois précédent : "+fmtN(ptotal)+" "+DB.params.devise, delta:deltaPct(total,ptotal), spark:sparkline(sparkTotals,"#C9A227"),
      tip:"Total des dépenses de déplacement de la période"}),
    kpiCard({i:2, label:"Collaborateurs concernés", icon:"users", value:fmtN(agentsActifs.length), unit:"/ "+DB.agents.length,
      foot:"ayant effectué au moins une sortie", delta:null, tone:"",
      tip:"Personnes concernées par au moins un déplacement"}),
    kpiCard({i:3, label:"Déplacements en attente", icon:"clock", value:fmtN(openList.length), tone:"warn",
      foot:fmtN(sum(openList))+" "+DB.params.devise+" à régler", delta:null,
      tip:"Déplacements dont le remboursement n'est pas encore réglé"}),
    kpiCard({i:4, label:"Déplacements validés", icon:"check", value:fmtN(okList.length), tone:"ok",
      foot:(n? Math.round(okList.length/n*100)+" % de la période" : "aucun déplacement"), delta:null,
      tip:"Déplacements déjà réglés / remboursés"}),
    kpiCard({i:5, label:"Coût moyen par déplacement", icon:"gauge", value:fmtN(avg), unit:DB.params.devise,
      foot:"sur "+fmtN(n)+" déplacement(s)", delta:deltaPct(avg, pn? ptotal/pn : 0),
      tip:"Dépense moyenne par déplacement de la période"})
  ].join("");

  /* --- 4. Évolution des dépenses --- */
  const months=monthRange(m, evoRange);
  const series=months.map(x=>{
    const l=tripsOf(x).filter(t=>{
      const f=dashFilters;
      if(f.service && t.service!==f.service) return false;
      if(f.agent && t.agent!==f.agent) return false;
      if(f.type && t.transport!==f.type) return false;
      return true;
    });
    return { label:MONTHS_SHORT[Number(x.split("-")[1])-1], tipLabel:monthLabel(x),
      value:sum(l), count:l.length, nb:new Set(l.map(t=>t.agent)).size, current:(x===m) };
  });
  const ed=$("#evoDesc"); if(ed) ed.textContent=evoRange+" derniers mois — total mensuel consolidé, filtres appliqués";
  $("#chartEvo").innerHTML=areaChart(series);

  /* --- 5. Part des services (anneau) --- */
  const aggSvc=byService(list);
  const svcItems=SERVICES.map(x=>({ label:x.short, sub:x.role, value:aggSvc[x.id].total, n:aggSvc[x.id].n,
    logo:(x.logo? '<img src="'+LOGOS[x.logo].uri+'" style="max-width:100%;max-height:28px;object-fit:contain">':'<span style="color:'+x.color2+'">'+ic(x.icon)+'</span>'),
    color:x.color2 }));
  $("#chartSvc").innerHTML = svcItems.some(x=>x.value>0)
    ? donutBlock(svcItems.filter(x=>x.value>0), total, {centerSub:DB.params.devise})
    : emptyState("chart","Aucune dépense sur la période","Enregistrez un déplacement ou ajustez les filtres.");

  /* --- 6. Répartition par service (cliquable = filtre) --- */
  $("#svcList").innerHTML = SERVICES.map(x=>{
    const cur=aggSvc[x.id], prv=(function(){
      const pm=shiftMonth(m,-1);
      return DB.trips.filter(t=>monthOf(t.date)===pm && t.service===x.id &&
        (!dashFilters.agent || t.agent===dashFilters.agent) && (!dashFilters.type || t.transport===dashFilters.type));
    })();
    const share = total? (cur.total/total*100) : 0;
    const delta = deltaPct(cur.total, sum(prv));
    const dTxt = delta===null? "n/d" : (Math.abs(delta)<1? "stable" : (delta>0?"+":"")+delta.toFixed(0)+"%");
    const on = dashFilters.service===x.id? " on":"";
    return '<button type="button" class="svc-row'+on+'" data-svc-filter="'+x.id+'" aria-pressed="'+(on?"true":"false")+'">'+
      '<span class="sv-logo">'+(x.logo? '<img src="'+LOGOS[x.logo].uri+'" alt="">' : '<span class="ic" style="color:'+x.color2+';width:22px;height:22px">'+ic(x.icon)+'</span>')+'</span>'+
      '<span class="sv-name"><b>'+esc(x.name)+'</b><span>'+esc(x.role)+(x.id==="DIRECTION"? "":"")+'</span></span>'+
      '<span class="sv-num">'+fmtN(cur.n)+'<span>déplacement(s)</span></span>'+
      '<span class="sv-num">'+fmtN(cur.total)+'<span>'+esc(DB.params.devise)+'</span></span>'+
      '<span class="sv-num hide-sm" style="color:'+(delta>0? "#B4645F" : delta<0? "#2C7F62" : "var(--muted)")+'">'+esc(dTxt)+'<span>vs mois -1</span></span>'+
      '<span class="sv-share"><span class="sv-bar"><i style="transform:scaleX('+(share/100).toFixed(3)+')"></i></span><b>'+share.toFixed(0)+'%</b></span>'+
      '<span class="sv-go">'+ic(dashFilters.service===x.id? "check":"chevRight")+'</span>'+
    '</button>';
  }).join("") + (dashFilters.service? '<div class="small" style="padding:6px 4px">Filtre actif : <b>'+esc(svc(dashFilters.service).name)+'</b> — cliquez de nouveau pour revenir à toute l\'organisation.</div>' : "");
  $$("#svcList [data-svc-filter]").forEach(b=>b.onclick=()=>{
    dashFilters.service = (dashFilters.service===b.dataset.svcFilter)? "" : b.dataset.svcFilter;
    renderDashboard();
    toast(dashFilters.service? "Filtre appliqué" : "Filtre retiré",
          dashFilters.service? svc(dashFilters.service).name+" — le tableau de bord est filtré." : "Le tableau de bord affiche toute l'organisation.", "info");
  });

  /* --- 7. Activité des collaborateurs --- */
  const q=($("#caSearch")? $("#caSearch").value : "").toLowerCase().trim();
  const ba=byAgent(list);
  const eff = dashFilters.agent? DB.agents.filter(a=>a.nom===dashFilters.agent) : DB.agents;
  const rows = eff.filter(a=>{
    if(dashFilters.service && a.service!==dashFilters.service) return false;
    if(q && (a.nom+" "+svc(a.service).name).toLowerCase().indexOf(q)<0) return false;
    return true;
  }).map(a=>{
    const st=ba[a.nom]||{n:0,total:0,last:null};
    const pen=list.filter(t=>t.agent===a.nom && t.statut==="A_REGLE");
    return {a,st,pen};
  }).sort((x,y)=>y.st.total-x.st.total);
  $("#collabActivity").innerHTML = rows.length? '<table class="tbl" style="min-width:820px"><thead><tr>'+
      '<th class="no-sort">Collaborateur</th><th class="no-sort">Service</th><th class="no-sort">Déplacements</th>'+
      '<th class="no-sort">Dernier déplacement</th><th class="no-sort">Dépenses</th><th class="no-sort">Statut</th></tr></thead><tbody>'+
    rows.map(r=>'<tr>'+
      '<td><div class="avatar-row"><span class="avatar">'+esc(initials(r.a.nom))+'</span><span class="who"><b>'+esc(r.a.nom)+'</b><span>'+(r.a.actif===false? "Inactif":"Actif")+'</span></span></div></td>'+
      '<td>'+serviceTag(r.a.service)+'</td>'+
      '<td><b>'+fmtN(r.st.n)+'</b></td>'+
      '<td>'+(r.st.last? dateFR(r.st.last) : "—")+'</td>'+
      '<td class="amount strong">'+fmtN(r.st.total)+' <span class="small">'+esc(DB.params.devise)+'</span></td>'+
      '<td>'+(r.st.n===0? '<span class="st-pill mute">'+ic("minus")+'Aucune sortie</span>'
            : r.pen.length? '<span class="st-pill gold">'+ic("clock")+r.pen.length+' à régler</span>'
            : '<span class="st-pill ok">'+ic("check")+'À jour</span>')+'</td>'+
    '</tr>').join("")+'</tbody><tfoot><tr class="tfoot"><td colspan="2">'+rows.length+' collaborateur(s) affiché(s)</td>'+
      '<td>'+rows.reduce((x,r)=>x+r.st.n,0)+'</td><td></td><td class="amount">'+fmtN(rows.reduce((x,r)=>x+r.st.total,0))+' '+esc(DB.params.devise)+'</td><td></td></tr></tfoot></table>'
    : emptyState("users","Aucun collaborateur","Modifiez la recherche ou les filtres de la période.");

  /* --- 8. Derniers déplacements --- */
  const last=dashTrips(m).sort((a,b)=> (b.date||"").localeCompare(a.date||"")).slice(0,6);
  $("#recentWrap").innerHTML = last.length? tableHTML(last,{compact:false}) :
    emptyState("route","Aucun déplacement sur la période","Ajustez les filtres ou enregistrez un nouveau déplacement.");

  /* --- 9. Points d'attention --- */
  const noJustif=list.filter(t=>t.justif==="NON");
  const att=[];
  if(openList.length) att.push({ico:"wallet",t:openList.length+" déplacement(s) en attente de règlement",s:fmtN(sum(openList))+" "+DB.params.devise+" à rembourser",go:"rapports",tone:"gold"});
  if(noJustif.length) att.push({ico:"alert",t:noJustif.length+" justificatif(s) manquant(s)",s:"Complétez les reçus avant la clôture du mois",go:"registre",tone:"warn"});
  const sansTrajet=list.filter(t=>!t.from||!t.to).length;
  if(sansTrajet) att.push({ico:"route",t:sansTrajet+" trajet(s) incomplet(s)",s:"Renseignez le départ et la destination",go:"registre",tone:""});
  if(!att.length) att.push({ico:"check",t:"Aucun point bloquant",s:"La période est propre et complète",go:"dashboard",tone:"ok"});
  $("#attentionList").innerHTML = att.slice(0,4).map(a=>
    '<div class="rank-item" data-go="'+a.go+'" style="cursor:pointer"><span class="ic-wrap" style="width:36px;height:36px;border-radius:11px;display:grid;place-items:center;background:var(--surface-3);color:'+
      (a.tone==="gold"?"#8E7318":a.tone==="warn"?"var(--warn)":a.tone==="ok"?"var(--ok)":"var(--secondary)")+'">'+ic(a.ico)+'</span>'+
      '<span class="who"><b style="white-space:normal">'+esc(a.t)+'</b><span>'+esc(a.s)+'</span></span>'+
      '<span style="color:var(--faint)">'+ic("chevRight")+'</span></div>').join("");
  $$("#attentionList [data-go]").forEach(el=>el.onclick=()=>go(el.dataset.go));

  /* --- 10. Contrôle & conformité --- */
  const bt=byTransport(list);
  const trTop=Object.keys(bt).map(k=>({k,v:bt[k].total})).sort((x,y)=>y.v-x.v)[0];
  const topSvc=SERVICES.map(x=>({x,t:aggSvc[x.id].total})).sort((x,y)=>y.t-x.t)[0];
  const taux = n? Math.round(((n-noJustif.length)/n)*100) : 100;
  $("#insights").innerHTML=[
    {icon:"clock", k:"Restant à régler", v:fmtN(sum(openList))+" "+DB.params.devise, s:openList.length+" déplacement(s) en attente", tone: openList.length? "gold":""},
    {icon:"shield", k:"Taux de justificatifs", v:taux+" %", s:(n-noJustif.length)+" reçu(s) sur "+n, tone: taux>=90? "ok":"warn"},
    {icon:"building", k:"Service le plus actif", v:(topSvc&&topSvc.t? topSvc.x.short : "—"), s:(topSvc&&topSvc.t? fmtN(topSvc.t)+" "+DB.params.devise : "aucune dépense"), tone:""},
    {icon:"route", k:"Transport dominant", v:(trTop? trunc(trTop.k,20) : "—"), s:(trTop? fmtN(trTop.v)+" "+DB.params.devise : "aucune donnée"), tone:""}
  ].map((it,i)=>'<div class="stat-tile reveal" style="--i:'+i+'"><span class="ic-wrap">'+ic(it.icon)+'</span>'+
      '<div><div class="k">'+esc(it.k)+'</div><div class="v">'+esc(it.v)+'</div><div class="s">'+esc(it.s)+'</div></div></div>').join("");

  bindChartTips();
}

'''
s = s[:d0] + new_dash + s[d1:]
print("  ✓ dashboard RH centralisé (filtres globaux, 6 KPI, services cliquables, collaborateurs)")

# ============================================================ 3. SUPPRESSION VÉHICULES
v0 = s.index('function vehicleStateTag(st){')
v1 = s.index('function renderCollabs(){')
s = s[:v0] + s[v1:]
print("  ✓ fonctions Véhicules supprimées (renderVehicules, vehicleModal)")

open(p, 'w').write(s)
print("part3b_dash.js.html — étape 1 terminée")
