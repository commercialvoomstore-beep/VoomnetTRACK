# -*- coding: utf-8 -*-
"""v3.11 — l'interface travaille réellement sur la base PostgreSQL (Neon).

Modifie les sources de l'application pour :
  1. brancher la couche Cloud (src/part3c_api.js.html) dans le build ;
  2. authentifier via l'API (plus aucune vérification dans le navigateur) ;
  3. charger / écrire les données en base, écran clair si la base ne répond pas ;
  4. gérer les comptes via l'API (mot de passe haché côté serveur) ;
  5. afficher l'état de la base dans l'en-tête.
Aucune fonctionnalité existante n'est supprimée.
"""
import io, sys

def lire(p): return io.open(p, encoding="utf-8").read()
def ecrire(p, s): io.open(p, "w", encoding="utf-8").write(s)
def remplacer(s, avant, apres, nom):
    assert avant in s, "ANCRE INTROUVABLE : " + nom
    assert s.count(avant) == 1, "ANCRE AMBIGUË (%d) : %s" % (s.count(avant), nom)
    return s.replace(avant, apres, 1)

# ---------------------------------------------------------------- build.py
p = "build.py"
s = lire(p)
s = remplacer(s,
  'for f in ("part1_head.html", "part2_body.html", "part3_core.js.html",\n                   "part3b_dash.js.html", "part4_pdf.js.html")]',
  'for f in ("part1_head.html", "part2_body.html", "part3_core.js.html",\n                   "part3c_api.js.html", "part3b_dash.js.html", "part4_pdf.js.html")]',
  "build : liste des parties")
ecrire(p, s)
print("✓ build.py : part3c_api.js.html ajouté")

# ---------------------------------------------------------------- part1_head.html (styles)
p = "src/part1_head.html"
s = lire(p)
css = """
/* ---- v3.11 : état de la base de données & écran « base injoignable » ---- */
.cloud-off{position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;padding:24px;
  background:linear-gradient(180deg,rgba(248,247,250,.96),rgba(241,236,245,.98));backdrop-filter:blur(6px)}
.cloud-off.on{display:flex}
.cloud-off-card{width:min(460px,100%);background:#fff;border:1px solid var(--line,#E7E1F0);border-radius:18px;
  box-shadow:0 24px 60px rgba(48,22,80,.16);padding:30px 28px;text-align:center;display:flex;flex-direction:column;gap:10px;align-items:center}
.cloud-off-ic{width:52px;height:52px;border-radius:15px;display:grid;place-items:center;background:var(--warn-bg,#FDF6E3);
  color:var(--gold-real,#B58A2B);border:1px solid #F0E3BC}
.cloud-off-ic svg{width:26px;height:26px}
.cloud-off-card b{font-size:17px;color:var(--ink,#2A1A44);font-weight:680}
.cloud-off-card p{margin:0;font-size:13.5px;line-height:1.55;color:var(--ink2,#5A4A75)}
.cloud-off-d{font-size:12.5px;color:var(--silver,#8E93A1)}
.cloud-off-card .btn{margin-top:8px}
#cloudState{font-variant-numeric:tabular-nums}
@media (max-width:900px){ #cloudState{display:none} }
"""
ancre = "</style>"
assert s.count(ancre) >= 1
s = s.replace(ancre, css + "\n" + ancre, 1)
ecrire(p, s)
print("✓ part1_head.html : styles ajoutés")

# ---------------------------------------------------------------- part2_body.html (badge + mention)
p = "src/part2_body.html"
s = lire(p)
s = remplacer(s,
  '      <span class="chip gold" id="chipMonth" title="Mois courant">—</span>',
  '      <span class="chip" id="cloudState" title="État de la base de données"><span class="ic" data-ico="refresh"></span><span id="cloudStateTxt">Connexion…</span></span>\n\n      <span class="chip gold" id="chipMonth" title="Mois courant">—</span>',
  "topbar : badge base")
