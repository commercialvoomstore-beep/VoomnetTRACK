#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.7 — SÉCURITÉ (version corrigée) :
   1. plus aucun mot de passe en clair dans le fichier livré (empreintes seules) ;
   2. plus aucun identifiant affiché sur l'écran de connexion.

Empreintes calculées avec le moteur de l'application (Node) :
   hashPwd("Rh@Voomnet2026")    = 6e6b4ab8
   hashPwd("Admin@Voomnet2026") = 460c9900
"""
import re

# ------------------------------------------------------------------ 1. noyau
p = 'src/part3_core.js.html'
s = open(p, encoding='utf-8').read()

# 1.a — remplacer UNIQUEMENT le tableau ACCOUNT_DEFAULTS (borné par son '];')
i = s.index('const ACCOUNT_DEFAULTS = [')
j = s.index('];', i) + 2
new_defs = '''/* Les mots de passe par défaut ne figurent JAMAIS en clair dans ce fichier :
   seules des empreintes non réversibles (FNV-1a salée) sont embarquées. */
const ACCOUNT_DEFAULTS = [
  { id:"rh",    login:"rh",    label:"Service Ressources Humaines", role:"Responsable RH",
    admin:false, hash:"6e6b4ab8" },
  { id:"admin", login:"admin", label:"Administrateur VOOMNET",      role:"Administrateur RH",
    admin:true,  hash:"460c9900" }
];'''
s = s[:i] + new_defs + s[j:]

# 1.b — defaultAccounts() : renvoie l'empreinte embarquée (plus de calcul depuis un mot de passe)
old_da = '''function defaultAccounts(){
  return ACCOUNT_DEFAULTS.map(a=>({ id:a.id, login:a.login, label:a.label, role:a.role,
    admin:!!a.admin, hash:hashPwd(a.pwd) }));
}'''
new_da = '''function defaultAccounts(){
  return ACCOUNT_DEFAULTS.map(a=>({ id:a.id, login:a.login, label:a.label, role:a.role,
    admin:!!a.admin, hash:a.hash }));
}'''
assert old_da in s, "defaultAccounts introuvable"
s = s.replace(old_da, new_da, 1)

# 1.c — supprimer la constante qui exposait les identifiants
s = re.sub(r"const ACCOUNT_HINTS = [^\n]*\n",
           '/* ACCOUNT_HINTS supprimé : aucun identifiant n\'est exposé dans l\'interface. */\n', s)

# 1.d — supprimer la fonction qui alimentait le bloc « Comptes d'accès »
k = s.index("/* Écran d'accès : deux comptes nominatifs")
l = s.index('function isTouch()')
s = s[:k] + s[l:]

# 1.e — supprimer l'appel résiduel
s = s.replace('  renderAccountHints();\n', '')
open(p, 'w', encoding='utf-8').write(s)
print("✓ noyau : empreintes seules, bloc de rappel supprimé, hashPwd conservé")

# ------------------------------------------------------------------ 2. connexion
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
        <div>Accès réservé au personnel autorisé. Les identifiants sont remis par la direction et se
        modifient dans <b>Paramètres → Comptes &amp; sécurité</b>.</div>
      </div>
'''
b = b.replace(old, new, 1)
open(p2, 'w', encoding='utf-8').write(b)
print("✓ écran de connexion : bloc d'identifiants remplacé par une note de confidentialité")

# ------------------------------------------------------------------ 3. Paramètres
p3 = 'src/part3b_dash.js.html'
d = open(p3, encoding='utf-8').read()
old_r = '''    const i=Number(b.dataset.accreset), def=ACCOUNT_DEFAULTS[i];
    DB.accounts[i].login=def.login; DB.accounts[i].hash=hashPwd(def.pwd); DB.save();
    renderAccounts(); toast("Identifiant rétabli", def.login+" · mot de passe "+def.pwd,"ok");'''
new_r = '''    const i=Number(b.dataset.accreset), def=ACCOUNT_DEFAULTS[i];
    DB.accounts[i].login=def.login; DB.accounts[i].hash=def.hash; DB.save();
    renderAccounts();
    toast("Identifiant rétabli", def.login+" · le mot de passe d'origine est de nouveau actif.","ok");'''
assert old_r in d, "bouton rétablir introuvable"
d = d.replace(old_r, new_r, 1)
open(p3, 'w', encoding='utf-8').write(d)
print("✓ bouton « rétablir l'identifiant » : plus aucun mot de passe affiché")
