"""Prototipo "LicLink app" (estilo Suits/Billions + Uber): genera public/nuevo/index.html con los abogados reales de guia.json.
Es una vista de prueba (noindex); no reemplaza el sitio actual.
Uso: python3 herramientas/nuevo.py
"""
import json, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
g = json.loads((RAIZ / "prospectos" / "guia.json").read_text(encoding="utf-8"))
ab = {a["slug"]: a for a in json.loads((RAIZ / "prospectos" / "abogados.json").read_text(encoding="utf-8"))}
src = (RAIZ / "herramientas" / "guia.py").read_text(encoding="utf-8")
ns = {}; exec(re.search(r"CIUDADES = \{.*?\}\n", src, re.S).group(0), ns)
CIUDADES = {k: v[0] for k, v in ns["CIUDADES"].items()}

abogados = []
for a in g:
    if a.get("estado") != "activo": continue
    x = ab.get(a["slug"], {})
    promos = [{"n": p["nombre"], "p": p.get("precio", ""), "t": p.get("texto", "")} for p in x.get("paquetes", []) if "express" in p.get("nombre", "").lower() or p.get("destacado")]
    abogados.append({"s": a["slug"], "n": a["nombre"], "r": a.get("rol", ""), "c": a["ciudad"], "oc": a.get("otras_ciudades", []),
                     "m": a.get("materias", []), "p": a["plan"], "f": a.get("foto", ""), "l": bool(a.get("logo")), "bg": a.get("fondo", ""),
                     "i": a.get("iniciales", ""), "w": a.get("whatsapp", ""), "u": a.get("pagina", ""), "q": a.get("consulta", ""),
                     "h24": "24/7" in json.dumps(x.get("horario", {})) or "24/7" in a.get("rol", "") or "24" in x.get("modalidad", ""),
                     "pr": promos})
ciudades = {k: v for k, v in CIUDADES.items() if any(a["c"] == k or k in a["oc"] for a in abogados)}

HTML = (RAIZ / "herramientas" / "nuevo.html").read_text(encoding="utf-8")
HTML = HTML.replace("/*DATOS*/", "const AB=" + json.dumps(abogados, ensure_ascii=False) + ";const CIU=" + json.dumps(ciudades, ensure_ascii=False) + ";")
(RAIZ / "public" / "nuevo").mkdir(exist_ok=True)
(RAIZ / "public" / "nuevo" / "index.html").write_text(HTML, encoding="utf-8")
print("Prototipo listo:", len(abogados), "abogados,", len(ciudades), "ciudades")