s = remplacer(s,
  '<div class="login-foot">Données conservées localement sur cet appareil · VOOMNET Track v3.10</div>',
  '<div class="login-foot">Données centralisées dans la base sécurisée VOOMNET · VOOMNET Track v3.11</div>',
  "pied de l'écran d'accès")
s = s.replace("VOOMNET Track · v3.10", "VOOMNET Track · v3.11")
ecrire(p, s)
print("✓ part2_body.html : badge + témoin v3.11")

# ---------------------------------------------------------------- part3_core.js.html
p = "src/part3_core.js.html"
s = lire(p)

# 1) alias d'état : vehicules ↔ vehicles, comptes ↔ accounts (une seule vérité)
s = remplacer(s,
  """  removeVehicle(id){ this.vehicles=this.vehicles.filter(v=>v.id!==id); this.save(); }
};""",
  """  removeVehicle(id){ this.vehicles=this.vehicles.filter(v=>v.id!==id); this.save(); }
};
/* v3.11 — la base parle de « vehicules » et « comptes » : on garde un seul état. */
Object.defineProperty(DB, "vehicules", { get(){ return this.vehicles; }, set(v){ this.vehicles = v; }, configurable: true });
Object.defineProperty(DB, "comptes",   { get(){ return this.accounts; }, set(v){ this.accounts = v; }, configurable: true });
DB.services = DB.services || SERVICES.slice();""",
  "part3_core : alias d'état")

# 2) connexion : le serveur décide (plus aucune comparaison locale d'empreinte)
s = remplacer(s,
  """function doLogin(ident, pwd){
  const id=(ident||"").trim().toLowerCase(), p=(pwd||"");
  const ok = DB.accounts.find(a=> a.login.toLowerCase()===id && a.hash===hashPwd(p));
  if(!ok){
    loginError(!id? "Renseignez votre identifiant." : (!p? "Renseignez votre mot de passe." : "Identifiant ou mot de passe incorrect."));
    return false;
  }
  connectAccount(ok);
  return true;
}""",
  """async function doLogin(ident, pwd){
  const id=(ident||"").trim().toLowerCase(), p=(pwd||"");
  if(!id){ loginError("Renseignez votre identifiant."); return false; }
  if(!p){ loginError("Renseignez votre mot de passe."); return false; }
  /* v3.11 : l'authentification est vérifiée par le serveur, jamais dans le navigateur. */
  const btn=$("#btnLogin"); const libelle = btn? btn.innerHTML : "";
  if(btn){ btn.disabled=true; btn.innerHTML='<span class="ic" data-ico="refresh"></span> Vérification…'; hydrateIcons(btn); }
  try{
    const profil = await Cloud.connexion(id, p);
    Cloud.ouvrirSession(profil);
    return true;
  }catch(e){
    if(e.code==="RESEAU" || e.statut>=500){
      Cloud.ecranBase(true, "Base de données injoignable", e.message || "");
      return false;
    }
    if(e.code==="TROP_DE_TENTATIVES") loginError("Trop de tentatives. Patientez quelques minutes.");
    else if(e.code==="COMPTE_INACTIF") loginError("Ce compte est désactivé.");
    else loginError(!p? "Renseignez votre mot de passe." : "Identifiant ou mot de passe incorrect.");
    return false;
  }finally{
    if(btn){ btn.disabled=false; btn.innerHTML=libelle; hydrateIcons(btn); }
  }
}""",
  "doLogin → serveur")

# 3) déconnexion : la session serveur est révoquée
s = remplacer(s,
  """function logout(){
  try{ sessionStorage.removeItem("vt_session"); }catch(e){}""",
  """function logout(){
  /* v3.11 : révocation de la session côté serveur (le jeton ne peut plus servir). */
  try{ if(typeof Cloud!=="undefined") Cloud.deconnexion(); }catch(e){}
  try{ sessionStorage.removeItem("vt_session"); }catch(e){}""",
  "logout → serveur")
ecrire(p, s)
print("✓ part3_core.js.html : connexion et déconnexion côté serveur")

# ---------------------------------------------------------------- part3b_dash.js.html
p = "src/part3b_dash.js.html"
s = lire(p)

