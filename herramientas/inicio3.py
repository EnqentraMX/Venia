"""Inicio v3 — OFICIAL (lo llama guia.py). Genera public/index.html con "Cuéntanos tu caso", destacados del día y consejo del día.
Uso: python3 herramientas/inicio3.py
"""
import json, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
g = json.loads((RAIZ / "prospectos" / "guia.json").read_text(encoding="utf-8"))
ab = {a["slug"]: a for a in json.loads((RAIZ / "prospectos" / "abogados.json").read_text(encoding="utf-8"))}
src = (RAIZ / "herramientas" / "guia.py").read_text(encoding="utf-8")
ns = {}; exec(re.search(r"CIUDADES = \{.*?\}\n", src, re.S).group(0), ns)
CIU = {k: v[0] for k, v in ns["CIUDADES"].items()}

L = []
for a in g:
    if a.get("estado") != "activo": continue
    x = ab.get(a["slug"], {})
    L.append({"s": a["slug"], "n": a["nombre"], "r": a.get("rol", ""), "c": a["ciudad"], "oc": a.get("otras_ciudades", []),
              "m": a.get("materias", []), "p": a["plan"], "f": a.get("foto", ""), "l": bool(a.get("logo")), "bg": a.get("fondo") or x.get("fondo_logo") or "#15120e",
              "i": a.get("iniciales", ""), "w": a.get("whatsapp", ""), "u": a.get("pagina", "") or f"/{a['slug']}/",
              "q": a.get("consulta", ""), "fr": x.get("frase", "")})
ciu = {k: v for k, v in CIU.items() if any(a["c"] == k or k in a["oc"] for a in L)}

gns = {}; exec((RAIZ / "herramientas" / "guias_legales.py").read_text(encoding="utf-8"), gns)
GUIAS = [{"s": x["slug"], "t": x["titulo"], "d": x["resumen"], "m": x["materia"]} for x in gns["GUIAS"]]
H = (RAIZ / "herramientas" / "inicio3.html").read_text(encoding="utf-8")
H = H.replace("/*DATOS*/", "const AB=" + json.dumps(L, ensure_ascii=False) + ";const CIU=" + json.dumps(ciu, ensure_ascii=False) + ";const GUIAS=" + json.dumps(GUIAS, ensure_ascii=False) + ";")
# --- Partes que van escritas en el HTML (para que Google las lea sin JavaScript) ---
from html import escape as e
exec(re.search(r"MATERIAS = \{.*?\n\}\n", src, re.S).group(0), ns)
exec(re.search(r"ICONOS = \{.*?\n\}\n", src, re.S).group(0), ns)
MATS, ICONOS = ns["MATERIAS"], ns["ICONOS"]
MAT_CORTO = {"penal": "penal", "familiar": "familiar", "laboral": "laboral", "civil": "civil", "mercantil": "mercantil", "sucesiones": "herencias", "amparo": "amparo", "fiscal": "fiscal", "agrario": "agrario"}
cuenta = lambda k: sum(1 for a in L if a["c"] == k or k in a["oc"])
c0 = max(ciu, key=cuenta)  # el estado con más abogados (igual que en el navegador)

def tarjeta(a):
    if a["f"]:
        st = (f"background-color:{a['bg']};" if a["l"] else "") + f"background-image:url('{a['f']}')"
    else:
        st = ""
    tags = "".join(f"<span>{e(MAT_CORTO.get(m, m))}</span>" for m in a["m"][:3]) + (f"<span>{e(a['q'])}</span>" if a["q"] else "")
    wa = f"https://wa.me/{a['w']}?text=" + "Hola%2C%20lo%20encontr%C3%A9%20en%20LicLink.%20Necesito%20asesor%C3%ADa."
    return (f'<article class="tar"><div class="ft{" lg" if a["l"] else ""}" style="{st}"><span class="sello"><b>★</b> {e(CIU.get(a["c"], ""))}</span></div>'
            f'<div class="cu"><h3>{e(a["n"])}</h3>' + (f"<q>{e(a['fr'])}</q>" if a["fr"] else "") + f'<div class="tags">{tags}</div>'
            f'<div class="acc"><a class="btn btn-linea" href="{a["u"]}">Ver perfil</a><a class="btn btn-oro" target="_blank" rel="noopener" href="{wa}">WhatsApp</a></div></div></article>')

