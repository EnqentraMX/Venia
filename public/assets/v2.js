/* LicLink v2 · motor de la página. Lee window.DATOS (datos.js de cada despacho). */
(function () {
  "use strict";
  const D = window.DATOS || {};
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const esc = t => String(t ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const ok = '<svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>';
  const estilo = D.estilo === "oro" ? "oro" : "vino";
  document.documentElement.dataset.estilo = estilo;
  document.querySelector('meta[name="theme-color"]').content = estilo === "oro" ? "#0c0b0a" : "#ffffff";

  /* ---------- WhatsApp y teléfono ---------- */
  const wa = msg => `https://wa.me/${D.whatsapp}?text=${encodeURIComponent(msg)}`;
  const base = `Hola, vi su página y me gustaría una asesoría.`;
  $$(".js-wa").forEach(a => { a.href = wa(base); a.target = "_blank"; a.rel = "noopener"; });
  $$(".js-tel").forEach(a => { if (D.telefono) a.href = `tel:+52${D.telefono}`; else a.remove(); });

  /* ---------- Encabezado y portada ---------- */
  if (D.propuesta) { const a = $("#aviso"); a.textContent = `Propuesta de página para ${D.propuesta} · Vista privada de LicLink`; a.hidden = false; }
  $("#firma").innerHTML = `<b>${esc(D.despacho)}</b><span>${esc(D.sufijo || "")}</span>`;
  const r = $("#retrato");
  if (D.foto) { r.innerHTML = `<img src="${esc(D.foto)}" alt="${esc(D.despacho)}">`; if (D.fotoLogo) r.classList.add("logo"); }
  else { r.classList.add("mono"); r.innerHTML = `<span>${esc(D.iniciales || D.despacho.slice(0, 2))}</span>`; }
  if (D.titulo && D.titulo !== D.sufijo) $("#cargo").textContent = D.titulo; else $("#cargo").remove();
  const t = (D.portada && D.portada.titulo) || [D.despacho];
  $("#titular").innerHTML = t.map((l, i) => i === t.length - 1 && t.length > 1 ? `<em>${esc(l)}</em>` : esc(l)).join(" ");
  $("#bajada").textContent = (D.portada && D.portada.texto) || D.descripcion || "";
  const sellos = [];
  if (D.cedula) sellos.push(`${ok}Cédula ${esc(D.cedula)}`);
  if (D.anios) sellos.push(`${ok}${esc(D.anios)} años de experiencia`);
  if (D.modalidad) sellos.push(`${ok}${esc(D.modalidad)}`);
  (D.oficinas || []).slice(0, 1).forEach(o => o.nombre && sellos.push(`<svg viewBox="0 0 24 24"><use href="#i-pin"/></svg>${esc(o.nombre)}`));
  sellos.push(`${ok}Atención confidencial`);
  $("#sellos").innerHTML = sellos.map(s => `<li>${s}</li>`).join("");
  document.title = document.title === "Despacho jurídico" ? `${D.despacho} ${D.sufijo || ""}`.trim() : document.title;

  /* Barra fija: aparece cuando los botones de la portada salen de la pantalla */
  const fija = $(".fija"), acc = $(".acciones");
  if ("IntersectionObserver" in window && fija && acc) {
    fija.classList.add("oculta");
    new IntersectionObserver(([e]) => fija.classList.toggle("oculta", e.isIntersecting || e.boundingClientRect.top > 0)).observe(acc);
  }

  /* ---------- Situaciones (hoja de mensaje) ---------- */
  const hoja = $("#hoja"); let sitActual = null;
  $("#situaciones").innerHTML = (D.situaciones || []).map((s, i) =>
    `<button class="sit${s.urgente ? " urg" : ""}" type="button" data-i="${i}"><span>${s.urgente ? "<small>Urgente</small>" : ""}${esc(s.texto)}</span><span class="flecha">→</span></button>`).join("");
  function mensaje() {
    const l = [sitActual && sitActual.urgente ? "Hola, necesito ayuda URGENTE." : base];
    const n = $("#hNombre").value.trim(), d = $("#hDetalle").value.trim();
    if (n) l.push(`Mi nombre es ${n}.`);
    if (sitActual) l.push(`• Situación: ${sitActual.texto}`);
    if (sitActual && sitActual.area) l.push(`• Tema: ${sitActual.area}`);
    if (d) l.push(`• Detalle: ${d}`);
    return l.join("\n");
  }
  const actualizar = () => { $("#hEnviar").href = wa(mensaje()); };
  function abrir(s) {
    sitActual = s; $("#hojaTitulo").textContent = s.texto;
    $("#hojaUrgente").innerHTML = s.urgente && D.telefono ? `<div class="urgente"><b>Es urgente:</b> llama directo y te atendemos de inmediato.<a class="btn" href="tel:+52${D.telefono}">Llamar al ${esc(D.telefonoVisible)}</a></div>` : "";
    hoja.hidden = false; document.body.style.overflow = "hidden"; actualizar();
    setTimeout(() => $("#hNombre").focus({ preventScroll: true }), 300);
  }
  $$(".sit").forEach(b => b.onclick = () => abrir(D.situaciones[+b.dataset.i]));
  ["#hNombre", "#hDetalle"].forEach(id => $(id).addEventListener("input", actualizar));
  function cerrar(el) { el.hidden = true; document.body.style.overflow = ""; }
  $$("[data-cerrar]").forEach(b => b.onclick = () => cerrar(b.closest(".hoja")));
  document.addEventListener("keydown", e => { if (e.key === "Escape") $$(".hoja").forEach(h => !h.hidden && cerrar(h)); });

  /* ---------- Áreas ---------- */
  $("#listaAreas").innerHTML = (D.areas || []).map((a, i) => `
    <div class="area${i === 0 ? " abierta" : ""}">
      <button type="button" aria-expanded="${i === 0}"><h3>${esc(a.nombre)}</h3><span class="mas">+</span></button>
      <div class="area-cuerpo"><div>
        <p>${esc(a.texto)}</p>
        ${(a.puntos || []).length ? `<ul>${a.puntos.map(p => `<li>${ok}<span>${esc(p)}</span></li>`).join("")}</ul>` : ""}
        <button type="button" class="consultar" data-area="${i}">Consultar sobre ${esc(a.nombre.toLowerCase())}</button>
      </div></div>
    </div>`).join("");
  $$(".area>button").forEach(b => b.onclick = () => { const a = b.parentElement, o = !a.classList.contains("abierta"); a.classList.toggle("abierta", o); b.setAttribute("aria-expanded", o); });
  $$(".consultar").forEach(b => b.onclick = () => { const a = D.areas[+b.dataset.area]; abrir({ texto: `Quiero consultar sobre ${a.nombre.toLowerCase()}`, area: a.nombre }); });

  /* ---------- Paquetes (opcional, con fecha de vencimiento) ---------- */
  const hoy = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Mexico_City" }).format(new Date());
  const paqs = (D.paquetes || []).filter(p => !p.hasta || hoy <= p.hasta);
  if (paqs.length) {
    $("#paquetes").hidden = false;
    const f = x => new Intl.DateTimeFormat("es-MX", { day: "numeric", month: "long", timeZone: "UTC" }).format(new Date(x + "T12:00:00Z"));
    $("#listaPaquetes").innerHTML = paqs.map(p => `<div class="paq${p.destacado ? " dest" : ""}">${p.hasta ? `<span class="vence">Hasta el ${f(p.hasta)}</span>` : ""}
      <h3>${esc(p.nombre)}</h3>${p.subtitulo ? `<div class="sub">${esc(p.subtitulo)}</div>` : ""}<div class="precio">${esc(p.precio)}</div>
      ${p.texto ? `<p>${esc(p.texto)}</p>` : ""}${(p.incluye || []).length ? `<ul>${p.incluye.map(i => `<li>${ok}<span>${esc(i)}</span></li>`).join("")}</ul>` : ""}
      <a class="btn btn-wa" target="_blank" rel="noopener" href="${wa(`Hola, me interesa "${p.nombre}" (${p.precio}).`)}">Preguntar por este paquete</a></div>`).join("");
  }

  /* ---------- Perfil ---------- */
  $("#frase").textContent = D.frase || "";
  $("#nombreAbogado").textContent = D.abogado || D.despacho;
  $("#rolAbogado").textContent = D.descripcion || D.titulo || "";
  $("#compromisos").innerHTML = (D.compromisos || []).map(c => `<li>${ok}<span>${esc(c)}</span></li>`).join("");
  if (D.cedula) { const v = $("#verificar"); v.hidden = false; v.innerHTML = `Cédula profesional <b>${esc(D.cedula)}</b> · Verifícala en el Registro Nacional de Profesionistas`; }

  /* ---------- Ubicación y horario ---------- */
  const ofs = (D.oficinas || []).filter(o => o.direccion);
  $("#oficinas").innerHTML = ofs.map(o => { const q = encodeURIComponent(o.direccion); return `<div class="ofi">
    <div class="mapa"><iframe loading="lazy" title="Mapa" src="https://maps.google.com/maps?q=${q}&z=15&output=embed"></iframe></div>
    <p>${esc(o.direccion)}${o.referencia ? `<small>${esc(o.referencia)}</small>` : ""}</p>
    <a class="btn btn-linea" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=${q}">Cómo llegar</a></div>`; }).join("");
  const DIAS = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"], NOM = { lunes: "Lunes", martes: "Martes", miercoles: "Miércoles", jueves: "Jueves", viernes: "Viernes", sabado: "Sábado", domingo: "Domingo" };
  const H = D.horario && DIAS.some(d => D.horario[d]) ? D.horario : null;
  if (H) {
    const p = new Intl.DateTimeFormat("en-US", { timeZone: "America/Mexico_City", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).formatToParts(new Date());
    const g = x => p.find(y => y.type === x).value, dia = DIAS[["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(g("weekday"))], min = (+g("hour") % 24) * 60 + +g("minute");
    const m = s => { const [h, mm] = s.split(":"); return +h * 60 + +mm; }, hh = s => { let [h, mm] = s.split(":").map(Number); const a = h >= 12 ? "pm" : "am"; h = h % 12 || 12; return `${h}:${String(mm).padStart(2, "0")} ${a}`; };
    const hoyH = H[dia], abierto = hoyH && min >= m(hoyH[0]) && min < m(hoyH[1]), todoDia = hoyH && hoyH[0] === "00:00" && hoyH[1] >= "23:59";
    const e = $("#estado"); e.hidden = false; e.querySelector("i").classList.toggle("on", !!abierto);
    e.querySelector("span").textContent = abierto ? (todoDia ? "Abierto 24 h" : "Abierto ahora") : "Cerrado ahora";
    const orden = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"], todo = orden.every(d => H[d] && H[d][0] === "00:00");
    const h = $("#horario"); h.hidden = false;
    h.innerHTML = (todo ? `<div class="hoy"><span>Todos los días</span><span>24 horas</span></div>` : orden.map(d => `<div class="${d === dia ? "hoy" : ""}"><span>${NOM[d]}</span><span>${H[d] ? hh(H[d][0]) + " – " + hh(H[d][1]) : "Cerrado"}</span></div>`).join("")) + (D.notaHorario ? `<p>${esc(D.notaHorario)}</p>` : "");
  } else if (D.notaHorario) { const h = $("#horario"); h.hidden = false; h.innerHTML = `<p>${esc(D.notaHorario)}</p>`; }
  if (!ofs.length && !H && !D.notaHorario) $("#ubicacion").remove();

  /* ---------- Preguntas ---------- */
  const precio = D.precioConsulta ? `La primera consulta: ${D.precioConsulta}. Escríbenos y te explicamos qué incluye.` : "Escríbenos con tu caso y te informamos el costo antes de agendar, sin compromiso.";
  $("#faq").innerHTML = (D.preguntas || []).map(f => `<details><summary>${esc(f.p)}</summary><p>${esc(f.r === "{precio}" ? precio : f.r)}</p></details>`).join("");
  if (!(D.preguntas || []).length) $("#preguntas").remove();

  /* ---------- Pie, redes, privacidad, contacto ---------- */
  const redes = Object.entries(D.redes || {}).filter(([k, u]) => u && ["facebook", "instagram", "tiktok"].includes(k));
  $("#redes").innerHTML = redes.map(([k, u]) => `<a href="${esc(u)}" target="_blank" rel="noopener" aria-label="${k}"><svg viewBox="0 0 24 24"><use href="#i-${k}"/></svg></a>`).join("");
  $("#pieTxt").textContent = `${D.despacho} ${D.sufijo || ""}${D.telefonoVisible ? " · " + D.telefonoVisible : ""}`;
  $("#privTxt").textContent = `${D.abogado || D.despacho} es responsable del tratamiento de los datos personales que nos proporciones.`;
  $("#abrirPrivacidad").onclick = () => { $("#privacidad").hidden = false; };
  $("#guardar").onclick = () => {
    const v = ["BEGIN:VCARD", "VERSION:3.0", `FN:${D.abogado || D.despacho}`, `ORG:${D.despacho} ${D.sufijo || ""}`, D.telefono ? `TEL;TYPE=CELL:+52${D.telefono}` : "", D.correo ? `EMAIL:${D.correo}` : "", `URL:${location.href.split("#")[0]}`, "END:VCARD"].filter(Boolean).join("\r\n");
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([v], { type: "text/vcard" })); a.download = `${D.despacho.replace(/\W+/g, "-")}.vcf`; a.click();
  };
})();
