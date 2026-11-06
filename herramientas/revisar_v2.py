"""Capturas de teléfono de páginas v2 (Bodoni Moda + Archivo locales). Uso: python3 herramientas/revisar_v2.py slug [slug...]"""
import asyncio, sys, pathlib
from playwright.async_api import async_playwright
NM="/home/claude/spot/node_modules"
B=f"{NM}/@fontsource/bodoni-moda/files/bodoni-moda-latin-"; A=f"{NM}/@fontsource-variable/archivo/files/archivo-latin-wght-normal.woff2"
F={"b4n":B+"400-normal.woff2","b4i":B+"400-italic.woff2","b5n":B+"500-normal.woff2","b5i":B+"500-italic.woff2","b6n":B+"600-normal.woff2","arch":A}
CSS="".join(f"@font-face{{font-family:'Bodoni Moda';font-style:{'italic' if k[2]=='i' else 'normal'};font-weight:{k[1]}00;src:url(https://fonts.gstatic.com/{k}.woff2)}}" for k in F if k[0]=="b")+"@font-face{font-family:'Archivo';font-weight:100 900;src:url(https://fonts.gstatic.com/arch.woff2)}"
MAP="<html><body style='margin:0;background:#e8e4df;display:grid;place-items:center;height:100vh;font:14px sans-serif;color:#888'>[mapa]</body></html>"
OUT="/tmp/claude-0/-home-claude/f0659219-5364-5d6e-9693-f46b78a72ea8/scratchpad/v2_"
async def main(slugs):
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for s in slugs:
            c=await b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=2); pg=await c.new_page()
            await pg.route("**://fonts.googleapis.com/**",lambda r:r.fulfill(status=200,content_type="text/css",body=CSS))
            await pg.route("**://fonts.gstatic.com/**",lambda r:r.fulfill(status=200,content_type="font/woff2",body=pathlib.Path(F[r.request.url.rsplit("/",1)[-1].split(".")[0]]).read_bytes(),headers={"Access-Control-Allow-Origin":"*"}))
            await pg.route("**://maps.google.com/**",lambda r:r.fulfill(status=200,content_type="text/html",body=MAP))
            pg.on("pageerror",lambda e,s=s:errs.append(s+" "+str(e)))
            await pg.goto(f"http://localhost:8097/{s}/"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(2600)
            await pg.screenshot(path=OUT+s+"_1.png")
            await pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('si'));document.querySelectorAll('.bloque h2').forEach(e=>e.classList.add('si'))"); await pg.wait_for_timeout(900)
            await pg.screenshot(path=OUT+s+"_full.png",full_page=True)
            print(s,"alto",await pg.evaluate("document.body.scrollHeight"))
            await pg.locator(".sit").first.click(); await pg.fill("#hNombre","María López"); await pg.fill("#hDetalle","Detuvieron a mi hermano anoche"); await pg.wait_for_timeout(600)
            await pg.screenshot(path=OUT+s+"_hoja.png")
            await c.close()
        print("ERR",errs); await b.close()
asyncio.run(main(sys.argv[1:]))
