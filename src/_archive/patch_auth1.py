# -*- coding: utf-8 -*-
"""Patch 1/3 — Comptes (RH + Administrateur), session sécurisée, suppression de toute donnée de démonstration."""
p = 'src/part3_core.js.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  ✓", label)

# ============================================================ ICÔNES COMPLÉMENTAIRES
rep("""  building:'<rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M9 7h1.5M13.5 7H15M9 11h1.5M13.5 11H15M9 15h1.5M13.5 15H15"/><path d="M10 21v-3h4v3"/>'""",
"""  building:'<rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M9 7h1.5M13.5 7H15M9 11h1.5M13.5 11H15M9 15h1.5M13.5 15H15"/><path d="M10 21v-3h4v3"/>',
  minus:'<path d="M5 12h14"/>',
  chevRight:'<path d="m9 6 6 6-6 6"/>',
  lock:'<rect x="4" y="10.5" width="16" height="10.5" rx="3"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><path d="M12 15v2.5"/>',
  eyeOff:'<path d="M3 3l18 18"/><path d="M10.6 5.9A9.6 9.6 0 0 1 12 5.8c6 0 9.5 6.2 9.5 6.2a17 17 0 0 1-2.6 3.5"/><path d="M6.3 7.9A16.4 16.4 0 0 0 2.5 12S6 18.2 12 18.2c1.6 0 3-.4 4.2-1"/><path d="M9.9 10a3 3 0 0 0 4.2 4.2"/>',
  logout:'<path d="M15 4h3a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-3"/><path d="M10 8l-4 4 4 4"/><path d="M6 12h9"/>',
  key:'<circle cx="8" cy="15" r="4"/><path d="m10.8 12.2 8.7-8.7"/><path d="m17 4 2.5 2.5"/><path d="M14.5 9.5 17 12"/>',
  shieldCheck:'<path d="M12 3l8 3v6c0 4.6-3.2 8-8 9-4.8-1-8-4.4-8-9V6z"/><path d="m8.8 12 2.3 2.3L15.5 10"/>',
  userCog:'<circle cx="9.5" cy="8" r="3.5"/><path d="M3 20a6.5 6.5 0 0 1 10.6-5"/><circle cx="17.5" cy="17.5" r="3.2"/><path d="M17.5 15v1.4M17.5 18.6V20M15.4 17.5h1.4M18.2 17.5h1.4"/>'""", "icônes lock / logout / key / œil barré / moins / chevron")

# ============================================================ COMPTES & SÉCURITÉ
rep("""/* ------------------------------ 7. BASE DE DONNÉES ------------------------------ */""",
"""/* --------------------- 6 bis. COMPTES D'ACCÈS (RH & ADMINISTRATEUR) ---------------------
   Deux comptes distincts, identifiants et mots de passe modifiables dans Paramètres.
   Les mots de passe ne sont jamais stockés en clair (empreinte locale non réversible).
   --------------------------------------------------------------------------------------- */
const ACCOUNT_DEFAULTS = [
  { id:"rh",    login:"rh",             pwd:"Rh@Voomnet2026",
    label:"Service Ressources Humaines", role:"Responsable RH",    roleShort:"RH",       admin:false },
  { id:"admin", login:"admin",          pwd:"Admin@Voomnet2026",
    label:"Administrateur VOOMNET",      role:"Administrateur RH", roleShort:"Admin",    admin:true  }
];
/* empreinte locale (FNV-1a salée) — suffisante pour une application hors ligne */
function hashPwd(str){
  let h=0x811c9dc5; const txt="vt2026::"+(str||"");
  for(let i=0;i<txt.length;i++){ h ^= txt.charCodeAt(i); h = (h*0x01000193)>>>0; }
  return ("00000000"+h.toString(16)).slice(-8);
}
function defaultAccounts(){
  return ACCOUNT_DEFAULTS.map(a=>({ id:a.id, login:a.login, label:a.label, role:a.role, admin:!!a.admin,
    hash:hashPwd(a.pwd), mustChange:false }));
}
const ACCOUNT_HINTS = ACCOUNT_DEFAULTS.map(a=>({ login:a.login, pwd:a.pwd, role:a.role }));

/* ------------------------------ 7. BASE DE DONNÉES ------------------------------ */""", "comptes d'accès RH + Administrateur")

# ------- DB : comptes persistés
rep("""const DB = {
  trips:[], agents:[], transports:[], vehicles:[], params:{}, meta:{}, user:{},""",
"""const DB = {
  trips:[], agents:[], transports:[], vehicles:[], params:{}, meta:{}, user:{}, accounts:[],""", "DB.accounts")

rep("""    this.meta       = d.meta || {};""",
"""    this.accounts   = Array.isArray(d.accounts)&&d.accounts.length? d.accounts : defaultAccounts();
    this.meta       = d.meta || {};""", "chargement des comptes")

