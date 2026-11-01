# -*- coding: utf-8 -*-
"""LicLink · genera public/<slug>/compartir.png (1200x630), la imagen que aparece al mandar el enlace
por WhatsApp o Messenger. Uso: python3 herramientas/compartir.py [slug ...]   (sin slugs = todos)"""
import asyncio, base64, json, os, sys, html as H
sys.path.insert(0, os.path.dirname(__file__))
from generar import DATOS, PUBLICO, TEMAS, area

FUENTES = "/home/claude/spot"  # tipografías locales (opcional)
NEGRO_ORO = {"fondo": "#09080a", "tarjeta": "#16141a", "linea": "#2a2630", "acento": "#c8a46a", "acento2": "#e2c48f"}

def tarjeta(a):
    t = TEMAS.get(a.get("tema", "negro-oro")) or NEGRO_ORO
    carpeta = os.path.join(PUBLICO, a["slug"])
    foto = ""
    if a.get("foto") and os.path.exists(os.path.join(carpeta, a["foto"])):
        foto = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(carpeta, a["foto"]), "rb").read()).decode()
    nombre = f"{a['despacho']} {a.get('sufijo','')}".strip() if a.get("despacho") else a["nombre"]
    lema = " ".join(a.get("portada") or []) or a.get("frase", "")
    areas = " · ".join(area(x)["nombre"].replace("Derecho ", "").capitalize() for x in a.get("areas", [])[:5])
    tel = a.get("telefono", "")
    tel = f"{tel[:2]} {tel[2:6]} {tel[6:]}" if tel[:2] in ("55", "33", "81", "56") else f"{tel[:3]} {tel[3:6]} {tel[6:]}"
    lugar = a.get("ciudad", "")
    lado = f'<div class="foto{" logo" if a.get("logo") else ""}"><img src="{foto}"></div>' if foto else f'<div class="foto mono">{H.escape(a.get("iniciales") or nombre[:2])}</div>'
    return f"""<html><head><link href="https://fonts.googleapis.com/css2?family=x" rel="stylesheet"><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:radial-gradient(120% 120% at 0% 0%,{t['tarjeta']},{t['fondo']} 60%);color:#efe9df;font-family:Manrope,sans-serif;display:grid;grid-template-columns:1fr 400px;overflow:hidden}}
.txt{{padding:70px 40px 60px 80px;display:flex;flex-direction:column}}
.nm{{font-family:Newsreader,serif;font-size:30px;color:{t['acento2']};letter-spacing:.02em}}
h1{{font-family:Newsreader,serif;font-weight:300;font-size:{72 if len(lema) < 46 else 60}px;line-height:1.02;margin-top:28px;letter-spacing:-.01em}}
.ar{{margin-top:26px;font-size:22px;color:rgba(239,233,223,.7)}}
.pie{{margin-top:auto;display:flex;gap:28px;align-items:center;font-size:24px;font-weight:600;color:{t['acento2']}}}
.pie span{{color:rgba(239,233,223,.55);font-weight:500;font-size:20px}}
.foto{{position:relative;margin:56px 70px 56px 0;border-radius:22px;overflow:hidden;border:2px solid {t['acento']};background:{t['fondo']}}}
.foto img{{width:100%;height:100%;object-fit:cover;object-position:50% 18%}}
.logo img{{object-fit:contain}}
.mono{{display:grid;place-items:center;font-family:Newsreader,serif;font-size:120px;color:{t['acento']}}}
.raya{{position:absolute;left:80px;top:0;width:90px;height:5px;background:{t['acento']}}}
</style></head><body><div class="raya"></div>
<div class="txt"><div class="nm">{H.escape(nombre)}</div><h1>{H.escape(lema)}</h1><div class="ar">{H.escape(areas)}</div>
<div class="pie">{H.escape(tel)}<span>{H.escape(lugar)}</span></div></div>{lado}</body></html>"""

async def main(slugs):
    from playwright.async_api import async_playwright
    rutas = None
    if os.path.isdir(FUENTES):
        sys.path.insert(0, FUENTES)
        try: from common import setup_routes as rutas
        except Exception: rutas = None
    lista = [a for a in json.load(open(DATOS, encoding="utf-8")) if a.get("estado") != "borrar" and (not slugs or a["slug"] in slugs)]
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1200, "height": 630})
        if rutas: await rutas(pg)
        for a in lista:
            await pg.set_content(tarjeta(a)); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=os.path.join(PUBLICO, a["slug"], "compartir.png"))
            print("ok", a["slug"])
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
