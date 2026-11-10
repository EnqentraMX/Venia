# -*- coding: utf-8 -*-
"""LicLink · genera public/<slug>/compartir.png (1200x630), la imagen que aparece al mandar el enlace
por WhatsApp o Messenger. Uso: python3 herramientas/compartir.py [slug ...]   (sin slugs = todos)"""
import asyncio, base64, json, os, sys, html as H
sys.path.insert(0, os.path.dirname(__file__))
from generar import DATOS, PUBLICO, TEMAS, area

NEGRO_ORO = {"fondo": "#09080a", "tarjeta": "#16141a", "linea": "#2a2630", "acento": "#c8a46a", "acento2": "#e2c48f"}

WA_SVG = '<svg viewBox="0 0 24 24" width="30" height="30" fill="#1f9d55"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4c-1-1.6-1.5-3.4-1.5-5.2C2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9 1.8 1.8 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8z"/></svg>'
PIN_SVG = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#94702c" stroke-width="2"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0114 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'

def tarjeta(a):
    """Vista previa 1200x630 en crema, como las páginas: logo grande a la derecha, nombre, lema, materias, WhatsApp y ciudad."""
    carpeta = os.path.join(PUBLICO, a["slug"])
    img = a.get("imagen_vista") or a.get("foto")
    foto = ""
    if img and os.path.exists(os.path.join(carpeta, img)):
        foto = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(carpeta, img), "rb").read()).decode()
    nombre = a.get("despacho_largo", "").split(" · ")[0] if a.get("despacho_largo") else (f"{a['despacho']} {a.get('sufijo','')}".strip() if a.get("despacho") else a["nombre"])
    lema = " ".join(a.get("portada") or []) or a.get("frase", "")
    mats = [area(x)["nombre"].replace("Derecho ", "") for x in a.get("areas", [])][:4]
    chips = "".join(f"<span>{H.escape(m[:1].upper() + m[1:])}</span>" for m in mats)
    tel = a.get("whatsapp") or a.get("telefono", "")
    tel = f"{tel[:2]} {tel[2:6]} {tel[6:]}" if tel[:2] in ("55", "56", "33", "81") else f"{tel[:3]} {tel[3:6]} {tel[6:]}"
    lugar = a.get("ciudad", "")
    es_logo = a.get("logo") or a.get("imagen_vista")
    fondo = a.get("fondo_logo") or ("#1a1814" if es_logo else "#efe8db")
    if es_logo and foto and not a.get("fondo_logo"):  # usa el color del borde del logo para que no se vea un recuadro
        from PIL import Image
        px = Image.open(os.path.join(carpeta, img)).convert("RGB").getpixel((3, 3)); fondo = "#%02x%02x%02x" % px
    lado = (f'<div class="img{" logo" if es_logo else ""}" style="background:{fondo}"><img src="{foto}"></div>' if foto
            else f'<div class="img mono">{H.escape(a.get("iniciales") or nombre[:2])}</div>')
    tam = 58 if len(lema) < 40 else 50 if len(lema) < 56 else 44
    return f"""<html><head><link href="https://fonts.googleapis.com/css2?family=x" rel="stylesheet"><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#faf6ef;font-family:'Plus Jakarta Sans';color:#1a1814;display:grid;grid-template-columns:1fr 470px;overflow:hidden;position:relative}}
body::before{{content:"";position:absolute;inset:0;background:radial-gradient(60% 70% at 0% 100%,rgba(212,176,106,.16),transparent 70%)}}
.txt{{position:relative;padding:44px 30px 40px 60px;display:flex;flex-direction:column}}
.top{{display:flex;align-items:center;gap:12px;font-weight:800;font-size:24px;letter-spacing:-1px}}
.top i{{font-style:normal;color:#94702c}}
.top span{{font-size:15px;font-weight:700;letter-spacing:1px;color:#fff;background:#1a1814;padding:6px 12px;border-radius:99px}}
.nm{{margin-top:30px;font-size:26px;font-weight:700;color:#94702c;letter-spacing:-.5px;line-height:1.2}}
h1{{font-weight:800;font-size:{tam}px;line-height:1.06;letter-spacing:-2px;margin-top:10px}}
.chips{{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}}
.chips span{{font-size:19px;font-weight:700;background:#fff;border:2px solid #e7e0d3;border-radius:99px;padding:7px 16px}}
.mod{{margin-top:16px;font-size:20px;font-weight:700;color:#1d7a46}}
.cta{{margin-top:auto;align-self:flex-start;background:#1a1814;color:#f3dfae;font-size:21px;font-weight:700;padding:14px 22px;border-radius:12px}}
.pie{{margin-top:20px;display:flex;flex-direction:column;gap:10px}}
.fila{{display:flex;align-items:center;gap:10px;font-size:26px;font-weight:800}}
.fila.l{{font-size:21px;font-weight:600;color:#57524a}}
.img{{position:relative;margin:34px 34px 34px 0;border-radius:26px;overflow:hidden;border:4px solid #d4b06a;box-shadow:0 30px 60px -30px rgba(60,40,10,.5)}}
.img img{{width:100%;height:100%;object-fit:cover;object-position:50% 20%}}
.img.logo img{{object-fit:contain;object-position:center;padding:22px}}
.mono{{display:grid;place-items:center;background:#1a1814;color:#d4b06a;font-weight:800;font-size:150px}}
</style></head><body>
<div class="txt"><div class="top"><b>Lic<i>Link</i></b><span>GUÍA DE ABOGADOS</span></div>
<div class="nm">{H.escape(nombre)}</div><h1>{H.escape(lema)}</h1><div class="chips">{chips}</div>{f'<div class="mod">✓ {H.escape(a["modalidad"])}</div>' if a.get("modalidad") else ""}
<div class="cta">Ver perfil y escribir por WhatsApp →</div>
<div class="pie"><div class="fila">{WA_SVG}{H.escape(tel)}</div>{f'<div class="fila l">{PIN_SVG}{H.escape(lugar)}</div>' if lugar else ""}</div></div>{lado}</body></html>"""

async def main(slugs):
    from playwright.async_api import async_playwright
    import pathlib
    src = open(os.path.join(os.path.dirname(__file__), "revisar_v2.py"), encoding="utf-8").read().split("async def main")[0]
    ns = {"__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "revisar_v2.py")}; exec(src, ns)
    async def rutas(pg):
        await pg.route("**://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=ns["CSS"]))
        await pg.route("**://fonts.gstatic.com/**", lambda r: r.fulfill(status=200, content_type="font/woff2", body=pathlib.Path(ns["F"][r.request.url.rsplit("/", 1)[-1].split(".")[0]]).read_bytes(), headers={"Access-Control-Allow-Origin": "*"}))
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
