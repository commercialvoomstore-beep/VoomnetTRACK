# -*- coding: utf-8 -*-
"""Patch cœur : affichage du rôle/session + blocage visuel des actions administrateur."""
p = 'src/part3_core.js.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  \u2713", label)

# ============================================================ 1. renderUser : rôle + session
rep("""function renderUser(){""",
"""function renderRoleBadges(){
  const a=currentAccount();
  const badge=$("#roleBadge"), txt=$("#roleBadgeTxt");
  if(badge && txt){
    const admin = !!(a && a.admin);
    badge.classList.toggle("admin", admin);
    txt.textContent = a? (admin? "Administrateur" : "Responsable RH") : (isGuest()? "Consultation" : "Hors session");
  }
  const side=$("#sideUserName"), sideRole=$("#sideUserRole"), sideAv=$("#sideAvatar");
  if(side) side.textContent = DB.user.name||"Espace RH";
  if(sideRole) sideRole.textContent = DB.user.role||"";
  if(sideAv) sideAv.textContent = initials(DB.user.name||"RH");
  const card=$("#cardDataMgmt");
  if(card) card.classList.toggle("locked", !isAdmin());
}
function renderUser(){""", "affichage du rôle et de la session")


open(p, 'w').write(s)
print("part3_core.js.html : rôle & session ✓")
