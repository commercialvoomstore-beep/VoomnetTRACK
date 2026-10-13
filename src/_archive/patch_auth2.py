# -*- coding: utf-8 -*-
"""Patch affichage : connexion RH/Admin, déconnexion, comptes & sécurité, KPI animés, fin des données de démo."""
p = 'src/part3b_dash.js.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  ✓", label)

# ============================================================ 2. COMPTES & SÉCURITÉ (paramètres)
rep("""/* ------------------------------ 8. INITIALISATION ------------------------------ */""",
"""/* ================= 7 bis. COMPTES & SÉCURITÉ (Paramètres) ================= */
function renderAccounts(){
  const box=$("#accountCards"); if(!box) return;
  box.innerHTML = DB.accounts.map((a,i)=>
    '<div class="account-item" data-acc="'+i+'">'+
      '<div class="account-head">'+
        '<span class="ac-ic">'+ic(a.admin? "shieldCheck":"userCog")+'</span>'+
        '<span class="ac-who"><b>'+esc(a.label)+'</b><span>'+esc(a.role)+' · '+(a.admin? "accès complet":"pilotage RH")+'</span></span>'+
        (a.id===sessionAccountId()? '<span class="st-pill ok">'+ic("check")+'Connecté</span>':'')+
      '</div>'+
      '<div class="grid g-2" style="gap:0 16px">'+
        '<div class="field"><label for="acLogin'+i+'">Identifiant</label>'+
          '<input class="input" id="acLogin'+i+'" value="'+esc(a.login)+'" autocomplete="off" spellcheck="false"></div>'+
        '<div class="field"><label for="acPwd'+i+'">Nouveau mot de passe</label>'+
          '<input class="input" id="acPwd'+i+'" type="password" placeholder="Laisser vide pour conserver" autocomplete="new-password"></div>'+
      '</div>'+
      '<div class="field"><label for="acLabel'+i+'">Nom du compte</label>'+
        '<input class="input" id="acLabel'+i+'" value="'+esc(a.label)+'"></div>'+
      '<div class="btn-row"><button class="btn btn-primary btn-sm" data-accsave="'+i+'">'+ic("check")+' Enregistrer</button>'+
        '<button class="btn btn-ghost btn-sm" data-accreset="'+i+'">'+ic("refresh")+' Rétablir l\\'identifiant par défaut</button></div>'+
    '</div>').join("");
  $$("[data-accsave]").forEach(b=>b.onclick=()=>saveAccount(Number(b.dataset.accsave)));
  $$("[data-accreset]").forEach(b=>b.onclick=()=>{
    const i=Number(b.dataset.accreset), def=ACCOUNT_DEFAULTS[i];
    DB.accounts[i].login=def.login; DB.accounts[i].hash=hashPwd(def.pwd); DB.save();
    renderAccounts(); toast("Identifiant rétabli", def.login+" · mot de passe "+def.pwd,"ok");
  });
}
function saveAccount(i){
  const a=DB.accounts[i];
  const login=$("#acLogin"+i).value.trim(), pwd=$("#acPwd"+i).value, label=$("#acLabel"+i).value.trim();
  if(login.length<3){ toast("Identifiant trop court","Choisissez au moins 3 caractères.","err"); return; }
  if(DB.accounts.some((x,j)=> j!==i && x.login.toLowerCase()===login.toLowerCase())){
    toast("Identifiant déjà utilisé","Chaque compte doit avoir un identifiant unique.","err"); return; }
  if(pwd && pwd.length<6){ toast("Mot de passe trop court","Prévoyez au moins 6 caractères.","err"); return; }
  a.login=login;
  a.label=label||a.label;
  if(pwd) a.hash=hashPwd(pwd);
  DB.save();
  if(a.id===sessionAccountId()){ DB.user.name=a.label; DB.user.role=a.role; DB.save(); renderUser(); }
  renderAccounts();
  toast("Compte mis à jour", a.login+" · connexion "+(pwd? "et mot de passe modifiés":"inchangée"),"ok");
}

/* ------------------------------ 8. INITIALISATION ------------------------------ */""", "module comptes & sécurité")

