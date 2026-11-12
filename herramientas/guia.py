# -*- coding: utf-8 -*-
"""LicLink · genera la guía de abogados:
  public/index.html                      portada (clientes + sección para abogados)
  public/abogados/<ciudad>/              listado por ciudad
  public/abogados/<ciudad>/<materia>/    listado por ciudad y materia (para Google)
  public/para-abogados/                  planes y registro
  public/assets/guia-datos.js            abogados publicados (solo los que pagaron: estado "vendido" con "plan")
Uso: python3 herramientas/guia.py
"""
import json, os, html as H, sys
sys.path.insert(0, os.path.dirname(__file__))
from generar import DATOS, PUBLICO, URL_BASE, area, slugify, version

CIUDADES = {"cdmx": ("Ciudad de México", "CDMX"), "edomex": ("Estado de México", "Edomex"),
            "guadalajara": ("Guadalajara", "Jalisco"), "puebla": ("Puebla", "Puebla"),
            "monterrey": ("Monterrey", "Nuevo León"), "tijuana": ("Tijuana", "Baja California"), "leon": ("León", "Guanajuato"),
            "chihuahua": ("Chihuahua", "Chihuahua"), "san-luis-potosi": ("San Luis Potosí", "SLP"), "los-cabos": ("Los Cabos", "Baja California Sur"),
            "yucatan": ("Yucatán", "Yucatán"), "queretaro": ("Querétaro", "Querétaro")}
PRINCIPALES = ["cdmx", "edomex", "guadalajara", "puebla"]
FONDOS = {"cdmx": "radial-gradient(90% 80% at 100% 0%,#6b5326 0%,transparent 60%),linear-gradient(160deg,#1e1a14,#0c0b0a)",
          "edomex": "radial-gradient(90% 80% at 0% 0%,#4f4a2b 0%,transparent 60%),linear-gradient(200deg,#1a1913,#0c0b0a)",
          "guadalajara": "radial-gradient(90% 80% at 100% 100%,#6a3f2a 0%,transparent 60%),linear-gradient(160deg,#1d1612,#0c0b0a)",
          "puebla": "radial-gradient(90% 80% at 0% 100%,#2d4a52 0%,transparent 60%),linear-gradient(200deg,#121a1b,#0c0b0a)"}
MATERIAS = {
    "penal": ("Penal", "Detenciones, denuncias y defensa", "abogado penalista"),
    "familiar": ("Familiar", "Divorcio, pensión y custodia", "abogado familiar"),
    "laboral": ("Laboral", "Despidos y liquidaciones", "abogado laboral"),
    "civil": ("Civil e inmobiliario", "Casas, terrenos, rentas y contratos", "abogado civil"),
    "mercantil": ("Mercantil", "Pagarés, deudas y cobranza", "abogado mercantil"),
    "sucesiones": ("Herencias", "Testamentos e intestados", "abogado de herencias"),
    "amparo": ("Amparo", "Contra abusos de autoridad", "abogado de amparo"),
    "fiscal": ("Fiscal", "SAT, multas y embargos", "abogado fiscal"),
    "agrario": ("Agrario y ambiental", "Ejidos, tierras y medio ambiente", "abogado agrario"),
}
PLURAL = {"penal": "Abogados penalistas", "familiar": "Abogados familiares", "laboral": "Abogados laborales", "civil": "Abogados civiles",
          "mercantil": "Abogados mercantiles", "sucesiones": "Abogados de herencias", "amparo": "Abogados de amparo", "fiscal": "Abogados fiscalistas", "agrario": "Abogados agrarios"}
ICONOS = {
    "penal": '<path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "familiar": '<circle cx="8" cy="7" r="2.5"/><circle cx="16.5" cy="8.5" r="2"/><path d="M3.5 20v-4a4.5 4.5 0 019 0v4M13 20v-3a3.5 3.5 0 017 0v3"/>',
    "laboral": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M3 13h18"/>',
    "civil": '<path d="M3 11l9-7 9 7v9a1 1 0 01-1 1h-5v-6H9v6H4a1 1 0 01-1-1z"/>',
    "mercantil": '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.8"/><path d="M6 9.5v5M18 9.5v5"/>',
    "sucesiones": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    "amparo": '<path d="M12 4v16M7 20h10M5 7h14M5 7l-3 6a3 3 0 006 0zM19 7l-3 6a3 3 0 006 0z"/>',
    "fiscal": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "agrario": '<path d="M12 21V11"/><path d="M12 11c0-4 3-7 7-7 0 4-3 7-7 7zM12 14c0-3-2.5-5.5-6-5.5 0 3 2.5 5.5 6 5.5z"/><path d="M5 21h14"/>',
}
SIMBOLOS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-ok" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-no" viewBox="0 0 24 24"><path d="M7 12h10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4c-1-1.6-1.5-3.4-1.5-5.2C2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9 1.8 1.8 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zm8.3-18.1C18.1 1.5 15.1.2 12 .2 5.5.2.2 5.5.2 12c0 2.1.5 4.1 1.6 5.9L.1 23.8l6.1-1.6c1.7.9 3.7 1.4 5.7 1.4 6.5 0 11.8-5.3 11.8-11.8 0-3.1-1.2-6.1-3.4-8.3z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0114 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></g></symbol>
<symbol id="i-lupa" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></g></symbol>
<symbol id="i-flecha" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-sello" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 2.5l2.4 1.8 3-.2.9 2.9 2.4 1.8-1 2.8 1 2.8-2.4 1.8-.9 2.9-3-.2L12 21.5l-2.4-1.8-3 .2-.9-2.9-2.4-1.8 1-2.8-1-2.8 2.4-1.8.9-2.9 3 .2z"/><path d="M8.5 12l2.3 2.3 4.7-4.6"/></g></symbol>
<symbol id="i-candado" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 018 0v3"/></g></symbol>
<symbol id="i-mano" viewBox="0 0 24 24"><path d="M4 12l4-4 4 2 4-2 4 4-6 6-2-1-2 1z M8 8l4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
<symbol id="i-facebook" viewBox="0 0 24 24"><path fill="currentColor" d="M14 8h3V4h-3c-2.8 0-4.5 1.8-4.5 4.6V11H7v4h2.5v9h4v-9H16l.6-4h-3.1V8.9c0-.6.3-.9.5-.9z"/></symbol>
<symbol id="i-instagram" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/></g></symbol>
<symbol id="i-tiktok" viewBox="0 0 24 24"><path fill="currentColor" d="M16.6 3c.4 2.2 1.8 3.7 4 3.9v3.3c-1.5 0-2.8-.4-4-1.2v6.3c0 3.5-2.6 5.7-5.6 5.7-3.2 0-5.6-2.5-5.6-5.5 0-3.4 2.9-5.9 6.5-5.4v3.4c-1.6-.4-3.1.6-3.1 2.1 0 1.2 1 2.1 2.2 2.1 1.4 0 2.3-.9 2.3-2.6V3h3.3z"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5" stroke-linecap="round"/></g></symbol>
<symbol id="i-web" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></g></symbol>
""" + "".join(f'<symbol id="m-{k}" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{v}</g></symbol>' for k, v in ICONOS.items()) + "</svg>"

e = H.escape
OK = '<svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>'
NO = '<svg viewBox="0 0 24 24"><use href="#i-no"/></svg>'
WA = '<svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>'


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>\n"


def cabeza(titulo, desc, ruta, robots="", extra=""):
    url = URL_BASE + ruta
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="LicLink">
<meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{URL_BASE}/assets/liclink-compartir.png?v={version('liclink-compartir.png')}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#faf6ef">
<link rel="manifest" href="/manifest.webmanifest"><link rel="apple-touch-icon" href="/assets/icono-192.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230c0b0a'/%3E%3Ctext x='32' y='44' font-family='Arial' font-weight='800' font-size='36' text-anchor='middle' fill='%23d4b06a'%3EL%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/guia.css?v={version('guia.css')}">
{extra}
</head>
"""


