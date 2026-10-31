# -*- coding: utf-8 -*-
"""LicLink · generador de páginas de prospectos.

Lee prospectos/abogados.json y, por cada abogado:
  estado "propuesta" -> crea public/<slug>/ oculta para Google, con aviso "Propuesta de página para…"
  estado "vendido"   -> página definitiva (visible en Google, sin aviso)
  estado "borrar"    -> elimina public/<slug>/ (los datos se conservan en el JSON por si regresa)
Además escribe prospectos/ESTADO.md con el resumen.

Uso: python3 herramientas/generar.py
"""
import json, os, re, shutil, unicodedata, datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "prospectos", "abogados.json")
PLANTILLA = os.path.join(RAIZ, "plantilla", "index.html")
PUBLICO = os.path.join(RAIZ, "public")
PROTEGIDOS = {"assets", "plantilla", "castillo-abogados", "gabriel-sanchez", "miguel-manzano", "dalia-marquez"}

# ---------------------------------------------------------------- catálogo de áreas
AREAS = {
    "familiar": ("Derecho familiar", "familia", "Te acompaño en asuntos de familia con un enfoque humano: acuerdos claros y el bienestar de tus hijos primero.", ["Divorcios", "Pensión alimenticia", "Guarda, custodia y convivencia"]),
    "penal": ("Derecho penal", "escudo", "Defensa penal desde el primer momento: detenciones, audiencias y todo el proceso.", ["Detenciones y audiencias iniciales", "Defensa en el proceso penal", "Denuncias y querellas"]),
    "laboral": ("Derecho laboral", "maletin", "Defensa de tus derechos como trabajador cuando hay un despido o un conflicto en el trabajo.", ["Despidos injustificados", "Reclamación de prestaciones", "Liquidaciones y finiquitos"]),
    "civil": ("Derecho civil", "balanza", "Contratos, propiedades y juicios civiles con seguimiento puntual.", ["Contratos y arrendamientos", "Juicios civiles", "Propiedad y posesión"]),
    "mercantil": ("Derecho mercantil", "acuerdo", "Cobranza y conflictos mercantiles para personas y empresas.", ["Cobranza judicial y extrajudicial", "Pagarés, cheques y facturas", "Juicios mercantiles"]),
    "amparo": ("Juicio de amparo", "escudo", "Defensa de tus derechos cuando un acto de autoridad los vulnera.", ["Amparo indirecto", "Amparo directo", "Suspensión del acto reclamado"]),
    "migratorio": ("Derecho migratorio", "acuerdo", "Trámites y defensa migratoria con acompañamiento en cada etapa.", ["Regularización migratoria", "Residencia temporal y permanente", "Naturalización"]),
    "fiscal": ("Derecho fiscal", "edificio", "Defensa y orientación frente a la autoridad fiscal.", ["Defensa ante el SAT", "Juicio de nulidad fiscal", "Cumplimiento de obligaciones fiscales"]),
    "administrativo": ("Derecho administrativo", "edificio", "Defensa frente a actos de autoridad que afectan tus derechos o tu negocio.", ["Defensa ante actos de autoridad", "Juicio de nulidad", "Multas y clausuras"]),
    "inmobiliario": ("Derecho inmobiliario", "edificio", "Seguridad jurídica al comprar, vender o regularizar un inmueble.", ["Compraventa de inmuebles", "Regularización de propiedades", "Escrituración"]),
    "corporativo": ("Derecho corporativo", "maletin", "Asesoría legal para que tu empresa opere con orden y seguridad.", ["Constitución de sociedades", "Contratos empresariales", "Asambleas y actas"]),
    "sucesiones": ("Sucesiones y herencias", "familia", "Orientación para resolver herencias y proteger el patrimonio de tu familia.", ["Juicios sucesorios", "Testamentos", "Herencias sin testamento"]),
    "agrario": ("Derecho agrario", "edificio", "Defensa de derechos sobre tierras ejidales y comunales.", ["Derechos ejidales y comunales", "Juicios agrarios", "Sucesión de derechos agrarios"]),
    "pensiones": ("Pensiones IMSS e ISSSTE", "acuerdo", "Te ayudo a obtener o corregir tu pensión.", ["Trámite de pensión", "Corrección de semanas cotizadas", "Defensa ante negativas"]),
    "marcas": ("Propiedad intelectual", "lupa", "Protección de tu marca y tus creaciones.", ["Registro de marcas", "Derechos de autor", "Defensa de marca"]),
}
SINONIMOS = {"familia": "familiar", "divorcio": "familiar", "divorcios": "familiar", "criminal": "penal", "trabajo": "laboral", "despidos": "laboral",
             "cobranza": "mercantil", "amparos": "amparo", "migracion": "migratorio", "inmigracion": "migratorio", "sat": "fiscal",
             "herencias": "sucesiones", "sucesorio": "sucesiones", "imss": "pensiones", "issste": "pensiones", "propiedad intelectual": "marcas",
             "empresarial": "corporativo", "inmuebles": "inmobiliario", "notarial": "inmobiliario"}

