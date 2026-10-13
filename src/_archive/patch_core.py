# -*- coding: utf-8 -*-
"""Patch cœur JS : session RH centralisée, retrait total de l'interface Véhicules (données conservées)."""
p = 'src/part3_core.js.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  ✓", label)

# ---------------------------------------------------------------- 1. NAVIGATION
rep('''  vehicules:["Véhicules","État, affectation et kilométrage du parc"],
''', '', "VIEW_META : entrée Véhicules retirée")
rep('''  if(view==="vehicules") renderVehicules();
''', '', "go() : appel renderVehicules retiré")

# ---------------------------------------------------------------- 2. NOTIFICATIONS
rep('''  const maint=DB.vehicles.filter(v=>v.state==="Maintenance"||v.state==="Hors service");
''', '', "notifications : alerte flotte retirée")
rep('''  if(maint.length) items.push({ico:"car",t:maint.length+" véhicule(s) immobilisé(s)",s:maint.map(v=>v.plate).join(" · "),go:"vehicules"});
''', '', "notifications : item flotte retiré")
rep('  const n = open.length+noJustif.length+maint.length;',
    '  const n = open.length+noJustif.length;', "notifications : compteur")

# ---------------------------------------------------------------- 3. RAFRAÎCHISSEMENT
rep('''  $("badgeVehicules").textContent = DB.vehicles.length;
'''.replace('$("badgeVehicules")', '$("#badgeVehicules")'), '', "refreshAll : badge Véhicules retiré")
rep('''  if($("#view-vehicules").classList.contains("active")) renderVehicules();
''', '', "refreshAll : vue Véhicules retirée")

# ---------------------------------------------------------------- 4. TABLEAU / CSV
rep('''      '<td style="white-space:nowrap">'+esc(t.transport)+
        (v? '<div class="small">'+esc(v.plate)+'</div>':'')+'</td>'+''',
'''      '<td style="white-space:nowrap">'+esc(t.transport)+'</td>'+''', "tableau : ligne véhicule retirée")
rep('''  const rows = list.map(t=>{
    const v=vehicleLabel(t.vehicule);
    return '<tr data-id="'+t.id+'">'+''',
'''  const rows = list.map(t=>{
    return '<tr data-id="'+t.id+'">'+''', "tableau : variable véhicule retirée")

rep('''  const head=["Date","Service","Personne","Motif","Départ","Destination","Transport","Véhicule","Distance (km)","Montant","Statut","Justificatif","Observation"];''',
'''  const head=["Date","Service","Personne","Motif","Départ","Destination","Transport","Distance (km)","Montant","Statut","Justificatif","Observation"];''', "CSV : colonne Véhicule retirée")
rep('''  list.forEach(t=>{
    const v=vehicleLabel(t.vehicule);
    lines.push([dateFR(t.date),svc(t.service).name,t.agent,t.motif,t.from,t.to,t.transport,
      v? v.plate:"", Number(t.km)||0, t.montant,''',
'''  list.forEach(t=>{
    lines.push([dateFR(t.date),svc(t.service).name,t.agent,t.motif,t.from,t.to,t.transport,
      Number(t.km)||0, t.montant,''', "CSV : ligne véhicule retirée")
rep('''  lines.push(["","","","","","","","","TOTAL",sum(list),"","",""].map(q).join(";"));''',
'''  lines.push(["","","","","","","","TOTAL",sum(list),"","",""].map(q).join(";"));''', "CSV : ligne TOTAL alignée")

