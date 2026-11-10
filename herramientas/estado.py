"""Imagen vertical (1080x1920) con QR para el estado de WhatsApp / historias de un abogado.

Uso:
  python3 herramientas/estado.py <slug> [opciones]

Toma los datos de prospectos/abogados.json. Opciones (todas opcionales):
  --modo foto|logo      foto grande arriba (si tiene foto de persona) o logo centrado.
                        Por defecto: logo si "logo": true, si no foto.
  --etiqueta "TEXTO"    línea dorada pequeña (por defecto: nombre en mayúsculas).
  --titulo "Texto <em>dorado</em>"   frase grande; lo que va entre <em> sale dorado.
                        Por defecto: la "frase" del abogado.
  --chips "Penal,Familiar,Civil"     materias (por defecto: sus áreas, máx. 8).
  --info "Mérida, Yucatán<br>Atención 24/7"   texto junto al QR.

Sale en estados/Estado-<slug>.png y comprueba que el QR abre el perfil.
Estilo: fondo oscuro, sello dorado "★ DESPACHO DESTACADO", tarjeta crema con QR.
"""
import argparse, asyncio, base64, html, io, json, pathlib, re, sys
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent.parent
URL_BASE = "https://liclink.com.mx"
src = (RAIZ / "herramientas" / "revisar_v2.py").read_text(encoding="utf-8").split("async def main")[0]
NS = {"__file__": str(RAIZ / "herramientas" / "revisar_v2.py")}; exec(src, NS)


def b64(ruta):
    return base64.b64encode(pathlib.Path(ruta).read_bytes()).decode()


def oscuro(hexa):
    try:
        h = hexa.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return (r * 299 + g * 587 + b * 114) / 1000 < 15
    except Exception:
        return False


def corto(nombre):
    n = re.sub(r"^Derecho\s+", "", nombre).strip()
    return n[:1].upper() + n[1:]


