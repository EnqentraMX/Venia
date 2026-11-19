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
import hashlib
H = H.replace("__VER__", hashlib.md5((RAIZ / "public" / "assets" / "v3.css").read_bytes()).hexdigest()[:8])
H = H.replace("__OGV__", hashlib.md5((RAIZ / "public" / "assets" / "liclink-compartir.png").read_bytes()).hexdigest()[:8])
(RAIZ / "public" / "index.html").write_text(H, encoding="utf-8")
print("Inicio v3 listo:", len(L), "abogados")
