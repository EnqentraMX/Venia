"""Flyer personalizado (1080x1350, formato de publicación de Facebook/Instagram) para que el abogado lo suba a su página.

Uso:
  python3 herramientas/flyer.py <slug> [--titulo "Texto <em>dorado</em>"] [--servicios "A,B,C"] [--etiqueta "MÉRIDA · ABOGADA"]

Toma los datos de prospectos/abogados.json. Sale en estados/Flyer-<Slug>.png y comprueba el QR.
Estilo crema como su perfil: imagen arriba (foto real o logo), servicios, botón de WhatsApp y QR a su perfil.
"""
import argparse, asyncio, html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estado as E

RAIZ = E.RAIZ
WA = '<svg viewBox="0 0 24 24" width="46" height="46" fill="#25d366"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-3.3-.8-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.6 2.1 1.1 1 2.1 1.3 2.4 1.4.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 .9c.3.1.5.2.5.3.1.1.1.6-.1 1.2z"/></svg>'


def tel(n):
    n = re.sub(r"\D", "", n)
    if len(n) == 10 and n[:2] in ("55", "56", "33", "81"): return f"{n[:2]} {n[2:6]} {n[6:]}"
    return f"{n[:3]} {n[3:6]} {n[6:]}" if len(n) == 10 else n


def construir(a, titulo, servicios, etiqueta):
    slug = a["slug"]; carpeta = RAIZ / "public" / slug
    url = f"{E.URL_BASE}/{slug}/"
    import io, base64, qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=16, border=1); q.add_data(url); q.make(fit=True)
    buf = io.BytesIO(); q.make_image(fill_color="#111111", back_color="white").convert("RGB").save(buf, "PNG")
    qr = base64.b64encode(buf.getvalue()).decode()
    fondo_logo = a.get("fondo_logo", "#0b0b0b")
    img_logo = a.get("imagen_vista") or "logo.jpg"
    if not a.get("logo") and a.get("foto") and (carpeta / a["foto"]).exists():
        arriba = f'<div class=img style="background:url(data:image/jpeg;base64,{E.b64(carpeta / a["foto"])}) center 22%/cover"></div>'
        if (carpeta / img_logo).exists() and img_logo != a["foto"]:
            arriba += f'<div class=mini style="background:{fondo_logo} url(data:image/jpeg;base64,{E.b64(carpeta / img_logo)}) center/88% no-repeat"></div>'
    else:
        arriba = f'<div class=img style="background:{fondo_logo} url(data:image/jpeg;base64,{E.b64(carpeta / img_logo)}) center 64%/auto {"68%" if E.oscuro(fondo_logo) else "58%"} no-repeat"></div>'
    servs = "".join(f"<li>{html.escape(s)}</li>" for s in servicios)
    largo = len(re.sub("<[^>]+>", "", titulo))
    return url, f"""<html><head><link href="https://fonts.googleapis.com/css2?family=x" rel="stylesheet"><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#faf6ef;font-family:'Plus Jakarta Sans';color:#1a1814;position:relative;overflow:hidden}}
.img{{position:absolute;left:0;right:0;top:0;height:560px}}
.img::after{{content:'';position:absolute;inset:auto 0 0 0;height:120px;background:linear-gradient(180deg,rgba(250,246,239,0),#faf6ef)}}
.mini{{position:absolute;left:56px;top:56px;width:150px;height:150px;border-radius:26px;border:4px solid #fff;box-shadow:0 14px 34px rgba(0,0,0,.25)}}
.sello{{position:absolute;right:56px;top:56px;background:#1a1814;color:#e8cf95;font-weight:800;font-size:25px;padding:15px 26px;border-radius:99px;box-shadow:0 10px 30px rgba(0,0,0,.25)}}
.sello b{{color:#fff}} .sello i{{font-style:normal;color:#d4b06a}}
.cuerpo{{position:absolute;left:64px;right:64px;top:540px}}
.eti{{font-size:25px;font-weight:800;letter-spacing:5px;color:#94702c}}
h1{{font-size:{70 if largo <= 48 else 58}px;font-weight:800;line-height:1.04;letter-spacing:-2.5px;margin-top:12px}}
h1 em{{font-style:normal;color:#a67c2e}}
ul{{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:12px 28px;margin-top:28px}}
li{{font-size:29px;font-weight:700;display:flex;gap:12px;align-items:center}}
li::before{{content:'✓';flex:none;width:38px;height:38px;border-radius:50%;background:#1a1814;color:#e8cf95;font-size:22px;display:grid;place-items:center}}
.pie{{position:absolute;left:64px;right:64px;bottom:60px;display:flex;gap:26px;align-items:stretch}}
.wa{{flex:1;background:#1a1814;color:#fff;border-radius:30px;padding:30px 34px;display:flex;flex-direction:column;justify-content:center}}
.wa small{{font-size:24px;color:#cfc6b8;font-weight:600}}
.wa .n{{display:flex;align-items:center;gap:14px;font-size:54px;font-weight:800;letter-spacing:-1.5px;margin-top:8px}}
.wa .u{{margin-top:14px;font-size:{25 if len(slug) <= 20 else 21}px;font-weight:800;color:#e8cf95}}
.qr{{width:250px;background:#fff;border:3px solid #e6dccb;border-radius:30px;padding:18px;text-align:center}}
.qr img{{width:100%;display:block}}
.qr span{{display:block;font-size:20px;font-weight:800;margin-top:8px;color:#57524a}}
</style></head><body>
{arriba}
<div class=sello>★ Destacado en <b>Lic</b><i>Link</i></div>
<div class=cuerpo><div class=eti>{html.escape(etiqueta)}</div><h1>{titulo}</h1><ul>{servs}</ul></div>
<div class=pie><div class=wa><small>{"Escríbeme" if re.match(r"(Lic\b|Abogad[oa]\b|Mtr|Dr)", a.get("nombre","")) else "Escríbenos"} por WhatsApp</small><div class=n>{WA}{tel(a.get("telefono", ""))}</div><div class=u>liclink.com.mx/{slug}</div></div>
<div class=qr><img src="data:image/png;base64,{qr}"><span>{"Ver mi perfil" if re.match(r"(Lic\b|Abogad[oa]\b|Mtr|Dr)", a.get("nombre","")) else "Ver perfil"}</span></div></div>
</body></html>"""