# ============================================================ 3. KPI : compteur animé
rep("""function kpiCard(o){""",
"""/* compteur animé (respecte prefers-reduced-motion) — valeurs de KPI */
function animateValue(el, target, unit){
  if(!el) return;
  const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fmt = v => fmtN(Math.round(v));
  if(reduce || !target){ el.textContent=fmt(target||0); return; }
  const dur=760, t0=performance.now();
  const step=now=>{
    const p=Math.min(1,(now-t0)/dur), e=1-Math.pow(1-p,3);
    el.textContent=fmt(target*e);
    if(p<1 && el.isConnected) requestAnimationFrame(step); else el.textContent=fmt(target);
  };
  requestAnimationFrame(step);
}
function kpiCard(o){""", "fonction de compteur animé")

rep("""    '<div class="val">'+o.value+(o.unit? ' <small>'+esc(o.unit)+'</small>':'')+'</div>'+""",
"""    '<div class="val"><span class="num"'+(o.amount!==undefined? ' data-count="'+o.amount+'"':'')+'>'+o.value+'</span>'+(o.unit? ' <small>'+esc(o.unit)+'</small>':'')+'</div>'+""", "structure KPI pour le compteur")

# ============================================================ 4. INIT : liaisons
rep("""  /* navigation */""",
"""  /* comptes & sécurité */
  renderAccounts();

  /* navigation */""", "rendu initial des comptes")

rep("""  const goNow=$("#btnLogin"); if(goNow) goNow.onclick=()=>{
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
  const skip=$("#btnLoginSkip"); if(skip) skip.onclick=()=>doLogin("Mode consultation","Consultation (lecture seule)");""",
"""  /* ---- écran d'accès : identifiant + mot de passe ---- */
  const tryLogin=()=>{
    const ok = doLogin($("#loginIdent").value, $("#loginPwd").value);
    if(ok){ const p=$("#loginPwd"); if(p) p.value=""; }
  };
  const goNow=$("#btnLogin"); if(goNow) goNow.onclick=tryLogin;
  const skip=$("#btnLoginSkip"); if(skip) skip.onclick=()=>doGuest();
  ["loginIdent","loginPwd"].forEach(id=>{
    const el=$("#"+id); if(!el) return;
    el.addEventListener("keydown",e=>{ if(e.key==="Enter") tryLogin(); });
    el.addEventListener("input",()=>{
      el.classList.remove("err");
      const b=$("#err-login"); if(b) b.classList.remove("on");
    });
  });
  const eye=$("#btnEye");
  if(eye) eye.onclick=()=>{
    const p=$("#loginPwd"); if(!p) return;
    const show = p.type==="password";
    p.type = show? "text":"password";
    eye.innerHTML = ic(show? "eyeOff":"eye");
    p.focus();
  };

  /* ---- déconnexion (header, sidebar, menu) ---- */
  const bindLogout=sel=>{ const b=$(sel); if(b) b.onclick=()=>logout(); };
  bindLogout("#btnLogoutTop"); bindLogout("#btnLogoutSide");""", "connexion identifiant/mot de passe + déconnexion")

# ============================================================ 5. FIN DES DONNÉES DE DÉMO
rep("""  if(!DB.trips.length && !DB.meta.seeded){ seedDemo(true); DB.meta.seeded=true; DB.save(); }
""", "", "plus de génération automatique au démarrage")
rep("""  $("#btnSeedDemo").onclick=()=>{ seedDemo(); refreshAll(); };""", "", "bouton Exemples retiré")
rep("""  $("#btnDemoFill").onclick=demoFill;
""", "", "exemple automatique du formulaire retiré")
rep("""  $("#btnSeed2").onclick=()=>{ seedDemo(); refreshAll(); renderParams(); };
""", "", "données d'exemple des paramètres retirées")

# ============================================================ 6. SÉCURITÉ : actions sensibles réservées à l'administrateur
rep("""  $("#btnWipe").onclick=()=>confirmDlg(\"Tout effacer ?\",""",
"""  if(!isAdmin()){
    const lock=(sel,msg)=>{ const b=$(sel); if(!b) return;
      b.disabled=true; b.title=msg; b.style.opacity=".5"; b.style.cursor="not-allowed"; };
    lock("#btnWipe","Action réservée à l'administrateur");
    lock("#fileRestore","Action réservée à l'administrateur");
  }
  $("#btnWipe").onclick=()=>{ if(!isAdmin()){ toast("Action réservée","Seul le compte Administrateur peut effacer les données.","err"); return; } confirmDlg(\"Tout effacer ?\",""", "actions sensibles protégées")

open(p, 'w').write(s)
print("part3b_dash.js.html mis à jour")
