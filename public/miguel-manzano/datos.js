/* ================================================================
   LICLINK · Datos del despacho: Miguel Ángel Manzano Macías
   Solo edita lo que está entre comillas "..." y guarda.
   Si un dato se deja vacío (""), esa parte de la página se oculta sola.
   ================================================================ */

window.DATOS = {

  // true = se marcan los datos que faltan confirmar. Cambiar a false cuando esté todo.
  vistaPrevia: true,
  muestra: false,

  // ---------- Colores propios (azul marino y oro, como sus flyers) ----------
  tema: {
    fondo: "#0a1220",
    fondo2: "#0e1828",
    tarjeta: "#122036",
    linea: "#22324b",
    acento: "#d2ae6c",
    acento2: "#ecd29e"
  },
  simbolo: "balanza",           // figura de la portada: "balanza" o "huella"

  // ---------- Identidad ----------
  despacho: "Miguel Ángel Manzano",
  sufijo: "Asesoría jurídica",
  abogado: "Miguel Ángel Manzano Macías",
  titulo: "Abogado",
  descripcion: "Derecho familiar, laboral y administrativo en Guadalajara",
  cedula: "",                   // POR CONFIRMAR: número de cédula profesional
  modalidad: "Atención presencial y en línea",
  iniciales: "MM",
  foto: "",                     // Ej: "foto.jpg" (subir la foto a esta misma carpeta)
  frase: "No estás solo, estoy para ayudarte. Tu bienestar y el de tu familia son mi prioridad.",

  // ---------- Portada ----------
  portada: {
    titulo: ["Lo que más", "importa:", "tu familia."],
    texto: "Más de 10 años de experiencia en derecho familiar. También te asesoro en asuntos laborales y administrativos. Atiendo en Guadalajara, Zapopan, Tlaquepaque y alrededores, en persona con cita o en línea."
  },

  // ---------- Contacto ----------
  whatsapp: "523335940403",
  telefono: "3335940403",
  telefonoVisible: "333 594 0403",
  correo: "",
  precioConsulta: "",           // POR CONFIRMAR: costo de la primera consulta

  // ---------- Áreas de práctica ----------
  areas: [
    {
      nombre: "Derecho familiar",
      icono: "familia",
      texto: "Te acompaño en los momentos más importantes con un enfoque humano: procesos justos, acuerdos claros y el bienestar de tus hijos primero.",
      puntos: ["Divorcios", "Custodia y convivencia", "Pensión alimenticia", "Convenios y acuerdos"]
    },
    {
      nombre: "Derecho laboral",
      icono: "maletin",
      texto: "Defensa, asesoría y representación cuando tus derechos como trabajador están en juego.",
      puntos: ["Despidos injustificados", "Reclamaciones de prestaciones", "Conflictos individuales y colectivos", "Reinstalaciones y liquidaciones"]
    },
    {
      nombre: "Derecho administrativo",
      icono: "edificio",
      texto: "Defensa frente a actos de autoridad que afectan tus derechos o los de tu negocio.",
      puntos: ["Defensa ante actos de autoridad", "Procedimientos administrativos", "Recursos y juicios de nulidad", "Responsabilidades administrativas"]
    }
  ],

  // ---------- Paquetes con precio ----------
  // "hasta" oculta el paquete solo después de esa fecha.
  paquetes: [
    {
      nombre: "Divorcio integral premium",
      subtitulo: "Estrategia familiar y patrimonial",
      precio: "$100,000 MXN",
      destacado: true,
      texto: "No se trata solamente de terminar un matrimonio: se trata de proteger y ordenar tu patrimonio, tus derechos y los acuerdos con tu familia.",
      incluye: [
        "Diagnóstico jurídico y estrategia personalizada",
        "Elaboración y presentación de la demanda, y seguimiento del expediente",
        "Representación en audiencias y negociación con la contraparte",
        "Análisis y liquidación del régimen matrimonial (bienes, inmuebles, vehículos, cuentas, empresas)",
        "Alimentos, custodia y convivencia, cuando existan hijos",
        "Coordinación con peritos, contador, valuador o notario cuando sea necesario",
        "Cierre y regularización documental posterior a la sentencia"
      ]
    },
    {
      nombre: "Divorcio express",
      subtitulo: "Solo necesitamos tu firma",
      precio: "Desde $1,000 al mes",
      hasta: "2026-10-31",
      texto: "Para quien busca terminar su matrimonio de forma rápida y segura, pagando en mensualidades.",
      incluye: ["Trámite ágil", "Asesoría profesional", "Proceso seguro y confidencial"]
    }
  ],

  // ---------- Compromisos ----------
  compromisos: ["Atención personalizada", "Discreción y confidencialidad", "Estrategias efectivas", "Honestidad y transparencia", "Enfoque humano y profesional"],

  // ---------- Asistente "Cuéntanos tu caso" ----------
  situaciones: [
    { texto: "Tengo una audiencia o un plazo que vence pronto", urgente: true },
    { texto: "Me despidieron o tengo un problema en mi trabajo", urgente: false },
    { texto: "Quiero iniciar un trámite (divorcio, pensión, custodia)", urgente: false },
    { texto: "Solo quiero orientación para decidir qué hacer", urgente: false }
  ],

  // ---------- Cómo trabajamos ----------
  pasos: [
    { titulo: "Agenda tu cita por WhatsApp", texto: "Cuéntame brevemente tu situación. Tu información se trata con discreción y confidencialidad." },
    { titulo: "Revisamos tu caso", texto: "En persona en la Colonia Americana o en línea, analizamos tus opciones con claridad y honestidad." },
    { titulo: "Definimos la estrategia", texto: "Te acompaño en cada paso del proceso, con atención personalizada hasta el final." }
  ],

  // ---------- Horario ----------
  horario: null,                // POR CONFIRMAR: horario de atención (atiende con cita)
  notaHorario: "",

  // ---------- Oficinas ----------
  oficinas: [
    { nombre: "Guadalajara", direccion: "Manuel López Cotilla 1505, Col. Americana, Guadalajara, Jalisco", referencia: "Atención previa cita. Agenda por WhatsApp." }
  ],

  // ---------- Redes sociales ----------
  redes: { facebook: "", instagram: "", tiktok: "", youtube: "", linkedin: "" },

  // ---------- Preguntas frecuentes ----------
  preguntas: [
    { p: "¿Cuánto cuesta la primera consulta?", r: "{precio}" },
    { p: "¿Atiendes en línea?", r: "Sí. Puedes recibir asesoría desde cualquier lugar por videollamada, o en persona con cita previa en la Colonia Americana, Guadalajara." },
    { p: "¿En qué zonas atiendes?", r: "Guadalajara, Zapopan, Tlaquepaque y alrededores. Si tu asunto está en otro lugar, escríbeme y lo revisamos." },
    { p: "¿Qué incluye el divorcio integral premium?", r: "Diagnóstico y estrategia, la demanda y el seguimiento del expediente, audiencias y negociación, la liquidación de bienes, alimentos, custodia y convivencia, coordinación con peritos o notario, y la regularización de documentos después de la sentencia." },
    { p: "¿Lo que te cuento es confidencial?", r: "Sí. Todo lo que me compartas se trata con discreción, confidencialidad y secreto profesional." }
  ]
};