def construir(a, modo, etiqueta, titulo, chips, info):
    slug = a["slug"]; carpeta = RAIZ / "public" / slug
    url = f"{URL_BASE}/{slug}/"
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=20, border=1); q.add_data(url); q.make(fit=True)
    buf = io.BytesIO(); q.make_image(fill_color="#111111", back_color="white").convert("RGB").save(buf, "PNG")
    qr = base64.b64encode(buf.getvalue()).decode()
    img_logo = a.get("imagen_vista") or a.get("foto") or "logo.jpg"
    fondo_logo = a.get("fondo_logo", "#0b0b0b")
    fondo = "#000" if (modo == "logo" and oscuro(fondo_logo)) else "#0b0b0b"
    chips_html = "".join(f"<span>{html.escape(c)}</span>" for c in chips)
    if modo == "foto":
        foto = b64(carpeta / a["foto"])
        logo_mini = ""
        if (carpeta / img_logo).exists() and img_logo != a["foto"]:
            logo_mini = f'<div class=logo style="background:{fondo_logo} url(data:image/jpeg;base64,{b64(carpeta / img_logo)}) center/88% no-repeat"></div>'
        arriba = f"<div class=foto></div><div class=top>{logo_mini or '<div></div>'}<div class=sello>★ DESPACHO DESTACADO</div></div>"
        css_foto = (f".foto{{position:absolute;inset:0 0 auto 0;height:1150px;background:url(data:image/jpeg;base64,{foto}) center 20%/cover}}"
                    ".foto::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,11,.15) 0%,rgba(11,11,11,0) 35%,rgba(11,11,11,.85) 78%,#0b0b0b 100%)}")
        top_txt = 820
    else:
        logo = b64(carpeta / img_logo)
        if oscuro(fondo_logo):
            css_foto = (f".foto{{position:absolute;left:0;right:0;top:150px;height:720px;background:url(data:image/jpeg;base64,{logo}) center/contain no-repeat}}"
                        "body::before{content:'';position:absolute;inset:0;background:radial-gradient(60% 40% at 50% 30%,rgba(212,176,106,.22),transparent 70%)}")
        else:  # logo con fondo claro o de color: va en una tarjeta con marco dorado
            css_foto = (f".foto{{position:absolute;left:190px;top:170px;width:700px;height:700px;border-radius:40px;border:4px solid #d4b06a;"
                        f"background:{fondo_logo} url(data:image/jpeg;base64,{logo}) center/86% no-repeat;box-shadow:0 30px 80px rgba(212,176,106,.18)}}")
        arriba = "<div class=foto></div><div class=top><div></div><div class=sello>★ DESPACHO DESTACADO</div></div>"
        top_txt = 900
    return url, f"""<html><head><link href="https://fonts.googleapis.com/css2?family=x" rel="stylesheet"><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:{fondo};font-family:'Plus Jakarta Sans';color:#f7f2e9;position:relative;overflow:hidden}}
{css_foto}
.top{{position:absolute;top:60px;left:60px;right:60px;display:flex;justify-content:space-between;align-items:center}}
.logo{{width:150px;height:150px;border-radius:24px;border:3px solid #d4b06a;box-shadow:0 20px 40px rgba(0,0,0,.5)}}
.sello{{background:#d4b06a;color:#17120a;font-weight:800;font-size:26px;padding:16px 26px;border-radius:99px;letter-spacing:.5px}}
.txt{{position:absolute;top:{top_txt}px;left:70px;right:70px}}
.eti{{font-size:30px;font-weight:700;letter-spacing:6px;color:#d4b06a}}
h1{{font-size:{84 if len(re.sub('<[^>]+>', '', titulo)) <= 60 else 70}px;font-weight:800;line-height:1.02;letter-spacing:-3px;margin-top:16px}}
h1 em{{font-style:normal;color:#d4b06a}}
.chips{{display:flex;gap:14px;margin-top:28px;flex-wrap:wrap}}
.chips span{{font-size:26px;font-weight:700;border:2px solid #4a443a;border-radius:99px;padding:12px 24px;color:#f3dfae}}
.qrbox{{position:absolute;left:70px;right:70px;bottom:110px;display:flex;gap:40px;align-items:center;background:#faf6ef;color:#1a1814;border-radius:36px;padding:36px}}
.qrbox img{{width:330px;height:330px;border-radius:16px}}
.qrbox b{{display:block;font-size:50px;font-weight:800;letter-spacing:-2px;line-height:1.05}}
.qrbox p{{font-size:28px;color:#57524a;margin-top:14px;font-weight:600;line-height:1.3}}
.qrbox .u{{margin-top:18px;font-size:{26 if len(slug) <= 20 else 21}px;font-weight:800;color:#94702c}}
.pie{{position:absolute;bottom:42px;left:0;right:0;text-align:center;font-size:24px;color:#a59d92;font-weight:600}}
.pie b{{color:#f7f2e9}} .pie i{{font-style:normal;color:#d4b06a}}
</style></head><body>
{arriba}
<div class=txt><div class=eti>{html.escape(etiqueta)}</div><h1>{titulo}</h1><div class=chips>{chips_html}</div></div>
<div class=qrbox><img src="data:image/png;base64,{qr}"><div><b>Escanea y escríbenos</b><p>{info}</p><div class=u>liclink.com.mx/{slug}</div></div></div>
<div class=pie>Perfil destacado en <b>Lic<i>Link</i></b> · La guía de abogados de México</div>
</body></html>"""


async def render(H, salida):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.route("**://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=NS["CSS"]))
        await pg.route("**://fonts.gstatic.com/**", lambda r: r.fulfill(status=200, content_type="font/woff2", body=pathlib.Path(NS["F"][r.request.url.rsplit("/", 1)[-1].split(".")[0]]).read_bytes(), headers={"Access-Control-Allow-Origin": "*"}))
        await pg.set_content(H); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(salida)); await b.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--modo", choices=["foto", "logo"])
    ap.add_argument("--etiqueta"); ap.add_argument("--titulo"); ap.add_argument("--chips"); ap.add_argument("--info")
    o = ap.parse_args()
    datos = json.loads((RAIZ / "prospectos" / "abogados.json").read_text(encoding="utf-8"))
    a = next((x for x in datos if x["slug"] == o.slug), None)
    if not a: sys.exit(f"No existe {o.slug} en abogados.json")
    modo = o.modo or ("logo" if a.get("logo") else "foto")
    etiqueta = o.etiqueta or a.get("nombre", "").upper()
    titulo = o.titulo or html.escape(a.get("frase") or a.get("titulo", ""))
    chips = [c.strip() for c in o.chips.split(",")] if o.chips else [corto(x["nombre"]) for x in a.get("areas", [])][:8]
    info = o.info or f"{html.escape(a.get('ciudad', ''))}<br>{html.escape(a.get('modalidad', 'Atención personalizada'))}"
    url, H = construir(a, modo, etiqueta, titulo, chips, info)
    (RAIZ / "estados").mkdir(exist_ok=True)
    nombre = "Estado-" + "-".join(w.capitalize() for w in o.slug.split("-")) + ".png"
    salida = RAIZ / "estados" / nombre
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
