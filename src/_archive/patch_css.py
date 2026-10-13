# -*- coding: utf-8 -*-
"""Patch CSS : palette violet doux + or, espacement généreux, écran d'accès RH, nouveaux composants."""
p = 'src/part1_head.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  ✓", label)

# ---------------------------------------------------------------- 1. PALETTE
rep('''  /* ---- Palette ---- */
  --primary:#32104F;
  --primary-600:#43156A;
  --secondary:#6F2DBD;
  --secondary-500:#8347CE;
  --accent:#D7B238;
  --accent-600:#BFA02F;
  --bg:#F7F6FA;
  --surface:#FFFFFF;
  --surface-2:#FBFAFD;
  --surface-3:#F3F1F8;
  --line:#EDEAF3;
  --line-2:#E3DFEC;
  --ink:#211A27;
  --ink-2:#4A4550;
  --muted:#77727D;
  --faint:#9C97A3;
  --ok:#38A879; --ok-bg:#EBF8F2;
  --warn:#B98F1F; --warn-bg:#FCF6E3;
  --danger:#D95C5C; --danger-bg:#FDF0F0;
  --info:#4C6FFF; --info-bg:#EEF2FF;
  --primary-50:#F5F1FA; --primary-100:#ECE4F6; --primary-200:#DCCEEC;
  --secondary-50:#F5EFFC; --accent-50:#FBF6E4;''',
'''  /* ---- Palette : violet DOUX + OR premium ---- */
  --primary:#4A2A63;          /* violet principal (profond mais doux) */
  --primary-600:#3D2253;
  --secondary:#6B4A82;        /* violet secondaire */
  --secondary-500:#7E5C97;
  --accent:#C9A227;           /* or principal */
  --accent-600:#A98A1F;
  --accent-300:#E2C866;       /* or clair */
  --bg:#F8F7FA;
  --surface:#FFFFFF;
  --surface-2:#FCFBFD;
  --surface-3:#F1ECF5;        /* violet très clair */
  --line:#ECE7F0;
  --line-2:#E1DAE7;
  --ink:#292331;
  --ink-2:#4B4451;
  --muted:#77717D;
  --faint:#9A95A0;
  --ok:#43A982; --ok-bg:#EDF7F3;
  --warn:#B08A22; --warn-bg:#FBF6E7;
  --danger:#C96A6A; --danger-bg:#FBEFEF;
  --info:#5D6BB0; --info-bg:#F0F1FA;
  --primary-50:#F6F2F9; --primary-100:#EFE8F4; --primary-200:#DFD2E9;
  --secondary-50:#F5F0F8; --accent-50:#FBF7E7;''', "palette violet doux + or")

# ---------------------------------------------------------- 2. RADII / OMBRES
rep('''  --r-xs:8px; --r-sm:10px; --r:12px; --r-md:14px; --r-lg:18px; --r-xl:22px; --r-2xl:28px; --pill:999px;''',
'''  --r-xs:8px; --r-sm:10px; --r:12px; --r-md:14px; --r-lg:18px; --r-card:20px; --r-xl:24px; --r-2xl:30px; --pill:999px;''', "radii")

rep('''  --sh-xs:0 1px 2px rgba(33,26,39,.04);
  --sh-sm:0 1px 2px rgba(33,26,39,.04), 0 6px 16px -10px rgba(33,26,39,.10);
  --sh-md:0 2px 6px rgba(33,26,39,.04), 0 20px 44px -26px rgba(50,16,79,.20);
  --sh-lg:0 36px 70px -38px rgba(50,16,79,.32);
  --ring:0 0 0 4px rgba(111,45,189,.13);
  --ring-gold:0 0 0 4px rgba(215,178,56,.18);''',
'''  --sh-xs:0 1px 2px rgba(41,35,49,.03);
  --sh-sm:0 1px 2px rgba(41,35,49,.03), 0 8px 20px -14px rgba(41,35,49,.10);
  --sh-md:0 2px 8px rgba(41,35,49,.03), 0 22px 48px -30px rgba(74,42,99,.22);
  --sh-lg:0 40px 78px -44px rgba(74,42,99,.30);
  --ring:0 0 0 4px rgba(107,74,130,.14);
  --ring-gold:0 0 0 4px rgba(201,162,39,.18);''', "ombres plus douces")