BARRA = """<header class="barra"><div class="w">
  <a href="/" class="marca" aria-label="LicLink, inicio">Lic<i>Link</i></a>
  <nav><a class="txt" href="/#materias">Materias</a><a class="txt" href="/#ciudades">Ciudades</a><a class="txt" href="/guias/">Guías legales</a>
  <a class="btn btn-linea btn-chico" href="/para-abogados/">Soy abogado</a></nav>
</div></header>"""

PIE = """<footer class="pie"><div class="w">
  <div class="cols">
    <div><a href="/" class="marca" style="color:var(--claro)">Lic<i>Link</i></a><p style="margin-top:12px;max-width:340px">La guía de abogados de México. Encuentra, compara y habla directo con tu abogado.</p></div>
    <div><b>Ciudades</b><ul>""" + "".join(f'<li><a href="/abogados/{k}/">{v[0]}</a></li>' for k, v in CIUDADES.items()) + """</ul></div>
    <div><b>Materias</b><ul>""" + "".join(f'<li><a href="/abogados/cdmx/{k}/">{v[0]}</a></li>' for k, v in list(MATERIAS.items())[:6]) + """</ul></div>
    <div><b>LicLink</b><ul><li><a href="/para-abogados/">Planes para abogados</a></li><li><a href="/para-abogados/#registro">Registrarme</a></li><li><a href="/guias/">Guías legales</a></li><li><a href="/aviso-de-privacidad/">Aviso de privacidad</a></li><li><a href="/terminos/">Términos y condiciones</a></li></ul></div>
  </div>
  <p class="legal">LicLink es un directorio: no presta servicios legales ni cobra comisiones por los casos. Cada abogado es responsable de su servicio. «Cédula profesional verificada» significa que revisamos la cédula en el Registro Nacional de Profesionistas de la SEP; «Datos profesionales registrados» significa que aún no la revisamos. Si estás en peligro inmediato, llama al 911.<br>© LicLink 2026</p>
</div></footer>"""


AYUDA = """<a class="ayuda js-liclink" data-msg="Hola, necesito ayuda para encontrar abogado." aria-label="¿Te ayudamos a elegir abogado?"><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg><span>¿Te ayudamos a elegir?</span></a>"""


def fin(ayuda=True):
    return (AYUDA if ayuda else "") + SIMBOLOS + '\n<script src="/assets/guia-datos.js?v=' + version('guia-datos.js') + '" defer></script>\n<script src="/assets/guia.js?v=' + version('guia.js') + '" defer></script>\n</body>\n</html>\n'


def cargar_guia():
    ruta = os.path.join(os.path.dirname(DATOS), "guia.json")
    return [a for a in (json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else []) if a.get("plan") in ("basico", "premium") and a.get("estado", "activo") == "activo"]


def wa_url(num, msg):
    from urllib.parse import quote
    return f"https://wa.me/{num}?text={quote(msg)}"


def ficha_html(a, clase="ficha"):
    """Ficha del directorio. Básico: WhatsApp y llamada. Premium: además perfil completo, redes y reseñas."""
    prem = a.get("plan") == "premium"
    nc = CIUDADES.get(a.get("ciudad"), ("",))[0]
    foto = f'<img src="{e(a["foto"])}" alt="" loading="lazy" decoding="async" width="72" height="72">' if a.get("foto") else e(a.get("iniciales") or a["nombre"][:2])
    ver = (f'<span class="ver si"><svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>Cédula profesional verificada</span>' if a.get("verificada")
           else '<span class="ver no">Datos profesionales registrados</span>')
    rol = e(a.get("rol", "")) + (f" · {e(nc)}" if nc and nc not in a.get("rol", "") else "")
    tags = "".join(f"<span>{e(MATERIAS[k][0])}</span>" for k in a.get("materias", []) if k in MATERIAS)
    redes = ""
    if prem:
        redes = "".join(f'<a href="{e(u)}" target="_blank" rel="noopener" aria-label="{k}"><svg viewBox="0 0 24 24"><use href="#i-{k}"/></svg></a>' for k, u in (a.get("redes") or {}).items() if u)
    acc = ""
    if prem and a.get("pagina"): acc += f'<a class="btn btn-negro uno" href="{e(a["pagina"])}">Ver perfil completo</a>'
    acc += f'<a class="btn btn-wa{"" if a.get("telefono") else " uno"}" target="_blank" rel="noopener" href="{e(wa_url(a["whatsapp"], "Hola, lo encontré en LicLink. Necesito asesoría."))}" data-evento="whatsapp" data-slug="{e(a["slug"])}">{WA}WhatsApp</a>'
    if a.get("telefono"): acc += f'<a class="btn btn-linea" href="tel:+52{e(a["telefono"])}" data-evento="llamada" data-slug="{e(a["slug"])}">Llamar</a>'
    if prem and a.get("resena"): acc += f'<a class="btn btn-linea uno" target="_blank" rel="noopener" href="{e(a["resena"])}">★ Ver y dejar reseñas en Google</a>'
    return (f'<article class="{clase}{" prem" if prem else ""}" data-plan="{a["plan"]}"><div class="foto{" logo" if a.get("logo") else ""}"{f' style="background:{e(a["fondo"])}"' if a.get("fondo") else ""}>{foto}</div><div>'
            + ('<span class="sello-p">Destacado</span>' if prem else "")
            + f'<h3>{e(a["nombre"])}</h3><div class="rol">{rol}</div>{ver}'
            + (f'<span class="consulta-p">{e(a["consulta"])}</span>' if a.get("consulta") else "")
            + (f'<div class="redes">{redes}</div>' if redes else "") + f'<div class="tags">{tags}</div></div><div class="acc">{acc}</div></article>')


def opciones_ciudad(sel="cdmx"):
    return "".join(f'<option value="{k}"{" selected" if k == sel else ""}>{v[0]}</option>' for k, v in CIUDADES.items())


