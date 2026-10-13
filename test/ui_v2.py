import asyncio, os
from playwright.async_api import async_playwright
OUT="/home/user/test/shots4"   # v3.11 : l'application passe par l'API (node dev-server.js); os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={"width":1500,"height":1020}, device_scale_factor=1.25, accept_downloads=True)
        pg=await ctx.new_page()
        errs=[]
        pg.on("pageerror", lambda e: errs.append("PAGEERROR: "+str(e)))
        pg.on("console", lambda m: errs.append("CONSOLE["+m.type+"]: "+m.text) if m.type=="error" else None)

        # 1. SPLASH visible au chargement
        await pg.goto("http://127.0.0.1:8090/index.html")
        await pg.wait_for_timeout(700)
        splash_visible = await pg.is_visible("#splash")
        await pg.screenshot(path=f"{OUT}/00-splash.png")
        await pg.wait_for_timeout(2300)
        splash_gone = not await pg.is_visible("#splash")
        print("splash visible au départ:", splash_visible, "| disparu après ~2s:", splash_gone)
        # ---- ÉCRAN D'ACCÈS RH ----
        login_shown = await pg.is_visible("#login")
        print("écran d'accès RH affiché:", login_shown,
              "| titre:", await pg.inner_text("#login h3"),
              "| liste de collaborateurs:", await pg.evaluate("!!document.querySelector('#loginProfiles')"))
        await pg.screenshot(path=f"{OUT}/05-connexion.png")
        await pg.fill("#loginIdent", "rh")                            # compte RH
        await pg.fill("#loginPwd", "Rh@Voomnet2026")
        await pg.screenshot(path=f"{OUT}/06-connexion-remplie.png")
        await pg.click("#btnLogin")
        await pg.wait_for_timeout(1200)
        print("après connexion → vue:", await pg.evaluate("document.querySelector('.view.active').id"),
              "| user:", await pg.evaluate("DB.user.name"))
        # rechargement : session conservée (pas de splash ni login)
        await pg.reload(); await pg.wait_for_timeout(1400)
        print("rechargement → splash:", await pg.is_visible("#splash"), "| login:", await pg.is_visible("#login"))
        await pg.screenshot(path=f"{OUT}/01-dashboard.png")

        # 2. Navigation dans toutes les vues
        for v in ["registre","analyse","collaborateurs","rapports","params"]:
            await pg.click(f'.nav-item[data-view="{v}"]')
            await pg.wait_for_timeout(650)
            await pg.screenshot(path=f"{OUT}/10-{v}.png")
        # retour dashboard
        await pg.click('.nav-item[data-view="dashboard"]'); await pg.wait_for_timeout(500)

        # 3. Enregistrement d'un déplacement
        await pg.click('.nav-item[data-view="dashboard"]'); await pg.wait_for_timeout(400)
        await pg.click('.hero [data-goto="new"]'); await pg.wait_for_timeout(600)
        await pg.click('#svcPick .pick[data-svc="TECHNOLOGY"]')
        await pg.fill("#fAgent","M. KOFFI Jean-Marc")
        await pg.fill("#fMotif","Contrôle réseau client Plateau")
        await pg.fill("#fFrom","Siège VOOMNET"); await pg.fill("#fTo","Plateau, Abidjan")
        await pg.select_option("#fTrans","Véhicule personnel (carburant)")
        await pg.fill("#fKm","24"); await pg.fill("#fMontant","9000")
        await pg.click('#formDep button[type="submit"]'); await pg.wait_for_timeout(1100)
        state = await pg.evaluate("({trips:DB.trips.length, mois:currentMonth(), total:sum(tripsOf(currentMonth()))})")
        print("après enregistrement:", state)

        # 4. Vues qui dépendent des données
        for v in ["dashboard","registre","analyse","collaborateurs"]:
            await pg.click(f'.nav-item[data-view="{v}"]'); await pg.wait_for_timeout(700)
            await pg.screenshot(path=f"{OUT}/20-{v}.png")

        # 5. Recherche globale header
        await pg.fill("#searchInput","KOFFI"); await pg.press("#searchInput","Enter"); await pg.wait_for_timeout(800)
        print("recherche → vue active:", await pg.evaluate("document.querySelector('.view.active').id"))

        # 6. Popovers
        await pg.click("#btnBell"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=f"{OUT}/30-notifications.png")
        await pg.click("#btnUser"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=f"{OUT}/31-profil.png")
        await pg.keyboard.press("Escape")

        # 7. PDF + CSV
        await pg.click('.nav-item[data-view="rapports"]'); await pg.wait_for_timeout(700)
        async with pg.expect_download(timeout=25000) as dl:
            await pg.click("#btnPdf")
        d=await dl.value; await d.save_as("/home/user/test/rapport_v2.pdf")
        print("PDF:", d.suggested_filename, os.path.getsize("/home/user/test/rapport_v2.pdf"), "octets")
        await pg.click('.nav-item[data-view="registre"]'); await pg.wait_for_timeout(500)
        async with pg.expect_download(timeout=20000) as dl2:
            await pg.click("#btnExportCsv")
        d2=await dl2.value; await d2.save_as("/home/user/test/export_v2.csv")
        print("CSV:", os.path.getsize("/home/user/test/export_v2.csv"), "octets")

        # 8. AUDIT : l'onglet Véhicules doit être totalement absent
        audit = await pg.evaluate("""(() => { const h=document.body.innerHTML;
            return { onglet:!!document.querySelector('[data-view=\"vehicules\"]'),
                     vue:!!document.querySelector('#view-vehicules'),
                     raccourci:/data-goto="vehicules"/.test(h),
                     libelleSidebar:/Véhicules/.test(document.querySelector('#sidebar').textContent) }; })()""")
        print("AUDIT Véhicules (tout doit être False) :", audit)

        # 9. Collaborateurs : ajout
        await pg.click('.nav-item[data-view="collaborateurs"]'); await pg.wait_for_timeout(500)
        await pg.click("#btnAddCollab"); await pg.wait_for_timeout(400)
        await pg.fill("#cNom","Mme YAO Christelle"); await pg.select_option("#cSvc","ENCACI")
        await pg.click("#cSave"); await pg.wait_for_timeout(700)
        print("collaborateurs:", await pg.evaluate("DB.agents.length"))
        await pg.screenshot(path=f"{OUT}/41-collaborateurs.png")

        # 10. Mobile
        mb=await ctx.new_page(); await mb.set_viewport_size({"width":412,"height":900})
        await mb.goto("http://127.0.0.1:8090/index.html"); await mb.wait_for_timeout(2600)
        if await mb.is_visible("#login"):
            await mb.fill("#loginIdent","rh"); await mb.fill("#loginPwd","Rh@Voomnet2026"); await mb.click("#btnLogin"); await mb.wait_for_timeout(1500)
        await mb.screenshot(path=f"{OUT}/50-mobile.png")
        await mb.click("#burger"); await mb.wait_for_timeout(600)
        await mb.screenshot(path=f"{OUT}/51-mobile-menu.png")

        # 11. Tablette
        tb=await ctx.new_page(); await tb.set_viewport_size({"width":900,"height":1000})
        await tb.goto("http://127.0.0.1:8090/index.html"); await tb.wait_for_timeout(2600)
        if await tb.is_visible("#login"):
            await tb.fill("#loginIdent","rh"); await tb.fill("#loginPwd","Rh@Voomnet2026"); await tb.click("#btnLogin"); await tb.wait_for_timeout(1500)
        await tb.screenshot(path=f"{OUT}/60-tablette.png")

        # 12. Vérifs techniques + AUDIT FINAL de l'architecture RH
        tech = await pg.evaluate("""() => {
          const q=s=>document.querySelector(s);
          return {
            police: getComputedStyle(document.body).fontFamily.slice(0,40),
            interChargee: document.fonts? document.fonts.check('14px InterVar') : null,
            kpis: document.querySelectorAll('#kpiRow .kpi').length,
            kpiLabels: [...document.querySelectorAll('#kpiRow .kpi .lbl')].map(x=>x.textContent),
            badges: {reg:q('#badgeRegistre').textContent, col:q('#badgeCollabs').textContent,
                     vehicules: q('#badgeVehicules')? 'PRÉSENT (erreur)' : 'absent'},
            nav: [...document.querySelectorAll('.nav-item')].map(n=>n.dataset.view),
            views: document.querySelectorAll('.view').length,
            navItems: document.querySelectorAll('.nav-item').length,
            filtresGlobaux: ['gService','gAgent','gType','dashMonth'].filter(i=>!!document.getElementById(i)).length,
            servicesCliquables: document.querySelectorAll('#svcList [data-svc-filter]').length,
            lignesCollabs: document.querySelectorAll('#collabActivity tbody tr').length,
            colonnesCollabs: [...document.querySelectorAll('#collabActivity thead th')].map(x=>x.textContent.trim()),
            uneInterfaceRH: !!q('#view-dashboard') && !q('#view-vehicules'),
            palette: {violet:getComputedStyle(document.documentElement).getPropertyValue('--primary').trim(),
                      or:getComputedStyle(document.documentElement).getPropertyValue('--accent').trim(),
                      violetClair:getComputedStyle(document.documentElement).getPropertyValue('--surface-3').trim(),
                      fond:getComputedStyle(document.documentElement).getPropertyValue('--bg').trim()},
            overflowX: document.documentElement.scrollWidth > window.innerWidth + 2
          };
        }""")
        print("technique:", tech)
        # 12 bis. Déconnexion
        await pg.click("#btnLogoutSide"); await pg.wait_for_timeout(1500)
        print("déconnexion → écran d'accès :", await pg.is_visible("#login"),
              "| session vidée :", await pg.evaluate("!sessionStorage.getItem('vt_session')"))

        # 12 ter. VERROUILLAGE (v3.8) : aucun accès sans identifiant
        lock = await pg.evaluate("""(() => ({
            boutonConsultation: !!document.querySelector('#btnLoginSkip'),
            indiceIdentifiant: /ex\s*:\s*rh/i.test((document.querySelector('#loginIdent')||{}).placeholder||''),
            infosComptes: /Voomnet2026|un compte Responsable RH/i.test((document.querySelector('#login')||{}).innerText||'')
        }))()""")
        print("verrouillage → bouton consultation:", lock["boutonConsultation"],
              "| indice identifiant:", lock["indiceIdentifiant"],
              "| infos comptes visibles:", lock["infosComptes"])
        await pg.evaluate("sessionStorage.setItem('vt_session','guest'); location.reload();")
        await pg.wait_for_timeout(3400)
        rep = await pg.evaluate("""(() => { const L=document.querySelector('#login');
            return { accesRefuse: !!L && !L.classList.contains('hidden'),
                     vue: (document.querySelector('.view.active')||{}).id }; })()""")
        print("session « consultation » forcée → écran d'accès:", rep["accesRefuse"], "| vue:", rep["vue"])

        # reconnexion nominative obligatoire pour la suite des tests (plus d'accès anonyme)
        await pg.fill("#loginIdent","rh"); await pg.fill("#loginPwd","Rh@Voomnet2026")
        await pg.click("#btnLogin"); await pg.wait_for_timeout(1600)
        print("reconnexion RH →", await pg.evaluate("document.querySelector('.view.active').id"))

        # 13. Filtre global : clic sur un service = filtre (jamais un espace séparé)
        await pg.click('.nav-item[data-view="dashboard"]'); await pg.wait_for_timeout(500)
        before = await pg.inner_text("#kpiRow .kpi .val")
        await pg.click('#svcList [data-svc-filter="FORMATION"]'); await pg.wait_for_timeout(700)
        after = await pg.inner_text("#kpiRow .kpi .val")
        print("filtre service : KPI avant/après =", before.strip(), "/", after.strip(),
              "| vue active:", await pg.evaluate("document.querySelector('.view.active').id"),
              "| chip:", (await pg.inner_text("#filterChips")).strip())
        await pg.select_option("#gService", ""); await pg.click("#btnResetFilters"); await pg.wait_for_timeout(500)
        print("retour à toute l'organisation :", await pg.inner_text("#kpiRow .kpi .val"))
        await pg.screenshot(path=f"{OUT}/70-audit-final.png", full_page=True)
        print("erreurs:", errs[:10] if errs else "aucune")
        await b.close()
asyncio.run(main())
