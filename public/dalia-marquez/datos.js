/* ================================================================
   LICLINK · Datos del despacho: Lic. Dalia Márquez Ramírez
   Solo edita lo que está entre comillas "..." y guarda.
   Si un dato se deja vacío (""), esa parte de la página se oculta sola.
   ================================================================ */

window.DATOS = {

  // true = se marcan los datos que faltan confirmar. Cambiar a false cuando esté todo.
  vistaPrevia: true,
  muestra: false,

  // ---------- Colores propios (negro y oro rosado, como sus flyers) ----------
  tema: {
    fondo: "#0c0b0b",
    fondo2: "#131111",
    tarjeta: "#1b1817",
    linea: "#2f2927",
    acento: "#c7a28a",
    acento2: "#e6cdbb"
  },
  simbolo: "dalia",             // figura de la portada: "dalia", "balanza" o "huella"

  // ---------- Identidad ----------
  despacho: "Dalia Márquez",
  sufijo: "Asesoría jurídica",
  abogado: "Lic. Dalia Márquez Ramírez",
  titulo: "Abogada y perito en documentos cuestionados",
  descripcion: "Asesoría jurídica",
  cedula: "",                   // POR CONFIRMAR: número de cédula profesional
  modalidad: "Asesoría personalizada",
  iniciales: "DM",
  foto: "foto.jpg",
  frase: "Tu tranquilidad también es un derecho.",

  // ---------- Portada ----------
  portada: {
    titulo: ["¿Te despidieron?", "Conoce", "tus derechos."],
    texto: "Asesoría jurídica en despidos injustificados, derecho burocrático, asuntos familiares y pensiones. También soy perito en documentos cuestionados: verifico firmas y detecto alteraciones."
  },

  // ---------- Contacto ----------
  whatsapp: "525533663408",
  telefono: "5533663408",
  telefonoVisible: "55 3366 3408",
  correo: "",
  precioConsulta: "",           // POR CONFIRMAR: costo de la primera consulta

  // ---------- Áreas de práctica ----------
  areas: [
    {
      nombre: "Laboral y burocrático",
      icono: "maletin",
      texto: "Si te despidieron sin causa justificada o trabajas para el gobierno y tienes un conflicto laboral, revisamos tu caso y te explico lo que te corresponde.",
      puntos: ["Despidos injustificados", "Derecho burocrático (trabajadores del Estado)", "Asesoría jurídica laboral"]
    },
    {
      nombre: "Familiar y pensiones",
      icono: "familia",
      texto: "Te oriento y te acompaño en asuntos familiares y en el trámite y defensa de pensiones.",
      puntos: ["Asuntos de derecho familiar", "Pensiones"]
    },
    {
      nombre: "Peritaje en documentos",
      icono: "lupa",
      texto: "Análisis, verificación y elaboración de peritajes en documentos cuestionados, con objetividad y respaldo técnico. Para procedimientos legales, trámites, empresas y particulares.",
      puntos: ["Peritaje en documentos: autenticidad y veracidad", "Verificación de firmas y rúbricas", "Detección de alteraciones, falsificaciones y enmendaduras", "Elaboración de dictámenes claros y objetivos", "Asesoría personalizada en todo el proceso"]
    }
  ],

  // ---------- Paquetes con precio ----------
  paquetes: [],

  // ---------- Compromisos ----------
  compromisos: ["Experiencia", "Objetividad", "Respaldo técnico en cada dictamen", "Profesionalismo y discreción"],

  // ---------- Asistente "Cuéntanos tu caso" ----------
  situaciones: [
    { texto: "Me despidieron hace poco (los plazos ya están corriendo)", urgente: true },
    { texto: "Necesito un peritaje de un documento o una firma", urgente: false },
    { texto: "Tengo un asunto familiar o de pensión", urgente: false },
    { texto: "Solo quiero orientación para decidir qué hacer", urgente: false }
  ],

  // ---------- Cómo trabajamos ----------
  pasos: [
    { titulo: "Escríbeme por WhatsApp", texto: "Cuéntame tu situación o qué documento necesitas analizar. Todo se trata con discreción." },
    { titulo: "Revisamos tu caso", texto: "Analizo los hechos o el documento y te explico tus opciones con claridad." },
    { titulo: "Estrategia o cotización", texto: "Te propongo cómo actuar o te doy la cotización de tu peritaje, y te acompaño en todo el proceso." }
  ],

  // ---------- Horario ----------
  horario: null,                // POR CONFIRMAR: horario de atención
  notaHorario: "",

  // ---------- Oficinas ----------
  oficinas: [
    // POR CONFIRMAR: dirección de su oficina, si atiende en persona
  ],

  // ---------- Redes sociales ----------
  redes: { facebook: "", instagram: "", tiktok: "", youtube: "", linkedin: "" },

  // ---------- Preguntas frecuentes ----------
  preguntas: [
    { p: "¿Cuánto cuesta la primera consulta?", r: "{precio}" },
    { p: "Me despidieron, ¿qué hago primero?", r: "Guarda todo lo que tengas sobre tu trabajo: contrato, recibos de nómina, credenciales y mensajes. No firmes nada sin asesoría y escríbeme pronto, porque las acciones por despido tienen plazos." },
    { p: "¿Qué es un documento cuestionado?", r: "Es un documento cuya autenticidad, firma o contenido está en duda. Con un peritaje se analiza si es auténtico o si fue alterado, y el resultado se entrega en un dictamen." },
    { p: "¿Cuánto cuesta un peritaje?", r: "Depende del tipo de documento y del análisis que se necesite. Escríbeme por WhatsApp con los detalles y te doy una cotización." },
    { p: "¿Lo que te cuento es confidencial?", r: "Sí. Todo lo que me compartas, y cualquier documento que me envíes, se trata con profesionalismo, discreción y secreto profesional." }
  ]
};