def planes_html(corto=False):
    basico = ["Ficha en el directorio de tu ciudad", "Fotografía o logotipo", "Nombre y especialidades", "Botón de WhatsApp", "Botón de llamada",
              "Verificación de cédula cuando la compruebes"]
    basico_no = ["Página profesional propia", "Posición destacada", "Redes sociales y reseñas de Google"]
    prem = ["Posición destacada en tu ciudad y especialidades", "Página profesional personalizada con tu propio enlace", "Enlaces a tus redes sociales y sitio web",
            "Botón para recibir reseñas en Google Maps", "Asistente que organiza cada consulta antes de llegar a tu WhatsApp", "Mapa y horarios",
            "Promociones y paquetes", "Estadísticas mensuales de visitas", "Código QR personalizado"]
    li = lambda t, s=True: f'<li{"" if s else " class=no"}>{OK if s else NO}<span>{e(t)}</span></li>'
    boton = (lambda p, t: f'<a class="btn {"btn-oro brilla" if p == "premium" else "btn-linea"} btn-ancho" href="/para-abogados/#registro" data-plan="{p}">{t}</a>')
    return f"""<div class="planes" data-escalona>
  <div class="plan"><h3>Básico</h3><p class="para">Para que te encuentren en tu ciudad.</p>
    <div class="precio"><b>$49</b><span>MXN al mes</span></div><p class="alta">Alta única de $99 MXN</p>
    <ul>{"".join(li(t) for t in basico)}{"".join(li(t, False) for t in basico_no)}</ul>{boton("basico", "Elegir Básico")}</div>
  <div class="plan prem"><span class="cinta">Más completo</span><h3>Premium</h3><p class="para">Tu presencia profesional por menos de $5 al día.</p>
    <div class="precio"><b>$149</b><span>MXN al mes</span></div><p class="alta">Alta única de $399 MXN</p>
    <ul><li class="lead">Todo lo del Básico, y además:</li>{"".join(li(t) for t in prem)}</ul>{boton("premium", "Elegir Premium")}</div>
</div>
<div class="fundadores rv">
  <b>Socios fundadores LicLink</b>
  <p>Para los despachos que se registren en la etapa de lanzamiento:</p>
  <ul><li>{OK}Precio de lanzamiento protegido mientras tu suscripción siga activa</li><li>{OK}Configuramos tu perfil por ti</li><li>{OK}Código QR para tu tarjeta y tu oficina</li><li>{OK}Atención directa por WhatsApp</li></ul>
  <small>Si cancelas y regresas después, aplica el precio vigente en ese momento.</small>
</div>
<ul class="garantias">
  <li>{OK}Sin contratos forzosos: pagas mes a mes</li>
  <li>{OK}Cancelas cuando quieras con un mensaje de WhatsApp</li>
  <li>{OK}Cero comisiones: el cliente te paga directo a ti</li>
  <li>{OK}No prometemos clientes: te damos visibilidad y herramientas para que te contacten</li>
</ul>"""


