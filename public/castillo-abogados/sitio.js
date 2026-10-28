/* Castillo & Abogados · funcionamiento del sitio
   Para cambiar teléfonos, WhatsApp o dirección, edite solo CONFIG. */
const CONFIG = {
  vistaPrevia: true,                 // false al publicar en su dominio (quita el aviso superior)
  whatsapp: "528111571262",          // 52 + 10 dígitos
  celular: "+528111571262",
  celularVisible: "81 1157 1262",
  oficina: "+528142644556",
  correo: "her_cas@yahoo.com",
  direccion: "Dr. Julián Villarreal 705 Nte, Centro, 64000 Monterrey, N.L.",
  despacho: "Castillo & Abogados"
};

(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const esc = t => String(t ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const wa = msg => `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(msg)}`;

  if (!CONFIG.vistaPrevia) $("#propuesta").remove();
  $("#anio").textContent = new Date().getFullYear();

  /* ---------- WhatsApp con mensaje según el botón ---------- */
  const MENSAJES = {
    general: "Hola, vi su página y me gustaría una asesoría legal.",
    corresponsalia: "Hola, soy abogado(a) foráneo(a) y necesito corresponsalía en Monterrey para un asunto."
  };
  $$(".js-wa").forEach(a => { a.href = wa(MENSAJES[a.dataset.msg] || MENSAJES.general); a.target = "_blank"; a.rel = "noopener"; });

  /* ---------- Áreas: pestañas en computadora, acordeón en celular ---------- */
  const paneles = $$("article", $("#areasDatos").content);
  const lista = $("#areasLista"), panel = $("#areasPanel"), acordeon = $("#areasAcordeon");
  const pie = nombre => `<div class="area-pie"><p>¿Su asunto es de ${esc(nombre.toLowerCase())}? Cuéntenoslo y le decimos cómo podemos ayudarle.</p>
    <button type="button" class="btn btn-oro js-consultar" data-area="${esc(nombre)}">Consultar este asunto</button></div>`;
  paneles.forEach((art, i) => {
    const nombre = art.dataset.area;
    const b = document.createElement("button");
    b.type = "button"; b.role = "tab"; b.id = "tab-" + i; b.textContent = nombre;
    b.setAttribute("aria-selected", i === 0); b.setAttribute("aria-controls", "areasPanel");
    b.onclick = () => mostrar(i);
    b.onkeydown = e => { if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); const n = (i + (e.key === "ArrowDown" ? 1 : -1) + paneles.length) % paneles.length; mostrar(n); $("#tab-" + n).focus(); } };
    lista.appendChild(b);
    const d = document.createElement("details");
    d.innerHTML = `<summary>${esc(nombre)}<span class="mas">+</span></summary>`;
    const copia = art.cloneNode(true); copia.insertAdjacentHTML("beforeend", pie(nombre)); d.appendChild(copia);
    acordeon.appendChild(d);
  });
  function mostrar(i) {
    $$("button", lista).forEach((b, k) => b.setAttribute("aria-selected", k === i));
    panel.innerHTML = ""; const copia = paneles[i].cloneNode(true);
    copia.setAttribute("role", "tabpanel"); copia.setAttribute("aria-labelledby", "tab-" + i);
    copia.insertAdjacentHTML("beforeend", pie(paneles[i].dataset.area)); panel.appendChild(copia);
  }
  mostrar(0);
  document.addEventListener("click", e => {
    const c = e.target.closest(".js-consultar"); if (c) { iniciar({ area: c.dataset.area }); }
    const g = e.target.closest(".js-agendar"); if (g) { iniciar({ tipo: g.dataset.tipo }); }
  });

  /* ---------- Asistente "Cuéntenos su caso" ---------- */
  const AREAS = ["Derecho familiar", "Derecho civil", "Derecho mercantil", "Juicio de amparo", "Nulidad de matrimonio católico", "Trámites en Monterrey", "No estoy seguro"];
  const URGENCIA = [
    { t: "Hay un embargo, desalojo o detención en curso", u: true },
    { t: "Tengo una fecha, citatorio o audiencia próxima", u: false },
    { t: "Quiero asesoría para decidir qué hacer", u: false }
  ];
  const TIPOS = [
    { t: "Presencial", d: "En la oficina del Centro de Monterrey", c: "$1,000" },
    { t: "En línea desde México", d: "Videollamada por WhatsApp o Facebook", c: "$1,000" },
    { t: "En línea desde otro país", d: "Videollamada internacional", c: "$1,500" }
  ];
  const caja = $("#asistente");
  let e = { paso: 0 };
  const PASOS = 4;
  const avance = () => `<div class="avance"><i style="width:${Math.min(e.paso + 1, PASOS + 1) / (PASOS + 1) * 100}%"></i></div>`;
  const atras = p => `<button type="button" class="atras" data-ir="${p}">Atrás</button>`;

  function siguientePaso() { // salta preguntas ya respondidas desde otro botón
    if (e.paso === 0 && e.area) e.paso = 1;
    if (e.paso === 2 && e.tipo) e.paso = 3;
  }
  function pintar() {
    siguientePaso();
    let h = avance();
    if (e.paso === 0) {
      h += `<div class="paso-n">Pregunta 1 de 4</div><div class="pregunta">¿De qué trata su asunto?</div><div class="opciones">
        ${AREAS.map(a => `<button type="button" class="opcion" data-v="${esc(a)}">${esc(a)}</button>`).join("")}</div>`;
    } else if (e.paso === 1) {
      h += `<div class="paso-n">Pregunta 2 de 4</div><div class="pregunta">¿Qué tan urgente es?</div><div class="opciones">
        ${URGENCIA.map((u, i) => `<button type="button" class="opcion" data-i="${i}">${esc(u.t)}${u.u ? '<span class="etq">Urgente</span>' : ""}</button>`).join("")}</div>
        <div class="asis-pie">${atras(0)}</div>`;
    } else if (e.paso === 2) {
      h += `<div class="paso-n">Pregunta 3 de 4</div><div class="pregunta">¿Cómo prefiere su asesoría?</div><div class="opciones">
        ${TIPOS.map((t, i) => `<button type="button" class="opcion" data-i="${i}"><span>${esc(t.t)}<small>${esc(t.d)}</small></span><span class="costo">${t.c}</span></button>`).join("")}</div>
        <div class="asis-pie">${atras(1)}</div>`;
    } else if (e.paso === 3) {
      h += `<div class="paso-n">Pregunta 4 de 4</div><div class="pregunta">Sus datos para agendar</div>
        ${e.urgente ? `<div class="urgente"><b>Su asunto es urgente.</b> Llámenos directamente para atenderle de inmediato.<br><a class="btn btn-rojo" href="tel:${CONFIG.celular}">Llamar al ${CONFIG.celularVisible}</a></div>` : ""}
        <div class="campo"><label for="fNombre">Su nombre</label><input id="fNombre" autocomplete="name" value="${esc(e.nombre || "")}"></div>
        <div class="campo"><label for="fCiudad">¿Desde qué ciudad nos escribe?</label><input id="fCiudad" value="${esc(e.ciudad || "")}" placeholder="Ej. San Nicolás de los Garza, N.L."></div>
        <div class="campo"><label for="fCuando">¿Cuándo le gustaría su asesoría?</label><select id="fCuando">
          ${["Lo antes posible", "Esta semana", "La próxima semana"].map(o => `<option${e.cuando === o ? " selected" : ""}>${o}</option>`).join("")}</select></div>
        <div class="campo"><label for="fDetalle">En pocas palabras, ¿qué pasó? (opcional)</label><textarea id="fDetalle">${esc(e.detalle || "")}</textarea></div>
        <div class="asis-pie">${atras(2)}<button type="button" class="btn btn-oro" id="verResumen">Ver mi mensaje</button></div>`;
    } else {
      const msg = mensaje();
      h += `<div class="pregunta" style="margin-top:0">Este es el mensaje que nos enviará</div>
        <div class="resumen">${esc(msg)}</div>
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <a class="btn btn-wa" href="${wa(msg)}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>Enviar por WhatsApp</a>
          ${e.urgente ? `<a class="btn btn-rojo" href="tel:${CONFIG.celular}">Llamar ahora</a>` : ""}
        </div>
        <p class="fino">Al enviarlo acepta nuestro <button type="button" class="js-aviso">aviso de privacidad</button>.</p>
        <div class="asis-pie">${atras(3)}<button type="button" class="atras" id="reiniciar">Empezar de nuevo</button></div>`;
    }
    caja.innerHTML = h;
    $$(".opcion", caja).forEach(o => o.onclick = () => {
      if (e.paso === 0) { e.area = o.dataset.v; e.paso = 1; }
      else if (e.paso === 1) { const u = URGENCIA[+o.dataset.i]; e.urgencia = u.t; e.urgente = u.u; e.paso = 2; }
      else if (e.paso === 2) { e.tipo = TIPOS[+o.dataset.i].t; e.paso = 3; }
      pintar();
    });
    $$("[data-ir]", caja).forEach(b => b.onclick = () => {
      guardarCampos(); const p = +b.dataset.ir;
      if (p <= 0) e.area = null; if (p <= 2) e.tipo = null;
      e.paso = p; pintar();
    });
    const v = $("#verResumen", caja); if (v) v.onclick = () => { guardarCampos(); e.paso = 4; pintar(); };
    const r = $("#reiniciar", caja); if (r) r.onclick = () => { e = { paso: 0 }; pintar(); };
    const a = $(".js-aviso", caja); if (a) a.onclick = abrirAviso;
  }
  function guardarCampos() {
    const g = id => { const x = $("#" + id, caja); return x ? x.value.trim() : undefined; };
    if ($("#fNombre", caja)) { e.nombre = g("fNombre"); e.ciudad = g("fCiudad"); e.cuando = g("fCuando"); e.detalle = g("fDetalle"); }
  }
  function mensaje() {
    const l = [e.urgente ? "Hola, necesito atención URGENTE." : "Hola, me gustaría agendar una asesoría."];
    if (e.nombre) l.push(`Mi nombre es ${e.nombre}.`);
    l.push(`• Asunto: ${e.area}`);
    if (e.urgencia) l.push(`• Situación: ${e.urgencia}`);
    const t = TIPOS.find(x => x.t === e.tipo);
    l.push(`• Asesoría: ${e.tipo}${t ? ` (${t.c})` : ""}`);
    if (e.cuando) l.push(`• Cuándo: ${e.cuando}`);
    if (e.ciudad) l.push(`• Desde: ${e.ciudad}`);
    if (e.detalle) l.push(`• Detalle: ${e.detalle}`);
    return l.join("\n");
  }
  function iniciar(pre) {
    e = { paso: 0, ...pre }; pintar();
    $("#caso").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }
  pintar();

  /* ---------- Preguntas: buscador y filtros ---------- */
  const items = $$("#faq details"), buscar = $("#buscarFaq"), filtros = $$("#filtrosFaq button");
  let cat = "";
  const norm = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  function filtrar() {
    const q = norm(buscar.value.trim()); let n = 0;
    items.forEach(d => {
      const ok = (!cat || d.dataset.cat === cat) && (!q || norm(d.textContent).includes(q));
      d.hidden = !ok; if (ok) n++;
      if (q && ok) d.open = true; else if (!q) d.open = false;
    });
    $("#sinResultados").hidden = n > 0;
  }
  buscar.addEventListener("input", filtrar);
  filtros.forEach(b => b.onclick = () => { cat = b.dataset.cat; filtros.forEach(x => x.setAttribute("aria-pressed", x === b)); filtrar(); });

  /* ---------- Mapa, cómo llegar y contacto ---------- */
  const q = encodeURIComponent(CONFIG.direccion);
  $("#mapa").src = `https://maps.google.com/maps?q=${q}&z=16&output=embed`;
  $("#comoLlegar").href = `https://www.google.com/maps/dir/?api=1&destination=${q}`;
  $("#guardarContacto").onclick = () => {
    const v = ["BEGIN:VCARD", "VERSION:3.0", `FN:${CONFIG.despacho}`, `ORG:${CONFIG.despacho}`,
      `TEL;TYPE=CELL:${CONFIG.celular}`, `TEL;TYPE=WORK:${CONFIG.oficina}`, `EMAIL:${CONFIG.correo}`,
      `ADR;TYPE=WORK:;;Dr. Julián Villarreal 705 Nte., Planta Baja;Monterrey;N.L.;64000;México`,
      `URL:https://www.abogadosenmonterrey.com/`, "END:VCARD"].join("\r\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([v], { type: "text/vcard" })); a.download = "Castillo-y-Abogados.vcf"; a.click();
  };

  /* ---------- Aviso de privacidad ---------- */
  const aviso = $("#aviso");
  function abrirAviso() { aviso.classList.add("abierto"); $("#cerrarAviso").focus(); }
  $("#abrirAviso").onclick = abrirAviso;
  $("#cerrarAviso").onclick = () => aviso.classList.remove("abierto");
  aviso.onclick = ev => { if (ev.target === aviso) aviso.classList.remove("abierto"); };
  document.addEventListener("keydown", ev => { if (ev.key === "Escape") aviso.classList.remove("abierto"); });
})();
