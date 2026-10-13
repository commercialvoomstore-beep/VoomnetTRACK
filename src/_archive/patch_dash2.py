# -*- coding: utf-8 -*-
"""Patch init() : liaisons des nouveaux filtres globaux, retrait de Véhicules et des raccourcis disparus."""
p = 'src/part3b_dash.js.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  ✓", label)

# ------------------------------------------------ 1. CONNEXION RH (validation en ligne)
rep('''  const goNow=$("#btnLogin"); if(goNow) goNow.onclick=()=>{
    const n=$("#loginName").value.trim();
    if(!n){ toast("Nom requis","Saisissez votre nom pour ouvrir votre espace.","err"); $("#loginName").classList.add("err"); return; }
    $("#loginName").classList.remove("err");
    doLogin(n, $("#loginRole").value);
  };
  const skip=$("#btnLoginSkip"); if(skip) skip.onclick=()=>doLogin(DB.user.name||"Mode consultation","Consultation");''',
'''  const goNow=$("#btnLogin"); if(goNow) goNow.onclick=()=>{
    const n=$("#loginName").value.trim();
    if(!n){
      $("#loginName").classList.add("err");
      const e=$("#err-loginName"); if(e) e.classList.add("on");
      toast("Identité requise","Indiquez votre nom ou votre identifiant d'accès.","err");
      return;
    }
    $("#loginName").classList.remove("err");
    const e=$("#err-loginName"); if(e) e.classList.remove("on");
    doLogin(n, $("#loginRole").value);
  };
  const skip=$("#btnLoginSkip"); if(skip) skip.onclick=()=>doLogin("Mode consultation","Consultation (lecture seule)");''', "connexion RH")

# ------------------------------------------------ 2. FILTRES GLOBAUX DU DASHBOARD
rep('''  /* dashboard */
  $("#dashMonth").value=currentMonth();
  $("#dashMonth").onchange=()=>{ refreshAll(); };
  $("#btnSeedDemo").onclick=()=>{ seedDemo(); refreshAll(); };''',
'''  /* dashboard RH : filtres globaux appliqués à tout le tableau de bord */
  $("#dashMonth").value=currentMonth();
  $("#dashMonth").onchange=()=>{ refreshAll(); };
  $("#btnSeedDemo").onclick=()=>{ seedDemo(); refreshAll(); };
  const bindGlobal=(id,key)=>{
    const el=$("#"+id); if(!el) return;
    el.addEventListener("change",()=>{ dashFilters[key]=el.value; renderDashboard(); });
  };
  bindGlobal("gService","service"); bindGlobal("gAgent","agent"); bindGlobal("gType","type");
  const rF=$("#btnResetFilters");
  if(rF) rF.onclick=()=>{
    dashFilters={service:"",agent:"",type:""};
    ["gService","gAgent","gType"].forEach(id=>{ const e=$("#"+id); if(e) e.value=""; });
    renderDashboard(); toast("Filtres réinitialisés","Toute l'organisation est affichée.","info");
  };
  const ca=$("#caSearch"); if(ca) ca.addEventListener("input",()=>{
    clearTimeout(window.__caT); window.__caT=setTimeout(renderDashboard,180);
  });''', "filtres globaux + recherche collaborateurs")

# ------------------------------------------------ 3. RACCOURCIS SUPPRIMÉS
rep('''  $("#qaPdf").onclick=()=>{ $("#rMonth").value=$("#dashMonth").value||currentMonth(); go("rapports"); setTimeout(()=>buildPDF(true),350); };
  $("#qaCsv").onclick=()=>exportCsv(tripsOf($("#dashMonth").value||currentMonth()),"VOOMNET_Track_"+($("#dashMonth").value||"")+".csv");
  $("#qaBackup").onclick=doBackup;''',
'''  $("#qaPdf").onclick=()=>{ $("#rMonth").value=$("#dashMonth").value||currentMonth(); go("rapports"); setTimeout(()=>buildPDF(true),350); };''', "raccourcis retirés (CSV/sauvegarde restent dans Rapports et Paramètres)")

# ------------------------------------------------ 4. REGISTRE : plus de filtre véhicule
rep('''  $("#fVehicule2").innerHTML='<option value="">Tous les véhicules</option>'+DB.vehicles.map(v=>'<option value="'+v.id+'">'+esc(v.plate)+'</option>').join("");
''', '', "registre : remplissage du filtre Véhicule retiré")
rep('''  ["fSearch","fMonth","fService","fTransport","fVehicule2","fStatut2","fJustif2"].forEach(id=>{''',
'''  ["fSearch","fMonth","fService","fTransport","fStatut2","fJustif2"].forEach(id=>{''', "registre : liste des filtres")
rep('''    ["fSearch","fService","fTransport","fVehicule2","fStatut2","fJustif2"].forEach(id=>$("#"+id).value="");''',
'''    ["fSearch","fService","fTransport","fStatut2","fJustif2"].forEach(id=>$("#"+id).value="");''', "registre : réinitialisation des filtres")

# ------------------------------------------------ 5. BLOC VÉHICULES
rep('''  /* véhicules */
  $("#btnAddVehicle").onclick=()=>vehicleModal(null);
  $("#vSearch").addEventListener("input",renderVehicules);
  $("#vState").addEventListener("change",renderVehicules);

''', '', "init : bloc Véhicules supprimé")

open(p, 'w').write(s)
print("part3b_dash.js.html — étape 2 terminée")