def portada():
    atajos = [("laboral", "Me despidieron"), ("familiar", "Necesito un divorcio"), ("penal", "Detuvieron a un familiar"), ("civil", "Problema con una propiedad"), ("mercantil", "Me deben dinero"), ("familiar", "Pensión alimenticia")]
    mats = "".join(f'<a class="materia" href="/abogados/cdmx/{k}/" data-m="{k}"><span class="ic"><svg viewBox="0 0 24 24"><use href="#m-{k}"/></svg></span><b>{v[0]}</b><small>{v[1]}</small></a>' for k, v in MATERIAS.items())
    ciuds = "".join(f'<a class="ciudad" href="/abogados/{k}/" style="--fondo-c:{FONDOS[k]}"><span class="flecha"><svg width="18" height="18" viewBox="0 0 24 24"><use href="#i-flecha"/></svg></span><b>{v[0]}</b><small><svg width="15" height="15" viewBox="0 0 24 24"><use href="#i-pin"/></svg>Ver abogados</small></a>' for k, v in CIUDADES.items() if k in PRINCIPALES)
    otras = "".join(f'<a href="/abogados/{k}/">{v[0]}</a>' for k, v in CIUDADES.items() if k not in PRINCIPALES)
    preguntas = [
        ("¿Cuánto me cuesta usar LicLink?", "Nada. Buscar y escribirle a un abogado es gratis. Tú acuerdas sus honorarios directamente con él."),
        ("¿Cómo sé que es abogado de verdad?", "Cuando un perfil dice «Cédula profesional verificada», revisamos su cédula en el Registro Nacional de Profesionistas de la SEP. Los perfiles que dicen «Datos profesionales registrados» aún no tienen esa revisión. Tú también puedes consultar cualquier cédula en la SEP."),
        ("¿LicLink cobra comisión por mi caso?", "No. Hablas directo con el abogado por WhatsApp o por teléfono, sin intermediarios."),
        ("¿Qué pasa con lo que le cuento al abogado?", "Tu mensaje va directo a su WhatsApp. LicLink no guarda ni lee tu caso."),
        ("¿LicLink me da asesoría legal?", "No. LicLink es un directorio: te ayuda a encontrar y contactar abogados. La asesoría la da cada abogado."),
        ("¿Las reseñas son reales?", "Las reseñas están en Google Maps, a la vista de todos. Nosotros no las escribimos, no las editamos ni las borramos."),
    ]
    faq = "".join(f"<details><summary>{e(p)}</summary><p>{e(r)}</p></details>" for p, r in preguntas)
    g = cargar_guia()
    import random
    random.seed(len(g))
    prem = [a for a in g if a["plan"] == "premium"]; resto = [a for a in g if a["plan"] != "premium" and a.get("foto")]
    random.shuffle(resto)
    destacados = "".join(ficha_html(a) for a in (prem + resto)[:8])
    guias_cards = "".join(f'<a class="g-card" href="/guias/{x["slug"]}/"><span class="eti">{e(MATERIAS[x["materia"]][0])}</span><b>{e(x["titulo"])}</b><span class="g-leer">Leer guía →</span></a>' for x in GUIAS)
    titulo = "LicLink · Encuentra abogado en CDMX, Edomex, Guadalajara, Puebla y más"
    desc = "La guía de abogados de México. Busca por ciudad y materia, revisa su perfil y escríbele directo por WhatsApp. Gratis."
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": "LicLink", "url": URL_BASE + "/"},
        {"@type": "Organization", "name": "LicLink", "url": URL_BASE + "/", "logo": URL_BASE + "/assets/liclink-compartir.png"}]}
    return cabeza(titulo, desc, "/", extra=jsonld(ld)) + f"""<body>
{BARRA}
<main>
<section class="portada"><div class="w">
  <span class="eti entra" style="--d:.05s">Guía de abogados de México</span>
  <h1><span class="l"><span style="--i:0">Encuentra al abogado que necesitas.</span></span><span class="l"><span style="--i:1"><em>Sin complicaciones.</em></span></span></h1>
  <p class="sub entra" style="--d:.6s">Busca por ciudad y especialidad. Compara perfiles y contacta directo por WhatsApp, sin pagar por usar LicLink.</p>
  <form class="buscador entra" id="buscar" style="--d:.75s" role="search">
    <div class="campo libre"><svg viewBox="0 0 24 24"><use href="#i-chat"/></svg><div><label for="bTexto">¿Qué te pasó?</label><input id="bTexto" autocomplete="off" placeholder="Ej. me corrieron del trabajo"><span class="sugerido" id="bSug" hidden></span></div></div>
    <div class="campo"><svg viewBox="0 0 24 24"><use href="#i-pin"/></svg><div><label for="bCiudad">Ciudad</label><select id="bCiudad">{opciones_ciudad()}</select></div></div>
    <div class="campo"><svg viewBox="0 0 24 24"><use href="#i-lupa"/></svg><div><label for="bMateria">Especialidad</label><select id="bMateria"><option value="">Todas las especialidades</option>{"".join(f'<option value="{k}">{v[0]} · {v[1]}</option>' for k, v in MATERIAS.items())}</select></div></div>
    <button class="btn btn-oro brilla" type="submit"><svg viewBox="0 0 24 24"><use href="#i-lupa"/></svg>Buscar abogados</button>
  </form>
  <p class="atajos-t entra" style="--d:.85s">¿Qué te pasó?</p>
  <div class="atajos entra" style="--d:.9s">{"".join(f'<a href="/abogados/cdmx/{k}/" data-atajo="{k}">{e(t)}</a>' for k, t in atajos)}</div>
  <ul class="confianza entra" style="--d:1s">
    <li><svg viewBox="0 0 24 24"><use href="#i-candado"/></svg>Gratis para ti, sin comisiones</li>
    <li><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>Contacto directo con el abogado</li>
    <li><svg viewBox="0 0 24 24"><use href="#i-sello"/></svg>Te decimos qué cédulas están verificadas</li>
  </ul>
</div></section>

<section class="marfil" style="padding:36px 0 20px"><div class="w">
  <span class="eti rv">Abogados en LicLink</span>
  <h2 class="rv">Conoce a algunos de <em>nuestros abogados.</em></h2>
  <div class="destacados" id="destacados">{destacados}</div>
</div></section>

<section class="preg-sec" id="preguntar"><div class="w">
  <form class="pregunta rv" id="pregunta">
    <div class="preg-cab"><span class="preg-ic"><svg viewBox="0 0 24 24"><use href="#i-chat"/></svg></span>
      <div><h2>¿No sabes qué abogado necesitas?</h2><p>Cuéntanos qué pasó y te orientamos sobre qué especialista buscar. Gratis y sin dar tu nombre.</p></div></div>
    <div class="preg-caja"><label class="oculto" for="pTexto">Tu caso</label>
      <textarea id="pTexto" required maxlength="600" rows="3" placeholder="Ej. Me despidieron sin darme finiquito, ¿qué abogado necesito?"></textarea>
      <span class="cuenta" id="pCuenta">0 / 600</span></div>
    <div class="fila"><select id="pCiudad" aria-label="Tu ciudad">{opciones_ciudad()}</select><button class="btn btn-linea" type="submit">{WA}Enviar por WhatsApp</button></div>
  </form>
</div></section>

<div class="historia-caja historia oscuro"><section style="background:none"><div class="w historia-grid">
  <div class="rv h-txt">
    <span class="eti">Así funciona</span>
    <h2>De la angustia a la <em>tranquilidad</em>, en minutos.</h2>
    <p class="sub">Un problema legal llega sin avisar, muchas veces de noche. Con LicLink encuentras a un abogado cerca de ti y le escribes en ese momento.</p>

  </div>
  <div class="rv h-et">
    <ol class="etapas">
      <li class="activa"><span class="cara">😟</span><div><b>Angustia</b><small>11:42 p.m. · Detienen a su hijo y no sabe a quién llamar.</small></div></li>
      <li><span class="cara">🤝</span><div><b>Alguien responde</b><small>Encuentra un penalista verificado y le escribe por WhatsApp.</small></div></li>
      <li><span class="cara">😌</span><div><b>Tranquilidad</b><small>2:51 a.m. · Su hijo ya está en casa.</small></div></li>
    </ol>
  </div>
  <div class="rv h-tel" style="--d:.15s">
    <div class="telefono"><div class="pantalla">
      <div class="chat-top"><span class="av">LR</span><div><b>Lic. Ramírez · Penalista</b><small><svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>Cédula verificada</small></div></div>
      <div class="chat" id="chat"></div>
    </div></div>
    <p class="ilustrativa">Historia ilustrativa</p>
  </div>
</div></section></div>

<section class="marfil"><div class="w">
  <span class="eti rv">Tres pasos</span>
  <h2 class="rv">Encontrar abogado <em>ya no es un volado.</em></h2>
  <div class="pasos" data-escalona>
    <div class="paso"><span class="n">1</span><div><h3>Busca</h3><p>Elige tu ciudad y lo que te está pasando, en palabras normales.</p></div></div>
    <div class="paso"><span class="n">2</span><div><h3>Compara</h3><p>Revisa sus especialidades, si su cédula está verificada y dónde está su despacho.</p></div></div>
    <div class="paso"><span class="n">3</span><div><h3>Escríbele</h3><p>Un toque y hablas directo con el abogado por WhatsApp. Sin intermediarios.</p></div></div>
  </div>
</div></section>

<section class="marfil" id="materias" style="padding-top:0"><div class="w">
  <span class="eti rv">Materias</span>
  <h2 class="rv">¿Qué te está <em>pasando?</em></h2>
  <div class="materias" data-escalona>{mats}</div>
</div></section>

<section class="marfil" id="ciudades" style="padding-top:0"><div class="w">
  <span class="eti rv">Ciudades</span>
  <h2 class="rv">Abogados cerca de ti.</h2>
  <div class="ciudades" data-escalona>{ciuds}</div>
  <p class="pronto rv">También en:</p><div class="atajos rv" style="margin-top:10px">{otras}</div>
</div></section>

<section class="marfil" style="padding-top:0"><div class="w">
  <span class="eti rv">Guías legales gratis</span>
  <h2 class="rv">Entiende tu caso <em>antes de llamar.</em></h2>
  <div class="g-grid" data-escalona>{guias_cards}</div>
  <a class="ver-todas rv" href="/guias/">Ver todas las guías →</a>
</div></section>

<section class="marfil" style="padding-top:0"><div class="w">
  <span class="eti rv">Por qué LicLink</span>
  <h2 class="rv">Confianza antes de <em>contratar.</em></h2>
  <div class="porque" data-escalona>
    <div><b>Transparencia</b><p>Te decimos con claridad qué cédulas revisamos en la SEP y cuáles aún no.</p></div>
    <div><b>Directo con el abogado</b><p>Le escribes a su WhatsApp. Sin centros de llamadas ni intermediarios.</p></div>
    <div><b>Reseñas públicas</b><p>Las opiniones están en Google Maps, donde nadie las puede maquillar.</p></div>
    <div><b>Gratis para ti</b><p>No pagas por buscar ni por escribir. Los honorarios los acuerdas con tu abogado.</p></div>
  </div>
</div></section>

<section class="abogados oscuro" id="abogados"><div class="w">
  <span class="eti rv">Para abogados</span>
  <h2 class="rv">Haz visible tu despacho <em>cuando te buscan.</em></h2>
  <p class="sub rv">Crea tu perfil profesional, destaca tus especialidades y recibe contactos directo en tu WhatsApp. Desde $49 MXN al mes.</p>
  {planes_html()}
</div></section>

<section class="marfil"><div class="w">
  <span class="eti rv">Preguntas frecuentes</span>
  <h2 class="rv">Lo que más nos <em>preguntan.</em></h2>
  <div class="faq rv">{faq}</div>
</div></section>

<section class="cierre oscuro"><div class="w">
  <h2 class="rv">Actuar a tiempo hace <em>la diferencia.</em></h2>
  <div class="acciones rv"><a class="btn btn-oro brilla" href="#buscar" onclick="setTimeout(function(){{document.getElementById('bCiudad').focus()}},500)"><svg viewBox="0 0 24 24"><use href="#i-lupa"/></svg>Buscar abogados</a>
  <a class="btn btn-linea" href="/para-abogados/">Soy abogado: quiero aparecer</a></div>
</div></section>
</main>
{PIE}
""" + fin()


