"""Capturas de teléfono de la guía. Uso: python3 herramientas/revisar_guia.py ruta [ruta...]  (ej. / /abogados/cdmx/)"""
import asyncio, sys, pathlib, re
src=open(pathlib.Path(__file__).with_name("revisar_v2.py")).read().split("async def main")[0]
exec(src)
from playwright.async_api import async_playwright
async def main(rutas):
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for r in rutas:
            n=re.sub(r"\W+","_",r).strip("_") or "inicio"
            c=await b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=2); pg=await c.new_page()
            await pg.route("**://fonts.googleapis.com/**",lambda q:q.fulfill(status=200,content_type="text/css",body=CSS))
            await pg.route("**://fonts.gstatic.com/**",lambda q:q.fulfill(status=200,content_type="font/woff2",body=pathlib.Path(F[q.request.url.rsplit("/",1)[-1].split(".")[0]]).read_bytes(),headers={"Access-Control-Allow-Origin":"*"}))
            pg.on("pageerror",lambda e,r=r:errs.append(r+" "+str(e)))
            await pg.goto("http://localhost:8097"+r); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(2200)
            await pg.screenshot(path=OUT+"g_"+n+"_1.png")
            await pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('si'))")
            if await pg.query_selector("#chat"):
                await pg.evaluate("document.getElementById('chat').scrollIntoView()"); await pg.wait_for_timeout(9500)
            await pg.wait_for_timeout(900)
            await pg.screenshot(path=OUT+"g_"+n+"_full.png",full_page=True)
            print(r,"alto",await pg.evaluate("document.body.scrollHeight"))
            await c.close()
        print("ERR",errs); await b.close()
asyncio.run(main(sys.argv[1:]))
