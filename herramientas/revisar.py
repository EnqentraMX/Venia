import asyncio, sys
sys.path.insert(0, "/home/claude/spot")
from common import setup_routes
from playwright.async_api import async_playwright
OUT="/tmp/claude-0/-home-claude/f0659219-5364-5d6e-9693-f46b78a72ea8/scratchpad/r_"
async def main(slugs):
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for s in slugs:
            c=await b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True); pg=await c.new_page(); await setup_routes(pg)
            pg.on("pageerror",lambda e,s=s:errs.append(s+" "+str(e)))
            await pg.goto(f"http://localhost:8097/{s}/"); await pg.wait_for_timeout(600)
            await pg.add_style_tag(content=".reveal{opacity:1!important;transform:none!important}"); await pg.wait_for_timeout(700)
            await pg.screenshot(path=OUT+s+".png")
            n=await pg.locator(".pend").count(); print(s,"por confirmar visibles:",n)
            await c.close()
        print("ERR",errs); await b.close()
asyncio.run(main(sys.argv[1:]))