def listado(c, m="", g=None):
    nc = CIUDADES[c][0]
    g = cargar_guia() if g is None else g
    todos = [a for a in g if (a.get("ciudad") == c or c in a.get("otras_ciudades", [])) and (not m or m in a.get("materias", []))]
    todos.sort(key=lambda a: (a["plan"] != "premium", a["nombre"]))
    migas = [("Inicio", "/"), (nc, f"/abogados/{c}/")]
    if m:
        nm, desc_m, busq = MATERIAS[m]
        titulo = f"{PLURAL[m]} en {nc} | LicLink"
        desc = f"Encuentra {busq} en {nc}. {desc_m}. Revisa su perfil y escríbele directo por WhatsApp, gratis."
        pl = PLURAL[m].split(" ", 1)
        h1 = f'{pl[0]} <em>{e(pl[1])}</em> en {e(nc)}'
        ruta = f"/abogados/{c}/{m}/"
        migas.append((nm, ruta))
    else:
        titulo = f"Abogados en {nc} | LicLink"
        desc = f"Abogados en {nc}: penal, familiar, laboral, civil, mercantil y más. Revisa su perfil y escríbeles directo por WhatsApp."
        h1 = f'Abogados en <em>{e(nc)}</em>'
        ruta = f"/abogados/{c}/"
    gr = next((x for x in GUIAS if x["materia"] == m), None) if m else None
    guia_rel = f'<a class="g-card g-rel" href="/guias/{gr["slug"]}/"><span class="eti">Guía gratis</span><b>{e(gr["titulo"])}</b><span class="g-leer">Leer guía →</span></a>' if gr else ""
    cuantos = f"{len(todos)} abogado{'s' if len(todos) != 1 else ''} en LicLink" if todos else ""
    robots = "" if todos else '<meta name="robots" content="noindex, follow">\n'  # sin abogados no pedimos a Google que la muestre
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": t, "item": URL_BASE + u} for n, (t, u) in enumerate(migas)]}
    nav = " <span>›</span> ".join(f'<a href="{u}">{e(t)}</a>' for t, u in migas[:-1]) + f" <span>›</span> <b>{e(migas[-1][0])}</b>"
    return cabeza(titulo, desc, ruta, robots, extra=jsonld(ld)) + f"""<body data-ciudad="{c}" data-materia="{m}" data-plural="{PLURAL.get(m, "abogados").lower()}">
{BARRA}
<main>
<section class="encabezado"><div class="w">
  <nav class="migas" aria-label="Estás en">{nav}</nav>
  <h1>{h1}</h1>
  <p class="sub">{e(cuantos + " · " if cuantos else "")}Revisa su perfil y escríbeles directo por WhatsApp, sin costo para ti.</p>
  <nav class="filtros" id="filtros" aria-label="Especialidades"></nav>
</div></section>
<section class="marfil" style="padding-top:0"><div class="w"><div class="lista" id="lista">{"".join(ficha_html(a) for a in todos)}</div>{guia_rel}</div></section>
</main>
{PIE}
""" + fin()


