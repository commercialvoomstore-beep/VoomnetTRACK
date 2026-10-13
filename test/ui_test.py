import asyncio, os
from playwright.async_api import async_playwright

OUT = "/home/user/test/shots"
os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":1500,"height":1000}, device_scale_factor=1.4, accept_downloads=True)
        page = await ctx.new_page()
        errs = []
        page.on("console", lambda m: errs.append(f"[{m.type}] {m.text}") if m.type in ("error","warning") else None)
        page.on("pageerror", lambda e: errs.append("PAGEERROR: " + str(e)))

        await page.goto("http://127.0.0.1:8899/index.html")
        await page.wait_for_timeout(2500)
        await page.screenshot(path=f"{OUT}/01-dashboard.png", full_page=True)

        # --- Nouveau déplacement : remplissage réel du formulaire ---
        await page.click('.nav-item[data-view="new"]')
        await page.wait_for_timeout(500)
        await page.click('#svcPick .pick[data-svc="VOOMSTORE"]')
        await page.fill("#fAgent", "Mme BAMBA Aïcha")
        await page.fill("#fMotif", "Livraison colis client Riviera 4")
        await page.fill("#fFrom", "Entrepôt Voomstore")
        await page.fill("#fTo", "Riviera 4, Cocody")
        await page.select_option("#fTrans", "Moto-taxi")
        await page.fill("#fMontant", "2500")
        await page.fill("#fNote", "Reçu n°A-1187")
        await page.select_option("#fStatut", "A_REGLE")
        await page.screenshot(path=f"{OUT}/02-formulaire.png", full_page=True)
        await page.click('#formDep button[type="submit"]')
        await page.wait_for_timeout(1200)
        await page.screenshot(path=f"{OUT}/03-apres-enregistrement.png", full_page=True)

        # --- Registre ---
        await page.click('.nav-item[data-view="registre"]')
        await page.wait_for_timeout(700)
        await page.fill("#fSearch", "BAMBA")
        await page.wait_for_timeout(600)
        await page.screenshot(path=f"{OUT}/04-registre-filtre.png", full_page=True)
        await page.click("#btnClearFilters")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{OUT}/05-registre.png", full_page=True)

        # --- Rapport + PDF réel ---
        await page.click('.nav-item[data-view="rapports"]')
        await page.wait_for_timeout(800)
        await page.screenshot(path=f"{OUT}/06-rapport-apercu.png", full_page=True)
        async with page.expect_download(timeout=25000) as dl:
            await page.click("#btnPdf")
        d = await dl.value
        path = "/home/user/test/rapport_navigateur.pdf"
        await d.save_as(path)
        print("PDF navigateur :", d.suggested_filename, os.path.getsize(path), "octets")
        await page.wait_for_timeout(900)
        await page.screenshot(path=f"{OUT}/07-pdf-toast.png", full_page=True)

        # --- Paramètres ---
        await page.click('.nav-item[data-view="params"]')
        await page.wait_for_timeout(600)
        await page.screenshot(path=f"{OUT}/08-parametres.png", full_page=True)

        # --- KPI vérifiés programmatiquement ---
        kpis = await page.evaluate("""() => ({total: document.querySelector('#kpiTotal').innerText,
            count: document.querySelector('#kpiCount').innerText, rows: DB.trips.length,
            store: (typeof Store!=='undefined'? Store.mode : '?'),
            pdfBytes: typeof buildPDF === 'function'})""")
        print("KPI:", kpis)
        print("Erreurs console:", errs[:8] if errs else "aucune")
        await b.close()

asyncio.run(main())
