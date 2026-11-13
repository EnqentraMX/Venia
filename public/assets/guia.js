/* LicLink · Guía de abogados. Un solo archivo para portada, listados por ciudad y registro. */
(function () {
  "use strict";
  /* ====== CONFIGURACIÓN ====== */
  // Número de WhatsApp de LicLink (10 dígitos con 52 adelante, ej. "5215512345678"). Aquí llegan registros y clientes sin abogado.
  var LICLINK_WA = "529511836468";
  var CIUDADES = window.CIUDADES || { cdmx: "Ciudad de México", edomex: "Estado de México", guadalajara: "Guadalajara", puebla: "Puebla" };
  var MATERIAS = {
    penal: ["Penal", "Detenciones, denuncias y defensa"],
    familiar: ["Familiar", "Divorcio, pensión y custodia"],
    laboral: ["Laboral", "Despidos y liquidaciones"],
    civil: ["Civil e inmobiliario", "Casas, terrenos, rentas y contratos"],
    mercantil: ["Mercantil", "Pagarés, deudas y cobranza"],
    sucesiones: ["Herencias", "Testamentos e intestados"],
    amparo: ["Amparo", "Contra abusos de autoridad"],
    fiscal: ["Fiscal", "SAT, multas y embargos"],
    agrario: ["Agrario y ambiental", "Ejidos, tierras y medio ambiente"]
  };
  /* =========================== */

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var esc = function (t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var quieto = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var wa = function (num, msg) { return "https://wa.me/" + num + "?text=" + encodeURIComponent(msg); };
  var ok = '<svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>';

  /* Enlaces de WhatsApp a LicLink */
  $$(".js-liclink").forEach(function (a) {
    var msg = a.getAttribute("data-msg") || "Hola, quiero información de LicLink.";
    if (LICLINK_WA) { a.href = wa(LICLINK_WA, msg); a.target = "_blank"; a.rel = "noopener"; }
    else if (!a.getAttribute("href")) a.href = "/para-abogados/#registro";
  });

  /* Burbuja de ayuda: se hace pequeña al bajar para no tapar */
  var ay = $(".ayuda");
  if (ay) addEventListener("scroll", function () { ay.classList.toggle("chica", scrollY > 400); }, { passive: true });

  /* Barra con sombra al bajar */
  var barra = $(".barra");
  if (barra) addEventListener("scroll", function () { barra.classList.toggle("bajo", scrollY > 20); }, { passive: true });

  /* ---------- Portada: buscador ---------- */
  /* ---------- Buscador inteligente: entiende el problema en palabras normales ---------- */
  var PALABRAS = {
    penal: "detuv deten arrest carcel cárcel preso ministerio publico público denuncia delito acusa robo fraude golpe lesion lesión homicid policia policía audiencia fiscalia fiscalía querella violacion violación abuso amenaza",
    familiar: "divorci separa esposo esposa pareja pension pensión alimentos hijo hija niño niña custodia visita convivencia paternidad matrimonio boda violencia familiar adopc",
    laboral: "despid corrier corri trabajo patron patrón jefe finiquito liquidac sueldo salario imss infonavit afore renuncia incapacidad accidente de trabajo horas extra aguinaldo utilidad sindicato",
    civil: "casa terreno propiedad renta rentar inquilino arrendat desalojo escritura predio vecino contrato compraventa construcc hipoteca departamento",
    mercantil: "deuda debe deben pagare pagaré prestamo préstamo cobrar cobranza factura cheque negocio empresa socio tarjeta banco",
    sucesiones: "herencia heredar testamento intestado fallec murio murió difunto sucesion sucesión albacea",
    amparo: "amparo autoridad abuso de autoridad suspension suspensión inconstitucional clausura",
    agrario: "ejido ejidal ejidatario parcela comunero comunal tierra agraria agrario ambiental profepa semarnat forestal bosque tala monte",
    fiscal: "sat impuesto hacienda multa embargo fiscal credito fiscal crédito fiscal declaracion declaración"
  };
  var CIUDAD_PAL = { cdmx: "cdmx ciudad de mexico ciudad de méxico df iztapalapa coyoacan coyoacán tlalpan gam gustavo madero iztacalco benito juarez cuauhtemoc", edomex: "edomex estado de mexico estado de méxico neza nezahualcoyotl ecatepec toluca naucalpan tlalnepantla lerma cuautitlan texcoco chalco", guadalajara: "guadalajara jalisco zapopan tlaquepaque tonala tonalá", puebla: "puebla cholula", monterrey: "monterrey nuevo leon nuevo león", queretaro: "queretaro querétaro", hermosillo: "hermosillo sonora son",  "gomez-palacio": "gomez palacio gómez palacio durango dgo laguna comarca lagunera lerdo torreon torreón saltillo coahuila san pedro de las colonias", yucatan: "yucatan yucatán merida mérida halacho halachó progreso valladolid" };
  function adivina(t, dic) {
    t = " " + t.toLowerCase() + " "; var mejor = "", pts = 0;
    Object.keys(dic).forEach(function (k) { var n = 0; dic[k].split(" ").forEach(function (w) { if (w.length > 2 && t.indexOf(w) > -1) n += w.length; }); if (n > pts) { pts = n; mejor = k; } });
    return mejor;
  }
  var bt = $("#bTexto");
  if (bt) bt.addEventListener("input", function () {
    var m = adivina(bt.value, PALABRAS), c = adivina(bt.value, CIUDAD_PAL), sg = $("#bSug");
    if (m) $("#bMateria").value = m;
    if (c) $("#bCiudad").value = c;
    sg.hidden = !m; if (m) sg.textContent = "Te recomendamos: " + MATERIAS[m][0] + (c ? " · " + CIUDADES[c] : "");
  });

  var fb = $("#buscar");
  if (fb) fb.addEventListener("submit", function (e) {
    e.preventDefault();
    var c = $("#bCiudad").value, m = $("#bMateria").value;
    location.href = "/abogados/" + c + "/" + (m ? m + "/" : "");
  });
  $$("[data-atajo]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var c = ($("#bCiudad") && $("#bCiudad").value) || "cdmx";
      location.href = "/abogados/" + c + "/" + a.getAttribute("data-atajo") + "/";
    });
  });

  /* ---------- Portada: historia en el teléfono ---------- */
  var chat = $("#chat");
  if (chat) {
    var guion = [
      { t: "yo", x: "Buenas noches. Detuvieron a mi hijo hace una hora 😟 ¿Qué hago?", h: "11:42 p.m.", e: 0 },
      { t: "el", x: "Buenas noches, soy el Lic. Ramírez. Tranquila: ¿en qué Ministerio Público está?", h: "11:44 p.m.", e: 1 },
      { t: "yo", x: "En la agencia de Coyoacán", h: "11:44 p.m." },
      { t: "el", x: "Voy en camino. Que no firme nada hasta que yo llegue.", h: "11:45 p.m." },
      { t: "sep", x: "3 horas después" },
      { t: "yo", x: "Ya está en casa. Gracias, licenciado 🙏", h: "2:51 a.m.", e: 2 }
    ];
    var etapas = $$(".etapas li"), pantalla = $(".pantalla");
    var activa = function (i) { etapas.forEach(function (li, k) { li.classList.toggle("activa", k === i); }); pantalla.classList.toggle("calma", i === 2); };
    var corre = false;
    var reproducir = function () {
      if (corre) return; corre = true;
      chat.innerHTML = ""; activa(0);
      var i = 0;
      var paso = function () {
        if (i >= guion.length) { setTimeout(function () { corre = false; reproducir(); }, 4200); return; }
        var g = guion[i++];
        var poner = function () {
          var d = document.createElement("div");
          d.className = "msg " + g.t;
          d.innerHTML = esc(g.x) + (g.h ? "<time>" + g.h + "</time>" : "");
          chat.appendChild(d);
          while (chat.children.length > 6) chat.removeChild(chat.firstChild);
          if (g.e != null) activa(g.e);
          setTimeout(paso, g.t === "sep" ? 900 : 1500);
        };
        if (g.t === "el") {
          var tp = document.createElement("div"); tp.className = "escribiendo"; tp.innerHTML = "<i></i><i></i><i></i>";
          chat.appendChild(tp); setTimeout(function () { tp.remove(); poner(); }, 1300);
        } else poner();
      };
      paso();
    };
    if (quieto) { guion.forEach(function (g) { var d = document.createElement("div"); d.className = "msg " + g.t; d.innerHTML = esc(g.x) + (g.h ? "<time>" + g.h + "</time>" : ""); chat.appendChild(d); }); activa(2); }
    else if ("IntersectionObserver" in window) new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { reproducir(); o.disconnect(); } }, { threshold: .3 }).observe(chat);
    else reproducir();
  }

  /* ---------- Listado de ciudad ---------- */
  var lista = $("#lista");
  if (lista) {
    var C = document.body.getAttribute("data-ciudad"), M = document.body.getAttribute("data-materia") || "";
    var nc = CIUDADES[C] || C, nm = M ? MATERIAS[M][0] : "";
    $("#filtros").innerHTML = '<a href="/abogados/' + C + '/" class="' + (M ? "" : "si") + '">Todas</a>' +
      Object.keys(MATERIAS).map(function (k) { return '<a href="/abogados/' + C + "/" + k + '/" class="' + (k === M ? "si" : "") + '">' + MATERIAS[k][0] + "</a>"; }).join("");
    var si = $("#filtros .si"); if (si) si.scrollIntoView({ inline: "center", block: "nearest" });
    var hechas = $$(".ficha", lista);
    if (hechas.length) {
      // Las fichas ya vienen en el HTML (así Google las lee). Los destacados se alternan en cada visita para que ninguno quede siempre primero.
      var pr = hechas.filter(function (x) { return x.getAttribute("data-plan") === "premium"; });
      for (var q = pr.length - 1; q > 0; q--) { var z = Math.floor(Math.random() * (q + 1)), tt = pr[q]; pr[q] = pr[z]; pr[z] = tt; }
      pr.slice().reverse().forEach(function (x) { lista.insertBefore(x, lista.firstChild); });
    } else {
      lista.innerHTML = '<div class="vacio"><span class="eti">Estamos creciendo</span><h2>Estamos sumando a los primeros ' + esc(document.body.getAttribute("data-plural") || "abogados") + " en " + esc(nc) + ".</h2>" +
        "<p>Mientras tanto, cuéntanos qué pasó y te orientamos para encontrar abogado. Sin costo para ti.</p>" +
        '<div class="acciones"><a class="btn btn-wa js-ayuda" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>Pedir orientación por WhatsApp</a>' +
        '<a class="btn btn-linea" href="/para-abogados/">Soy abogado: quiero aparecer</a></div></div>';
      var ay = $(".js-ayuda");
      if (LICLINK_WA) ay.href = wa(LICLINK_WA, "Hola, busco abogado" + (nm ? " de " + nm.toLowerCase() : "") + " en " + nc + ". Mi caso es: ");
      else ay.href = "/para-abogados/";
    }
  }

  function ficha(a) {
    var prem = a.plan === "premium";
    var tags = (a.materias || []).map(function (k) { return "<span>" + esc((MATERIAS[k] || [k])[0]) + "</span>"; }).join("");
    var foto = a.foto ? '<img src="' + esc(a.foto) + '" alt="" loading="lazy" decoding="async" width="72" height="72">' : esc(a.iniciales || a.nombre.slice(0, 2));
    var msg = "Hola, lo encontré en LicLink. Necesito asesoría.";
    var redes = prem ? Object.keys(a.redes || {}).filter(function (k) { return a.redes[k]; }).map(function (k) { return '<a href="' + esc(a.redes[k]) + '" target="_blank" rel="noopener" aria-label="' + k + '"><svg viewBox="0 0 24 24"><use href="#i-' + k + '"/></svg></a>'; }).join("") : "";
    return '<article class="ficha rv' + (prem ? " prem" : "") + '">' +
      '<div class="foto' + (a.logo ? " logo" : "") + '">' + foto + "</div><div>" + (prem ? '<span class="sello-p">Destacado</span>' : "") + "<h3>" + esc(a.nombre) + '</h3><div class="rol">' + esc(a.rol || "") + (CIUDADES[a.ciudad] && (a.rol || "").indexOf(CIUDADES[a.ciudad]) < 0 ? " · " + esc(CIUDADES[a.ciudad]) : "") + "</div>" +
      (a.verificada ? '<span class="ver si"><svg viewBox="0 0 24 24"><use href="#i-ok"/></svg>Cédula profesional verificada</span>' : '<span class="ver no">Datos profesionales registrados</span>') +
      (redes ? '<div class="redes">' + redes + "</div>" : "") +
      '<div class="tags">' + tags + "</div></div>" +
      '<div class="acc">' +
      (prem && a.pagina ? '<a class="btn btn-negro uno" href="' + esc(a.pagina) + '">Ver perfil completo</a>' : "") +
      '<a class="btn btn-wa' + (a.telefono ? "" : " uno") + '" target="_blank" rel="noopener" href="' + wa(a.whatsapp, msg) + '"><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>WhatsApp</a>' +
      (a.telefono ? '<a class="btn btn-linea" href="tel:+52' + esc(a.telefono) + '">Llamar</a>' : "") +
      (prem && a.resena ? '<a class="btn btn-linea uno" target="_blank" rel="noopener" href="' + esc(a.resena) + '">★ Ver y dejar reseñas en Google</a>' : "") +
      "</div></article>";
  }

  /* ---------- Portada: abogados destacados (Premium primero, luego al azar) ---------- */
  var dest = $("#destacados");
  if (dest && !dest.children.length) {
    var g = (window.GUIA || []).slice(), prem = g.filter(function (a) { return a.plan === "premium"; }), resto = g.filter(function (a) { return a.plan !== "premium" && a.foto; });
    for (var i = resto.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = resto[i]; resto[i] = resto[j]; resto[j] = t; }
    var sel = prem.concat(resto).slice(0, 8);
    dest.innerHTML = sel.map(function (a) { return ficha(a).replace(" rv", ""); }).join("");
    dest.closest("section").hidden = !sel.length;
  }

  /* ---------- Portada: pregúntale a un abogado ---------- */
  var pf = $("#pregunta");
  if (pf) {
    var pt = $("#pTexto"), pc = $("#pCuenta");
    pt.addEventListener("input", function () { pc.textContent = pt.value.length + " / 600"; });
    $$("[data-idea]").forEach(function (b) { b.addEventListener("click", function () { pt.value = b.getAttribute("data-idea") + " "; pt.dispatchEvent(new Event("input")); pt.focus(); }); });
  }
  if (pf) pf.addEventListener("submit", function (e) {
    e.preventDefault();
    var t = $("#pTexto").value.trim(); if (!t) return;
    window.open(wa(LICLINK_WA, "Hola, no sé qué abogado necesito (" + CIUDADES[$("#pCiudad").value] + "). Esto es lo que pasó:\n\n" + t), "_blank");
  });

  /* ---------- Registro de abogados ---------- */
  var reg = $("#formRegistro");
  if (reg) {
    $("#rMaterias").innerHTML = Object.keys(MATERIAS).map(function (k) { return '<label><input type="checkbox" value="' + k + '">' + MATERIAS[k][0] + "</label>"; }).join("");
    $$("[data-plan]").forEach(function (b) { b.addEventListener("click", function () { var s = $("#rPlan"); if (s) s.value = b.getAttribute("data-plan"); }); });
    reg.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = function (id) { return ($("#" + id).value || "").trim(); };
      var mats = $$("#rMaterias input:checked").map(function (i) { return MATERIAS[i.value][0]; });
      var txt = ["Hola, quiero aparecer en LicLink.", "• Nombre: " + v("rNombre"), "• Ciudad: " + CIUDADES[v("rCiudad")],
        "• Especialidades: " + (mats.join(", ") || "por definir"), "• WhatsApp: " + v("rWa"), v("rCedula") ? "• Cédula: " + v("rCedula") : "", "• Plan: " + $("#rPlan").selectedOptions[0].text].filter(Boolean).join("\n");
      if (LICLINK_WA) window.open(wa(LICLINK_WA, txt), "_blank");
      else { $("#rAviso").hidden = false; $("#rAviso").textContent = txt; }
    });
  }

  /* ---------- Aparecer al bajar ---------- */
  var objetivos = $$(".rv");
  $$("[data-escalona]").forEach(function (g) { Array.prototype.forEach.call(g.children, function (e, i) { e.classList.add("rv"); e.style.setProperty("--d", Math.min(i, 7) * 70 + "ms"); objetivos.push(e); }); });
  if (!quieto && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("si"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    objetivos.forEach(function (e) { io.observe(e); });
    setTimeout(function () { $$(".lista .rv").forEach(function (e) { io.observe(e); }); }, 0);
  } else $$(".rv").forEach(function (e) { e.classList.add("si"); });
})();
