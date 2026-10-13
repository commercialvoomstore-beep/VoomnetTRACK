# -*- coding: utf-8 -*-
"""v3.11b — Retrait des dernières empreintes de mots de passe du fichier livré.

Depuis la v3.11, l'authentification est vérifiée par le serveur : les empreintes
présentes dans le navigateur n'ont plus aucune utilité et n'ont plus à y figurer
(le dépôt est public). Les identifiants de compte ne sont plus qu'une liste
d'affichage, sans secret.
"""
import io, re

p = "src/part3_core.js.html"
s = io.open(p, encoding="utf-8").read()

ANCIEN = '''const ACCOUNT_DEFAULTS = [
  { id:"rh",    login:"rh",    label:"Service Ressources Humaines", role:"Responsable RH",
    admin:false, hash:"6e6b4ab8" },
  { id:"admin", login:"admin", label:"Administrateur VOOMNET",      role:"Administrateur RH",
    admin:true,  hash:"460c9900" }
];
/* empreinte locale (FNV-1a salée) : suffisante pour une application hors ligne */
function hashPwd(str){
  let h=0x811c9dc5; const txt="vt2026::"+(str||"");
  for(let i=0;i<txt.length;i++){ h ^= txt.charCodeAt(i); h = (h*0x01000193)>>>0; }
  return ("00000000"+h.toString(16)).slice(-8);
}
function defaultAccounts(){
  return ACCOUNT_DEFAULTS.map(a=>({ id:a.id, login:a.login, label:a.label, role:a.role,
    admin:!!a.admin, hash:a.hash }));
}'''

NOUVEAU = '''/* v3.11 — Plus AUCUNE empreinte de mot de passe dans le navigateur : l'identité
   est vérifiée par le serveur (scrypt + sessions en base). Cette liste ne sert
   qu'à l'affichage des comptes tant que la base n'a pas répondu. */
const ACCOUNT_DEFAULTS = [
  { id:"rh",    login:"rh",    label:"Service Ressources Humaines", role:"Responsable RH",    admin:false },
  { id:"admin", login:"admin", label:"Administrateur VOOMNET",      role:"Administrateur RH", admin:true  }
];
function defaultAccounts(){
  return ACCOUNT_DEFAULTS.map(a=>({ id:a.id, login:a.login, label:a.label, role:a.role,
    admin:!!a.admin, actif:true }));
}'''

assert ANCIEN in s, "bloc ACCOUNT_DEFAULTS introuvable"
s = s.replace(ANCIEN, NOUVEAU, 1)
assert "6e6b4ab8" not in s and "460c9900" not in s
assert "hashPwd" not in s, "hashPwd encore référencé"
io.open(p, "w", encoding="utf-8").write(s)
print("✓ part3_core.js.html : plus aucune empreinte de mot de passe côté navigateur")
