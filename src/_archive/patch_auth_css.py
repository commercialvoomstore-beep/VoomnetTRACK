# -*- coding: utf-8 -*-
"""Patch CSS : écran d'accès premium, carte de session, comptes & sécurité, micro-animations."""
p = 'src/part1_head.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  ✓", label)

# ---------------------------------------------- 1. CHAMPS AVEC ICÔNE (écran d'accès)
rep(""".login-form .field{margin-bottom:0}""",
""".login-form .field{margin-bottom:0}
/* champs avec icône intégrée */
.field-ic{position:relative;display:flex;align-items:center}
.field-ic>.ic{position:absolute;left:14px;width:17px;height:17px;color:var(--faint);pointer-events:none;transition:color .18s}
.field-ic .input{padding-left:42px;padding-right:46px;height:46px}
.field-ic:focus-within>.ic{color:var(--secondary)}
.eye-btn{position:absolute;right:8px;width:32px;height:32px;display:grid;place-items:center;border:0;border-radius:9px;
  background:transparent;color:var(--faint);cursor:pointer;transition:background .16s,color .16s}
.eye-btn:hover{background:var(--surface-3);color:var(--secondary)}
.eye-btn .ic{width:17px;height:17px}
/* message d'erreur de connexion */
.err-msg.alert-inline{display:none;align-items:center;gap:9px;padding:11px 14px;border-radius:var(--r-md);
  background:var(--danger-bg);border:1px solid #F2DEDE;color:#A85454;font-size:12.5px;font-weight:600;margin-top:2px}
.err-msg.alert-inline.on{display:flex;animation:rise .3s var(--ease-out)}
.err-msg.alert-inline .ic{width:15px;height:15px;flex:0 0 15px}
#loginIdent.err,#loginPwd.err{border-color:#E3BEBE;background:#FFFBFB}
/* secousse discrète en cas d'échec */
.login-card.shake{animation:vtShake .42s cubic-bezier(.36,.07,.19,.97)}
@keyframes vtShake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}30%,50%,70%{transform:translateX(-6px)}40%,60%{transform:translateX(6px)}}
/* aide : comptes d'accès */
.login-help{margin-top:2px}
.login-help summary{display:flex;align-items:center;gap:8px;cursor:pointer;list-style:none;
  font-size:12px;font-weight:640;color:var(--secondary);padding:6px 0}
.login-help summary::-webkit-details-marker{display:none}
.login-help summary .ic{width:15px;height:15px}
.login-help[open] summary{color:var(--primary)}
.login-hints{display:flex;flex-direction:column;gap:8px;margin:10px 0 8px;padding:14px;border-radius:var(--r-md);
  background:var(--surface-3);border:1px solid var(--line-2)}
.hint-row{display:flex;align-items:center;gap:8px;font-size:12.5px;flex-wrap:wrap}
.hint-row .hr-role{min-width:128px;font-weight:650;color:var(--primary)}
.hint-row code{background:#fff;border:1px solid var(--line-2);border-radius:7px;padding:3px 9px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;color:var(--ink)}
.hint-row .hr-sep{color:var(--faint)}""", "champs identifiant/mot de passe + erreurs + aide")

# ---------------------------------------------- 2. ANIMATION DE FOND (très lente, sobre)
rep("""#login{
  position:fixed;inset:0;z-index:900;display:grid;place-items:center;padding:32px;overflow:auto;
  background:
    radial-gradient(1000px 560px at 8% -8%, #F3EDF9 0%, rgba(243,237,249,0) 62%),
    radial-gradient(820px 480px at 98% 106%, #FBF6E6 0%, rgba(251,246,230,0) 58%),
    var(--bg);""",
"""#login{
  position:fixed;inset:0;z-index:900;display:grid;place-items:center;padding:32px;overflow:auto;
  background:
    radial-gradient(1000px 560px at 8% -8%, #F3EDF9 0%, rgba(243,237,249,0) 62%),
    radial-gradient(820px 480px at 98% 106%, #FBF6E6 0%, rgba(251,246,230,0) 58%),
    #FFFFFF;
  background-size:140% 140%, 140% 140%, auto;
  animation:vtAmbient 26s ease-in-out infinite alternate;""", "fond animé très lent")

rep(""".login-brand::before{""",
"""@keyframes vtAmbient{
  0%{background-position:0% 0%, 100% 100%, 0 0}
  100%{background-position:14% 8%, 86% 92%, 0 0}
}
@media (prefers-reduced-motion:reduce){#login{animation:none}}
.login-brand::before{""", "keyframes du fond")

# ---------------------------------------------- 3. CARTE DE SESSION (sidebar) + DÉCONNEXION
rep(""".side-foot{""",
"""/* ---- session active : carte + déconnexion ---- */
.session-card{border:1px solid var(--line);border-radius:var(--r-lg);padding:13px 13px 11px;background:var(--surface-2);margin-bottom:10px}
.sc-top{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.sc-who{min-width:0;flex:1}
.sc-who b{display:block;font-size:12.3px;font-weight:660;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sc-who span{display:block;font-size:10.8px;color:var(--muted)}
.sc-dot{width:7px;height:7px;border-radius:50%;background:var(--ok);flex:0 0 7px;box-shadow:0 0 0 3px var(--ok-bg)}
.btn-logout{width:100%;display:flex;align-items:center;justify-content:center;gap:8px;padding:9px 12px;
  border:1px solid var(--line-2);border-radius:var(--r-md);background:var(--surface);cursor:pointer;
  font-size:12.3px;font-weight:640;color:var(--ink-2);transition:.18s var(--ease)}
.btn-logout .ic{width:15px;height:15px;color:var(--faint);transition:color .18s}
.btn-logout:hover{border-color:#E6C7C7;background:#FFF9F9;color:#A85454}
.btn-logout:hover .ic{color:#A85454}
.icon-btn.danger-soft:hover{background:#FFF6F6;border-color:#EBD3D3;color:#A85454}
.role-badge{display:inline-flex;align-items:center;gap:7px;padding:6px 11px;border-radius:var(--pill);
  background:var(--primary-50);border:1px solid var(--primary-100);color:var(--primary);
  font-size:11.5px;font-weight:660;white-space:nowrap}
.role-badge .ic{width:13px;height:13px;color:var(--accent)}
.role-badge.admin{background:var(--accent-50);border-color:#EFE2B8;color:#8A6F14}
.role-badge.admin .ic{color:var(--accent-600)}
@media(max-width:1180px){.role-badge{display:none}}

/* ---- comptes & sécurité (paramètres) ---- */
.account-list{display:flex;flex-direction:column;gap:14px}
.account-item{border:1px solid var(--line);border-radius:var(--r-lg);padding:16px 18px;background:var(--surface-2)}
.account-head{display:flex;align-items:center;gap:11px;margin-bottom:14px;flex-wrap:wrap}
.account-head .ac-ic{width:36px;height:36px;border-radius:11px;display:grid;place-items:center;flex:0 0 36px;
  background:var(--primary-50);border:1px solid var(--primary-100);color:var(--secondary)}
.account-head .ac-ic .ic{width:17px;height:17px}
.account-head .ac-who{flex:1;min-width:0}
.account-head .ac-who b{display:block;font-size:13.4px;font-weight:670}
.account-head .ac-who span{font-size:11.5px;color:var(--muted)}
.account-item .grid{margin-bottom:0}
.account-item .input{height:42px;background:#fff}

.side-foot{""", "carte de session, badges, comptes")

print("part1_head.html mis à jour")
open(p, "w").write(s)