def para_abogados():
    preguntas = [
        ("¿Hay contrato forzoso?", "No. Pagas mes a mes y cancelas cuando quieras con un mensaje de WhatsApp. Sin penalizaciones."),
        ("¿Cuánto tardan en publicar mi perfil?", "Entre 24 y 48 horas después de recibir tus datos. Primero te lo enseñamos y solo lo publicamos cuando tú lo apruebas."),
        ("¿Me garantizan clientes?", "No. Nadie puede garantizarlos de forma honesta. Te damos visibilidad profesional y herramientas para que quien te busque te encuentre y te contacte fácil."),
        ("¿Por qué piden mi cédula?", "Para mostrar en tu perfil «Cédula profesional verificada» después de revisarla en el Registro Nacional de Profesionistas de la SEP. Es lo que más confianza da a quien busca abogado."),
        ("¿Cobran comisión por los clientes?", "No. El cliente te escribe a ti y te paga a ti. Nosotros solo cobramos tu plan."),
        ("¿Cómo funcionan las reseñas en Google?", "En Premium ponemos en tu perfil un botón para que tus clientes te dejen reseña en tu ficha de Google Maps. Más reseñas te ayudan a aparecer más arriba en Google. Si aún no tienes ficha en Google Maps, te ayudamos a crearla."),
        ("¿Puedo cambiar de plan?", "Sí, cuando quieras. Si subes a Premium solo pagas la diferencia del alta."),
        ("¿Mis datos aparecen sin mi permiso?", "Nunca. En LicLink solo aparecen los abogados que se registran y aceptan."),
    ]
    faq = "".join(f"<details><summary>{e(p)}</summary><p>{e(r)}</p></details>" for p, r in preguntas)
    g = cargar_guia()
    ej_p = next((a for a in g if a["plan"] == "premium" and a.get("pagina")), None)
    ej_b = next((a for a in g if a["plan"] == "basico" and a.get("foto") and not a.get("logo")), None)
    muestra = (ficha_html(ej_b) if ej_b else "") + (ficha_html(ej_p) if ej_p else "")
    demo = f'''<a class="demo" href="{e(ej_p["pagina"])}"><img src="{e(ej_p["pagina"])}compartir.png" alt="Perfil Premium de {e(ej_p["nombre"])}" loading="lazy" width="1200" height="630"><span>Ver un perfil Premium real →</span></a>''' if ej_p else ""
    titulo = "Aparece en LicLink · Perfil profesional para abogados"
    desc = "Haz visible tu despacho cuando alguien necesita ayuda legal. Desde $49 MXN al mes, sin contratos forzosos y sin comisiones."
    return cabeza(titulo, desc, "/para-abogados/") + f"""<body>
{BARRA}
<main>
<section class="portada"><div class="w">
  <span class="eti entra" style="--d:.05s">Para abogados</span>
  <h1><span class="l"><span style="--i:0">Tu próximo cliente</span></span><span class="l"><span style="--i:1">podría estar</span></span><span class="l"><span style="--i:2"><em>buscándote ahora.</em></span></span></h1>
  <p class="sub entra" style="--d:.6s">Haz visible tu despacho cuando alguien necesita ayuda legal. Crea tu perfil profesional, destaca tus especialidades y recibe contactos directo en tu WhatsApp.</p>
  <div class="acciones entra" style="--d:.8s;display:grid;gap:10px;margin-top:26px;max-width:420px"><a class="btn btn-oro brilla" href="#registro">Quiero aparecer en LicLink</a><a class="btn btn-linea" href="#planes">Ver planes</a></div>
  <p class="nota-cta entra" style="--d:.9s">Desde $49 MXN al mes · Sin contratos forzosos</p>
</div></section>

<section class="marfil" style="padding-top:10px"><div class="w">
  <span class="eti rv">Así te ven tus clientes</span>
  <h2 class="rv">Básico o Premium: <em>la diferencia se nota.</em></h2>
  <div class="muestra-fichas" data-escalona>{muestra}</div>
  {demo}
</div></section>

<section class="abogados oscuro" id="planes"><div class="w">
  <span class="eti rv">Planes</span>
  <h2 class="rv">Dos planes. <em>Sin letras chiquitas.</em></h2>
  {planes_html()}
</div></section>

<section class="marfil"><div class="w">
  <span class="eti rv">Cómo funciona</span>
  <h2 class="rv">De tus datos a tu perfil <em>en cinco pasos.</em></h2>
  <div class="pasos cinco" data-escalona>
    <div class="paso"><span class="n">1</span><div><h3>Nos mandas tus datos</h3><p>Con el formulario de abajo, en un minuto.</p></div></div>
    <div class="paso"><span class="n">2</span><div><h3>Revisamos tu información</h3><p>Y tu cédula en la SEP, si nos la compartes.</p></div></div>
    <div class="paso"><span class="n">3</span><div><h3>Creamos tu perfil</h3><p>Nosotros lo armamos por ti.</p></div></div>
    <div class="paso"><span class="n">4</span><div><h3>Lo apruebas</h3><p>Te lo enseñamos antes de publicarlo.</p></div></div>
    <div class="paso"><span class="n">5</span><div><h3>Lo activamos</h3><p>Al recibir tu pago se publica en la guía.</p></div></div>
  </div>
</div></section>

<section class="marfil" style="padding-top:0"><div class="w">
  <span class="eti rv">Lo que nos hace distintos</span>
  <h2 class="rv">Escuchamos lo que los profesionales <em>odian</em> de otras plataformas.</h2>
  <div class="porque" data-escalona>
    <div><b>Sin contratos anuales</b><p>Otras plataformas amarran con contratos de un año. Aquí pagas mes a mes.</p></div>
    <div><b>Cancelar es fácil</b><p>Un mensaje de WhatsApp y listo. Sin llamadas de retención ni cargos después de cancelar.</p></div>
    <div><b>Precio protegido</b><p>Como socio fundador, tu precio se mantiene mientras sigas activo.</p></div>
    <div><b>Reseñas honestas</b><p>Tus reseñas viven en Google Maps, a la vista de todos.</p></div>
  </div>
</div></section>

<section class="oscuro" id="registro"><div class="w">
  <span class="eti rv">Registro</span>
  <h2 class="rv">Crea tu perfil <em>profesional.</em></h2>
  <p class="sub rv"><b>No pagas hasta revisar y aprobar tu perfil.</b> Llena tus datos y te escribimos por WhatsApp.</p>
  <form class="form rv" id="formRegistro">
    <div><label for="rNombre">Nombre o despacho</label><input id="rNombre" required autocomplete="name" placeholder="Lic. Nombre Apellido o despacho"></div>
    <div><label for="rCiudad">Ciudad</label><select id="rCiudad">{opciones_ciudad()}</select></div>
    <div><label>Especialidades</label><div class="opciones" id="rMaterias"></div></div>
    <div><label for="rWa">Tu WhatsApp</label><input id="rWa" required inputmode="tel" autocomplete="tel" placeholder="10 dígitos" pattern="[0-9 ]{{10,14}}"></div>
    <div><label for="rCedula">Cédula profesional (opcional)</label><input id="rCedula" inputmode="numeric" placeholder="Para verificarla en la SEP"></div>
    <div><label for="rPlan">Plan</label><select id="rPlan"><option value="premium">Premium · $399 alta + $149 MXN/mes</option><option value="basico">Básico · $99 alta + $49 MXN/mes</option></select></div>
    <label class="acepto"><input type="checkbox" required> Acepto el <a href="/aviso-de-privacidad/" target="_blank">aviso de privacidad</a> y que LicLink me contacte por WhatsApp.</label>
    <button class="btn btn-oro brilla" type="submit">{WA}Crear mi perfil profesional</button>
    <p class="fino">Solo publicamos tu perfil cuando tú lo apruebas.</p>
    <pre id="rAviso" hidden style="white-space:pre-wrap;font:14px/1.4 var(--sans);background:var(--marfil);padding:12px;border-radius:6px"></pre>
  </form>
</div></section>

<section class="marfil" id="preguntas"><div class="w">
  <span class="eti rv">Preguntas</span>
  <h2 class="rv">Antes de <em>registrarte.</em></h2>
  <div class="faq rv">{faq}</div>
</div></section>
</main>
{PIE}
""" + fin(False)


def datos_guia():
    """prospectos/guia.json: abogados que aceptaron aparecer, con su plan. Nadie aparece sin su permiso."""
    ruta = os.path.join(os.path.dirname(DATOS), "guia.json")
    g = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else []
    sal = []
    for a in g:
        if a.get("plan") not in ("basico", "premium"): continue
        x = dict(a)
        if a["plan"] != "premium":  # el Básico no lleva enlace propio, redes ni reseñas
            for k in ("pagina", "redes", "resena"): x.pop(k, None)
        sal.append(x)
    ciu = {k: v[0] for k, v in CIUDADES.items()}
    return ("window.GUIA = " + json.dumps(sal, ensure_ascii=False, separators=(",", ":")) + ";\n"
            "window.CIUDADES = " + json.dumps(ciu, ensure_ascii=False) + ";\n")

