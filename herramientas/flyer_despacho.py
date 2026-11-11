"""Flyer estilo despacho (1080x1350): oscuro, foto a sangre, título con serif elegante,
sello circular "Despacho destacado LicLink" (estilo insignia Superhost) y botón de WhatsApp + QR.
El título va al dolor del cliente y a algo concreto (estilo campañas de Habi).

Uso:
  python3 herramientas/flyer_despacho.py <slug> --titulo "¿Detuvieron a un familiar?" --dorado "Cada hora cuenta."
      [--sub "Defensa penal estratégica en Edo. de México y CDMX."] [--servicios "A,B,C,D"] [--imagen foto|logo]
Sale en estados/Flyer-Despacho-<Slug>.png y comprueba el QR.
"""
import argparse, asyncio, base64, html, io, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estado as E
import flyer as FL
import qrcode

RAIZ = E.RAIZ


def construir(a, titulo, dorado, sub, servicios, imagen):
    slug = a["slug"]; carpeta = RAIZ / "public" / slug; url = f"{E.URL_BASE}/{slug}/"
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=16, border=1); q.add_data(url); q.make(fit=True)
    buf = io.BytesIO(); q.make_image(fill_color="#0d0c0a", back_color="white").convert("RGB").save(buf, "PNG")
    qr = base64.b64encode(buf.getvalue()).decode()
    fondo_logo = a.get("fondo_logo") or "#0b0b0b"
    logo_f = a.get("imagen_vista") or "logo.jpg"
    if imagen == "foto":
        fondo = f"background:#0d0c0a url(data:image/jpeg;base64,{E.b64(carpeta / a['foto'])}) center top/100% auto no-repeat"
    else:
        fondo = "background:radial-gradient(70% 45% at 50% 28%,rgba(212,176,106,.16),transparent 70%),#0d0c0a"
    marca = ""
    if imagen == "logo":
        marca = f'<div class=logobox style="background:{fondo_logo} url(data:image/jpeg;base64,{E.b64(carpeta / logo_f)}) center/cover"></div>'
    if imagen == "foto" and (carpeta / logo_f).exists() and logo_f != a.get("foto"):
        marca = f'<div class=marca style="background:{fondo_logo} url(data:image/jpeg;base64,{E.b64(carpeta / logo_f)}) center/cover"></div>'
    nos = not re.match(r"(Lic|Abogad|Mtr|Dr)", a.get("nombre", ""))
    servs = '<i>◆</i>'.join(f"<span>{html.escape(s)}</span>" for s in servicios)
    sello = ("<svg class=sello viewBox='0 0 200 200'><defs><path id=c d='M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0'/></defs>"
             "<circle cx=100 cy=100 r=98 fill='#0d0c0a' stroke='#d4b06a' stroke-width=3 />"
             "<circle cx=100 cy=100 r=62 fill='none' stroke='#d4b06a' stroke-width=1.5 />"
             "<text font-family='Plus Jakarta Sans' font-weight=800 font-size=15.5 letter-spacing=3.2 fill='#e8cf95'>"
             "<textPath href='#c'>DESPACHO DESTACADO ◆ LICLINK 2026 ◆</textPath></text>"
             "<text x=100 y=98 text-anchor=middle font-size=46 fill='#d4b06a'>★</text>"
             "<text x=100 y=130 text-anchor=middle font-family='Plus Jakarta Sans' font-weight=800 font-size=17 fill='#fff'>Lic<tspan fill='#d4b06a'>Link</tspan></text></svg>")
    return url, f"""<html><head><link href="https://fonts.googleapis.com/css2?family=x" rel="stylesheet"><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;{fondo};font-family:'Plus Jakarta Sans';color:#f7f2e9;position:relative;overflow:hidden}}
.vel{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(13,12,10,.75) 0%,rgba(13,12,10,.25) 40%,rgba(13,12,10,0) 60%),linear-gradient(180deg,rgba(13,12,10,0) 30%,rgba(13,12,10,.8) 46%,#0d0c0a 58%)}}
.marco{{position:absolute;inset:28px;border:1.5px solid rgba(212,176,106,.55);pointer-events:none}}
.marca{{position:absolute;left:70px;top:70px;width:120px;height:120px;border:2px solid #d4b06a}}
.logobox{{position:absolute;left:310px;top:150px;width:460px;height:460px;border:3px solid #d4b06a;box-shadow:0 0 0 12px rgba(212,176,106,.12),0 30px 80px rgba(0,0,0,.6)}}
.nombre{{position:absolute;left:70px;top:{220 if imagen == "foto" else 66}px;font-size:24px;font-weight:800;letter-spacing:6px;color:#d4b06a;max-width:{560 if imagen == "foto" else 680}px;line-height:1.4}}
.sello{{position:absolute;right:64px;top:{70 if imagen == "logo" else 400}px;width:190px;height:190px;filter:drop-shadow(0 12px 30px rgba(0,0,0,.6))}}
.txt{{position:absolute;left:70px;right:70px;top:{585 if imagen == "foto" else 650}px}}
h1{{font-family:'Bodoni Moda';font-weight:500;font-size:{84 if len(titulo) <= 26 else 72}px;line-height:1.06;letter-spacing:-1.5px;max-width:940px}}
h1 em{{display:block;font-style:italic;color:#d4b06a;font-weight:400}}
.sub{{font-size:30px;line-height:1.35;color:#d9d1c4;margin-top:22px;max-width:860px;font-weight:500}}
.servs{{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;margin-top:26px;font-size:25px;font-weight:700;letter-spacing:.5px;color:#f3dfae}}
.servs i{{font-style:normal;color:#8a7344;font-size:16px}}
.pie{{position:absolute;left:70px;right:70px;bottom:70px;display:flex;gap:24px;align-items:stretch}}
.wa{{flex:1;background:linear-gradient(135deg,#e8cf95,#c79f55);color:#17120a;padding:26px 32px;display:flex;flex-direction:column;justify-content:center}}
.wa small{{font-size:24px;font-weight:800;letter-spacing:2px}}
.wa .n{{display:flex;align-items:center;gap:14px;font-size:54px;font-weight:800;letter-spacing:-1.5px;margin-top:4px}}
.wa .u{{font-size:{23 if len(slug) <= 22 else 19}px;font-weight:700;margin-top:8px;color:#4a3a1c}}
.qr{{width:210px;background:#fff;padding:14px;text-align:center;color:#17120a}}
.qr img{{width:100%;display:block}} .qr span{{display:block;font-size:17px;font-weight:800;margin-top:6px}}
</style></head><body><div class=vel></div><div class=marco></div>{marca}
<div class=nombre>{html.escape(a.get("nombre", "").upper())}</div>{sello}
<div class=txt><h1>{html.escape(titulo)}<em>{html.escape(dorado)}</em></h1><div class=sub>{html.escape(sub)}</div><div class=servs>{servs}</div></div>
<div class=pie><div class=wa><small>{"ESCRÍBENOS" if nos else "ESCRÍBEME"} AHORA POR WHATSAPP</small><div class=n>{FL.WA.replace('#25d366', '#17120a')}{FL.tel(a.get("telefono", ""))}</div><div class=u>liclink.com.mx/{slug}</div></div>
<div class=qr><img src="data:image/png;base64,{qr}"><span>{"VER PERFIL" if nos else "VER MI PERFIL"}</span></div></div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--titulo", required=True); ap.add_argument("--dorado", required=True)
    ap.add_argument("--sub"); ap.add_argument("--servicios"); ap.add_argument("--imagen", choices=["foto", "logo"])
    o = ap.parse_args()
    a = next((x for x in json.loads((RAIZ / "prospectos" / "abogados.json").read_text(encoding="utf-8")) if x["slug"] == o.slug), None)
    if not a: sys.exit(f"No existe {o.slug}")
    imagen = o.imagen or ("foto" if (not a.get("logo") and a.get("foto") and (RAIZ / "public" / o.slug / a["foto"]).exists()) else "logo")
    sub = o.sub or a.get("titulo", "")
    servicios = [s.strip() for s in o.servicios.split(",")] if o.servicios else [E.corto(x["nombre"]) for x in a.get("areas", [])][:4]
    url, H = construir(a, o.titulo, o.dorado, sub, servicios, imagen)
    (RAIZ / "estados").mkdir(exist_ok=True)
    salida = RAIZ / "estados" / ("Flyer-Despacho-" + "-".join(w.capitalize() for w in o.slug.split("-")) + ".png")
    asyncio.run(FL.render(H, salida))
    import cv2
    leido = cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(salida)))[0]
    print("QR ok" if leido == url else f"OJO: QR leyó '{leido}'"); print(salida)


if __name__ == "__main__":
    main()