prem = [a for a in L if a["p"] == "premium"]
prem.sort(key=lambda a: (not (a["c"] == c0 or c0 in a["oc"]), a["n"]))
DEST = "".join(tarjeta(a) for a in prem[:6])

MATS_H = "".join(
    f'<a class="mt rv d{i % 3}{" u" if k == "penal" else ""}" data-mat="{k}" href="/abogados/{c0}/{k}/"><span class="ic"><svg viewBox="0 0 24 24">{ICONOS[k]}</svg></span>'
    f'<b>{e(v[0])}</b><small>{e(v[1])}</small></a>' for i, (k, v) in enumerate(MATS.items()))
EDOS_H = "".join(f'<a href="/abogados/{k}/">{e(v)}</a>' for k, v in CIU.items() if k in ciu)
PIE_EDOS = "".join(f'<a href="/abogados/{k}/">{e(v)}</a>' for k, v in CIU.items() if k in ciu)
PIE_MATS = "".join(f'<a href="/abogados/{c0}/{k}/">{e(v[0])}</a>' for k, v in MATS.items())
GUIAS_H = "".join(f'<a class="gu rv d{i % 4}" href="/guias/{g["s"]}/"><span class="n">{i + 1:02d}</span><span><b>{e(g["t"])}</b><p>{e(g["d"])}</p></span></a>' for i, g in enumerate(GUIAS))
FAQ = [("¿Cuánto me cuesta usar LicLink?", "Nada. Buscar y escribirle a un abogado es gratis. Tú acuerdas sus honorarios directamente con él."),
       ("¿Cómo sé que es abogado de verdad?", "Cuando un perfil dice «Cédula profesional verificada», revisamos su cédula en el Registro Nacional de Profesionistas de la SEP. Tú también puedes consultar cualquier cédula en la SEP."),
       ("¿LicLink cobra comisión por mi caso?", "No. Hablas directo con el abogado por WhatsApp o por teléfono, sin intermediarios."),
       ("¿Qué pasa con lo que le cuento al abogado?", "Tu mensaje va directo a su WhatsApp. LicLink no guarda ni lee tu caso."),
       ("¿LicLink me da asesoría legal?", "No. LicLink te ayuda a encontrar y contactar abogados. La asesoría la da cada abogado.")]
FAQ_H = "".join(f'<div class="fq"><button>{e(p)}<i>+</i></button><div class="r"><div><p>{e(r)}</p></div></div></div>' for p, r in FAQ)
FAQ_LD = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in FAQ]}, ensure_ascii=False)
for k, v in {"__DESTACADOS__": DEST, "__MATERIAS__": MATS_H, "__ESTADOS__": EDOS_H, "__PIE_EDOS__": PIE_EDOS, "__PIE_MATS__": PIE_MATS,
             "__GUIAS__": GUIAS_H, "__FAQ__": FAQ_H, "__FAQLD__": FAQ_LD, "__NEDOS__": str(len(ciu)), "__C0__": c0, "__CIUDAD0__": e(CIU[c0])}.items():
    H = H.replace(k, v)
import hashlib
H = H.replace("__VER__", hashlib.md5((RAIZ / "public" / "assets" / "v3.css").read_bytes()).hexdigest()[:8])
H = H.replace("__OGV__", hashlib.md5((RAIZ / "public" / "assets" / "liclink-compartir.png").read_bytes()).hexdigest()[:8])
(RAIZ / "public" / "index.html").write_text(H, encoding="utf-8")
print("Inicio v3 listo:", len(L), "abogados")
