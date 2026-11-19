"""Perfil v3 (landing de cada abogado) — PRUEBA. Genera public/nuevo/<slug>/index.html.
Uso: python3 herramientas/v3.py <slug> [<slug> ...]   (o "todos")
"""
import html, json, pathlib, re, sys, urllib.parse

RAIZ = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
datos = json.loads((RAIZ / "prospectos" / "abogados.json").read_text(encoding="utf-8"))
guia = {g["slug"]: g for g in json.loads((RAIZ / "prospectos" / "guia.json").read_text(encoding="utf-8"))}

I = {
 "ok": '<path d="M20 6 9 17l-5-5"/>',
 "esc": '<path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="m9 12 2 2 4-4"/>',
 "tel": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "comp": '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M16 6l-4-4-4 4"/><path d="M12 2v13"/>',
 "fl": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "mas": '<path d="M12 5v14M5 12h14"/>',
 "reloj": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "red": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 "atras": '<path d="M15 18l-6-6 6-6"/>',
}
WA = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-3.3-.8-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.6 2.1 1.1 1 2.1 1.3 2.4 1.4.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 .9c.3.1.5.2.5.3.1.1.1.6-.1 1.2z"/></svg>'


def ic(n, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24">{I[n]}</svg>'


def tel(n):
    n = re.sub(r"\D", "", n)
    if len(n) == 10 and n[:2] in ("55", "56", "33", "81"): return f"{n[:2]} {n[2:6]} {n[6:]}"
    return f"{n[:3]} {n[3:6]} {n[6:]}" if len(n) == 10 else n


def construir(a):
    s = a["slug"]; g = guia.get(s, {})
    wa_num = g.get("whatsapp") or ("52" + re.sub(r"\D", "", a.get("telefono", "")))
    def wa(msg): return "https://wa.me/" + wa_num + "?text=" + urllib.parse.quote("Hola, lo encontré en LicLink. " + msg)
    tiene_foto = (not a.get("logo")) and a.get("foto") and (RAIZ / "public" / s / a["foto"]).exists()
    img = f"/{s}/{a['foto']}" if tiene_foto else f"/{s}/{a.get('imagen_vista') or 'logo.jpg'}"
    avatar = f"/{s}/{a.get('imagen_vista') or a.get('foto')}" if (RAIZ / "public" / s / (a.get("imagen_vista") or "x")).exists() else img
    nombre = re.sub(r"^(Lic\.|Licda\.|Mtra\.|Mtro\.)\s*", "", a["nombre"])
    partes = nombre.split()
    h1 = (E(" ".join(partes[:-1])) + f"<span>{E(partes[-1])}</span>") if len(partes) > 1 else E(nombre)
    titulo_ab = "Abogada" if re.search(r"\b(Abogada|Licda|Mtra)\b", a["nombre"] + " " + a.get("despacho", "") + " " + a.get("despacho_largo", "")) else ("Abogado" if a["nombre"].startswith("Lic") else "Despacho jurídico")
    materias = [re.sub(r"^Derecho\s+", "", x["nombre"]).capitalize() for x in a.get("areas", [])]
    ciudad = a.get("ciudad", "")
    cons = a.get("consultas", [])
    gratis = [c for c in cons if not c.get("precio")]
    if gratis: consulta_txt = "1ª asesoría gratis"
    elif cons: consulta_txt = f"Desde ${min(c['precio'] for c in cons):,}"
    else: consulta_txt = "Pregunta sin compromiso"
    h24 = all(v == ["00:00", "23:59"] for v in a.get("horario", {}).values()) and a.get("horario")

    # Tu caso
    casos = "".join(
        f'<a class="caso{" urg" if c.get("urgente") else ""} rv d{min(i,4)}" target="_blank" rel="noopener" href="{E(wa(c["texto"].rstrip(".") + ". ¿Me puede orientar?"))}">'
        f'<span class="n">{i+1:02d}</span><p>{E(c["texto"])}<small>{"Urgente · escríbele ahora" if c.get("urgente") else "Escríbele por WhatsApp"}</small></p>{ic("fl","i fl")}</a>'
        for i, c in enumerate(a.get("situaciones", [])))
    serv = "".join(
        f'<div class="sv{" ab" if i == 0 else ""} rv"><button aria-expanded="{"true" if i == 0 else "false"}"><span class="num">{i+1:02d}</span><h3>{E(x["nombre"])}</h3><span class="mas">{ic("mas")}</span></button>'
        f'<div class="det"><div><p>{E(x.get("texto",""))}</p><ul>{"".join(f"<li>{E(p)}</li>" for p in x.get("puntos", []))}</ul></div></div></div>'
        for i, x in enumerate(a.get("areas", [])))
    if cons:
        precios = "".join(f'<div class="f"><span>{E(c["modo"])}</span><b class="{"" if c.get("precio") else "g"}">{"$%s" % format(c["precio"], ",") + (f" <small>/ {E(c["unidad"])}</small>" if c.get("unidad") else "") if c.get("precio") else "Gratis"}</b></div>' for c in cons)
        precios += '<p class="nota">Precios de referencia. El costo de tu asunto depende de cada caso.</p>'
    else:
        precios = f'<div class="pide"><b class="cs" style="font-size:24px">Cada caso es distinto.</b><span style="color:var(--gris)">Cuéntale tu situación por WhatsApp y te dice cuánto costaría, sin compromiso.</span><a class="btn btn-tinta" target="_blank" rel="noopener" href="{E(wa("¿Cuánto cuesta una consulta?"))}">Preguntar el costo</a></div>'
    valores = "".join(f'<span>{ic("ok")}{E(v)}</span>' for v in a.get("compromisos", [])[:6])
    contacto = f'<a class="ct rv" href="tel:{re.sub(r"[^0-9]","",a.get("telefono",""))}"><span class="ic">{ic("tel")}</span><span><small>Teléfono</small><b>{tel(a.get("telefono",""))}</b></span></a>'
    for t in a.get("telefonos_extra", []):
        contacto += f'<a class="ct rv" href="tel:{t["numero"]}"><span class="ic">{ic("tel")}</span><span><small>Otro número</small><b>{tel(t["numero"])}</b></span></a>'
    if a.get("direccion"):
        contacto += f'<a class="ct rv" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(a["direccion"])}"><span class="ic">{ic("pin")}</span><span><small>Dónde atiende</small><b>{E(a["direccion"])}</b></span></a>'
    if a.get("correo"):
        contacto += f'<a class="ct rv" href="mailto:{E(a["correo"])}"><span class="ic">{ic("mail")}</span><span><small>Correo</small><b>{E(a["correo"])}</b></span></a>'
    for red, url in (("Facebook", a.get("facebook")), ("Instagram", a.get("instagram"))):
        if url: contacto += f'<a class="ct rv" target="_blank" rel="noopener" href="{E(url)}"><span class="ic">{ic("red")}</span><span><small>{red}</small><b>Ver su página</b></span></a>'
    cinta = "".join(f"<span>{E(p)}</span>" for x in a.get("areas", []) for p in x.get("puntos", [])) or "".join(f"<span>{E(m)}</span>" for m in materias)
    cinta = cinta * 2
    guia_url = "/abogados/" + g["ciudad"] + "/" if g.get("ciudad") else "/"
    estado_ciudad = ciudad.split(",")[0]
    texto_intro = a.get("texto_portada") or a.get("descripcion", "")
    dato1 = " · ".join(materias[:3]) or a.get("titulo", "")
    bg_hero = f"background-image:url('{img}')" + ("" if tiene_foto else f";background-color:{a.get('fondo_logo','#15120e')}")

    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex"><meta name="theme-color" content="#15120e">
<title>{E(a.get("despacho_largo") or a["nombre"])} · LicLink</title>
<link rel="stylesheet" href="/assets/v3.css"><link rel="stylesheet" href="/assets/perfil3.css"></head>
<body>
<header class="top" id="top"><a class="ic" href="/nuevo/" aria-label="Volver">{ic("atras")}</a><a class="marca" href="/nuevo/">Lic<b>Link</b></a><button class="ic" id="bComp" aria-label="Compartir">{ic("comp")}</button></header>

<section class="hero"><div class="img{"" if tiene_foto else " logo"}" style="{bg_hero}"></div>
 <div class="txt intro">
  <div class="kick lt">{E(titulo_ab)} · {E(estado_ciudad)}</div>
  <h1 class="cs lt">{h1}</h1>
  <p class="lema lt">{E(a.get("frase") or a.get("titulo",""))}</p>
  <div class="verif lt">{ic("esc")}Perfil destacado en LicLink</div>
  <div class="acc lt"><a class="btn btn-oro" target="_blank" rel="noopener" href="{E(wa("Necesito asesoría."))}">{WA}Escribir por WhatsApp</a><a class="btn btn-linea" href="#caso">Cuéntale tu caso</a></div>
 </div><span class="baja"></span></section>
<div class="datos"><ul><li><small>Atiende</small><b>{E(dato1)}</b></li><li><small>Consulta</small><b>{E(consulta_txt)}</b></li><li><small>{"Horario" if h24 else "Dónde"}</small><b>{"24/7" if h24 else E(estado_ciudad)}</b></li></ul></div>
<div class="cinta" aria-hidden="true"><div>{cinta}</div></div>

<nav class="tabs" id="tabs"><div><a href="#sobre" class="on">Sobre {E("ella" if titulo_ab=="Abogada" else "él" if titulo_ab=="Abogado" else "el despacho")}</a><a href="#caso">Tu caso</a><a href="#servicios">Servicios</a><a href="#costos">Costos</a><a href="#contacto">Contacto</a></div></nav>

<div class="cuerpo"><div class="grid2"><main>
 <section class="cita sec" id="sobre"><div class="comillas rv">“</div><blockquote class="rv d1">{E(a.get("frase") or a.get("titulo",""))}</blockquote><p class="rv d2">{E(texto_intro)}</p>
  <div class="firma-c rv d3"><span class="av" style="background-image:url('{avatar}')"></span><span><b>{E(a["nombre"])}</b><small>{E(a.get("titulo",""))}</small></span></div>
  <div class="valores rv d3">{valores}</div></section>
 <section class="sec" id="caso"><div class="kick rv">Tu caso</div><h2 class="cs rv d1">¿Qué te <span>pasó?</span></h2><p class="baj rv d2">Toca tu situación y se abre WhatsApp con tu mensaje listo.</p><div class="casos">{casos}</div></section>
 <section class="sec" id="servicios"><div class="kick rv">Servicios</div><h2 class="cs rv d1">En qué te <span>puede ayudar.</span></h2><div class="serv">{serv}</div></section>
 <section class="sec" id="costos"><div class="kick rv">Costos</div><h2 class="cs rv d1">Sin <span>sorpresas.</span></h2><div class="precios rv d2">{precios}</div></section>
 <section class="sec"><div class="kick rv">Cómo funciona</div><h2 class="cs rv d1">Tres pasos, <span>cero vueltas.</span></h2><div class="pasos"><div class="paso rv"><b>Escríbele</b><p>Cuéntale tu situación por WhatsApp, con tus palabras.</p></div><div class="paso rv d1"><b>Te orienta</b><p>Te explica tus opciones y lo que necesitas.</p></div><div class="paso rv d2"><b>Defiende tu caso</b><p>Si decides avanzar, se encarga de todo el proceso.</p></div></div></section>
 <section class="sec" id="contacto"><div class="kick rv">Contacto</div><h2 class="cs rv d1">Hablemos <span>hoy.</span></h2><div class="contacto">{contacto}</div></section>
</main>
<aside class="lado"><span class="av" style="display:block;background-image:url('{avatar}')"></span><h3>{E(a["nombre"])}</h3><p>{E(dato1)} · {E(ciudad)}</p>
 <p style="display:flex;gap:8px;align-items:center;margin-top:12px;color:var(--tinta);font-weight:700"><span class="pulso"></span>Responde por WhatsApp</p>
 <a class="btn btn-oro" target="_blank" rel="noopener" href="{E(wa("Necesito asesoría."))}">{WA}Escribir por WhatsApp</a><a class="btn btn-linea" href="tel:{re.sub(r"[^0-9]","",a.get("telefono",""))}">Llamar · {tel(a.get("telefono",""))}</a>
 <div class="qr"><img src="/{s}/qr.png" alt="QR"><span>Escanea para abrir este perfil en tu teléfono</span></div></aside>
</div></div>

<section class="cierre"><div class="kick">{E(estado_ciudad)}</div><h2 class="cs">Tu caso merece <span>la mejor defensa.</span></h2><p>Escríbele ahora. La primera conversación es para escucharte.</p>
 <a class="btn btn-oro" target="_blank" rel="noopener" href="{E(wa("Necesito asesoría."))}">{WA}Escribir por WhatsApp</a>
 <a class="lk" href="{guia_url}">Perfil destacado en <b>LicLink</b> · Ver más abogados →</a></section>

<div class="fija" id="fija"><span class="av" style="background-image:url('{avatar}')"></span><span class="t"><b>{E(a["nombre"])}</b><small><span class="pulso"></span>{E(consulta_txt)}</small></span><a class="btn btn-oro" target="_blank" rel="noopener" href="{E(wa("Necesito asesoría."))}">{WA}WhatsApp</a></div>

<script>
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add("si");io.unobserve(e.target)}}}}),{{threshold:.12}});
document.querySelectorAll(".rv").forEach(el=>io.observe(el));
const barra=document.getElementById("top"),fija=document.getElementById("fija"),hero=document.querySelector(".hero");
addEventListener("scroll",()=>{{const y=scrollY;barra.classList.toggle("lleno",y>60);fija.classList.toggle("on",y>hero.offsetHeight*.7)}},{{passive:true}});
document.querySelectorAll(".sv button").forEach(b=>b.onclick=()=>{{const s=b.parentElement;s.classList.toggle("ab");b.setAttribute("aria-expanded",s.classList.contains("ab"))}});
const tabs=[...document.querySelectorAll(".tabs a")],secs=tabs.map(t=>document.querySelector(t.getAttribute("href")));
const so=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{const i=secs.indexOf(e.target);tabs.forEach((t,j)=>t.classList.toggle("on",j===i));const c=tabs[i].parentElement;c.scrollTo({{left:tabs[i].offsetLeft-c.clientWidth/2+tabs[i].offsetWidth/2,behavior:"smooth"}})}}}}),{{rootMargin:"-40% 0px -55% 0px"}});
secs.forEach(s=>s&&so.observe(s));
document.getElementById("bComp").onclick=async()=>{{const d={{title:document.title,url:location.href}};try{{if(navigator.share)await navigator.share(d);else{{await navigator.clipboard.writeText(location.href);alert("Enlace copiado")}}}}catch(e){{}}}};
</script>
</body></html>"""


def main():
    pedidos = sys.argv[1:]
    lista = [a for a in datos if a.get("estado") == "vendido" and a.get("plantilla") == "v2"] if pedidos == ["todos"] else [a for a in datos if a["slug"] in pedidos]
    for a in lista:
        d = RAIZ / "public" / "nuevo" / a["slug"]; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(construir(a), encoding="utf-8")
        print("ok", a["slug"])


if __name__ == "__main__":
    main()
