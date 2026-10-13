#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôle de la liaison application ↔ base de données (v3.11).
Vérifie réellement, sans simulation :
  1. la base répond et les routes protégées refusent les requêtes sans jeton ;
  2. la connexion se fait côté serveur (mauvais mot de passe refusé) ;
  3. les écritures de l'interface arrivent bien dans PostgreSQL ;
  4. une session révoquée ne donne plus accès ;
  5. aucune empreinte de mot de passe n'est exposée au navigateur ;
  6. l'application refuse de fonctionner si la base est injoignable.

Prérequis : node dev-server.js en écoute sur 8090, DATABASE_URL définie.
"""
import asyncio, json, os, subprocess, urllib.request, urllib.error
from playwright.async_api import async_playwright

BASE = os.environ.get("TRACK_URL", "http://127.0.0.1:8090")
PG = os.environ.get("PGURL", "postgres://postgres@127.0.0.1:5433/voomnet")
ok = []
ko = []

def verifier(nom, condition, detail=""):
    (ok if condition else ko).append(nom)
    print(("  ✓ " if condition else "  ✗ ") + nom + (("  → " + detail) if detail else ""))

def api(method, chemin, corps=None, jeton=None):
    req = urllib.request.Request(
        BASE + "/api" + chemin, method=method,
        data=json.dumps(corps).encode() if corps is not None else None,
        headers={"Content-Type": "application/json", **({"Authorization": "Bearer " + jeton} if jeton else {})})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode() or "{}")
        except Exception: return e.code, {}
    except Exception as e:
        return 0, {"erreur": str(e)}

def sql(requete):
    return subprocess.run(["psql", PG, "-tAc", requete], capture_output=True, text=True).stdout.strip()

async def main():
    print("1) API et sécurité")
    st, sante = api("GET", "/health")
    verifier("la base répond (/health)", st == 200 and sante.get("ok") is True, str(sante.get("base")))

    st, _ = api("GET", "/state")
    verifier("état refusé sans jeton", st == 401, "HTTP %d" % st)
    st, _ = api("GET", "/state", jeton="jeton-invente")
    verifier("état refusé avec un faux jeton", st == 401, "HTTP %d" % st)
    st, _ = api("GET", "/journal")
    verifier("journal réservé (sans jeton)", st == 401, "HTTP %d" % st)

    st, rep = api("POST", "/auth/login", {"identifiant": "rh", "motDePasse": "mauvais"})
    verifier("mauvais mot de passe refusé", st == 401, str(rep.get("code")))

    print("2) Connexion réelle et rôle")
    st, rep = api("POST", "/auth/login", {"identifiant": "rh", "motDePasse": "Rh@Voomnet2026"})
    verifier("connexion RH", st == 200 and rep.get("jeton"), rep.get("profil", {}).get("role", ""))
    jeton_rh = rep.get("jeton", "")
    st, rep = api("POST", "/auth/login", {"identifiant": "admin", "motDePasse": "Admin@Voomnet2026"})
    verifier("connexion ADMIN", st == 200 and rep.get("profil", {}).get("admin") is True)
    jeton_admin = rep.get("jeton", "")

    st, rep = api("GET", "/journal", jeton=jeton_rh)
    verifier("route admin refusée au compte RH", st == 403, "HTTP %d" % st)
    st, rep = api("GET", "/journal", jeton=jeton_admin)
    verifier("journal accessible à l'ADMIN", st == 200 and rep.get("entrees") is not None,
             "%d entrées" % len(rep.get("entrees", [])))

    st, rep = api("PATCH", "/comptes/admin", {"label": "Test interdit"}, jeton=jeton_rh)
    verifier("modification de compte refusée au RH", st == 403, "HTTP %d" % st)

    print("3) Écriture depuis l'interface → PostgreSQL")
    marque = "Contrôle automatique base " + str(os.getpid())
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1500, "height": 1000}, accept_downloads=True)
        pg = await ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        appels = []
        pg.on("response", lambda r: appels.append((r.request.method, r.url.split("/api")[1], r.status)) if "/api/" in r.url else None)

        await pg.goto(BASE + "/index.html?splash=0")
        await pg.wait_for_timeout(1300)
        verifier("app démarrée avec la base", "Base" in await pg.evaluate("(document.querySelector('#cloudState')||{}).textContent"))
        await pg.fill("#loginIdent", "rh"); await pg.fill("#loginPwd", "Rh@Voomnet2026")
        await pg.click("#btnLogin"); await pg.wait_for_timeout(2500)
        verifier("interface ouverte après authentification serveur",
                 await pg.evaluate("(document.querySelector('.view.active')||{}).id") == "view-dashboard")

        empruntes = await pg.evaluate("JSON.stringify(DB.accounts) + JSON.stringify(DB.comptes)")
        verifier("aucune empreinte de mot de passe dans le navigateur",
                 ("scrypt" not in empruntes) and ("mot_de_passe" not in empruntes) and ("hash" not in empruntes))

        await pg.evaluate("go('new')"); await pg.wait_for_timeout(500)
        await pg.click("#svcPick [data-svc='ENCACI']")
        await pg.fill("#fDate", "2026-10-14"); await pg.fill("#fAgent", "Test Base Automatique")
        await pg.fill("#fMotif", marque[:80])
        await pg.fill("#fFrom", "Abobo"); await pg.fill("#fTo", "Cocody")
        await pg.select_option("#fTrans", "Taxi (ville)")
        await pg.fill("#fMontant", "12345"); await pg.fill("#fKm", "7")
        await pg.click("#formDep button[type=submit]")
        await pg.wait_for_timeout(3200)

        ligne = sql("SELECT montant FROM deplacements WHERE motif = '%s'" % marque)
        verifier("déplacement enregistré DANS la base", ligne.strip().startswith("12345"), "montant lu en base : " + ligne.strip())
        auteur = sql("SELECT cree_par FROM deplacements WHERE motif = '%s'" % marque)
        verifier("auteur tracé en base", auteur.strip() == "rh", "cree_par = " + auteur.strip())

        await pg.reload(); await pg.wait_for_timeout(2800)
        relu = await pg.evaluate("DB.trips.filter(t=>t.motif.indexOf('Contrôle automatique base')===0).length")
        verifier("données relues de la base après rechargement", relu >= 1, "%d ligne(s)" % relu)

        # PDF toujours fonctionnel (données issues de la base)
        await pg.evaluate("go('rapports')"); await pg.wait_for_timeout(800)
        try:
            async with pg.expect_download(timeout=25000) as dl:
                await pg.click("#btnPdf")
            d = await dl.value
            chemin = "/home/user/test/rapport_v311.pdf"
            await d.save_as(chemin)
            verifier("rapport PDF généré depuis la base", os.path.getsize(chemin) > 100000,
                     "%d octets" % os.path.getsize(chemin))
        except Exception as e:
            verifier("rapport PDF généré depuis la base", False, str(e)[:60])

        verifier("aucune erreur console", not errs, "; ".join(errs[:2]))
        await b.close()

        print("4) Session révoquée")
        st, _ = api("GET", "/state", jeton=jeton_rh)
        verifier("jeton RH valide avant déconnexion", st == 200)
        api("POST", "/auth/logout", {}, jeton_rh)
        st, _ = api("GET", "/state", jeton=jeton_rh)
        verifier("même jeton refusé après déconnexion", st == 401, "HTTP %d" % st)

        print("5) Base injoignable → refus de fonctionner")
        b2 = await p.chromium.launch(); c2 = await b2.new_context(viewport={"width": 1200, "height": 800})
        p2 = await c2.new_page()
        await p2.route("**/api/**", lambda r: asyncio.ensure_future(r.abort()))
        await p2.goto(BASE + "/index.html?splash=0"); await p2.wait_for_timeout(2600)
        verifier("écran de blocage affiché", await p2.evaluate("!!document.querySelector('#cloudOff.on')"))
        verifier("aucune donnée locale utilisée",
                 await p2.evaluate("(document.querySelector('#login')||{}).classList.contains('hidden')") is not True
                 or await p2.evaluate("DB.trips.length") == 0)
        await b2.close()

    print("\n" + "=" * 62)
    print("RÉSULTAT : %d contrôle(s) au vert, %d échec(s)" % (len(ok), len(ko)))
    if ko:
        print("Échecs : " + "; ".join(ko))
    print("=" * 62)

asyncio.run(main())