AVISO = [
 ("Quién es responsable de tus datos", ["LicLink, con sede en Oaxaca, México, es responsable del tratamiento de los datos personales que se recaban en este sitio. Puedes contactarnos por WhatsApp al 951 183 6468."]),
 ("Qué datos recabamos", ["De los abogados que se registran: nombre, despacho, ciudad, especialidades, número de WhatsApp y teléfono, correo, cédula profesional, fotografía o logotipo y enlaces a sus redes sociales.",
   "De las personas que usan la sección «¿No sabes qué abogado necesitas?»: lo que decidan escribirnos y su número de WhatsApp, que conocemos porque el mensaje llega a nuestro WhatsApp. No es necesario dar tu nombre. Te pedimos no compartir datos sensibles.",
   "Los mensajes que envías a un abogado desde su ficha o su perfil van directamente a su WhatsApp: LicLink no los recibe ni los guarda."]),
 ("Para qué los usamos", ["Finalidades necesarias: publicar y mantener los perfiles de los abogados, verificar su cédula en el Registro Nacional de Profesionistas de la SEP, contactarlos sobre su suscripción y cobros, y orientar a quien nos escribe para encontrar abogado.",
   "Finalidades secundarias: elaborar estadísticas generales de uso del sitio y avisar a los abogados sobre mejoras. Puedes pedirnos por WhatsApp que no usemos tus datos para estas finalidades."]),
 ("Con quién los compartimos", ["No vendemos datos personales. Los datos que un abogado autoriza para su perfil son públicos en el sitio. Usamos proveedores para operar el servicio, como el alojamiento del sitio (Cloudflare) y la mensajería (WhatsApp)."]),
 ("Tus derechos", ["Puedes acceder a tus datos, corregirlos, pedir que los eliminemos u oponerte a su uso (derechos ARCO), y retirar tu consentimiento, escribiéndonos por WhatsApp al 951 183 6468. Responderemos en un plazo máximo de 20 días hábiles."]),
 ("Cookies y estadísticas", ["Este sitio no usa cookies de publicidad. Podemos medir visitas de forma agregada y sin identificarte para mejorar el servicio y dar estadísticas a los abogados."]),
 ("Cambios a este aviso", ["Cualquier cambio se publicará en esta página. Última actualización: 7 de noviembre de 2026."]),
]
TERMINOS = [
 ("Qué es LicLink", ["LicLink es un directorio en línea que ayuda a las personas a encontrar y contactar abogados. LicLink no presta servicios legales, no da asesoría jurídica, no es parte de la relación entre el cliente y el abogado y no garantiza resultados jurídicos ni clientes."]),
 ("Para quien busca abogado", ["Usar LicLink es gratis. Los honorarios y condiciones se acuerdan directamente con cada abogado, quien es el único responsable de su servicio. Si estás en peligro inmediato, llama al 911."]),
 ("Verificación", ["«Cédula profesional verificada» significa que LicLink consultó la cédula del abogado en el Registro Nacional de Profesionistas de la SEP y que corresponde a la persona del perfil, en la fecha indicada. «Datos profesionales registrados» significa que el abogado autorizó su perfil y nos dio sus datos, pero aún no completamos esa revisión."]),
 ("Para abogados: perfil y publicación", ["El abogado garantiza que sus datos son verdaderos y que tiene derecho a ejercer. Solo publicamos un perfil cuando el abogado lo aprueba. Podemos retirar perfiles con información falsa o engañosa."]),
 ("Planes y pagos", ["Básico: alta única de $99 MXN y $49 MXN al mes. Premium: alta única de $399 MXN y $149 MXN al mes. La mensualidad se paga por adelantado. Si un pago no se recibe, el perfil se oculta hasta que se regularice.",
   "Socios fundadores: quienes se registren en la etapa de lanzamiento conservan su precio mientras su suscripción siga activa sin interrupción. Si cancelan y regresan después, aplica el precio vigente."]),
 ("Cancelación", ["Puedes cancelar cuando quieras con un mensaje de WhatsApp, sin penalización ni contrato forzoso. El perfil sigue visible hasta el final del mes pagado. El alta no es reembolsable una vez que el perfil fue publicado."]),
 ("Reseñas", ["Las reseñas de los abogados viven en Google Maps. LicLink no las escribe, no las edita y no las borra, y no paga ni premia a nadie por dejarlas."]),
 ("Contacto", ["Para dudas, cancelaciones o aclaraciones: WhatsApp 951 183 6468. Última actualización: 7 de noviembre de 2026."]),
]


def pagina_legal(titulo, ruta, secciones, intro):
    cuerpo = "".join(f"<h2>{e(h)}</h2>" + "".join(f"<p>{e(p)}</p>" for p in ps) for h, ps in secciones)
    return cabeza(f"{titulo} | LicLink", intro, ruta) + f"""<body>
{BARRA}
<main><section class="marfil"><div class="w legal-txt"><span class="eti">LicLink</span><h1>{e(titulo)}</h1><p>{e(intro)}</p>{cuerpo}</div></section></main>
{PIE}
""" + fin()


def sitemap(g):
    urls = ["/", "/para-abogados/", "/guias/", "/aviso-de-privacidad/", "/terminos/"] + [f"/guias/{x['slug']}/" for x in GUIAS]
    for c in CIUDADES:
        if any((a.get("ciudad") == c or c in a.get("otras_ciudades", [])) for a in g): urls.append(f"/abogados/{c}/")
        for m in MATERIAS:
            if any((a.get("ciudad") == c or c in a.get("otras_ciudades", [])) and m in a.get("materias", []) for a in g): urls.append(f"/abogados/{c}/{m}/")
    urls += [a["pagina"] for a in g if a["plan"] == "premium" and a.get("pagina")]
    hoy = __import__("datetime").date.today().isoformat()
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{URL_BASE}{u}</loc><lastmod>{hoy}</lastmod></url>\n" for u in urls) + "</urlset>\n"



from guias_legales import GUIAS, ACTUALIZADA


