import asyncio, os
from playwright.async_api import async_playwright
OUT="/home/user/test/shots3"; os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={"width":1500,"height":1000},accept_downloads=True)
        pg=await ctx.new_page(); errs=[]
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("http://127.0.0.1:8899/index.html"); await pg.wait_for_timeout(2000)
        # tout effacer
        await pg.click('.nav-item[data-view="params"]'); await pg.wait_for_timeout(400)
        await pg.click("#btnWipe"); await pg.wait_for_timeout(500)
        await pg.click("#mOk"); await pg.wait_for_timeout(900)
        await pg.click('.nav-item[data-view="dashboard"]'); await pg.wait_for_timeout(700)
        await pg.screenshot(path=f"{OUT}/E1-dashboard-vide.png")
        # enregistrer un 1er déplacement depuis zéro
        await pg.click('.nav-item[data-view="new"]'); await pg.wait_for_timeout(400)
        await pg.click('#svcPick .pick[data-svc="TECHNOLOGY"]')
        await pg.fill("#fAgent","M. KOFFI Jean-Marc"); await pg.fill("#fMotif","Installation réseau client")
        await pg.fill("#fMontant","7500"); await pg.select_option("#fTrans","Taxi (ville)")
        await pg.click('#formDep button[type="submit"]'); await pg.wait_for_timeout(900)
        # registre vide puis avec 1 ligne
        await pg.click('.nav-item[data-view="registre"]'); await pg.wait_for_timeout(600)
        await pg.screenshot(path=f"{OUT}/E2-registre-1ligne.png")
        # PDF d'un mois sans données (mois précédent)
        await pg.click('.nav-item[data-view="rapports"]'); await pg.wait_for_timeout(500)
        await pg.fill("#rMonth","2026-09"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=f"{OUT}/E3-rapport-vide.png")
        async with pg.expect_download(timeout=20000) as dl:
            await pg.click("#btnPdf")
        d=await dl.value; await d.save_as("/home/user/test/rapport_vide.pdf")
        print("PDF vide :", os.path.getsize("/home/user/test/rapport_vide.pdf"), "octets")
        # CSV
        async with pg.expect_download(timeout=20000) as dl2:
            await pg.click("#btnExportCsv")
        d2=await dl2.value; await d2.save_as("/home/user/test/export.csv")
        print("CSV :", d2.suggested_filename, os.path.getsize("/home/user/test/export.csv"), "octets")
        print("Erreurs:", errs or "aucune")
        await b.close()
asyncio.run(main())
