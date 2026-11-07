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
from generar import DATOS, PUBLICO, URL_BASE, area, slugify

CIUDADES = {"cdmx": ("Ciudad de México", "CDMX"), "edomex": ("Estado de México", "Edomex"),
            "guadalajara": ("Guadalajara", "Jalisco"), "puebla": ("Puebla", "Puebla"),
            "monterrey": ("Monterrey", "Nuevo León"), "tijuana": ("Tijuana", "Baja California"), "leon": ("León", "Guanajuato"),
            "chihuahua": ("Chihuahua", "Chihuahua"), "san-luis-potosi": ("San Luis Potosí", "SLP"), "los-cabos": ("Los Cabos", "Baja California Sur"),
            "yucatan": ("Yucatán", "Yucatán")}
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
}
PLURAL = {"penal": "Abogados penalistas", "familiar": "Abogados familiares", "laboral": "Abogados laborales", "civil": "Abogados civiles",
          "mercantil": "Abogados mercantiles", "sucesiones": "Abogados de herencias", "amparo": "Abogados de amparo", "fiscal": "Abogados fiscalistas"}
ICONOS = {
    "penal": '<path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "familiar": '<circle cx="8" cy="7" r="2.5"/><circle cx="16.5" cy="8.5" r="2"/><path d="M3.5 20v-4a4.5 4.5 0 019 0v4M13 20v-3a3.5 3.5 0 017 0v3"/>',
    "laboral": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M3 13h18"/>',
    "civil": '<path d="M3 11l9-7 9 7v9a1 1 0 01-1 1h-5v-6H9v6H4a1 1 0 01-1-1z"/>',
    "mercantil": '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.8"/><path d="M6 9.5v5M18 9.5v5"/>',
    "sucesiones": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    "amparo": '<path d="M12 4v16M7 20h10M5 7h14M5 7l-3 6a3 3 0 006 0zM19 7l-3 6a3 3 0 006 0z"/>',
    "fiscal": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
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
<symbol id="i-web" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></g></symbol>
""" + "".join(f'<symbol id="m-{k}" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{v}</g></symbol>' for k, v in ICONOS.items()) + "</svg>"

e = H.escape
OK = '<svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>'
NO = '<svg viewBox="0 0 24 24"><use href="#i-no"/></svg>'
WA = '<svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>'


def cabeza(titulo, desc, ruta, robots=""):
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
<meta property="og:url" content="{url}"><meta property="og:image" content="{URL_BASE}/assets/liclink-compartir.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0c0b0a">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230c0b0a'/%3E%3Ctext x='32' y='44' font-family='Arial' font-weight='800' font-size='36' text-anchor='middle' fill='%23d4b06a'%3EL%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/guia.css">
</head>
"""


BARRA = """<header class="barra"><div class="w">
  <a href="/" class="marca" aria-label="LicLink, inicio">Lic<i>Link</i></a>
  <nav><a class="txt" href="/#materias">Materias</a><a class="txt" href="/#ciudades">Ciudades</a>
  <a class="btn btn-linea btn-chico" href="/para-abogados/">Soy abogado</a></nav>
</div></header>"""

PIE = """<footer class="pie"><div class="w">
  <div class="cols">
    <div><a href="/" class="marca" style="color:var(--claro)">Lic<i>Link</i></a><p style="margin-top:12px;max-width:340px">La guía de abogados de México. Encuentra, compara y habla directo con tu abogado.</p></div>
    <div><b>Ciudades</b><ul>""" + "".join(f'<li><a href="/abogados/{k}/">{v[0]}</a></li>' for k, v in CIUDADES.items()) + """</ul></div>
    <div><b>Materias</b><ul>""" + "".join(f'<li><a href="/abogados/cdmx/{k}/">{v[0]}</a></li>' for k, v in list(MATERIAS.items())[:6]) + """</ul></div>
    <div><b>Abogados</b><ul><li><a href="/para-abogados/">Planes y precios</a></li><li><a href="/para-abogados/#registro">Registrarme</a></li><li><a href="/para-abogados/#preguntas">Preguntas</a></li></ul></div>
  </div>
  <p class="legal">LicLink es un directorio: no presta servicios legales ni cobra comisiones por los casos. Cada abogado es responsable de su servicio. Verificamos la cédula de los perfiles con sello en el Registro Nacional de Profesionistas de la SEP. Si estás en peligro inmediato, llama al 911.<br>© LicLink 2026</p>
</div></footer>"""


def fin():
    return SIMBOLOS + '\n<script src="/assets/guia-datos.js" defer></script>\n<script src="/assets/guia.js" defer></script>\n</body>\n</html>\n'


def opciones_ciudad(sel="cdmx"):
    return "".join(f'<option value="{k}"{" selected" if k == sel else ""}>{v[0]}</option>' for k, v in CIUDADES.items())


def planes_html(corto=False):
    basico_si = ["Ficha profesional en la guía de tu ciudad", "Foto o logo, nombre y materias", "Botón de WhatsApp y llamada directa", "Sello de cédula verificada"]
    basico_no = ["Página propia con tu enlace", "Redes sociales y sitio web", "Reseñas en Google Maps", "Aparecer primero"]
    prem = ["Todo lo del Básico, y además:", "Apareces primero en tu ciudad y materias, con sello Premium", "Tu página profesional propia: liclink.mx/tu-nombre",
            "Enlaces a todas tus redes y tu sitio web", "Botón para que tus clientes te dejen reseña en Google Maps", "Asistente que ordena cada caso antes de llegar a tu WhatsApp",
            "Mapa, horario, promociones y paquetes", "Reporte mensual: cuántos te vieron y cuántos te escribieron", "Imagen para compartir y código QR para tu tarjeta"]
    li = lambda t, s=True: f'<li{"" if s else " class=no"}>{OK if s else NO}<span>{e(t)}</span></li>'
    boton = (lambda p, t: f'<a class="btn {"btn-oro brilla" if p == "premium" else "btn-linea"} btn-ancho" href="/para-abogados/#registro" data-plan="{p}">{t}</a>')
    return f"""<div class="planes" data-escalona>
  <div class="plan"><h3>Básico</h3><p class="para">Para que te encuentren y te escriban.</p>
    <div class="precio"><b>$49</b><span>al mes</span></div><p class="alta">Alta única de $99</p>
    <ul>{"".join(li(t) for t in basico_si)}{"".join(li(t, False) for t in basico_no)}</ul>{boton("basico", "Quiero el Básico")}</div>
  <div class="plan prem"><span class="cinta">Recomendado</span><h3>Premium</h3><p class="para">Para destacar y ganar más clientes que tu competencia.</p>
    <div class="precio"><b>$149</b><span>al mes</span></div><p class="alta">Alta única de $399</p>
    <ul><li class="lead">{e(prem[0])}</li>{"".join(li(t) for t in prem[1:])}</ul>{boton("premium", "Quiero el Premium")}</div>
</div>
<ul class="garantias">
  <li>{OK}Sin contrato forzoso: pagas mes a mes</li>
  <li>{OK}Cancelas cuando quieras con un mensaje de WhatsApp</li>
  <li>{OK}Sin cargos sorpresa ni aumentos sin aviso</li>
  <li>{OK}Cero comisiones: el cliente te paga directo a ti</li>
  <li>{OK}Te atiende una persona, no un robot</li>
</ul>"""


def portada():
    atajos = [("penal", "Detuvieron a un familiar"), ("laboral", "Me despidieron"), ("familiar", "Quiero divorciarme"), ("mercantil", "Me deben dinero"), ("familiar", "Pensión para mis hijos"), ("sucesiones", "Una herencia")]
    mats = "".join(f'<a class="materia" href="/abogados/cdmx/{k}/" data-m="{k}"><span class="ic"><svg viewBox="0 0 24 24"><use href="#m-{k}"/></svg></span><b>{v[0]}</b><small>{v[1]}</small></a>' for k, v in MATERIAS.items())
    ciuds = "".join(f'<a class="ciudad" href="/abogados/{k}/" style="--fondo-c:{FONDOS[k]}"><span class="flecha"><svg width="18" height="18" viewBox="0 0 24 24"><use href="#i-flecha"/></svg></span><b>{v[0]}</b><small><svg width="15" height="15" viewBox="0 0 24 24"><use href="#i-pin"/></svg>Ver abogados</small></a>' for k, v in CIUDADES.items() if k in PRINCIPALES)
    otras = "".join(f'<a href="/abogados/{k}/">{v[0]}</a>' for k, v in CIUDADES.items() if k not in PRINCIPALES)
    preguntas = [
        ("¿Cuánto me cuesta usar LicLink?", "Nada. Buscar y escribirle a un abogado es gratis. Tú acuerdas sus honorarios directamente con él."),
        ("¿Cómo sé que es abogado de verdad?", "Los perfiles con sello de cédula verificada fueron revisados por nosotros en el Registro Nacional de Profesionistas de la SEP. Tú también puedes consultarla ahí."),
        ("¿LicLink cobra comisión por mi caso?", "No. Hablas directo con el abogado por WhatsApp o por teléfono, sin intermediarios."),
        ("¿Qué pasa con lo que le cuento al abogado?", "Tu mensaje va directo a su WhatsApp. LicLink no guarda ni lee tu caso."),
        ("¿Las reseñas son reales?", "Las reseñas están en Google Maps, a la vista de todos. Nosotros no las escribimos, no las editamos ni las borramos."),
    ]
    faq = "".join(f"<details><summary>{e(p)}</summary><p>{e(r)}</p></details>" for p, r in preguntas)
    titulo = "LicLink · Encuentra abogado en CDMX, Edomex, Guadalajara, Puebla y más"
    desc = "La guía de abogados de México. Busca por ciudad y materia, revisa su perfil y escríbele directo por WhatsApp. Gratis."
    return cabeza(titulo, desc, "/") + f"""<body>
{BARRA}
<main>
<section class="portada"><div class="w">
  <span class="eti entra" style="--d:.05s">Guía de abogados de México</span>
  <h1><span class="l"><span style="--i:0">Tu problema legal</span></span><span class="l"><span style="--i:1"><em>tiene solución.</em></span></span></h1>
  <p class="sub entra" style="--d:.6s">Encuentra abogados en tu ciudad, revisa su perfil y escríbeles directo por WhatsApp. Gratis para ti.</p>
  <form class="buscador entra" id="buscar" style="--d:.75s" role="search">
    <div class="campo"><svg viewBox="0 0 24 24"><use href="#i-pin"/></svg><div><label for="bCiudad">¿Dónde?</label><select id="bCiudad">{opciones_ciudad()}</select></div></div>
    <div class="campo"><svg viewBox="0 0 24 24"><use href="#i-lupa"/></svg><div><label for="bMateria">¿Qué necesitas?</label><select id="bMateria"><option value="">Todas las materias</option>{"".join(f'<option value="{k}">{v[0]} · {v[1]}</option>' for k, v in MATERIAS.items())}</select></div></div>
    <button class="btn btn-oro brilla" type="submit"><svg viewBox="0 0 24 24"><use href="#i-lupa"/></svg>Buscar abogado</button>
  </form>
  <div class="atajos entra" style="--d:.9s">{"".join(f'<a href="#" data-atajo="{k}">{e(t)}</a>' for k, t in atajos)}</div>
  <ul class="confianza entra" style="--d:1s">
    <li><svg viewBox="0 0 24 24"><use href="#i-sello"/></svg>Sello de cédula verificada en la SEP</li>
    <li><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>Contacto directo por WhatsApp</li>
    <li><svg viewBox="0 0 24 24"><use href="#i-candado"/></svg>Gratis y confidencial para ti</li>
  </ul>
  <form class="pregunta entra" id="pregunta" style="--d:1.1s">
    <h2>Pregúntale gratis a un abogado</h2>
    <p>Escribe tu duda y un abogado de LicLink te responde por WhatsApp. Sin compromiso.</p>
    <label class="oculto" for="pTexto">Tu pregunta</label>
    <textarea id="pTexto" required maxlength="600" placeholder="Ej. Me despidieron sin darme finiquito, ¿qué puedo hacer?"></textarea>
    <div class="fila"><select id="pCiudad" aria-label="Tu ciudad">{opciones_ciudad()}</select><button class="btn btn-oro" type="submit">{WA}Enviar mi pregunta</button></div>
    <small>Tu pregunta es confidencial. No publicamos tu nombre.</small>
  </form>
</div></section>

<section class="marfil" style="padding:44px 0 20px"><div class="w">
  <span class="eti rv">Abogados en LicLink</span>
  <h2 class="rv">Conoce a algunos de <em>nuestros abogados.</em></h2>
  <div class="destacados" id="destacados"></div>
</div></section>

<div class="historia-caja historia oscuro"><section style="background:none"><div class="w historia-grid">
  <div class="rv h-txt">
    <span class="eti">Así funciona</span>
    <h2>De la angustia a la <em>tranquilidad</em>, en minutos.</h2>
    <p class="sub">Un problema legal llega sin avisar, muchas veces de noche. Con LicLink encuentras a un abogado verificado cerca de ti y le escribes en ese momento.</p>

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
    <div class="paso"><span class="n">2</span><div><h3>Compara</h3><p>Revisa su cédula, sus materias, sus reseñas en Google y dónde está su despacho.</p></div></div>
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
  <span class="eti rv">Por qué LicLink</span>
  <h2 class="rv">Confianza antes de <em>contratar.</em></h2>
  <div class="porque" data-escalona>
    <div><b>Cédula verificada</b><p>Revisamos la cédula profesional en la SEP. Adiós a los coyotes y a los falsos abogados.</p></div>
    <div><b>Directo con el abogado</b><p>Le escribes a su WhatsApp. Sin centros de llamadas ni intermediarios.</p></div>
    <div><b>Reseñas públicas</b><p>Las opiniones están en Google Maps, donde nadie las puede maquillar.</p></div>
    <div><b>Gratis para ti</b><p>No pagas por buscar ni por escribir. Los honorarios los acuerdas con tu abogado.</p></div>
  </div>
</div></section>

<section class="abogados oscuro" id="abogados"><div class="w">
  <span class="eti rv">Para abogados</span>
  <h2 class="rv">Clientes que te buscan, <em>hoy.</em></h2>
  <p class="sub rv">Aparece en la guía de tu ciudad y recibe a tus clientes directo en tu WhatsApp. Precio de lanzamiento para los primeros despachos.</p>
  {planes_html()}
</div></section>

<section class="marfil"><div class="w">
  <span class="eti rv">Preguntas frecuentes</span>
  <h2 class="rv">Lo que más nos <em>preguntan.</em></h2>
  <div class="faq rv">{faq}</div>
</div></section>

<section class="cierre oscuro"><div class="w">
  <h2 class="rv">Actuar a tiempo hace <em>la diferencia.</em></h2>
  <div class="acciones rv"><a class="btn btn-oro brilla" href="#buscar" onclick="setTimeout(function(){{document.getElementById('bCiudad').focus()}},500)"><svg viewBox="0 0 24 24"><use href="#i-lupa"/></svg>Buscar abogado</a>
  <a class="btn btn-linea" href="/para-abogados/">Soy abogado: quiero aparecer</a></div>
</div></section>
</main>
{PIE}
""" + fin()


def listado(c, m=""):
    nc = CIUDADES[c][0]
    if m:
        nm, desc_m, busq = MATERIAS[m]
        titulo = f"{PLURAL[m]} en {nc} | LicLink"
        desc = f"Encuentra {busq} en {nc}. {desc_m}. Revisa su perfil y escríbele directo por WhatsApp, gratis."
        pl = PLURAL[m].split(" ", 1)
        h1 = f'{pl[0]} <em>{e(pl[1])}</em> en {e(nc)}'
        ruta = f"/abogados/{c}/{m}/"
    else:
        titulo = f"Abogados en {nc} | LicLink"
        desc = f"Abogados en {nc}: penal, familiar, laboral, civil, mercantil y más. Revisa su cédula y escríbeles directo por WhatsApp."
        h1 = f'Abogados en <em>{e(nc)}</em>'
        ruta = f"/abogados/{c}/"
    return cabeza(titulo, desc, ruta) + f"""<body data-ciudad="{c}" data-materia="{m}" data-plural="{PLURAL.get(m, "abogados").lower()}">
{BARRA}
<main>
<section class="encabezado"><div class="w">
  <span class="eti">{e(nc)}</span>
  <h1>{h1}</h1>
  <p class="sub">Revisa su perfil y escríbeles directo por WhatsApp, sin costo para ti.</p>
  <nav class="filtros" id="filtros" aria-label="Materias"></nav>
</div></section>
<section class="marfil" style="padding-top:0"><div class="w"><div class="lista" id="lista"></div></div></section>
</main>
{PIE}
""" + fin()


def para_abogados():
    preguntas = [
        ("¿Hay contrato forzoso?", "No. Pagas mes a mes y cancelas cuando quieras con un mensaje de WhatsApp. Sin penalizaciones."),
        ("¿Cuánto tardan en publicar mi perfil?", "Entre 24 y 48 horas después de recibir tus datos y verificar tu cédula."),
        ("¿Por qué piden mi cédula?", "Porque el sello de cédula verificada es lo que hace que los clientes confíen en ti y no en un coyote. La revisamos en el Registro Nacional de Profesionistas de la SEP."),
        ("¿Cobran comisión por los clientes?", "No. El cliente te escribe a ti y te paga a ti. Nosotros solo cobramos tu plan."),
        ("¿Cómo funcionan las reseñas en Google?", "En Premium ponemos en tu perfil un botón para que tus clientes te dejen reseña en tu ficha de Google Maps. Más reseñas te ayudan a aparecer más arriba en Google. Si aún no tienes ficha en Google Maps, te ayudamos a crearla."),
        ("¿Puedo cambiar de plan?", "Sí, cuando quieras. Si subes a Premium solo pagas la diferencia del alta."),
        ("¿Mis datos aparecen sin mi permiso?", "Nunca. En LicLink solo aparecen los abogados que se registran y aceptan."),
    ]
    faq = "".join(f"<details><summary>{e(p)}</summary><p>{e(r)}</p></details>" for p, r in preguntas)
    ej_b = f"""<article class="ficha"><div class="foto">MR</div><div><h3>Lic. María Rodríguez</h3><div class="rol">Abogada familiar · Puebla</div>
      <span class="ver"><svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>Cédula verificada</span><div class="tags"><span>Familiar</span><span>Herencias</span></div></div>
      <div class="acc"><span class="btn btn-wa">{WA}WhatsApp</span><span class="btn btn-linea">Llamar</span></div></article>"""
    ej_p = f"""<article class="ficha prem"><div class="foto">JH</div><div><span class="sello-p">Premium</span><h3>Lic. Jorge Hernández</h3><div class="rol">Penalista · CDMX</div>
      <span class="ver"><svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>Cédula verificada</span>
      <div class="redes"><svg viewBox="0 0 24 24"><use href="#i-facebook"/></svg><svg viewBox="0 0 24 24"><use href="#i-instagram"/></svg><svg viewBox="0 0 24 24"><use href="#i-tiktok"/></svg><svg viewBox="0 0 24 24"><use href="#i-web"/></svg></div>
      <div class="tags"><span>Penal</span><span>Amparo</span></div></div>
      <div class="acc"><span class="btn btn-negro uno">Ver perfil completo</span><span class="btn btn-wa">{WA}WhatsApp</span><span class="btn btn-linea">Llamar</span><span class="btn btn-linea uno">★ Ver y dejar reseñas en Google</span></div></article>"""
    titulo = "Aparece en LicLink · La guía de abogados verificados"
    desc = "Recibe clientes directo en tu WhatsApp. Plan Básico desde $49 al mes. Sin contrato forzoso y sin comisiones."
    return cabeza(titulo, desc, "/para-abogados/") + f"""<body>
{BARRA}
<main>
<section class="portada"><div class="w">
  <span class="eti entra" style="--d:.05s">Para abogados</span>
  <h1><span class="l"><span style="--i:0">Clientes que</span></span><span class="l"><span style="--i:1">te buscan,</span></span><span class="l"><span style="--i:2"><em>hoy.</em></span></span></h1>
  <p class="sub entra" style="--d:.6s">La gente con un problema legal ya no pregunta en Facebook: busca en su celular y le escribe al primer abogado que le da confianza. Haz que ese abogado seas tú.</p>
  <div class="acciones entra" style="--d:.8s;display:grid;gap:10px;margin-top:26px;max-width:420px"><a class="btn btn-oro brilla" href="#registro">Registrarme ahora</a><a class="btn btn-linea" href="#planes">Ver planes</a></div>
</div></section>

<section class="abogados oscuro" id="planes"><div class="w">
  <span class="eti rv">Planes</span>
  <h2 class="rv">Dos planes. <em>Sin letras chiquitas.</em></h2>
  {planes_html()}
</div></section>

<section class="oscuro" style="padding-top:0"><div class="w">
  <span class="eti rv">Así te ven tus clientes</span>
  <h2 class="rv">La diferencia <em>se nota.</em></h2>
  <div class="muestra-fichas" data-escalona>{ej_b}{ej_p}</div>
  <p class="ilustrativa" style="text-align:left">Fichas de ejemplo con datos inventados.</p>
</div></section>

<section class="marfil"><div class="w">
  <span class="eti rv">Lo que nos hace distintos</span>
  <h2 class="rv">Escuchamos lo que los profesionales <em>odian</em> de otras plataformas.</h2>
  <div class="porque" data-escalona>
    <div><b>Sin contratos anuales</b><p>Otras plataformas amarran con contratos de un año y cobran aunque quieras irte. Aquí es mes a mes.</p></div>
    <div><b>Cancelar es fácil</b><p>Un mensaje de WhatsApp y listo. Sin llamadas de retención ni cargos después de cancelar.</p></div>
    <div><b>Precio que no se dispara</b><p>Si entras como fundador, tu precio se queda igual mientras sigas con nosotros.</p></div>
    <div><b>Reseñas honestas</b><p>No escondemos opiniones: tus reseñas viven en Google Maps y te suben en Google.</p></div>
  </div>
</div></section>

<section class="oscuro" id="registro"><div class="w">
  <span class="eti rv">Registro</span>
  <h2 class="rv">Aparece en la guía <em>en 48 horas.</em></h2>
  <p class="sub rv">Llena tus datos y te escribimos por WhatsApp para confirmar tu cédula y tu plan. No pagas nada hasta ver tu perfil listo.</p>
  <form class="form rv" id="formRegistro">
    <div><label for="rNombre">Nombre completo</label><input id="rNombre" required autocomplete="name" placeholder="Lic. Nombre Apellido"></div>
    <div><label for="rDespacho">Despacho (opcional)</label><input id="rDespacho" placeholder="Nombre del despacho"></div>
    <div><label for="rCiudad">Ciudad</label><select id="rCiudad">{opciones_ciudad()}</select></div>
    <div><label>Materias</label><div class="opciones" id="rMaterias"></div></div>
    <div><label for="rWa">Tu WhatsApp</label><input id="rWa" required inputmode="tel" autocomplete="tel" placeholder="10 dígitos"></div>
    <div><label for="rCedula">Cédula profesional</label><input id="rCedula" inputmode="numeric" placeholder="Para el sello de verificación"></div>
    <div><label for="rPlan">Plan</label><select id="rPlan"><option value="premium">Premium · $399 alta + $149/mes</option><option value="basico">Básico · $99 alta + $49/mes</option></select></div>
    <button class="btn btn-oro brilla" type="submit">{WA}Enviar por WhatsApp</button>
    <p class="fino">Al enviar aceptas que te contactemos por WhatsApp. Solo publicamos tu perfil cuando tú lo apruebas.</p>
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
""" + fin()


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


def escribir(ruta, txt):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    open(ruta, "w", encoding="utf-8").write(txt)


def main():
    escribir(os.path.join(PUBLICO, "index.html"), portada())
    escribir(os.path.join(PUBLICO, "para-abogados", "index.html"), para_abogados())
    for c in CIUDADES:
        escribir(os.path.join(PUBLICO, "abogados", c, "index.html"), listado(c))
        for m in MATERIAS:
            escribir(os.path.join(PUBLICO, "abogados", c, m, "index.html"), listado(c, m))
    escribir(os.path.join(PUBLICO, "assets", "guia-datos.js"), datos_guia())
    print("Guía lista:", len(CIUDADES), "ciudades ×", len(MATERIAS), "materias")


if __name__ == "__main__":
    main()