def guia_pagina(gd):
    def bloque(ps):
        out, lista = "", []
        for p in ps:
            if p.startswith("• "): lista.append(f"<li>{e(p[2:])}</li>")
            else:
                if lista: out += "<ul>" + "".join(lista) + "</ul>"; lista = []
                out += f"<p>{e(p)}</p>"
        if lista: out += "<ul>" + "".join(lista) + "</ul>"
        return out
    cuerpo = "".join(f"<h2>{e(h)}</h2>{bloque(ps)}" for h, ps in gd["secciones"])
    m = gd["materia"]; ruta = f"/guias/{gd['slug']}/"
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": gd["titulo"], "description": gd["desc"], "inLanguage": "es-MX",
          "dateModified": "2026-11-08", "publisher": {"@type": "Organization", "name": "LicLink", "url": URL_BASE + "/"}, "mainEntityOfPage": URL_BASE + ruta}
    ciudades = "".join(f'<a href="/abogados/{k}/{m}/">{v[0]}</a>' for k, v in CIUDADES.items() if k in PRINCIPALES)
    otras = "".join(f'<a class="g-otra" href="/guias/{x["slug"]}/"><b>{e(x["titulo"])}</b><span>Leer guía →</span></a>' for x in GUIAS if x["slug"] != gd["slug"])
    return cabeza(f"{gd['titulo']} | LicLink", gd["desc"], ruta, extra=jsonld(ld)) + f"""<body>
{BARRA}
<main><section class="marfil"><div class="w legal-txt guia-txt">
  <nav class="migas" aria-label="Estás en"><a href="/">Inicio</a> <span>›</span> <a href="/guias/">Guías legales</a></nav>
  <h1>{e(gd["titulo"])}</h1>
  <p class="g-resumen">{e(gd["resumen"])}</p>
  <p class="g-fecha">Información general · Actualizada el {ACTUALIZADA}</p>
  {cuerpo}
  <div class="g-cta"><b>¿Necesitas ayuda con tu caso?</b><p>Encuentra {e(PLURAL[m].lower())} y escríbeles directo por WhatsApp.</p><div class="atajos">{ciudades}</div></div>
  <p class="g-aviso">Esta guía es información general y no sustituye la asesoría de un abogado. Cada caso es distinto: los plazos y requisitos pueden cambiar según tu estado y tu situación.</p>
  <h2>Otras guías</h2><div class="g-otras">{otras}</div>
</div></section></main>
{PIE}
""" + fin()


def guias_indice():
    tarjetas = "".join(f'<a class="g-card" href="/guias/{x["slug"]}/"><span class="eti">{e(MATERIAS[x["materia"]][0])}</span><b>{e(x["titulo"])}</b><p>{e(x["resumen"])}</p><span class="g-leer">Leer guía →</span></a>' for x in GUIAS)
    return cabeza("Guías legales en palabras sencillas | LicLink", "Qué hacer si detienen a un familiar, si te despiden, cómo pedir pensión alimenticia y más. Información general gratuita.", "/guias/") + f"""<body>
{BARRA}
<main><section class="encabezado"><div class="w">
  <nav class="migas" aria-label="Estás en"><a href="/">Inicio</a> <span>›</span> <b>Guías legales</b></nav>
  <h1>Guías legales <em>en palabras sencillas.</em></h1>
  <p class="sub">Información general y gratuita para entender tu situación antes de hablar con un abogado.</p>
</div></section>
<section class="marfil" style="padding-top:0"><div class="w"><div class="g-grid">{tarjetas}</div></div></section></main>
{PIE}
""" + fin()


def pagina_404():
    return cabeza("Página no encontrada | LicLink", "Esta página no existe.", "/404", '<meta name="robots" content="noindex">\n') + f"""<body>
{BARRA}
<main><section class="portada"><div class="w" style="text-align:center;max-width:640px">
  <span class="eti">Error 404</span>
  <h1 style="font-size:clamp(30px,8vw,52px)">Esta página <em>no existe.</em></h1>
  <p class="sub" style="margin:14px auto 26px">Puede que el enlace esté mal escrito o que el perfil ya no esté activo. Busca abogado desde aquí:</p>
  <div style="display:grid;gap:10px;max-width:420px;margin:0 auto"><a class="btn btn-oro" href="/">Buscar abogados</a><a class="btn btn-linea" href="/guias/">Ver guías legales</a></div>
</div></section></main>
{PIE}
""" + fin()


def escribir(ruta, txt):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    open(ruta, "w", encoding="utf-8").write(txt)


def main():
    escribir(os.path.join(PUBLICO, "assets", "guia-datos.js"), datos_guia())
    escribir(os.path.join(PUBLICO, "index.html"), portada())
    escribir(os.path.join(PUBLICO, "para-abogados", "index.html"), para_abogados())
    g = cargar_guia()
    for c in CIUDADES:
        escribir(os.path.join(PUBLICO, "abogados", c, "index.html"), listado(c, "", g))
        for m in MATERIAS:
            escribir(os.path.join(PUBLICO, "abogados", c, m, "index.html"), listado(c, m, g))
    escribir(os.path.join(PUBLICO, "guias", "index.html"), guias_indice())
    for gd in GUIAS: escribir(os.path.join(PUBLICO, "guias", gd["slug"], "index.html"), guia_pagina(gd))
    escribir(os.path.join(PUBLICO, "404.html"), pagina_404())
    escribir(os.path.join(PUBLICO, "manifest.webmanifest"), json.dumps({"name": "LicLink · Guía de abogados", "short_name": "LicLink", "start_url": "/", "display": "standalone",
        "background_color": "#faf6ef", "theme_color": "#1a1814", "lang": "es-MX",
        "icons": [{"src": "/assets/icono-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icono-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False))
    escribir(os.path.join(PUBLICO, "aviso-de-privacidad", "index.html"), pagina_legal("Aviso de privacidad", "/aviso-de-privacidad/", AVISO, "Cómo cuidamos los datos personales de abogados y visitantes."))
    escribir(os.path.join(PUBLICO, "terminos", "index.html"), pagina_legal("Términos y condiciones", "/terminos/", TERMINOS, "Reglas de uso de LicLink, suscripciones, cancelación y verificación profesional."))
    g = cargar_guia()
    escribir(os.path.join(PUBLICO, "sitemap.xml"), sitemap(g))
    escribir(os.path.join(PUBLICO, "robots.txt"), f"User-agent: *\nAllow: /\nSitemap: {URL_BASE}/sitemap.xml\n")
    filas = ["| Abogado | Plan | Ciudad | Alta | Vence | Pago | Estado | Cédula verificada |", "|---|---|---|---|---|---|---|---|"]
    todos_g = json.load(open(os.path.join(os.path.dirname(DATOS), "guia.json"), encoding="utf-8"))
    for a in sorted(todos_g, key=lambda x: (x.get("plan") != "premium", x["nombre"])):
        filas.append(f"| {a['nombre']} | {a.get('plan','')} | {CIUDADES.get(a.get('ciudad'), ('',))[0]} | {a.get('alta','')} | {a.get('vence','') or '—'} | {a.get('pago','')} | {a.get('estado','')} | {a.get('verificada_fecha') or 'no'} |")
    escribir(os.path.join(os.path.dirname(DATOS), "CLIENTES.md"), "# Clientes de la guía LicLink\n\nSe genera solo desde prospectos/guia.json (campos: plan, alta, vence, pago, estado, verificada, verificada_fecha).\n\n" + "\n".join(filas) + "\n")
    print("Guía lista:", len(CIUDADES), "ciudades ×", len(MATERIAS), "materias · en sitemap:", sitemap(g).count("<url>"))


if __name__ == "__main__":
    main()