async def render(H, salida):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        await pg.route("**://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=E.NS["CSS"]))
        await pg.route("**://fonts.gstatic.com/**", lambda r: r.fulfill(status=200, content_type="font/woff2", body=pathlib.Path(E.NS["F"][r.request.url.rsplit("/", 1)[-1].split(".")[0]]).read_bytes(), headers={"Access-Control-Allow-Origin": "*"}))
        await pg.set_content(H); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(salida)); await b.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--titulo"); ap.add_argument("--servicios"); ap.add_argument("--etiqueta")
    o = ap.parse_args()
    datos = json.loads((RAIZ / "prospectos" / "abogados.json").read_text(encoding="utf-8"))
    a = next((x for x in datos if x["slug"] == o.slug), None)
    if not a: sys.exit(f"No existe {o.slug} en abogados.json")
    titulo = o.titulo or html.escape(a.get("frase") or a.get("titulo", ""))
    servicios = [s.strip() for s in o.servicios.split(",")] if o.servicios else [E.corto(x["nombre"]) for x in a.get("areas", [])][:6]
    etiqueta = o.etiqueta or f"{a.get('ciudad', '').split(',')[0].upper()} · {a.get('nombre', '').upper()}"
    url, H = construir(a, titulo, servicios, etiqueta)
    (RAIZ / "estados").mkdir(exist_ok=True)
    salida = RAIZ / "estados" / ("Flyer-" + "-".join(w.capitalize() for w in o.slug.split("-")) + ".png")
    asyncio.run(render(H, salida))
    try:
        import cv2
        leido = cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(salida)))[0]
        print("QR ok" if leido == url else f"OJO: el QR leyó '{leido}'")
    except ImportError:
        print("(sin cv2: no se comprobó el QR)")
    print(salida)


if __name__ == "__main__":
    main()
