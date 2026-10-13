#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.7 — SÉCURITÉ : les identifiants n'apparaissent plus sur l'écran de connexion,
et les mots de passe par défaut ne sont plus en clair dans le fichier livré.

Les empreintes ci-dessous ont été calculées avec le moteur de l'application (Node = même moteur JS) :
  hashPwd("Rh@Voomnet2026")    = 6e6b4ab8
  hashPwd("Admin@Voomnet2026") = 460c9900
Elles ne permettent PAS de retrouver le mot de passe.
"""

# ---------------------------------------------------------------- 1. noyau JS
p = 'src/part3_core.js.html'
s = open(p, encoding='utf-8').read()

# 1.a — plus aucun mot de passe en clair : uniquement des empreintes
old_defs = s[s.index('const ACCOUNT_DEFAULTS = ['):s.index('const ACCOUNT_HINTS')]
old_defs = s[s.index('const ACCOUNT_DEFAULTS = ['):s.index('\nconst ACCOUNT_HINTS')]
new_defs = '''/* Les mots de passe par défaut ne figurent JAMAIS en clair dans ce fichier :
   seules des empreintes non réversibles sont embarquées. */
const ACCOUNT_DEFAULTS = [
  { id:"rh",    login:"rh",    label:"Service Ressources Humaines", role:"Responsable RH",
    admin:false, hash:"6e6b4ab8" },
  { id:"admin", login:"admin", label:"Administrateur VOOMNET",      role:"Administrateur RH",
    admin:true,  hash:"460c9900" }
];'''
s = s.replace(old_defs, new_defs, 1)

# 1.b — defaultAccounts() renvoie directement les empreintes
old_da = s[s.index('function defaultAccounts(){'):s.index('\nconst ACCOUNT_HINTS')]
new_da = '''function defaultAccounts(){
  return ACCOUNT_DEFAULTS.map(a=>({ id:a.id, login:a.login, label:a.label, role:a.role,
    admin:!!a.admin, hash:a.hash }));
}'''
s = s.replace(old_da, new_da, 1)

# 1.c — suppression de la constante de rappel des identifiants
i = s.index('const ACCOUNT_HINTS')
j = s.index('\n', i) + 1
s = s[:i] + '/* ACCOUNT_HINTS supprimé : aucun identifiant n\'est exposé dans l\'interface. */\n' + s[j:]

# 1.d — suppression de la fonction qui alimentait le bloc « Comptes d'accès »
start = s.index("/* Écran d'accès : deux comptes nominatifs")
end = s.index('function isTouch()')
s = s[:start] + s[end:]

# 1.e — suppression de l appel à renderAccountHints()
s = s.replace('  renderAccountHints();\n', '')
open(p, 'w', encoding='utf-8').write(s)
print("✓ noyau : mots de passe par défaut → empreintes seules ; bloc de rappel supprimé")

# ---------------------------------------------------------------- 2. écran de connexion
p2 = 'src/part2_body.html'
b = open(p2, encoding='utf-8').read()
old = '''      <details class="login-help">
        <summary><span class="ic" data-ico="key"></span> Comptes d'accès — RH &amp; Administrateur</summary>
        <div class="login-hints" id="loginHints"></div>
        <div class="small">Ces identifiants sont modifiables dans <b>Paramètres → Comptes &amp; sécurité</b>.</div>
      </details>
'''
assert old in b, "bloc de connexion introuvable"
new = '''      <div class="login-note">
        <span class="ic" data-ico="lock"></span>
        <div>Accès réservé au personnel autorisé. Les identifiants sont remis par la direction —
        ils se modifient dans <b>Paramètres → Comptes &amp; sécurité</b>.</div>
      </div>
'''
b = b.replace(old, new, 1)
open(p2, 'w', encoding='utf-8').write(b)
print("✓ écran de connexion : bloc d'identifiants remplacé par une note de confidentialité")

# ---------------------------------------------------------------- 3. bouton « rétablir » (Paramètres)
p3 = 'src/part3b_dash.js.html'
d = open(p3, encoding='utf-8').read()
old_r = '''  $$("[data-accreset]").forEach(b=>b.onclick=()=>{
    const i=Number(b.dataset.accreset), def=ACCOUNT_DEFAULTS[i];
    DB.accounts[i].login=def.login; DB.accounts[i].hash=hashPwd(def.pwd); DB.save();
    renderAccounts(); toast("Identifiant rétabli", def.login+" · mot de passe "+def.pwd,"ok");
  });'''
new_r = '''  $$("[data-accreset]").forEach(b=>b.onclick=()=>{
    const i=Number(b.dataset.accreset), def=ACCOUNT_DEFAULTS[i];
    DB.accounts[i].login=def.login; DB.accounts[i].hash=def.hash; DB.save();
    renderAccounts();
    toast("Identifiant rétabli", def.login+" · le mot de passe d'origine est de nouveau actif.","ok");
  });'''
assert old_r in d, "bouton rétablir introuvable"
d = d.replace(old_r, new_r, 1)
open(p3, 'w', encoding='utf-8').write(d)
print("✓ bouton « rétablir l'identifiant » : plus aucun mot de passe affiché")