# ---------------------------------------------------------------- 3. ESPACES
rep('''  --sb-w:274px; --header-h:74px; --content-max:1460px;
  --gap:20px; --gap-lg:26px;''',
'''  --sb-w:276px; --header-h:78px; --content-max:1520px;
  --gap:22px; --gap-lg:34px;''', "variables de rythme")

rep('.content{padding:26px 30px 72px;max-width:var(--content-max);width:100%;margin:0 auto}',
    '.content{padding:34px 42px 110px;max-width:var(--content-max);width:100%;margin:0 auto}', "padding du contenu")

rep('''.card.pad-lg{padding:26px 26px 24px}
.card-h{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;margin-bottom:18px}''',
'''.card.pad-lg{padding:30px 32px 28px}
.card-h{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:22px}''', "padding des cartes")

rep('''.card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);''',
'''.card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-card);''', "rayon des cartes")

rep('.section-h{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;margin-bottom:14px}',
    '.section-h{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:20px}', "en-têtes de section")

rep('.nav-label{\n  font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);\n  padding:16px 10px 8px;\n}',
    '.nav-label{\n  font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);\n  padding:22px 12px 9px;\n}', "espace des groupes de nav")

rep('''.nav-item{
  position:relative;display:flex;align-items:center;gap:11px;padding:10px 12px;border-radius:var(--r);''',
'''.nav-item{
  position:relative;display:flex;align-items:center;gap:12px;padding:11px 13px;border-radius:var(--r-md);''', "nav-item plus aéré")

rep('.kpi{\n  position:relative;padding:18px 18px 16px;border-radius:var(--r-lg);background:var(--surface);',
    '.kpi{\n  position:relative;padding:22px 22px 20px;border-radius:var(--r-card);background:var(--surface);', "padding des KPI")

rep('.kpi .val{font-size:23px;font-weight:750;letter-spacing:-.035em;margin-top:12px;color:var(--ink);line-height:1.1}',
    '.kpi .val{font-size:25px;font-weight:750;letter-spacing:-.035em;margin-top:14px;color:var(--ink);line-height:1.1}', "taille des valeurs KPI")

rep('.kpi .foot{display:flex;align-items:center;gap:8px;margin-top:10px;font-size:11.8px;color:var(--muted);flex-wrap:wrap}',
    '.kpi .foot{display:flex;align-items:center;gap:8px;margin-top:12px;font-size:11.8px;color:var(--muted);flex-wrap:wrap}', "pied des KPI")

rep('.welcome{\n  display:grid;grid-template-columns:1.4fr auto;gap:20px;align-items:center;\n  padding:26px 28px;border-radius:var(--r-xl);',
    '.welcome{\n  display:grid;grid-template-columns:1.5fr auto;gap:24px;align-items:center;\n  padding:32px 34px;border-radius:var(--r-xl);', "bannière d'accueil")