# ---------------------------------------------------------------- 5. FICHE DE DÉPLACEMENT
rep('''  const vsel=$("#fVehicule"); const vcur=vsel.value;
  vsel.innerHTML = '<option value="">— Aucun —</option>'+
    DB.vehicles.map(v=>'<option value="'+v.id+'">'+esc(v.plate+" · "+v.marque+" "+v.modele)+'</option>').join("");
  if(vcur) vsel.value=vcur;
''', '', "fiche : remplissage du sélecteur Véhicule retiré")
rep('''    transport:$("#fTrans").value, vehicule:$("#fVehicule").value, km:Number($("#fKm").value)||0,''',
'''    transport:$("#fTrans").value, vehicule:"", km:Number($("#fKm").value)||0,''', "enregistrement : champ Véhicule retiré")
rep('''  const v=vehicleLabel(t.vehicule);
  if(v && v.state==="Disponible"){ DB.updateVehicle(v.id,{state:"En mission"}); }
''', '', "enregistrement : mise à jour de flotte retirée")
rep('''  $("#fVehicule").value="";
''', '', "resetForm : Véhicule retiré")
rep('''  if(/Véhicule personnel|Location/.test(tr) && DB.vehicles.length){
    const av=DB.vehicles.filter(v=>v.state!=="Hors service");
    if(av.length) $("#fVehicule").value=av[Math.floor(Math.random()*av.length)].id;
  }
''', '', "demoFill : Véhicule retiré")

# ---------------------------------------------------------------- 6. REGISTRE
rep('''        s=$("#fService").value, tr=$("#fTransport").value,
        vh=$("#fVehicule2").value, st=$("#fStatut2").value, ju=$("#fJustif2").value;''',
'''        s=$("#fService").value, tr=$("#fTransport").value,
        st=$("#fStatut2").value, ju=$("#fJustif2").value;''', "filtres : variable Véhicule retirée")
rep('''    if(vh && t.vehicule!==vh) return false;
''', '', "filtres : condition Véhicule retirée")
rep('''      const v=vehicleLabel(t.vehicule);
      const hay=[t.agent,t.motif,t.from,t.to,t.transport,t.note,t.date,svc(t.service).name,(v? v.plate+" "+v.marque+" "+v.modele:"")].join(" ").toLowerCase();''',
'''      const hay=[t.agent,t.motif,t.from,t.to,t.transport,t.note,t.date,svc(t.service).name].join(" ").toLowerCase();''', "recherche : terme véhicule retiré")

# ---------------------------------------------------------------- 7. MODALE D'ÉDITION
rep('''    '<div class="grid g-3" style="gap:0 15px">'+
      '<div class="field"><label>Transport</label><select class="input" id="mTrans">'+DB.transports.map(x=>'<option'+(x===t.transport?" selected":"")+'>'+esc(x)+'</option>').join("")+'</select></div>'+
      '<div class="field"><label>Véhicule</label><select class="input" id="mVehicule"><option value="">— Aucun —</option>'+
        DB.vehicles.map(v=>'<option value="'+v.id+'"'+(v.id===t.vehicule?" selected":"")+'>'+esc(v.plate)+'</option>').join("")+'</select></div>'+
      '<div class="field"><label>Distance (km)</label><input type="number" class="input" id="mKm" value="'+(Number(t.km)||0)+'"></div>'+
    '</div>'+''',
'''    '<div class="grid g-2" style="gap:0 15px">'+
      '<div class="field"><label>Transport</label><select class="input" id="mTrans">'+DB.transports.map(x=>'<option'+(x===t.transport?" selected":"")+'>'+esc(x)+'</option>').join("")+'</select></div>'+
      '<div class="field"><label>Distance (km)</label><input type="number" class="input" id="mKm" value="'+(Number(t.km)||0)+'"></div>'+
    '</div>'+''', "modale : champ Véhicule retiré")
rep('''      transport:$("#mTrans").value, vehicule:$("#mVehicule").value, km:Number($("#mKm").value)||0,''',
'''      transport:$("#mTrans").value, vehicule:(t.vehicule||""), km:Number($("#mKm").value)||0,''', "modale : sauvegarde sans Véhicule")

# ---------------------------------------------------------------- 8. PARAMÈTRES
rep('''  $("#statsBox").innerHTML="<b>"+s.length+"</b> déplacement(s) · <b>"+fmtN(sum(s))+"</b> "+esc(DB.params.devise)+
    " cumulés · <b>"+fmtN(sumKm(s))+"</b> km · "+(DB.vehicles.length)+" véhicule(s) · "+DB.agents.length+" collaborateur(s)"+''',
'''  $("#statsBox").innerHTML="<b>"+s.length+"</b> déplacement(s) · <b>"+fmtN(sum(s))+"</b> "+esc(DB.params.devise)+
    " cumulés · <b>"+fmtN(sumKm(s))+"</b> km · "+DB.agents.length+" collaborateur(s) · "+SERVICES.length+" service(s)"+''', "paramètres : statistiques sans flotte")

