/* Castillo & Abogados · panel administrativo
   Con PHP (su dominio) guarda en el servidor. Sin PHP (vista previa en LicLink) entra en modo demostración. */
(function () {
  "use strict";
  const $ = s => document.querySelector(s);
  const DIAS = [["lunes", "Lunes"], ["martes", "Martes"], ["miercoles", "Miércoles"], ["jueves", "Jueves"], ["viernes", "Viernes"], ["sabado", "Sábado"], ["domingo", "Domingo"]];
  const CLAVE_DEMO = "castillo_contenido_demo";
  let demo = false, csrf = "", original = null;

  /* ---------- comunicación ---------- */
  async function api(accion, datos) {
    const op = { method: datos ? "POST" : "GET", headers: { "X-CSRF": csrf }, credentials: "same-origin" };
    if (datos) { op.headers["Content-Type"] = "application/json"; op.body = JSON.stringify(datos); }
    const r = await fetch("api.php?accion=" + accion, op);
    let j; try { j = await r.json(); } catch (_) { throw new Error("SIN_PHP"); }
    if (!j.ok) { const e = new Error(j.error || "Ocurrió un error."); e.codigo = r.status; throw e; }
    return j;
  }
  async function contenidoBase() {
    const r = await fetch("../assets/contenido.json?t=" + Date.now(), { cache: "no-store" });
    return r.ok ? r.json() : {};
  }

  /* ---------- formulario ⇄ datos ---------- */
  function pintarDias() {
    $("#dias").innerHTML = DIAS.map(([k, n]) => `<div class="dia" data-d="${k}">
      <label class="interruptor" style="margin:0"><input type="checkbox" class="abre">${n}</label><span></span>
      <input type="time" class="de" aria-label="${n}: abre" step="900"><input type="time" class="a" aria-label="${n}: cierra" step="900"></div>`).join("");
    document.querySelectorAll(".dia .abre").forEach(c => c.addEventListener("change", () => { const f = c.closest(".dia"); f.querySelector(".de").disabled = f.querySelector(".a").disabled = !c.checked; if (c.checked && !f.querySelector(".de").value) { f.querySelector(".de").value = "09:00"; f.querySelector(".a").value = "18:00"; } cambio(); }));
  }
  function llenar(c) {
    const p = c.promocion || {}, a = c.aviso || {}, k = c.contacto || {}, pr = c.precios || {}, h = c.horario || {};
    $("#pActiva").checked = !!p.activa; $("#pEtiqueta").value = p.etiqueta || "Promoción"; $("#pBoton").value = p.boton || "Quiero aprovecharla";
    $("#pTitulo").value = p.titulo || ""; $("#pTexto").value = p.texto || ""; $("#pMensaje").value = p.mensaje || ""; $("#pDesde").value = p.desde || ""; $("#pHasta").value = p.hasta || "";
    $("#aActivo").checked = !!a.activo; $("#aTexto").value = a.texto || "";
    $("#prPresencial").value = pr.presencial ?? ""; $("#prNacional").value = pr.nacional ?? ""; $("#prInternacional").value = pr.internacional ?? "";
    $("#cWhatsapp").value = String(k.whatsapp || "").replace(/^52/, ""); $("#cCelular").value = k.celular || ""; $("#cOficina").value = k.oficina || ""; $("#cCorreo").value = k.correo || "";
    DIAS.forEach(([d]) => { const f = document.querySelector(`.dia[data-d="${d}"]`), x = h[d];
      f.querySelector(".abre").checked = !!x; f.querySelector(".de").value = x ? x[0] : ""; f.querySelector(".a").value = x ? x[1] : "";
      f.querySelector(".de").disabled = f.querySelector(".a").disabled = !x; });
    $("#nota").value = c.notaHorario || "";
    $("#actualizado").textContent = c.actualizado ? "Última actualización: " + new Date(c.actualizado).toLocaleString("es-MX", { dateStyle: "medium", timeStyle: "short" }) : "";
    vistaPromo();
  }
  function leer() {
    const horario = {};
    DIAS.forEach(([d]) => { const f = document.querySelector(`.dia[data-d="${d}"]`); horario[d] = f.querySelector(".abre").checked && f.querySelector(".de").value && f.querySelector(".a").value ? [f.querySelector(".de").value, f.querySelector(".a").value] : null; });
    const num = id => Number(String($(id).value).replace(/\D/g, "") || 0);
    return {
      promocion: { activa: $("#pActiva").checked, etiqueta: $("#pEtiqueta").value.trim(), titulo: $("#pTitulo").value.trim(), texto: $("#pTexto").value.trim(), boton: $("#pBoton").value.trim(), mensaje: $("#pMensaje").value.trim(), desde: $("#pDesde").value, hasta: $("#pHasta").value },
      aviso: { activo: $("#aActivo").checked, texto: $("#aTexto").value.trim() },
      precios: { presencial: num("#prPresencial"), nacional: num("#prNacional"), internacional: num("#prInternacional") },
      contacto: { whatsapp: $("#cWhatsapp").value, celular: $("#cCelular").value, oficina: $("#cOficina").value, correo: $("#cCorreo").value.trim() },
      horario, notaHorario: $("#nota").value.trim()
    };
  }
  function vistaPromo() {
    const t = $("#pTitulo").value.trim(), act = $("#pActiva").checked, h = $("#pHasta").value;
    const esc = s => s.replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
    $("#vistaPromo").innerHTML = act && t
      ? `<em>${esc($("#pEtiqueta").value || "Promoción")}${h ? " · termina el " + new Date(h + "T12:00:00").toLocaleDateString("es-MX", { day: "numeric", month: "long" }) : ""}</em><b>${esc(t)}</b>${esc($("#pTexto").value)}`
      : `<em>${act ? "Escriba un título para mostrar la promoción." : "La promoción está oculta."}</em>`;
  }

  /* ---------- validación en el navegador (el servidor valida de nuevo) ---------- */
  function validar(c) {
    const d = s => String(s).replace(/\D/g, "");
    if (d(c.contacto.whatsapp).replace(/^52/, "").length !== 10) return "El WhatsApp debe tener 10 dígitos.";
    if (d(c.contacto.celular).length !== 10 || d(c.contacto.oficina).length !== 10) return "Los teléfonos deben tener 10 dígitos.";
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(c.contacto.correo)) return "El correo no es válido.";
    if (c.promocion.activa && !c.promocion.titulo) return "La promoción activa necesita un título.";
    if (c.promocion.desde && c.promocion.hasta && c.promocion.desde > c.promocion.hasta) return "La promoción termina antes de empezar.";
    if (c.aviso.activo && !c.aviso.texto) return "El aviso activo necesita un texto.";
    for (const [k, n] of DIAS) { const x = c.horario[k]; if (x && x[0] >= x[1]) return `Revise el horario del ${n.toLowerCase()}: la hora de cierre debe ser después de la de apertura.`; }
    return "";
  }
  function normalizarDemo(c) { // imita lo que hace el servidor
    const t = s => { const x = String(s).replace(/\D/g, ""); return x.slice(0, 2) + " " + x.slice(2, 6) + " " + x.slice(6); };
    let w = String(c.contacto.whatsapp).replace(/\D/g, ""); if (w.length === 10) w = "52" + w;
    c.contacto = { whatsapp: w, celular: t(c.contacto.celular), oficina: t(c.contacto.oficina), correo: c.contacto.correo };
    c.actualizado = new Date().toISOString(); return c;
  }

  /* ---------- estado de cambios ---------- */
  function cambio() {
    vistaPromo();
    const sucio = JSON.stringify(leer()) !== JSON.stringify(original);
    $("#guardar").disabled = $("#descartar").disabled = !sucio;
    $("#estadoGuardar").textContent = sucio ? "Tiene cambios sin guardar." : "Sin cambios por guardar.";
  }
  function toast(t) { const x = $("#toast"); x.textContent = t; x.hidden = false; clearTimeout(x._t); x._t = setTimeout(() => x.hidden = true, 3200); }
  window.addEventListener("beforeunload", ev => { if (!$("#guardar").disabled) { ev.preventDefault(); ev.returnValue = ""; } });

  /* ---------- acciones ---------- */
  async function mostrarPanel(cambiar) {
    let c;
    if (demo) { c = await contenidoBase(); try { const d = localStorage.getItem(CLAVE_DEMO); if (d) Object.assign(c, JSON.parse(d)); } catch (_) {} }
    else c = (await api("leer")).contenido || await contenidoBase();
    $("#pantallaEntrar").hidden = true; $("#pantallaPanel").hidden = false; $("#avisoCambiar").hidden = !cambiar;
    llenar(c); original = leer(); cambio();
  }
  $("#formEntrar").addEventListener("submit", async ev => {
    ev.preventDefault(); const err = $("#errorEntrar"); err.hidden = true;
    const clave = $("#contrasena").value;
    try {
      if (demo) { if (clave !== "demo") throw new Error("Contraseña incorrecta. En la demostración es “demo”."); sessionStorage.setItem("panel_demo", "1"); await mostrarPanel(false); return; }
      const j = await api("entrar", { contrasena: clave }); csrf = j.csrf; await mostrarPanel(j.cambiar);
    } catch (e) { err.textContent = e.message; err.hidden = false; $("#contrasena").select(); }
  });
  $("#guardar").addEventListener("click", async () => {
    const c = leer(), m = validar(c); if (m) { toast(m); return; }
    $("#guardar").disabled = true; $("#estadoGuardar").textContent = "Guardando…";
    try {
      let nuevo;
      if (demo) { nuevo = normalizarDemo(c); localStorage.setItem(CLAVE_DEMO, JSON.stringify(nuevo)); }
      else nuevo = (await api("guardar", { contenido: c })).contenido;
      llenar(nuevo); original = leer(); cambio(); toast("Cambios guardados. Ya se ven en el sitio.");
    } catch (e) { if (e.codigo === 401) location.reload(); toast(e.message); cambio(); }
  });
  $("#descartar").addEventListener("click", () => { const o = original; llenar(Object.assign({}, o, { actualizado: null })); original = o; cambio(); });
  $("#deshacer").addEventListener("click", async () => {
    if (!confirm("¿Regresar el sitio a como estaba antes del último cambio guardado?")) return;
    try {
      let c;
      if (demo) { localStorage.removeItem(CLAVE_DEMO); c = await contenidoBase(); }
      else c = (await api("deshacer", {})).contenido;
      llenar(c); original = leer(); cambio(); toast("Listo: se recuperó la versión anterior.");
    } catch (e) { toast(e.message); }
  });
  $("#cambiarClave").addEventListener("click", async () => {
    const m = $("#msjClave"); m.hidden = true;
    if (demo) { m.className = "msj error"; m.textContent = "En la demostración no se puede cambiar la contraseña."; m.hidden = false; return; }
    try { await api("contrasena", { actual: $("#claveActual").value, nueva: $("#claveNueva").value });
      m.className = "msj bien"; m.textContent = "Contraseña cambiada."; $("#claveActual").value = $("#claveNueva").value = ""; $("#avisoCambiar").hidden = true;
    } catch (e) { m.className = "msj error"; m.textContent = e.message; }
    m.hidden = false;
  });
  $("#salir").addEventListener("click", async () => { if (demo) sessionStorage.removeItem("panel_demo"); else { try { await api("salir", {}); } catch (_) {} } location.reload(); });
  document.addEventListener("input", ev => { if (ev.target.closest("#pantallaPanel")) cambio(); });

  /* ---------- arranque ---------- */
  pintarDias();
  (async () => {
    try {
      const j = await api("estado"); csrf = j.csrf;
      if (j.sesion) return mostrarPanel(j.cambiar);
    } catch (e) {
      if (e.message === "SIN_PHP") { demo = true; $("#demo").hidden = false; $("#pistaDemo").hidden = false; if (sessionStorage.getItem("panel_demo")) return mostrarPanel(false); }
    }
    $("#pantallaEntrar").hidden = false; $("#contrasena").focus();
  })();
})();