TEMAS = {
    "negro-oro": None,
    "marino-oro": {"fondo": "#0a1220", "fondo2": "#0e1828", "tarjeta": "#122036", "linea": "#22324b", "acento": "#d2ae6c", "acento2": "#ecd29e"},
    "negro-rosa": {"fondo": "#0c0b0b", "fondo2": "#131111", "tarjeta": "#1b1817", "linea": "#2f2927", "acento": "#c7a28a", "acento2": "#e6cdbb"},
    "vino": {"fondo": "#130a0d", "fondo2": "#1a0f13", "tarjeta": "#221318", "linea": "#3a2229", "acento": "#cfa465", "acento2": "#ead2a3"},
    "verde": {"fondo": "#08120f", "fondo2": "#0c1813", "tarjeta": "#11211b", "linea": "#1f3a31", "acento": "#c9ab6b", "acento2": "#e8d5a6"},
    "azul-plata": {"fondo": "#0b1118", "fondo2": "#0f1720", "tarjeta": "#141d27", "linea": "#263343", "acento": "#b8c4d1", "acento2": "#e4eaf0"},
    "grafito-cobre": {"fondo": "#111214", "fondo2": "#16171a", "tarjeta": "#1c1d20", "linea": "#2e3034", "acento": "#cc8d5c", "acento2": "#ebb98f"},
}

SITUACIONES = {
    "penal": [("Hay una persona detenida en este momento", True), ("Recibí un citatorio o una notificación", False), ("Ya hay una carpeta o proceso abierto", False), ("Solo quiero orientación", False)],
    "laboral": [("Me despidieron hace poco (los plazos ya están corriendo)", True), ("Me deben prestaciones o mi liquidación", False), ("Tengo otro problema en mi trabajo", False), ("Solo quiero orientación", False)],
    "_": [("Tengo una audiencia o un plazo que vence pronto", True), ("Quiero iniciar un trámite o una demanda", False), ("Ya tengo un proceso abierto y necesito apoyo", False), ("Solo quiero orientación para decidir qué hacer", False)],
}

def slugify(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"\b(lic|licenciado|licenciada|abogado|abogada|mtro|mtra|dr|dra)\b\.?", " ", t)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40]

def clave_area(nombre):
    n = unicodedata.normalize("NFD", nombre.lower()); n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    n = n.replace("derecho", "").strip()
    return n if n in AREAS else SINONIMOS.get(n)

def area(e):
    """e puede ser texto ('familiar') o un objeto {nombre, texto, puntos, icono} con lo que el abogado publica."""
    if isinstance(e, dict):
        base = AREAS.get(clave_area(e.get("nombre", "")) or "", ("", "balanza", "", []))
        return {"nombre": e.get("nombre") or base[0], "icono": e.get("icono") or base[1], "texto": e.get("texto") or base[2], "puntos": e.get("puntos") or base[3]}
    k = clave_area(e)
    if k:
        n, i, t, p = AREAS[k]; return {"nombre": n, "icono": i, "texto": t, "puntos": p}
    return {"nombre": e.strip().capitalize(), "icono": "balanza", "texto": f"Asesoría y representación en {e.strip().lower()}.", "puntos": []}

def tel10(t):
    d = re.sub(r"\D", "", str(t or ""))
    if d.startswith("52") and len(d) == 12: d = d[2:]
    return d if len(d) == 10 else ""

def visible(d):
    return f"{d[:2]} {d[2:6]} {d[6:]}" if d.startswith(("55", "33", "81")) else f"{d[:3]} {d[3:6]} {d[6:]}"