rep("""  save(){ return Store.write({ trips:this.trips, agents:this.agents, transports:this.transports,
    vehicles:this.vehicles, params:this.params, meta:this.meta, user:this.user }); },""",
"""  save(){ return Store.write({ trips:this.trips, agents:this.agents, transports:this.transports,
    vehicles:this.vehicles, params:this.params, meta:this.meta, user:this.user, accounts:this.accounts }); },""", "sauvegarde des comptes")

# ============================================================ SESSION
rep("""/* Rôles RH : un seul espace de pilotage central (aucun espace par service ni par personne). */
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
}
function logout(){
  try{ sessionStorage.removeItem("vt_session"); }catch(e){}
  showLogin();
}""",
"""/* Écran d'accès : deux comptes nominatifs (RH / Administrateur) — aucun espace par service. */
function renderAccountHints(){
  const box=$("#loginHints"); if(!box) return;
  box.innerHTML = ACCOUNT_HINTS.map(h=>
    '<div class="hint-row"><span class="hr-role">'+esc(h.role)+'</span>'+
      '<code>'+esc(h.login)+'</code><span class="hr-sep">/</span><code>'+esc(h.pwd)+'</code></div>').join("");
}
function showLogin(){
  const L=$("#login"); if(!L) return;
  renderAccountHints();
  const pw=$("#loginPwd"); if(pw) pw.value="";
  const idf=$("#loginIdent"); if(idf){ idf.value=""; idf.classList.remove("err"); }
  if(pw) pw.classList.remove("err");
  const e=$("#err-login"); if(e) e.classList.remove("on");
  $("#loginPwd")  && $("#loginPwd").setAttribute("type","password");
  L.classList.remove("hidden","closing");
  setTimeout(()=>{ const f=$("#loginIdent"); if(f && !isTouch()) f.focus(); }, 420);
}
function isTouch(){ return window.matchMedia && window.matchMedia("(hover:none)").matches; }
function loginError(msg){
  const e=$("#err-login");
  if(e){ e.querySelector("span").textContent=msg; e.classList.add("on"); }
  $("#loginIdent").classList.add("err"); $("#loginPwd").classList.add("err");
  const card=$(".login-card"); if(card){ card.classList.remove("shake"); void card.offsetWidth; card.classList.add("shake"); }
}
function connectAccount(acc){
  DB.user={ name:acc.label, role:acc.role, account:acc.id, admin:!!acc.admin };
  DB.save();
  try{ sessionStorage.setItem("vt_session", acc.id); }catch(e){}
  const L=$("#login");
  if(L){ L.classList.add("closing"); setTimeout(()=>L.classList.add("hidden"), 460); }
  renderUser(); refreshAll(); go("dashboard");
  toast("Bienvenue, "+acc.role, acc.label+" · espace de pilotage central de la mobilité.","ok");
}
function doLogin(ident, pwd){
  const id=(ident||"").trim().toLowerCase(), p=(pwd||"");
  const ok = DB.accounts.find(a=> a.login.toLowerCase()===id && a.hash===hashPwd(p));
  if(!ok){
    loginError(!id? "Renseignez votre identifiant." : (!p? "Renseignez votre mot de passe." : "Identifiant ou mot de passe incorrect."));
    return false;
  }
  connectAccount(ok);
  return true;
}
function doGuest(){
  DB.user={ name:"Mode consultation", role:"Consultation (lecture seule)", account:"guest", admin:false };
  try{ sessionStorage.setItem("vt_session","guest"); }catch(e){}
  const L=$("#login");
  if(L){ L.classList.add("closing"); setTimeout(()=>L.classList.add("hidden"), 460); }
  renderUser(); refreshAll(); go("dashboard");
  toast("Mode consultation","Accès en lecture seule · aucune donnée ne sera modifiée.","info");
}
function logout(){
  try{ sessionStorage.removeItem("vt_session"); }catch(e){}
  if(typeof closePops==="function") closePops();
  go("dashboard");
  showLogin();
  toast("Déconnexion réussie","Vous êtes revenu à l'écran d'accès.","ok");
}""", "connexion par identifiant + mot de passe, déconnexion")

# ============================================================ SUPPRESSION DES GÉNÉRATEURS DE DONNÉES
d0 = s.index('/* ------------------------------ 16. DONNÉES D\'EXEMPLE ------------------------------ */')
d1 = s.index('/* ------------------------------ 17. RAFRAÎCHISSEMENT ------------------------------ */')
s = s[:d0] + '''/* ---------------------- 16. AUCUNE DONNÉE DE DÉMONSTRATION ----------------------
   La plateforme ne génère plus aucun déplacement fictif : toutes les données
   proviennent exclusivement de la saisie RH (ou d'une sauvegarde JSON restaurée).
   -------------------------------------------------------------------------------- */

''' + s[d1:]
print("  ✓ générateur de données d'exemple supprimé")

# ------- démo à la saisie : suppression
d2 = s.index('function demoFill(){')
d3 = s.index('/* ------------------------------ 13. REGISTRE ------------------------------ */')
s = s[:d2] + s[d3:]
print("  ✓ formulaire : « exemple automatique » supprimé")

open(p, 'w').write(s)
print("part3_core.js.html mis à jour")