# ------------------------------------------- 4. ÉCRAN D'ACCÈS RH (remplace v2)
old_login_start = s.index('#login{')
old_login_end   = s.index('/* ================================= PRINT ================================= */')
new_login = '''#login{
  position:fixed;inset:0;z-index:900;display:grid;place-items:center;padding:32px;overflow:auto;
  background:
    radial-gradient(1000px 560px at 8% -8%, #F3EDF9 0%, rgba(243,237,249,0) 62%),
    radial-gradient(820px 480px at 98% 106%, #FBF6E6 0%, rgba(251,246,230,0) 58%),
    var(--bg);
  transition:opacity .42s var(--ease), visibility .42s;
}
#login.closing{opacity:0;visibility:hidden;pointer-events:none}
.login-card{
  width:min(1020px,100%);background:var(--surface);border:1px solid var(--line);border-radius:var(--r-2xl);
  box-shadow:var(--sh-lg);overflow:hidden;display:grid;grid-template-columns:1.05fr 1fr;
}
/* --- panneau de marque --- */
.login-brand{
  padding:46px 44px;display:flex;flex-direction:column;gap:22px;position:relative;
  background:linear-gradient(150deg,#F6F1FA 0%,#FFFFFF 66%);border-right:1px solid var(--line);
}
.login-brand::before{
  content:"";position:absolute;left:0;top:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--secondary),var(--accent-300),var(--accent));
}
.login-logo{width:min(292px,84%);height:auto;display:block;margin-bottom:6px}   /* proportions exactes */
.login-badge{
  display:inline-flex;align-items:center;gap:9px;align-self:flex-start;padding:7px 14px;border-radius:var(--pill);
  background:rgba(255,255,255,.9);border:1px solid var(--line-2);font-size:11.5px;font-weight:650;
  color:var(--primary);letter-spacing:.01em;
}
.login-badge .ic{width:14px;height:14px;color:var(--accent)}
.login-brand h2{font-size:22px;letter-spacing:-.024em;line-height:1.32;margin-top:2px}
.login-brand p{font-size:13px;color:var(--muted);line-height:1.72;max-width:42ch}
.login-perks{list-style:none;padding:0;margin:auto 0 0;display:flex;flex-direction:column;gap:14px}
.login-perks li{display:flex;gap:11px;align-items:flex-start;font-size:12.8px;color:var(--ink-2)}
.login-perks .ic{width:16px;height:16px;color:var(--ok);margin-top:2px;flex:0 0 16px}
.login-perks b{font-weight:640;color:var(--ink)}
/* --- formulaire --- */
.login-form{padding:46px 44px;display:flex;flex-direction:column;gap:20px}
.login-form h3{font-size:19px;letter-spacing:-.02em}
.login-form .lead{font-size:13px;color:var(--muted);line-height:1.7;margin-top:6px}
.login-form .field{margin-bottom:0}
.login-role-hint{
  display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--muted);
  background:var(--surface-3);border:1px solid var(--line-2);border-radius:var(--r-md);padding:10px 13px;
}
.login-role-hint .ic{width:14px;height:14px;color:var(--secondary);flex:0 0 14px}
.login-actions{display:flex;flex-direction:column;gap:12px;margin-top:4px}
.login-foot{margin-top:auto;font-size:11px;color:var(--faint);text-align:center;line-height:1.75;padding-top:8px}
.login-sep{display:flex;align-items:center;gap:12px;color:var(--faint);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
.login-sep::before,.login-sep::after{content:"";height:1px;flex:1;background:var(--line-2)}
@media(max-width:880px){
  #login{padding:20px}
  .login-card{grid-template-columns:1fr}
  .login-brand{padding:30px 26px;border-right:none;border-bottom:1px solid var(--line);gap:16px}
  .login-brand p{font-size:12.5px}
  .login-perks{display:none}
  .login-logo{width:min(250px,80%)}
  .login-form{padding:30px 26px}
}

/* ===================== BARRE DE FILTRES GLOBAUX (dashboard RH) ===================== */
.filterbar{
  display:grid;grid-template-columns:repeat(4,minmax(0,1fr)) auto;gap:16px;align-items:end;
  padding:22px 24px;border-radius:var(--r-card);background:var(--surface);
  border:1px solid var(--line);box-shadow:var(--sh-xs);
}
.filterbar .fb-cell{min-width:0}
.filterbar label{display:block;font-size:11px;font-weight:650;color:var(--muted);margin-bottom:8px;letter-spacing:.02em}
.filterbar .input{width:100%}
.filterbar .fb-reset{display:flex;align-items:center;gap:8px;height:42px}
@media(max-width:1180px){.filterbar{grid-template-columns:repeat(2,minmax(0,1fr))}.filterbar .fb-reset{grid-column:1/-1;justify-content:flex-start}}
@media(max-width:640px){.filterbar{grid-template-columns:1fr;padding:20px}}
.filter-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.filter-chips .chip{cursor:default}
.filter-chips .chip b{font-weight:650}

/* ===================== RÉPARTITION PAR SERVICE (lignes cliquables) ===================== */
.svc-list{display:flex;flex-direction:column;gap:12px}
.svc-row{
  display:grid;grid-template-columns:auto 1.5fr 1fr 1fr 0.9fr auto;gap:18px;align-items:center;
  padding:16px 18px;border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);
  cursor:pointer;transition:border-color .18s,box-shadow .18s,transform .18s var(--ease);text-align:left;width:100%;
}
.svc-row:hover{border-color:var(--primary-200);box-shadow:var(--sh-sm);transform:translateY(-1px)}
.svc-row.on{border-color:var(--secondary);background:linear-gradient(120deg,var(--secondary-50),#fff 70%)}
.svc-row .sv-logo{width:56px;height:40px;display:grid;place-items:center;flex:0 0 56px}
.svc-row .sv-logo img{max-width:100%;max-height:34px;object-fit:contain}
.svc-row .sv-name{min-width:0}
.svc-row .sv-name b{display:block;font-size:13.5px;font-weight:660;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.svc-row .sv-name span{font-size:11.5px;color:var(--muted)}
.svc-row .sv-num{font-size:15px;font-weight:700;letter-spacing:-.02em}
.svc-row .sv-num span{display:block;font-size:11px;font-weight:600;color:var(--muted);letter-spacing:0;margin-top:2px}
.svc-row .sv-share{display:flex;align-items:center;gap:10px}
.svc-row .sv-bar{flex:1;height:6px;border-radius:99px;background:var(--surface-3);overflow:hidden;min-width:44px}
.svc-row .sv-bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--primary),var(--secondary));transform-origin:left}
.svc-row .sv-share b{font-size:12.5px;font-weight:700;min-width:44px;text-align:right}
.svc-row .sv-go{color:var(--faint);display:flex;align-items:center}
@media(max-width:1080px){
  .svc-row{grid-template-columns:auto 1fr auto;gap:12px 14px}
  .svc-row .sv-share{grid-column:2/-1}
  .svc-row .sv-num.hide-sm{display:none}
}
@media(max-width:640px){
  .svc-row{grid-template-columns:auto 1fr}
  .svc-row .sv-num{grid-column:2}
  .svc-row .sv-go{display:none}
}

/* ===================== ACTIVITÉ DES COLLABORATEURS ===================== */
.mini-search{display:flex;align-items:center;gap:9px;padding:0 13px;height:42px;border:1px solid var(--line-2);
  border-radius:var(--r-md);background:var(--surface);min-width:260px;transition:border-color .16s,box-shadow .16s}
.mini-search:focus-within{border-color:var(--secondary);box-shadow:var(--ring)}
.mini-search .ic{width:16px;height:16px;color:var(--faint);flex:0 0 16px}
.mini-search input{border:0;outline:0;background:transparent;width:100%;font-size:13px}
.row-scope{display:flex;align-items:center;gap:10px}
.scope-pill{display:inline-flex;align-items:center;gap:7px;padding:5px 11px;border-radius:var(--pill);
  background:var(--primary-50);border:1px solid var(--primary-100);color:var(--primary);font-size:11.5px;font-weight:640}
.scope-pill .ic{width:12px;height:12px}

'''
s = s[:old_login_start] + new_login + s[old_login_end:]
print("  ✓ écran d'accès RH + composants (filtres, services, collaborateurs)")

open(p, 'w').write(s)
print("part1_head.html mis à jour")
