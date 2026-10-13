import asyncio, os
from playwright.async_api import async_playwright

OUT = "/home/user/test/shots2"
os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":1500,"height":1020}, device_scale_factor=1.3, accept_downloads=True)
        page = await ctx.new_page()
        errs=[]
        page.on("pageerror", lambda e: errs.append("PAGEERROR: "+str(e)))
        await page.goto("http://127.0.0.1:8899/index.html")
        await page.wait_for_timeout(2200)

        for view, name in [("new","10-nouveau"),("registre","11-registre"),("rapports","12-rapport"),("params","13-parametres")]:
            await page.click(f'.nav-item[data-view="{view}"]')
            await page.wait_for_timeout(800)
            await page.screenshot(path=f"{OUT}/{name}.png")           # viewport
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(500)
            await page.screenshot(path=f"{OUT}/{name}-bas.png")

        # mobile (téléphone)
        mb = await ctx.new_page()
        await mb.set_viewport_size({"width":420,"height":880})
        await mb.goto("http://127.0.0.1:8899/index.html")
        await mb.wait_for_timeout(2000)
        await mb.click("#burger")
        await mb.wait_for_timeout(600)
        await mb.screenshot(path=f"{OUT}/14-mobile-menu.png")

        # vérifs fonctionnelles
        checks = await page.evaluate("""() => {
          const r = {};
          r.services = SERVICES.map(s=>s.id);
          r.logosOk = Object.keys(LOGOS).map(k=>k+':'+(LOGOS[k].uri.slice(0,22)));
          r.trips = DB.trips.length; r.month = currentMonth();
          r.total = sum(tripsOf(currentMonth()));
          r.pdfHeader = (function(){ try{ const b = makePDFStub ? null : null; return true; }catch(e){ return false; } })();
          r.transports = DB.transports.length;
          r.storageLocal = Store.mode;
          return r;
        }""")
        print("Vérifs:", checks)
        print("Erreurs:", errs or "aucune")
        await b.close()

asyncio.run(main())
