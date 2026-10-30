/* Castillo & Abogados · funcionamiento del sitio
   Los datos editables (promoción, aviso, precios, teléfonos y horario) viven en assets/contenido.json
   y se cambian desde el panel administrativo. Si ese archivo no carga, se usan los valores de abajo. */
(function () {
  "use strict";
  const BASE = {
    contacto: { whatsapp: "528111571262", celular: "81 1157 1262", oficina: "81 4264 4556", correo: "her_cas@yahoo.com" },
    precios: { presencial: 1000, nacional: 1000, internacional: 1500 },
    promocion: { activa: false, etiqueta: "Promoción", titulo: "", texto: "", boton: "Quiero aprovecharla", mensaje: "", desde: "", hasta: "" },
    aviso: { activo: false, texto: "" },
    horario: { lunes: null, martes: null, miercoles: null, jueves: null, viernes: null, sabado: null, domingo: null },
    notaHorario: ""
  };
  const S = window.SITIO || { raiz: "", vista: false };
  const ZONA = "America/Monterrey";
  const DIAS = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];
  const NOMBRE = { lunes: "Lunes", martes: "Martes", miercoles: "Miércoles", jueves: "Jueves", viernes: "Viernes", sabado: "Sábado", domingo: "Domingo" };
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const esc = t => String(t ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const digitos = t => String(t || "").replace(/\D/g, "");
  const dinero = n => "$" + Number(n || 0).toLocaleString("en-US");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let K = JSON.parse(JSON.stringify(BASE));

  function mezclar(a, b) { for (const k in b) { if (b[k] && typeof b[k] === "object" && !Array.isArray(b[k]) && a[k] && typeof a[k] === "object") mezclar(a[k], b[k]); else if (b[k] !== undefined) a[k] = b[k]; } return a; }
  const esVistaPrevia = () => /netlify\.app$|^localhost$|^127\.0\.0\.1$/.test(location.hostname);

  /* ---------- hora de Monterrey ---------- */
  function ahora() {
    const p = new Intl.DateTimeFormat("en-CA", { timeZone: ZONA, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false, weekday: "short" }).formatToParts(new Date());
    const g = t => p.find(x => x.type === t).value;
    const fecha = `${g("year")}-${g("month")}-${g("day")}`;
    return { fecha, dia: DIAS[["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(g("weekday"))], min: (+g("hour") % 24) * 60 + +g("minute") };
  }
  const aMin = t => { const [h, m] = t.split(":"); return +h * 60 + +m; };
  const fmtHora = t => { let [h, m] = t.split(":").map(Number); const s = h >= 12 ? "pm" : "am"; h = h % 12 || 12; return `${h}:${String(m).padStart(2, "0")} ${s}`; };
  const hayHorario = () => DIAS.some(d => Array.isArray(K.horario[d]));
  function sumarDias(fecha, n) { const [y, m, d] = fecha.split("-").map(Number); const x = new Date(Date.UTC(y, m - 1, d + n, 12)); return { fecha: x.toISOString().slice(0, 10), dia: DIAS[x.getUTCDay()], num: x.getUTCDate(), mes: x.getUTCMonth() }; }
  const MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];

  /* ---------- aplicar datos editables ---------- */
  function aplicar() {
    const c = K.contacto;
    $$(".js-tel").forEach(a => { const n = c[a.dataset.tel]; if (!n) return; a.href = "tel:+52" + digitos(n);
      const sp = a.querySelector("span"); const txt = a.dataset.tel === "celular" && a.classList.contains("cab-tel-m") ? "Llamar al " + n : n;
      if (sp) a.firstChild.nodeValue = n; else if (!a.querySelector("svg")) a.textContent = txt; });
    $$("[data-correo]").forEach(a => { a.textContent = c.correo; if (a.tagName === "A") a.href = "mailto:" + c.correo; });
    $$("[data-precio]").forEach(x => { const v = K.precios[x.dataset.precio]; if (v != null) x.textContent = dinero(v); });
    $$(".js-wa").forEach(a => { a.href = wa(MENSAJES[a.dataset.msg] || MENSAJES.general); a.target = "_blank"; a.rel = "noopener"; });
    // aviso superior
    const av = $("#avisoBarra");
    if (av) { if (K.aviso.activo && K.aviso.texto) { av.textContent = K.aviso.texto; av.hidden = false; } else av.hidden = true; }
    pintarPromo(); pintarEstado(); pintarHorario();
  }
  const MENSAJES = {
    general: "Hola, vi su página y me gustaría una asesoría legal.",
    corresponsalia: "Hola, soy abogado(a) foráneo(a) y necesito corresponsalía en Monterrey para un asunto."
  };
  const wa = msg => `https://wa.me/${digitos(K.contacto.whatsapp)}?text=${encodeURIComponent(msg)}`;

  /* ---------- promoción ---------- */
  let reloj = null;
  function promoVigente() {
    const p = K.promocion, hoy = ahora().fecha;
    return p.activa && p.titulo && (!p.desde || hoy >= p.desde) && (!p.hasta || hoy <= p.hasta);
  }
  function pintarPromo() {
    const cajas = $$("[data-promo]"); if (!cajas.length) return;
    clearInterval(reloj);
    if (!promoVigente()) { cajas.forEach(x => x.innerHTML = ""); return; }
    const p = K.promocion, msg = p.mensaje || `Hola, me interesa la promoción: ${p.titulo}.`;
    cajas.forEach(x => {
      if (x.dataset.promo === "fina") {
        x.innerHTML = `<div class="promo-fina"><b>${esc(p.etiqueta || "Promoción")}:</b> ${esc(p.titulo)}. <a href="${wa(msg)}" target="_blank" rel="noopener">${esc(p.boton || "Quiero aprovecharla")}</a></div>`;
      } else {
        x.innerHTML = `<section class="promo" aria-label="Promoción"><div class="promo-caja">
          <span class="promo-etq">${esc(p.etiqueta || "Promoción")}</span>
          <div><h2>${esc(p.titulo)}</h2>${p.texto ? `<p>${esc(p.texto)}</p>` : ""}${p.hasta ? `<div class="cuenta" aria-label="Tiempo restante"></div>` : ""}</div>
          <a class="btn btn-oro" href="${wa(msg)}" target="_blank" rel="noopener">${esc(p.boton || "Quiero aprovecharla")}</a></div></section>`;
      }
    });
    if (p.hasta) {
      const fin = new Date(p.hasta + "T23:59:59-06:00").getTime();
      const tic = () => {
        let s = Math.max(0, Math.floor((fin - Date.now()) / 1000));
        const d = Math.floor(s / 86400); s %= 86400; const h = Math.floor(s / 3600); s %= 3600; const m = Math.floor(s / 60);
        $$(".cuenta").forEach(c => c.innerHTML = `<span><b>${d}</b>días</span><span><b>${h}</b>horas</span><span><b>${m}</b>min</span>`);
      };
      tic(); reloj = setInterval(tic, 30000);
    }
  }

  /* ---------- estado abierto/cerrado y horario ---------- */
  function pintarEstado() {
    const el = $("#estado"); if (!el) return;
    if (!hayHorario()) { el.hidden = true; return; }
    const n = ahora(), hoy = K.horario[n.dia];
    const abierto = hoy && n.min >= aMin(hoy[0]) && n.min < aMin(hoy[1]);
    let sub = "";
    if (abierto) sub = "Abierto · cierra " + fmtHora(hoy[1]);
    else for (let k = 0; k < 8; k++) { const d = sumarDias(n.fecha, k), hr = K.horario[d.dia]; if (!hr) continue; if (k === 0 && n.min >= aMin(hr[0])) continue; sub = `Cerrado · abre ${k === 0 ? "hoy" : k === 1 ? "mañana" : NOMBRE[d.dia].toLowerCase()} ${fmtHora(hr[0])}`; break; }
    el.querySelector("i").classList.toggle("abierto", !!abierto); el.querySelector("span").textContent = sub; el.hidden = false;
  }
  function pintarHorario() {
    const b = $("#horarioBloque"); if (!b) return;
    if (!hayHorario()) { b.hidden = true; return; }
    const hoy = ahora().dia;
    $("#horarioTabla").innerHTML = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"].map(d =>
      `<div class="${d === hoy ? "hoy" : ""}"><span>${NOMBRE[d]}</span><span>${K.horario[d] ? fmtHora(K.horario[d][0]) + " – " + fmtHora(K.horario[d][1]) : "Cerrado"}</span></div>`).join("") +
      (K.notaHorario ? `<p style="margin-top:10px;font-size:15px;color:var(--oro-claro)">${esc(K.notaHorario)}</p>` : "");
    b.hidden = false;
  }

  /* ---------- menú en celular ---------- */
  const cajon = $("#cajon"), abrir = $("#abrirMenu");
  if (cajon && abrir) {
    const cerrar = () => { cajon.classList.remove("abierto"); abrir.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; };
    abrir.onclick = () => { cajon.classList.add("abierto"); abrir.setAttribute("aria-expanded", "true"); document.body.style.overflow = "hidden"; $("#cerrarMenu").focus(); };
    $("#cerrarMenu").onclick = cerrar;
    $$("a", cajon).forEach(a => a.addEventListener("click", cerrar));
    document.addEventListener("keydown", ev => { if (ev.key === "Escape") cerrar(); });
  }

  /* ---------- áreas de práctica ---------- */
  const datosAreas = $("#areasDatos");
  if (datosAreas) {
    const paneles = $$("article", datosAreas.content);
    const lista = $("#areasLista"), panel = $("#areasPanel"), acordeon = $("#areasAcordeon");
    const pie = n => `<div class="area-pie"><p>¿Su asunto es de ${esc(n.toLowerCase())}? Cuéntenoslo y le decimos cómo podemos ayudarle.</p><button type="button" class="btn btn-oro js-consultar" data-area="${esc(n)}">Consultar este asunto</button></div>`;
    const mostrar = i => {
      $$("button", lista).forEach((b, k) => { b.setAttribute("aria-selected", k === i); b.tabIndex = k === i ? 0 : -1; });
      panel.innerHTML = ""; const c = paneles[i].cloneNode(true); c.setAttribute("role", "tabpanel"); c.setAttribute("aria-labelledby", "tab-" + i);
      c.insertAdjacentHTML("beforeend", pie(paneles[i].dataset.area)); panel.appendChild(c);
    };
    paneles.forEach((art, i) => {
      const n = art.dataset.area, b = document.createElement("button");
      b.type = "button"; b.setAttribute("role", "tab"); b.id = "tab-" + i; b.textContent = n; b.setAttribute("aria-controls", "areasPanel");
      b.onclick = () => mostrar(i);
      b.onkeydown = ev => { if (ev.key === "ArrowDown" || ev.key === "ArrowUp") { ev.preventDefault(); const k = (i + (ev.key === "ArrowDown" ? 1 : -1) + paneles.length) % paneles.length; mostrar(k); $("#tab-" + k).focus(); } };
      lista.appendChild(b);
      const d = document.createElement("details"); d.innerHTML = `<summary>${esc(n)}<span class="mas">+</span></summary>`;
      const c = art.cloneNode(true); c.insertAdjacentHTML("beforeend", pie(n)); d.appendChild(c); acordeon.appendChild(d);
    });
    mostrar(0);
  }

  /* ---------- asistente "Cuéntenos su caso" con agenda ---------- */
  const caja = $("#asistente");
  const AREAS = ["Derecho familiar", "Derecho civil", "Derecho mercantil", "Juicio de amparo", "Nulidad de matrimonio católico", "Corresponsalía (soy abogado foráneo)", "Trámites en Monterrey", "No estoy seguro"];
  const URG = [{ t: "Hay un embargo, desalojo o detención en curso", u: true }, { t: "Tengo una fecha, citatorio o audiencia próxima", u: false }, { t: "Quiero asesoría para decidir qué hacer", u: false }];
  const TIPOS = () => [
    { t: "Presencial", d: "En la oficina del Centro de Monterrey", c: dinero(K.precios.presencial) },
    { t: "En línea desde México", d: "Videollamada por WhatsApp o Facebook", c: dinero(K.precios.nacional) },
    { t: "En línea desde otro país", d: "Videollamada internacional", c: dinero(K.precios.internacional) }];
  let st = { paso: 0 };
  function dias() {
    const n = ahora(), out = [];
    for (let k = 0; k < 21 && out.length < 8; k++) {
      const d = sumarDias(n.fecha, k), hr = K.horario[d.dia]; if (!hr) continue;
      const horas = []; for (let m = aMin(hr[0]); m + 60 <= aMin(hr[1]); m += 60) { if (k === 0 && m < n.min + 60) continue; horas.push(`${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`); }
      if (horas.length) out.push({ ...d, horas, etiqueta: k === 0 ? "Hoy" : k === 1 ? "Mañana" : NOMBRE[d.dia].slice(0, 3) });
    }
    return out;
  }
  function pintar() {
    if (!caja) return;
    if (st.paso === 0 && st.area) st.paso = 1;
    if (st.paso === 2 && st.tipo) st.paso = 3;
    const pasos = 4, av = `<div class="avance"><i style="width:${(Math.min(st.paso, pasos) + 1) / (pasos + 1) * 100}%"></i></div>`;
    const atras = p => `<button type="button" class="atras" data-ir="${p}">Atrás</button>`;
    let h = av;
    if (st.paso === 0) h += `<div class="paso-n">Pregunta 1 de 4</div><div class="pregunta">¿De qué trata su asunto?</div><div class="opciones">${AREAS.map(a => `<button type="button" class="opcion" data-v="${esc(a)}">${esc(a)}</button>`).join("")}</div>`;
    else if (st.paso === 1) h += `<div class="paso-n">Pregunta 2 de 4</div><div class="pregunta">¿Qué tan urgente es?</div><div class="opciones">${URG.map((u, i) => `<button type="button" class="opcion" data-i="${i}">${esc(u.t)}${u.u ? '<span class="etq">Urgente</span>' : ""}</button>`).join("")}</div><div class="asis-pie">${atras(0)}</div>`;
    else if (st.paso === 2) h += `<div class="paso-n">Pregunta 3 de 4</div><div class="pregunta">¿Cómo prefiere su asesoría?</div><div class="opciones">${TIPOS().map((t, i) => `<button type="button" class="opcion" data-i="${i}"><span>${esc(t.t)}<small>${esc(t.d)}</small></span><span class="costo">${t.c}</span></button>`).join("")}</div><div class="asis-pie">${atras(1)}</div>`;
    else if (st.paso === 3) {
      const ds = hayHorario() ? dias() : [];
      if (st.fecha && !ds.find(d => d.fecha === st.fecha)) { st.fecha = null; st.hora = null; }
      const dSel = ds.find(d => d.fecha === st.fecha);
      const agenda = ds.length ? `<div class="etq-campo">Elija el día y la hora que prefiere (opcional)</div>
        <div class="dias">${ds.map(d => `<button type="button" class="dia" data-f="${d.fecha}" aria-pressed="${d.fecha === st.fecha}">${d.etiqueta}<b>${d.num}</b>${MESES[d.mes]}</button>`).join("")}</div>
        ${dSel ? `<div class="horas">${dSel.horas.map(x => `<button type="button" class="hora" data-h="${x}" aria-pressed="${x === st.hora}">${fmtHora(x)}</button>`).join("")}</div>` : ""}`
        : `<div class="campo"><label for="fCuando">¿Cuándo le gustaría su asesoría?</label><select id="fCuando">${["Lo antes posible", "Esta semana", "La próxima semana"].map(o => `<option${st.cuando === o ? " selected" : ""}>${o}</option>`).join("")}</select></div>`;
      h += `<div class="paso-n">Pregunta 4 de 4</div><div class="pregunta">Sus datos para agendar</div>
        ${st.urgente ? `<div class="urgente"><b>Su asunto es urgente.</b> Llámenos directamente para atenderle de inmediato.<br><a class="btn btn-rojo" href="tel:+52${digitos(K.contacto.celular)}">Llamar al ${esc(K.contacto.celular)}</a></div>` : ""}
        <div class="campo"><label for="fNombre">Su nombre</label><input id="fNombre" autocomplete="name" maxlength="80" value="${esc(st.nombre || "")}"></div>
        <div class="campo"><label for="fCiudad">¿Desde qué ciudad nos escribe?</label><input id="fCiudad" maxlength="80" value="${esc(st.ciudad || "")}" placeholder="Ej. San Nicolás de los Garza, N.L."></div>
        ${agenda}
        <div class="campo"><label for="fDetalle">En pocas palabras, ¿qué pasó? (opcional)</label><textarea id="fDetalle" maxlength="600">${esc(st.detalle || "")}</textarea></div>
        <div class="asis-pie">${atras(2)}<button type="button" class="btn btn-oro" id="verResumen">Ver mi mensaje</button></div>`;
    } else {
      const m = mensaje();
      h += `<div class="pregunta" style="margin-top:0">Este es el mensaje que nos enviará</div><div class="resumen">${esc(m)}</div>
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <a class="btn btn-wa" href="${wa(m)}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>Enviar por WhatsApp</a>
          <a class="btn btn-borde" href="mailto:${esc(K.contacto.correo)}?subject=${encodeURIComponent("Solicitud de asesoría · " + (st.area || ""))}&body=${encodeURIComponent(m)}">Enviar por correo</a>
          ${st.urgente ? `<a class="btn btn-rojo" href="tel:+52${digitos(K.contacto.celular)}">Llamar ahora</a>` : ""}
        </div>
        <p class="fino">Al enviarlo acepta nuestro <button type="button" class="js-abrir-aviso">aviso de privacidad</button>.</p>
        <div class="asis-pie">${atras(3)}<button type="button" class="atras" id="reiniciar">Empezar de nuevo</button></div>`;
    }
    caja.innerHTML = h;
    $$(".opcion", caja).forEach(o => o.onclick = () => {
      if (st.paso === 0) { st.area = o.dataset.v; st.paso = 1; }
      else if (st.paso === 1) { const u = URG[+o.dataset.i]; st.urgencia = u.t; st.urgente = u.u; st.paso = 2; }
      else if (st.paso === 2) { st.tipo = TIPOS()[+o.dataset.i].t; st.paso = 3; }
      pintar(); const f = $(".opcion, input, .dia", caja); if (f) f.focus({ preventScroll: true });
    });
    $$(".dia", caja).forEach(b => b.onclick = () => { guardar(); st.fecha = b.dataset.f; st.hora = null; pintar(); });
    $$(".hora", caja).forEach(b => b.onclick = () => { guardar(); st.hora = b.dataset.h; pintar(); });
    $$("[data-ir]", caja).forEach(b => b.onclick = () => { guardar(); const p = +b.dataset.ir; if (p <= 0) st.area = null; if (p <= 2) st.tipo = null; st.paso = p; pintar(); });
    const v = $("#verResumen", caja); if (v) v.onclick = () => { guardar(); st.paso = 4; pintar(); };
    const r = $("#reiniciar", caja); if (r) r.onclick = () => { st = { paso: 0 }; pintar(); };
  }
  function guardar() {
    const g = id => { const x = $("#" + id, caja); return x ? x.value.trim() : undefined; };
    if ($("#fNombre", caja)) { st.nombre = g("fNombre"); st.ciudad = g("fCiudad"); st.detalle = g("fDetalle"); if ($("#fCuando", caja)) st.cuando = g("fCuando"); }
  }
  function mensaje() {
    const l = [st.urgente ? "Hola, necesito atención URGENTE." : "Hola, me gustaría agendar una asesoría."];
    if (st.nombre) l.push(`Mi nombre es ${st.nombre}.`);
    l.push(`• Asunto: ${st.area}`);
    if (st.urgencia) l.push(`• Situación: ${st.urgencia}`);
    const t = TIPOS().find(x => x.t === st.tipo); l.push(`• Asesoría: ${st.tipo}${t ? ` (${t.c})` : ""}`);
    if (st.fecha) { const [y, m, d] = st.fecha.split("-").map(Number); const dd = new Date(Date.UTC(y, m - 1, d, 12));
      l.push(`• Fecha preferida: ${NOMBRE[DIAS[dd.getUTCDay()]]} ${d} de ${["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"][m - 1]}${st.hora ? ", " + fmtHora(st.hora) : ""}`); }
    else if (st.cuando) l.push(`• Cuándo: ${st.cuando}`);
    if (st.ciudad) l.push(`• Desde: ${st.ciudad}`);
    if (st.detalle) l.push(`• Detalle: ${st.detalle}`);
    return l.join("\n");
  }
  function iniciar(pre, ir) {
    st = { paso: 0, ...pre }; pintar();
    if (ir !== false) $("#caso").scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
  }
  document.addEventListener("click", ev => {
    const c = ev.target.closest(".js-consultar"); if (c && caja) { iniciar({ area: c.dataset.area }); }
    const g = ev.target.closest(".js-agendar"); if (g && caja) { ev.preventDefault(); iniciar({ tipo: g.dataset.tipo }); }
    if (ev.target.closest(".js-abrir-aviso")) abrirAviso();
  });

  /* ---------- preguntas: buscador y filtros ---------- */
  const buscar = $("#buscarFaq");
  if (buscar) {
    const items = $$("#faq details"), filtros = $$("#filtrosFaq button"); let cat = "";
    const norm = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
    const filtrar = () => {
      const q = norm(buscar.value.trim()); let n = 0;
      items.forEach(d => { const okk = (!cat || d.dataset.cat === cat) && (!q || norm(d.textContent).includes(q)); d.hidden = !okk; if (okk) n++; if (q && okk) d.open = true; else if (!q) d.open = false; });
      $("#sinResultados").hidden = n > 0;
    };
    buscar.addEventListener("input", filtrar);
    filtros.forEach(b => b.onclick = () => { cat = b.dataset.cat; filtros.forEach(x => x.setAttribute("aria-pressed", x === b)); filtrar(); });
  }

  /* ---------- guardar contacto ---------- */
  const gc = $("#guardarContacto");
  if (gc) gc.onclick = () => {
    const c = K.contacto;
    const v = ["BEGIN:VCARD", "VERSION:3.0", "FN:Castillo & Abogados", "ORG:Castillo & Abogados", `TEL;TYPE=CELL:+52${digitos(c.celular)}`, `TEL;TYPE=WORK:+52${digitos(c.oficina)}`, `EMAIL:${c.correo}`,
      "ADR;TYPE=WORK:;;Dr. Julián Villarreal 705 Nte., Planta Baja;Monterrey;N.L.;64000;México", "URL:https://www.abogadosenmonterrey.com/", "END:VCARD"].join("\r\n");
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([v], { type: "text/vcard" })); a.download = "Castillo-y-Abogados.vcf"; a.click();
  };

  /* ---------- aviso de privacidad ---------- */
  const modal = $("#aviso");
  function abrirAviso() { modal.classList.add("abierto"); $("#cerrarAviso").focus(); }
  $("#cerrarAviso").onclick = () => modal.classList.remove("abierto");
  modal.onclick = ev => { if (ev.target === modal) modal.classList.remove("abierto"); };
  document.addEventListener("keydown", ev => { if (ev.key === "Escape") modal.classList.remove("abierto"); });
  $("#anio").textContent = new Date().getFullYear();

  /* ---------- arranque ---------- */
  aplicar(); pintar();
  fetch(S.raiz + "assets/contenido.json?t=" + Date.now(), { cache: "no-store" })
    .then(r => r.ok ? r.json() : null).catch(() => null)
    .then(json => {
      if (json) mezclar(K, json);
      if (esVistaPrevia()) { try { const d = localStorage.getItem("castillo_contenido_demo"); if (d) mezclar(K, JSON.parse(d)); } catch (_) {} }
      aplicar(); if (st.paso === 0) pintar();
      setInterval(pintarEstado, 60000);
    });
})();
