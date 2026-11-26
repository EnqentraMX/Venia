"""Calculadora de finiquito y liquidación (LFT). Genera public/calculadora-finiquito/index.html con el diseño v3.
Uso: python3 herramientas/calculadora.py   (también la llama guia.py)
Salario mínimo 2026 (DOF 9-dic-2025): general $315.04, Zona Libre Frontera Norte $440.87.
"""
import hashlib, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
V = hashlib.md5((RAIZ / "public" / "assets" / "v3.css").read_bytes()).hexdigest()[:8]
OG = hashlib.md5((RAIZ / "public" / "assets" / "liclink-compartir.png").read_bytes()).hexdigest()[:8]

HTML = r"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Calculadora de finiquito y liquidación 2026 | LicLink</title>
<meta name="description" content="Calcula gratis tu finiquito o liquidación según la Ley Federal del Trabajo: aguinaldo, vacaciones, prima vacacional, indemnización y prima de antigüedad. Actualizada con el salario mínimo 2026.">
<link rel="canonical" href="https://liclink.com.mx/calculadora-finiquito/"><meta name="theme-color" content="#f5efe4">
<meta property="og:type" content="website"><meta property="og:site_name" content="LicLink"><meta property="og:title" content="Calculadora de finiquito y liquidación 2026"><meta property="og:description" content="Calcula gratis cuánto te corresponde si renuncias o te despiden.">
<meta property="og:url" content="https://liclink.com.mx/calculadora-finiquito/"><meta property="og:image" content="https://liclink.com.mx/assets/liclink-compartir.png?v=__OG__"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230c0b0a'/%3E%3Ctext x='32' y='44' font-family='Arial' font-weight='800' font-size='36' text-anchor='middle' fill='%23d4b06a'%3EL%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="/assets/v3.css?v=__V__"><link rel="stylesheet" href="/assets/temporada.css?v=__T__"><script src="/assets/temporada.js?v=__T__"></script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebApplication","name":"Calculadora de finiquito y liquidación","url":"https://liclink.com.mx/calculadora-finiquito/","applicationCategory":"FinanceApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"MXN"},"inLanguage":"es-MX"}</script>
<style>
.cab{position:sticky;top:0;z-index:30;background:rgba(245,239,228,.9);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--linea)}
.cab .ancho{display:flex;align-items:center;justify-content:space-between;height:62px}
.wm{font-weight:800;letter-spacing:-.03em;font-size:26px}.wm b{color:var(--oro)}
.top{background:radial-gradient(80% 90% at 100% 0%,rgba(216,184,116,.22),transparent 60%),var(--tinta);color:#fff;border-radius:0 0 28px 28px;padding:30px 0 34px}
.top h1{font-size:clamp(36px,9.5vw,64px);line-height:1;margin-top:10px}.top h1 span{color:var(--oro2)}
.top p{color:#d9cfbf;margin-top:12px;max-width:560px}
.migas{font-size:13px;font-weight:700;color:var(--oro2)}.migas a{color:var(--oro2)}
.grid{display:grid;grid-template-columns:minmax(0,1fr);gap:18px;margin-top:22px}
.grid>*,.dos>*{min-width:0}
.campo input{min-width:0;-webkit-appearance:none;appearance:none}
@media(min-width:900px){.grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start}}
.caja{background:var(--papel);border:1px solid var(--linea);border-radius:26px;padding:20px}
.tipo{display:grid;grid-template-columns:1fr 1fr;gap:6px;background:var(--crema);border-radius:999px;padding:5px}
.tipo button{border-radius:999px;padding:12px 8px;font-weight:800;font-size:14.5px;color:var(--gris);transition:background .25s,color .25s}
.tipo button.on{background:var(--tinta);color:var(--crema)}
.campo{margin-top:16px}
.campo label{display:block;font-weight:800;font-size:14px}
.campo small{display:block;color:var(--gris);font-size:12.5px;margin-top:2px}
.campo input,.campo select{width:100%;margin-top:8px;height:52px;border:1.5px solid var(--linea);border-radius:16px;background:#fff;padding:0 14px;font-size:17px;font-weight:700;outline:0;transition:border-color .2s}
.campo input:focus,.campo select:focus{border-color:var(--oro)}
.dos{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px}
.chk{display:flex;gap:10px;align-items:flex-start;margin-top:16px;font-size:14px;font-weight:600}
.chk input{width:20px;height:20px;accent-color:#15120e;margin-top:1px}
.res{background:var(--tinta);color:#fff;border-radius:26px;padding:22px}
@media(min-width:900px){.res{position:sticky;top:80px}}
.res .tot small{display:block;font-size:12px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--oro2)}
.res .tot b{display:block;font-size:clamp(40px,11vw,58px);letter-spacing:-.04em;line-height:1.05;margin-top:6px}
.res .tot span{color:#bfb5a4;font-size:13px}
.res ul{list-style:none;margin-top:18px;border-top:1px solid #2f281f}
.res li{display:flex;justify-content:space-between;gap:12px;padding:12px 0;border-bottom:1px solid #2f281f;font-size:14.5px}
.res li span{color:#d9cfbf}.res li span small{display:block;color:#8f8473;font-size:12px}
.res li b{white-space:nowrap}
.res .extra{margin-top:14px;background:#221c14;border:1px solid #3a3125;border-radius:16px;padding:14px;font-size:13.5px;color:#d9cfbf}
.res .extra b{color:var(--oro2)}
.res .btn{width:100%;margin-top:16px}
.res .aviso{font-size:12px;color:#8f8473;margin-top:12px}
.sab{margin-top:40px}
.sab h2{font-size:clamp(30px,8vw,46px);line-height:1.05}.sab h2 span{color:var(--oro)}
.sab .it{background:var(--papel);border:1px solid var(--linea);border-radius:22px;padding:18px;margin-top:10px}
.sab .it b{font-size:16.5px}.sab .it p{color:var(--gris);font-size:14.5px;margin-top:4px}
.pie{padding:34px 20px 40px;text-align:center;font-size:12.5px;color:var(--gris)}
</style></head>
<body>
<header class="cab"><div class="ancho"><a class="wm" href="/">Lic<b>Link</b></a><a class="btn btn-linea" style="height:40px;padding:0 16px;font-size:13.5px" href="/para-abogados/">Soy abogado</a></div></header>
<section class="top top-calc"><div class="ancho">
 <nav class="migas"><a href="/">Inicio</a> › Calculadora</nav>
 <h1 class="cs">¿Cuánto te <span>corresponde?</span></h1>
 <p>Calcula tu finiquito o tu liquidación según la Ley Federal del Trabajo. Gratis, sin registro y actualizada con el salario mínimo 2026.</p>
</div></section>
<main class="ancho">
 <div class="grid">
  <div class="caja">
   <div class="tipo" role="tablist"><button class="on" data-t="despido">Me despidieron</button><button data-t="renuncia">Renuncié</button></div>
   <div class="campo"><label for="sal">Sueldo mensual</label><small>Lo que te pagaban al mes, antes de descuentos.</small><input id="sal" inputmode="decimal" placeholder="$ 12,000"></div>
   <div class="dos">
    <div class="campo"><label for="ini">Entré a trabajar</label><input id="ini" type="date"></div>
    <div class="campo"><label for="fin">Mi último día</label><input id="fin" type="date"></div>
   </div>
   <div class="dos">
    <div class="campo"><label for="pend">Días sin pagar</label><small>Trabajados y no pagados</small><input id="pend" inputmode="numeric" value="0"></div>
    <div class="campo"><label for="vac">Vacaciones pendientes</label><small>Días de años anteriores</small><input id="vac" inputmode="numeric" value="0"></div>
   </div>
   <label class="chk"><input type="checkbox" id="fron"> Trabajo en un municipio de la Zona Libre de la Frontera Norte</label>
  </div>
  <div class="res" id="res" aria-live="polite"></div>
 </div>
 <section class="sab">
  <div class="kick">Para que lo entiendas</div><h2 class="cs">Finiquito y liquidación <span>no son lo mismo.</span></h2>
  <div class="it"><b>Finiquito</b><p>Te corresponde siempre que termina tu trabajo, renuncies o te despidan: salarios pendientes y la parte proporcional de aguinaldo, vacaciones y prima vacacional.</p></div>
  <div class="it"><b>Liquidación</b><p>Aplica cuando el despido es injustificado. Además del finiquito incluye tres meses de salario y la prima de antigüedad; en algunos casos, también 20 días por año trabajado.</p></div>
  <div class="it"><b>Tienes poco tiempo para reclamar</b><p>La ley da dos meses desde el despido para reclamar un despido injustificado. No firmes tu renuncia ni hojas en blanco.</p></div>
 </section>
</main>
<footer class="pie">Cálculo estimado con base en la Ley Federal del Trabajo y las prestaciones mínimas de ley. Tu monto real puede ser mayor si tu empresa da más prestaciones, o variar según tu caso. No es asesoría legal.<br><a href="/" style="font-weight:800;color:var(--tinta)">LicLink · La guía de abogados de México</a></footer>
<script>
const $=s=>document.querySelector(s);
const SM={gen:315.04,fron:440.87};
const fmt=n=>"$"+n.toLocaleString("es-MX",{minimumFractionDigits:2,maximumFractionDigits:2});
const num=s=>parseFloat(String(s).replace(/[^0-9.]/g,""))||0;
let tipo="despido";
document.querySelectorAll(".tipo button").forEach(b=>b.onclick=()=>{tipo=b.dataset.t;document.querySelectorAll(".tipo button").forEach(x=>x.classList.toggle("on",x===b));calc()});
const hoy=new Date(),iso=d=>new Date(d-d.getTimezoneOffset()*6e4).toISOString().slice(0,10);
$("#fin").value=iso(hoy);const h2=new Date(hoy);h2.setFullYear(h2.getFullYear()-3);$("#ini").value=iso(h2);
// Vacaciones según la reforma de 2023 (art. 76 LFT)
function diasVac(anio){if(anio<=1)return 12;if(anio<=5)return 12+2*(anio-1);return 20+2*Math.ceil((anio-5)/5)}
function calc(){
 const sm=$("#fron").checked?SM.fron:SM.gen, sd=num($("#sal").value)/30;
 const ini=new Date($("#ini").value+"T00:00"),fin=new Date($("#fin").value+"T00:00");
 if(!sd||isNaN(ini)||isNaN(fin)||fin<=ini){$("#res").innerHTML=`<div class="tot"><small>Tu estimado</small><b>$0.00</b><span>Escribe tu sueldo y tus fechas.</span></div>`;return}
 const dias=(fin-ini)/864e5+1, anios=dias/365, completos=Math.floor(anios);
 // Aguinaldo proporcional del año en curso
 const ene=new Date(fin.getFullYear(),0,1), desde=ini>ene?ini:ene, dAno=(fin-desde)/864e5+1;
 const agui=15*sd*dAno/365;
 // Vacaciones proporcionales del año de servicio en curso
 const fracc=anios-completos, vacDias=diasVac(completos+1)*fracc+num($("#vac").value), vac=vacDias*sd, prima=vac*.25;
 const pend=num($("#pend").value)*sd;
 const L=[["Salarios pendientes",pend,num($("#pend").value)+" días"],["Aguinaldo proporcional",agui,Math.round(dAno)+" días trabajados este año"],["Vacaciones",vac,vacDias.toFixed(1)+" días"],["Prima vacacional (25%)",prima,""]];
 const tope=Math.min(sd,2*sm), primaAnt=12*tope*anios;
 let extra="";
 if(tipo==="despido"){L.push(["Indemnización (3 meses)",90*sd,"Despido injustificado"]);L.push(["Prima de antigüedad",primaAnt,"12 días por año"]);
  extra=`<div class="extra">En algunos casos también pueden corresponderte <b>20 días por año</b> trabajado: aprox. <b>${fmt(20*sd*anios)}</b>, y los salarios que dejaste de recibir durante el juicio. Un abogado laboral te dice si aplican.</div>`}
 else if(anios>=15){L.push(["Prima de antigüedad",primaAnt,"Por tener 15 años o más"])}
 const tot=L.reduce((a,x)=>a+x[1],0);
 const caso=(tipo==="despido"?"Me despidieron":"Renuncié")+` después de ${anios.toFixed(1)} años. Según la calculadora de LicLink me corresponderían unos ${fmt(tot)}. Quiero que un abogado lo revise.`;
 $("#res").innerHTML=`<div class="tot"><small>${tipo==="despido"?"Tu liquidación estimada":"Tu finiquito estimado"}</small><b>${fmt(tot)}</b><span>${anios.toFixed(1)} años trabajados · salario diario ${fmt(sd)}</span></div>
 <ul>${L.filter(x=>x[1]>0).map(x=>`<li><span>${x[0]}${x[2]?`<small>${x[2]}</small>`:""}</span><b>${fmt(x[1])}</b></li>`).join("")}</ul>${extra}
 <a class="btn btn-oro" href="/?caso=laboral&texto=${encodeURIComponent(caso)}">Que un abogado laboral lo revise →</a>
 <p class="aviso">Estimado con prestaciones mínimas de ley. No incluye impuestos ni prestaciones extra de tu empresa.</p>`;
}
["#sal","#ini","#fin","#pend","#vac","#fron"].forEach(s=>$(s).addEventListener("input",calc));
$("#sal").addEventListener("blur",()=>{const n=num($("#sal").value);if(n)$("#sal").value="$ "+n.toLocaleString("es-MX")});
calc();
</script>
</body></html>"""

d = RAIZ / "public" / "calculadora-finiquito"; d.mkdir(exist_ok=True)
(d / "index.html").write_text(HTML.replace("__V__", V).replace("__T__", hashlib.md5(b"".join((RAIZ / "public" / "assets" / f).read_bytes() for f in ("temporada.css", "temporada.js"))).hexdigest()[:8]).replace("__OG__", OG), encoding="utf-8")
print("Calculadora lista")
