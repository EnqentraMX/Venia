/* LicLink · motor de la página. Lee window.DATOS (datos.js de cada despacho). */
(function(){
const D = window.DATOS || {};
const $ = s => document.querySelector(s);
const esc = t => String(t ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const PRE = !!D.vistaPrevia;
const pend = () => PRE ? '<span class="pend">por confirmar</span>' : "";
const ico = n => `<svg><use href="#i-${n}"/></svg>`;

/* ---------- Básicos ---------- */
document.title = `${D.despacho} ${D.sufijo} | ${(D.areas||[]).map(a=>a.nombre).join(", ")}`;
$('meta[name="description"]').setAttribute("content", `${D.despacho} ${D.sufijo}. ${D.abogado}, ${D.titulo}. ${D.portada?.texto||""}`);
if (PRE) $("#preview").hidden = false;
if (D.muestra && !PRE) { const b=$("#preview"); b.hidden=false; b.textContent="Sitio de muestra creado por LicLink · Los datos de contacto, dirección y cédula son de ejemplo."; }
$("#logoNombre").textContent = D.despacho; $("#logoSufijo").textContent = D.sufijo;
document.querySelectorAll(".js-nombre").forEach(e=>e.textContent=D.despacho);
document.querySelectorAll(".js-sufijo").forEach(e=>e.textContent=D.sufijo);
$("#heroTitulo").innerHTML = (D.portada.titulo||[]).map(l=>`<span>${esc(l)}</span>`).join("");
$("#heroTexto").textContent = D.portada.texto;
$("#pieDesc").textContent = `${D.descripcion} · WhatsApp ${D.telefonoVisible}`;

/* ---------- WhatsApp ---------- */
const waLink = msg => `https://wa.me/${D.whatsapp}?text=${encodeURIComponent(msg)}`;
const msgGeneral = `Hola, vi su página y me gustaría una asesoría con ${D.abogado}.`;
document.querySelectorAll('[data-wa="general"]').forEach(a=>{a.href = waLink(msgGeneral); a.target="_blank"; a.rel="noopener";});

/* ---------- Credenciales (portada) ---------- */
$("#cred").innerHTML = `
  <div>${ico("check")}${esc(D.abogado)}</div>
  <div>${ico("doc")}${D.cedula ? "Cédula prof. "+esc(D.cedula) : "Cédula profesional"+pend()}</div>
  <div>${ico("lock")}Atención confidencial</div>`;

/* ---------- Áreas ---------- */
const areasHTML = (D.areas||[]).map((a,i)=>`
  <div class="area reveal ${i===0?"open":""}">
    <button class="area-h" aria-expanded="${i===0}">
      <span class="area-ico">${ico(a.icono||"escudo")}</span>
      <h3>${esc(a.nombre)}</h3><span class="plus">+</span>
    </button>
    <div class="area-b"><div><div class="area-in">
      <div><p>${esc(a.texto)}</p>
        <a class="btn btn-ghost" data-area="${i}">Consultar sobre ${esc(a.nombre.toLowerCase())} →</a></div>
      <ul>${(a.puntos||[]).map(p=>`<li>${esc(p)}</li>`).join("")}</ul>
    </div></div></div>
  </div>`).join("");
$("#listaAreas").innerHTML = areasHTML;
document.querySelectorAll(".area-h").forEach(b=>b.onclick=()=>{
  const el=b.parentElement, open=!el.classList.contains("open");
  el.classList.toggle("open",open); b.setAttribute("aria-expanded",open);
});
document.querySelectorAll("[data-area]").forEach(b=>b.onclick=()=>{
  estado = {paso:1, area:D.areas[+b.dataset.area].nombre};
  pintar(); $("#caso").scrollIntoView({behavior:"smooth"});
});

/* ---------- Asistente ---------- */
let estado = {paso:0};
const TOTAL = 4;
const sits = D.situaciones||[];
function prog(){return `<div class="prog">${Array.from({length:TOTAL},(_,i)=>`<i class="${i<=estado.paso?"on":""}"></i>`).join("")}</div>`}
function pintar(){
  const box=$("#asistente"); let h=prog();
  if(estado.paso===0){
    h+=`<div class="q-n">Pregunta 1 de 3</div><div class="q-t">¿Para quién es la asesoría?</div>
      <div class="opts">
        <button class="opt" data-v="Para mí">Para mí <span>→</span></button>
        <button class="opt" data-v="Para un familiar o conocido">Para un familiar o conocido <span>→</span></button>
      </div>`;
    box.innerHTML=h;
    box.querySelectorAll(".opt").forEach(o=>o.onclick=()=>{estado.quien=o.dataset.v;estado.paso=estado.area?2:1;pintar();});
    return;
  }
  if(estado.paso===1){
    h+=`<div class="q-n">Pregunta 2 de 3</div><div class="q-t">¿Sobre qué tema?</div><div class="opts">
      ${(D.areas||[]).map(a=>`<button class="opt" data-v="${esc(a.nombre)}">${esc(a.nombre)} <span>→</span></button>`).join("")}
      <button class="opt" data-v="No estoy seguro">No estoy seguro <span>→</span></button></div>`;
    h+=foot();
    box.innerHTML=h;
    box.querySelectorAll(".opt").forEach(o=>o.onclick=()=>{estado.area=o.dataset.v;estado.paso=2;pintar();});
    atras(box,estado.quien?0:0); return;
  }
  if(estado.paso===2){
    h+=`<div class="q-n">Pregunta 3 de 3</div><div class="q-t">¿Cuál es la situación?</div><div class="opts">
      ${sits.map((s,i)=>`<button class="opt" data-i="${i}">${esc(s.texto)} ${s.urgente?'<span class="tag">Urgente</span>':'<span>→</span>'}</button>`).join("")}</div>`;
    h+=foot();
    box.innerHTML=h;
    box.querySelectorAll(".opt").forEach(o=>o.onclick=()=>{const s=sits[+o.dataset.i];estado.sit=s.texto;estado.urgente=!!s.urgente;estado.paso=3;pintar();});
    atras(box,1); return;
  }
  if(estado.paso===3){
    h+=`<div class="q-t" style="margin-top:4px">Para darte seguimiento</div>
      ${estado.urgente?`<div class="urg"><b>Es urgente.</b> Llama directo para que te atiendan de inmediato.<div style="margin-top:12px"><a class="btn btn-danger" href="tel:+52${esc(D.telefono)}">Llamar ahora · ${esc(D.telefonoVisible)}</a></div></div>`:""}
      <div class="field"><label for="fNombre">Tu nombre</label><input id="fNombre" autocomplete="name" value="${esc(estado.nombre||"")}" placeholder="Opcional"></div>
      <div class="field"><label for="fCiudad">¿En qué ciudad o estado es el asunto?</label><input id="fCiudad" value="${esc(estado.ciudad||"")}" placeholder="Ej. Xalapa, Veracruz"></div>
      <div class="field"><label for="fDetalle">En una o dos líneas, ¿qué pasó?</label><textarea id="fDetalle" rows="2" placeholder="Opcional">${esc(estado.detalle||"")}</textarea></div>`;
    h+=`<div class="box-foot"><button class="back" id="atras">← Atrás</button>
      <button class="btn btn-main" id="listo">Ver mi resumen →</button></div>`;
    box.innerHTML=h;
    atras(box,2);
    $("#listo").onclick=()=>{estado.nombre=$("#fNombre").value.trim();estado.ciudad=$("#fCiudad").value.trim();estado.detalle=$("#fDetalle").value.trim();estado.paso=4;pintar();};
    return;
  }
  // Resumen
  const msg = mensaje();
  h=`<div class="prog">${Array.from({length:TOTAL},()=>'<i class="on"></i>').join("")}</div>
    <div class="q-t" style="margin-top:4px">Listo. Este es el mensaje que se enviará:</div>
    <div class="resumen">${esc(msg)}</div>
    <div class="ctas" style="display:flex;gap:10px;flex-wrap:wrap">
      <a class="btn btn-main" href="${waLink(msg)}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>Enviar por WhatsApp</a>
      ${estado.urgente?`<a class="btn btn-danger" href="tel:+52${esc(D.telefono)}">Llamar ahora</a>`:""}
    </div>
    <p class="fine">Al enviar aceptas el <button type="button" class="js-aviso">aviso de privacidad</button>.</p>
    <div class="box-foot"><button class="back" id="atras">← Corregir</button><button class="back" id="reini">Empezar de nuevo</button></div>`;
  box.innerHTML=h;
  atras(box,3);
  $("#reini").onclick=()=>{estado={paso:0};pintar();};
  box.querySelector(".js-aviso").onclick=abrirAviso;
}
function foot(){return `<div class="box-foot"><button class="back" id="atras">← Atrás</button></div>`}
function atras(box,p){const b=box.querySelector("#atras"); if(b) b.onclick=()=>{estado.paso=p;pintar();};}
function mensaje(){
  const l=[];
  l.push(`Hola, ${estado.urgente?"necesito ayuda URGENTE.":"me gustaría una asesoría."}`);
  if(estado.nombre) l.push(`Mi nombre es ${estado.nombre}.`);
  if(estado.quien) l.push(`• Es ${estado.quien.toLowerCase()}`);
  l.push(`• Tema: ${estado.area||"—"}`);
  l.push(`• Situación: ${estado.sit||"—"}`);
  if(estado.ciudad) l.push(`• Lugar: ${estado.ciudad}`);
  if(estado.detalle) l.push(`• Detalle: ${estado.detalle}`);
  return l.join("\n");
}
pintar();

/* ---------- Perfil ---------- */
const ini = D.despacho.split(/\s+/).map(w=>w[0]).join("").slice(0,2);
$("#retrato").innerHTML = D.foto ? `<img src="${esc(D.foto)}" alt="${esc(D.abogado)}">` : `<div class="mono">${esc(ini)}</div>${PRE?'<div class="ph">Aquí va la foto del licenciado</div>':""}`;
$("#frase").textContent = `“${D.frase}”`;
$("#nombreAbogado").textContent = D.abogado;
$("#rolAbogado").textContent = `${D.titulo} · ${D.descripcion}`;
$("#verif").innerHTML = `${ico("check")}<div><b>${D.cedula?"Cédula profesional "+esc(D.cedula):"Cédula profesional"}</b>${D.cedula?"":pend()}
  <small>Puedes verificarla en el <a href="https://www.cedulaprofesional.sep.gob.mx/" target="_blank" rel="noopener">Registro Nacional de Profesionistas (SEP)</a>.</small></div>`;

/* ---------- Pasos ---------- */
$("#listaPasos").innerHTML = (D.pasos||[]).map(p=>`<div class="paso reveal"><h3>${esc(p.titulo)}</h3><p>${esc(p.texto)}</p></div>`).join("");

/* ---------- Horario y "abierto ahora" ---------- */
const DIAS=["domingo","lunes","martes","miercoles","jueves","viernes","sabado"];
const NOM={lunes:"Lunes",martes:"Martes",miercoles:"Miércoles",jueves:"Jueves",viernes:"Viernes",sabado:"Sábado",domingo:"Domingo"};
function ahoraMx(){
  const p=new Intl.DateTimeFormat("en-US",{timeZone:D.zona||"America/Mexico_City",weekday:"short",hour:"2-digit",minute:"2-digit",hour12:false}).formatToParts(new Date());
  const g=t=>p.find(x=>x.type===t).value;
  const wd=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].indexOf(g("weekday"));
  return {dia:DIAS[wd], min:(+g("hour")%24)*60+ +g("minute")};
}
const aMin=t=>{const [h,m]=t.split(":");return +h*60+ +m};
const fmt=t=>{let [h,m]=t.split(":").map(Number);const s=h>=12?"pm":"am";h=h%12||12;return `${h}:${String(m).padStart(2,"0")} ${s}`};
if(D.horario){
  const now=ahoraMx(), hoy=D.horario[now.dia];
  const abierto = hoy && now.min>=aMin(hoy[0]) && now.min<aMin(hoy[1]);
  let sub="";
  if(abierto) sub=` · cierra ${fmt(hoy[1])}`;
  else{
    for(let k=0;k<8;k++){
      const d=DIAS[(DIAS.indexOf(now.dia)+k)%7], hr=D.horario[d];
      if(!hr) continue;
      if(k===0 && now.min>=aMin(hr[0])) continue;
      sub=` · abre ${k===0?"hoy":k===1?"mañana":NOM[d].toLowerCase()} ${fmt(hr[0])}`; break;
    }
  }
  $("#statusTop").hidden=false;
  $("#dotTop").classList.toggle("on",!!abierto);
  $("#statusTxt").textContent = abierto?"Abierto ahora":"Cerrado";
  $("#statusSub").textContent = sub;
  const orden=["lunes","martes","miercoles","jueves","viernes","sabado","domingo"];
  $("#panelHorario").innerHTML = `<h3><i class="dot ${abierto?"on":""}"></i>${abierto?"Abierto ahora":"Cerrado ahora"}${pend()}</h3>
    ${orden.map(d=>`<div class="hrow ${d===now.dia?"hoy":""}"><span>${NOM[d]}</span><span>${D.horario[d]?fmt(D.horario[d][0])+" – "+fmt(D.horario[d][1]):"Cerrado"}</span></div>`).join("")}
    ${D.notaHorario?`<div class="nota">${esc(D.notaHorario)}</div>`:""}`;
} else $("#panelHorario").remove();

/* ---------- Oficinas ---------- */
const ofs=(D.oficinas||[]).filter(o=>o.direccion);
if(ofs.length){
  let sel=0;
  const pintaOf=()=>{
    const o=ofs[sel], q=encodeURIComponent(o.direccion);
    $("#panelOficinas").innerHTML=`<h3>${ico("pin").replace("<svg>",'<svg style="width:22px;height:22px;color:var(--brass)">')}Oficinas</h3>
      ${ofs.length>1?`<div class="tabs">${ofs.map((x,i)=>`<button class="tab ${i===sel?"on":""}" data-i="${i}">${esc(x.nombre)}</button>`).join("")}</div>`:""}
      <div class="map"><iframe loading="lazy" title="Mapa" src="https://maps.google.com/maps?q=${q}&output=embed"></iframe></div>
      <div class="dir">${esc(o.direccion)}${o.referencia?`<br><small>${esc(o.referencia)}</small>`:""}</div>
      <a class="btn btn-ghost" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=${q}">Cómo llegar →</a>`;
    $("#panelOficinas").querySelectorAll(".tab").forEach(t=>t.onclick=()=>{sel=+t.dataset.i;pintaOf();});
  };
  pintaOf();
} else if(PRE){
  $("#panelOficinas").innerHTML=`<h3>Oficinas${pend()}</h3><div class="vacio">Aquí aparece el mapa de cada oficina con el botón <b>“Cómo llegar”</b>.<br>Si el despacho tiene varias sedes, se muestran en pestañas.</div>`;
} else $("#panelOficinas").remove();
if(!$("#panelHorario") && !$("#panelOficinas")) $("#ubicacion").remove();

/* ---------- FAQ ---------- */
const precioTxt = D.precioConsulta ? `La primera asesoría tiene un costo de ${D.precioConsulta}. Escríbenos y te explicamos qué incluye.` : "Escríbenos con tu caso y te informamos el costo de la primera asesoría antes de agendarla, sin compromiso.";
$("#listaFaq").innerHTML=(D.preguntas||[]).map(f=>`<div class="fq"><button>${esc(f.p)}<span class="plus">+</span></button>
  <div class="area-b"><div><p>${esc(f.r==="{precio}"?precioTxt:f.r)}</p></div></div></div>`).join("");
document.querySelectorAll(".fq>button").forEach(b=>b.onclick=()=>b.parentElement.classList.toggle("open"));

/* ---------- Cierre y contacto ---------- */
$("#telGrande").textContent=D.telefonoVisible; $("#telGrande").href=`tel:+52${D.telefono}`;
$("#guardar").onclick=()=>{
  const v=["BEGIN:VCARD","VERSION:3.0",`FN:${D.abogado}`,`ORG:${D.despacho} ${D.sufijo}`,`TITLE:${D.titulo}`,`TEL;TYPE=CELL:+52${D.telefono}`, D.correo?`EMAIL:${D.correo}`:"", `URL:${location.href.split("#")[0]}`,"END:VCARD"].filter(Boolean).join("\r\n");
  const a=document.createElement("a"); a.href=URL.createObjectURL(new Blob([v],{type:"text/vcard"}));
  a.download=`${D.despacho.replace(/\s+/g,"-")}.vcf`; a.click();
};

/* ---------- Redes ---------- */
const r=Object.entries(D.redes||{}).filter(([,u])=>u);
$("#redes").innerHTML = r.length ? r.map(([k,u])=>`<a href="${esc(u)}" target="_blank" rel="noopener" aria-label="${k}">${ico(k)}</a>`).join("")
  : (PRE?`<span class="legal">Redes sociales${pend()}</span>`:"");

/* ---------- Aviso de privacidad ---------- */
$("#avisoTxt").textContent=`${D.abogado} (${D.despacho} ${D.sufijo}) es responsable del tratamiento de los datos personales que nos proporciones.`;
function abrirAviso(){$("#aviso").classList.add("on")}
$("#abrirAviso").onclick=abrirAviso;
$("#cerrarAviso").onclick=()=>$("#aviso").classList.remove("on");
$("#aviso").onclick=e=>{if(e.target.id==="aviso")$("#aviso").classList.remove("on")};

/* ---------- Huella interactiva ---------- */
(function(){
  const svg=$("#huellaSvg"), NS="http://www.w3.org/2000/svg";
  const defs=document.createElementNS(NS,"defs");
  defs.innerHTML=`<radialGradient id="luz" cx="200" cy="200" r="150" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#e2c48f"/><stop offset=".55" stop-color="#c8a46a" stop-opacity=".55"/><stop offset="1" stop-color="#c8a46a" stop-opacity=".08"/></radialGradient>`;
  svg.appendChild(defs);
  const g=document.createElementNS(NS,"g"); svg.appendChild(g);
  // Crestas tipo huella: elipses abiertas con un ligero giro
  for(let i=0;i<22;i++){
    const rx=14+i*7.6, ry=18+i*8.6, a0=-0.9+Math.sin(i*1.7)*0.35, gap=0.5+((i*37)%10)/22;
    const pts=[];
    for(let t=a0+gap;t<a0+Math.PI*2-0.1;t+=0.05){
      const w=1+Math.sin(t*3+i)*0.025;
      pts.push(`${(200+Math.cos(t)*rx*w).toFixed(1)},${(212+Math.sin(t)*ry*w - i*0.9).toFixed(1)}`);
    }
    const p=document.createElementNS(NS,"polyline");
    p.setAttribute("points",pts.join(" ")); p.setAttribute("fill","none");
    p.setAttribute("stroke","url(#luz)"); p.setAttribute("stroke-width","1.6"); p.setAttribute("stroke-linecap","round");
    g.appendChild(p);
  }
  const grad=defs.querySelector("#luz");
  let tx=200,ty=200,cx=200,cy=200;
  const box=$("#huella");
  box.addEventListener("pointermove",e=>{const b=svg.getBoundingClientRect();tx=(e.clientX-b.left)/b.width*400;ty=(e.clientY-b.top)/b.height*400;});
  box.addEventListener("pointerleave",()=>{tx=200;ty=200});
  let t0=0;
  (function loop(t){
    if(!box.matches(":hover")){tx=200+Math.cos(t/2200)*70;ty=200+Math.sin(t/1700)*60;}
    cx+=(tx-cx)*.08; cy+=(ty-cy)*.08;
    grad.setAttribute("cx",cx); grad.setAttribute("cy",cy);
    requestAnimationFrame(loop);
  })(0);
})();

/* ---------- Animación al hacer scroll ---------- */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}}),{threshold:.12});
document.querySelectorAll(".reveal").forEach(el=>io.observe(el));
})();