# 1) démarrage : la base est interrogée avant d'afficher quoi que ce soit
s = remplacer(s,
  """  DB.load();
  hydrateIcons(document);
  hydrateBrand(document);
  initSplash(()=>{ if(!hasSession()) showLogin(); });""",
  """  DB.load();
  hydrateIcons(document);
  hydrateBrand(document);
  /* v3.11 : l'application se connecte d'abord à la base de données de l'entreprise.
     Sans base, aucune donnée locale n'est utilisée et un écran clair propose de réessayer. */
  Cloud.brancherEcritures();
  initSplash(()=>{ Cloud.demarrer(); });""",
  "init → base")

# 2) bouton de connexion : appel asynchrone au serveur
s = remplacer(s,
  """  const tryLogin=()=>{
    const ok = doLogin($("#loginIdent").value, $("#loginPwd").value);
    if(ok){ const p=$("#loginPwd"); if(p) p.value=""; }
  };""",
  """  const tryLogin=async ()=>{
    const ok = await doLogin($("#loginIdent").value, $("#loginPwd").value);
    if(ok){ const p=$("#loginPwd"); if(p) p.value=""; }
  };""",
  "tryLogin → async")

# 3) gestion des comptes : tout passe par l'API (mot de passe haché côté serveur)
s = remplacer(s,
  """  a.login=login;
  a.label=label||a.label;
  if(pwd) a.hash=hashPwd(pwd);
  DB.save();
  if(a.id===sessionAccountId()){ DB.user.name=a.label; DB.user.role=a.role; DB.save(); renderUser(); }
  renderAccounts();
  toast("Compte mis à jour", a.login+" · connexion "+(pwd? "et mot de passe modifiés":"inchangée"),"ok");
}""",
  """  /* v3.11 : l'enregistrement est fait par le serveur (le mot de passe y est haché ;
     l'application ne voit ni n'écrit jamais d'empreinte). */
  (async ()=>{
    try{
      await Cloud.modifierCompte(a.id, { login: login, label: label||a.label });
      if(pwd) await Cloud.motDePasseCompte(a.id, pwd);
      await Cloud.chargerEtat();
      renderAccounts(); refreshAll();
      if(a.id===sessionAccountId()){ const moi=DB.accounts.find(x=>x.id===a.id); if(moi){ DB.user.name=moi.label; DB.user.role=moi.role; renderUser(); } }
      toast("Compte mis à jour", login+" · enregistré dans la base"+(pwd? " (mot de passe modifié)":""), "ok");
    }catch(e){
      toast("Modification refusée", e.message, "err");
    }
  })();
}""",
  "saveAccount → API")

# 4) « rétablir l'accès d'origine » : côté serveur également
s = remplacer(s,
  """  $$("[data-accreset]").forEach(b=>b.onclick=()=>{
    const i=Number(b.dataset.accreset), def=ACCOUNT_DEFAULTS[i];
    DB.accounts[i].login=def.login; DB.accounts[i].hash=def.hash; DB.save();
    renderAccounts();
    toast("Identifiant rétabli", def.login+" · le mot de passe d'origine est de nouveau actif.","ok");
  });""",
  """  $$("[data-accreset]").forEach(b=>b.onclick=async ()=>{
    const a=DB.accounts[Number(b.dataset.accreset)];
    if(!a) return;
    if(!confirm("Rétablir l'accès d'origine du compte « "+a.label+" » ?\\n\\nLe mot de passe d'origine redeviendra actif et les sessions ouvertes seront fermées.")) return;
    try{
      await Cloud.reinitialiserCompte(a.id);
      await Cloud.chargerEtat();
      renderAccounts();
      toast("Accès rétabli", a.label+" · le mot de passe d'origine est de nouveau actif.","ok");
    }catch(e){ toast("Réinitialisation impossible", e.message, "err"); }
  });""",
  "reset compte → API")
ecrire(p, s)
print("✓ part3b_dash.js.html : comptes et démarrage via l'API")

print("\nPatch v3.11 appliqué.")