# ---------------------------------------------------------------- 9. SESSION RH
rep('''function hasSession(){ try{ return sessionStorage.getItem("vt_session")==="1"; }catch(e){ return false; } }
function renderLoginProfiles(){
  const list=DB.agents.filter(a=>a.actif!==false).slice(0,4);
  $("#loginProfiles").innerHTML=list.map(a=>
    '<button type="button" class="login-prof" data-nom="'+esc(a.nom)+'">'+
      '<span class="avatar">'+esc(initials(a.nom))+'</span>'+
      '<span class="tx"><b>'+esc(a.nom)+'</b><span>'+esc(svc(a.service).role)+'</span></span>'+
    '</button>').join("");
  $$("#loginProfiles .login-prof").forEach(b=>b.onclick=()=>{
    $$("#loginProfiles .login-prof").forEach(x=>x.classList.remove("sel"));
    b.classList.add("sel");
    $("#loginName").value=b.dataset.nom;
    const a=DB.agents.find(x=>x.nom===b.dataset.nom);
    if(a) $("#loginRole").value=svc(a.service).role;
  });
}
function showLogin(){
  const L=$("#login"); if(!L) return;
  $("#loginRole").innerHTML=SERVICES.map(s=>'<option>'+esc(s.role)+'</option>').join("")+'<option>Administration / Comptabilité</option>';
  renderLoginProfiles();
  $("#loginName").value=DB.user.name||"";
  $("#loginRole").value=DB.user.role||SERVICES[0].role;
  L.classList.remove("hidden","closing");
}
function doLogin(name, role){
  const nm=(name||"").trim()||"Utilisateur VOOMNET";
  DB.user={ name:nm, role:role||"Consultation" }; DB.save();
  try{ sessionStorage.setItem("vt_session","1"); }catch(e){}
  const L=$("#login");
  if(L){ L.classList.add("closing"); setTimeout(()=>L.classList.add("hidden"), 460); }
  renderUser(); refreshAll(); go("dashboard");
  toast("Bienvenue, "+nm.replace(/^(M\\.|Mme|Mlle)\\s*/i,"").split(" ")[0],"Votre espace VOOMNET Track est prêt.","ok");
}''',
'''function hasSession(){ try{ return sessionStorage.getItem("vt_session")==="1"; }catch(e){ return false; } }
/* Rôles RH : un seul espace de pilotage central (aucun espace par service ni par personne). */
const RH_ROLES = [
  "Responsable RH",
  "Administrateur RH",
  "Gestionnaire RH / Paie",
  "Contrôleur de gestion",
  "Consultation (lecture seule)"
];
function showLogin(){
  const L=$("#login"); if(!L) return;
  $("#loginRole").innerHTML=RH_ROLES.map(r=>'<option>'+esc(r)+'</option>').join("");
  $("#loginName").value=DB.user.name||"";
  $("#loginRole").value=RH_ROLES.indexOf(DB.user.role)>=0? DB.user.role : RH_ROLES[0];
  $("#loginName").classList.remove("err");
  const e=$("#err-loginName"); if(e) e.classList.remove("on");
  L.classList.remove("hidden","closing");
}
function doLogin(name, role){
  const nm=(name||"").trim()||"Service Ressources Humaines";
  DB.user={ name:nm, role:role||RH_ROLES[0] }; DB.save();
  try{ sessionStorage.setItem("vt_session","1"); }catch(e){}
  const L=$("#login");
  if(L){ L.classList.add("closing"); setTimeout(()=>L.classList.add("hidden"), 460); }
  renderUser(); refreshAll(); go("dashboard");
  toast("Bienvenue dans l'espace RH", nm+" · accès au pilotage central de la mobilité.","ok");
}''', "session RH centralisée (plus de profils multiples)")

open(p, 'w').write(s)
print("part3_core.js.html mis à jour")
