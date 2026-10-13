#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.8 — VERROUILLAGE TOTAL DE L'ACCÈS

1. Suppression du bouton « Mode consultation » : c'était la seule façon d'entrer
   dans la plateforme SANS identifiant.
2. Une ancienne session « consultation » enregistrée dans le navigateur n'ouvre plus rien
   (currentAccount() la refuse) : l'écran d'accès s'affiche.
3. Plus aucun indice sur les comptes dans la page de connexion :
   placeholder « Ex : rh » supprimé, texte « un compte Responsable RH et un compte
   Administrateur » remplacé par une mention générique.
"""

# ---------------------------------------------------------------- 1. structure
p = 'src/part2_body.html'
b = open(p, encoding='utf-8').read()

# 1.a — suppression du séparateur « ou » + du bouton Mode consultation
old = '''        <div class="login-sep">ou</div>
        <button class="link-btn" id="btnLoginSkip" type="button">Mode consultation</button>
'''
assert old in b, "bouton Mode consultation introuvable"
b = b.replace(old, '', 1)

# 1.b — plus d'indice sur l'identifiant
b = b.replace('placeholder="Ex : rh"', 'placeholder="Votre identifiant"')

# 1.c — texte générique (ne révèle plus la structure des comptes)
old_perk = '<li><span class="ic" data-ico="shieldCheck"></span><span><b>Accès nominatif</b> — un compte <b>Responsable RH</b> et un compte <b>Administrateur</b>, traçables et modifiables.</span></li>'
new_perk = '<li><span class="ic" data-ico="shieldCheck"></span><span><b>Accès protégé</b> — identifiant personnel obligatoire, aucune donnée ne quitte cet appareil.</span></li>'
assert old_perk in b, "texte « Accès nominatif » introuvable"
b = b.replace(old_perk, new_perk, 1)

# 1.d — version affichée
b = b.replace('VOOMNET Track · v3.7', 'VOOMNET Track · v3.8').replace('VOOMNET Track v3.7', 'VOOMNET Track v3.8')
open(p, 'w', encoding='utf-8').write(b)
print("✓ page de connexion : bouton « Mode consultation » supprimé, indices retirés")

# ---------------------------------------------------------------- 2. noyau
p2 = 'src/part3_core.js.html'
s = open(p2, encoding='utf-8').read()

# 2.a — une session « guest » n'ouvre plus la plateforme
old_ca = '''function currentAccount(){
  const id=sessionAccountId();
  if(!id) return null;
  return DB.accounts.find(a=>a.id===id) || null;
}'''
new_ca = '''function currentAccount(){
  const id=sessionAccountId();
  if(!id || id==="guest") return null;   /* aucune session anonyme : identifiant obligatoire */
  return DB.accounts.find(a=>a.id===id) || null;
}'''
assert old_ca in s, "currentAccount introuvable"
s = s.replace(old_ca, new_ca, 1)

# 2.b — doGuest() devient un refus explicite (plus aucune entrée sans identifiant)
i = s.index('function doGuest(){')
j = s.index('\n}\n', i) + 3
s = s[:i] + '''function doGuest(){
  /* Accès anonyme désactivé : la plateforme exige un identifiant nominatif. */
  try{ sessionStorage.removeItem("vt_session"); }catch(e){}
  showLogin();
  toast("Accès refusé","Un identifiant est obligatoire pour entrer dans la plateforme.","err");
}
''' + s[j:]
open(p2, 'w', encoding='utf-8').write(s)
print("✓ noyau : session anonyme refusée, doGuest() neutralisé")

# ---------------------------------------------------------------- 3. tableau de bord
p3 = 'src/part3b_dash.js.html'
d = open(p3, encoding='utf-8').read()
old_bind = '  const skip=$("#btnLoginSkip"); if(skip) skip.onclick=()=>doGuest();\n'
assert old_bind in d, "branchement du bouton introuvable"
d = d.replace(old_bind, '', 1)
open(p3, 'w', encoding='utf-8').write(d)
print("✓ branchement du bouton supprimé (aucune référence orpheline)")

# ---------------------------------------------------------------- 4. test automatisé
p4 = 'test/ui_v2.py'
t = open(p4, encoding='utf-8').read()
import re
m = re.search(r'\n\s*# mode consultation.*?\n(?=\s*#|\s*print|\s*await b\.close)', t, re.S)
if m:
    t = t.replace(m.group(0), '''
        # 8bis. VERROUILLAGE : aucun accès sans identifiant (v3.8)
        lock = await pg.evaluate("""(() => ({
            bouton: !!document.querySelector('#btnLoginSkip'),
            placeholderHints: /ex *: *rh/i.test(document.querySelector('#loginIdent')?.placeholder||''),
            infosComptes: /Voomnet2026|un compte Responsable RH/i.test(document.querySelector('#login')?.innerText||'')
        }))()""")
        print("verrouillage — bouton consultation:", lock["bouton"], "| indices:", lock["placeholderHints"], "| infos comptes:", lock["infosComptes"])
        await pg.evaluate("sessionStorage.setItem('vt_session','guest'); location.reload();")
        await pg.wait_for_timeout(3200)
        guest = await pg.evaluate("({ecran: !!document.querySelector('#login') && !document.querySelector('#login').classList.contains('hidden'), vue: document.querySelector('.view.active')?.id})")
        print("session « consultation » forcée → écran d'accès:", guest["ecran"], "| vue:", guest["vue"])
''', 1)
    print("✓ test automatisé mis à jour (le mode consultation doit être refusé)")
else:
    print("⚠ bloc « mode consultation » du test non trouvé — à vérifier manuellement")
open(p4, 'w', encoding='utf-8').write(t)