def datos_js(a):
    estado = a.get("estado", "propuesta")
    areas = [area(x) for x in a.get("areas", [])] or [area("civil")]
    principal = clave_area(areas[0]["nombre"]) or "_"
    tel = tel10(a.get("telefono")); wa = tel10(a.get("whatsapp") or a.get("telefono"))
    nombre = a["nombre"].strip()
    sit = SITUACIONES.get(principal, SITUACIONES["_"])
    redes = {k: a.get(k, "") for k in ["facebook", "instagram", "tiktok", "youtube", "linkedin"]}
    oficinas = [{"nombre": a.get("ciudad", "Oficina"), "direccion": a["direccion"], "referencia": a.get("referencia", "")}] if a.get("direccion") else []
    d = {
        "vistaPrevia": estado != "vendido",
        "propuesta": nombre if estado == "propuesta" else "",
        "muestra": False,
        "tema": TEMAS.get(a.get("tema", "negro-oro")),
        "simbolo": a.get("simbolo", "balanza"),
        "despacho": a.get("despacho") or re.sub(r"^(Lic\.|Licenciad[oa]|Abogad[oa]|Mtr[oa]\.?)\s+", "", nombre).split(" ")[0] + " " + (re.sub(r"^(Lic\.|Licenciad[oa]|Abogad[oa]|Mtr[oa]\.?)\s+", "", nombre).split(" ") + [""])[1],
        "sufijo": a.get("sufijo", "Abogados" if a.get("despacho") else "Asesoría jurídica"),
        "abogado": nombre,
        "titulo": a.get("titulo", "Abogado"),
        "descripcion": a.get("descripcion") or (", ".join(x["nombre"] for x in areas[:3]) + (f" en {a['ciudad']}" if a.get("ciudad") else "")),
        "cedula": a.get("cedula", ""),
        "modalidad": a.get("modalidad", "Atención personalizada"),
        "iniciales": a.get("iniciales", ""),
        "foto": a.get("foto", ""),
        "frase": a.get("frase", "Tu tranquilidad legal es nuestra prioridad."),
        "portada": {"titulo": a.get("portada", ["Tu asunto legal,", "en buenas", "manos."]),
                    "texto": a.get("texto_portada") or (", ".join(x["nombre"].lower() for x in areas[:3]).capitalize() + (f" en {a['ciudad']}" if a.get("ciudad") else "") + ". Escríbenos y te orientamos sobre tu caso.")},
        "whatsapp": ("52" + wa) if wa else "", "telefono": tel, "telefonoVisible": visible(tel) if tel else "",
        "correo": a.get("correo", ""), "precioConsulta": a.get("precio_consulta", ""),
        "areas": areas, "paquetes": a.get("paquetes", []), "compromisos": a.get("compromisos", []),
        "situaciones": [{"texto": t, "urgente": u} for t, u in sit],
        "pasos": [{"titulo": "Escríbenos por WhatsApp", "texto": "Cuéntanos brevemente tu situación. Tu información se trata con confidencialidad."},
                  {"titulo": "Revisamos tu caso", "texto": "Analizamos los hechos y los documentos que tengas, y te explicamos tus opciones con claridad."},
                  {"titulo": "Definimos la estrategia", "texto": "Te acompañamos en cada etapa del proceso hasta resolver tu asunto."}],
        "horario": a.get("horario"), "notaHorario": a.get("nota_horario", ""),
        "oficinas": oficinas, "redes": redes,
        "preguntas": a.get("preguntas") or [
            {"p": "¿Cuánto cuesta la primera consulta?", "r": "{precio}"},
            {"p": "¿Qué documentos debo tener a la mano?", "r": "Tu identificación y cualquier documento relacionado con tu asunto: contratos, citatorios, notificaciones o mensajes. Si no tienes nada, igual podemos orientarte."},
            {"p": "¿Pueden atenderme en línea?", "r": "Escríbenos por WhatsApp y te decimos si tu asunto puede atenderse por videollamada."},
            {"p": "¿Lo que les cuento es confidencial?", "r": "Sí. Todo lo que nos compartas se trata con estricta confidencialidad y secreto profesional."}],
    }
    if not d["tema"]: del d["tema"]
    return "/* LicLink · datos generados desde prospectos/abogados.json. Para cambiar algo, edita ese archivo y vuelve a generar. */\nwindow.DATOS = " + json.dumps(d, ensure_ascii=False, indent=2) + ";\n"

def main():
    lista = json.load(open(DATOS, encoding="utf-8")) if os.path.exists(DATOS) else []
    plantilla = open(PLANTILLA, encoding="utf-8").read()
    usados = set()
    for a in lista:
        a.setdefault("slug", slugify(a["nombre"])); a.setdefault("estado", "propuesta"); a.setdefault("alta", datetime.date.today().isoformat())
        if a["slug"] in usados or a["slug"] in PROTEGIDOS: raise SystemExit(f"Dirección repetida o reservada: {a['slug']}")
        usados.add(a["slug"])
        carpeta = os.path.join(PUBLICO, a["slug"])
        if a["estado"] == "borrar":
            if os.path.isdir(carpeta): shutil.rmtree(carpeta)
            continue
        os.makedirs(carpeta, exist_ok=True)
        html = plantilla
        if a["estado"] != "vendido":
            html = html.replace('<meta name="viewport"', '<meta name="robots" content="noindex, nofollow">\n<meta name="viewport"', 1)
        open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(html)
        open(os.path.join(carpeta, "datos.js"), "w", encoding="utf-8").write(datos_js(a))
    json.dump(lista, open(DATOS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # resumen
    filas = ["| Alta | Abogado | Dirección | Estado | Contacto |", "|---|---|---|---|---|"]
    for a in sorted(lista, key=lambda x: (x["estado"], x["alta"])):
        filas.append(f"| {a['alta']} | {a['nombre']} | /{a['slug']}/ | {a['estado']} | {a.get('facebook') or a.get('telefono', '')} |")
    cuenta = {e: sum(1 for a in lista if a["estado"] == e) for e in ["propuesta", "vendido", "borrar"]}
    open(os.path.join(RAIZ, "prospectos", "ESTADO.md"), "w", encoding="utf-8").write(
        f"# Prospectos LicLink\n\nPropuestas: {cuenta['propuesta']} · Vendidos: {cuenta['vendido']} · Borrados: {cuenta['borrar']}\n\n" + "\n".join(filas) + "\n")
    print(f"Listo · propuestas {cuenta['propuesta']} · vendidos {cuenta['vendido']} · borrados {cuenta['borrar']}")

if __name__ == "__main__":
    main()
