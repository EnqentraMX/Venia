/* ================================================================
   VENIA · Datos del despacho
   ----------------------------------------------------------------
   Este es el ÚNICO archivo que se cambia para cada abogado.
   Solo edita lo que está entre comillas "..." y guarda.
   Si un dato se deja vacío (""), esa parte de la página se oculta sola.
   ================================================================ */

window.DATOS = {

  // Mientras sea true, aparece un aviso discreto de "vista previa"
  // y se marcan los datos que faltan confirmar. Cambiar a false al publicar.
  vistaPrevia: true,
  muestra: false,

  // ---------- Identidad ----------
  despacho: "Gabriel Sánchez",
  sufijo: "Abogados",
  abogado: "Lic. Carlos Gabriel Sánchez Ortiz",
  titulo: "Abogado criminalista",
  descripcion: "Despacho jurídico y laboratorio pericial",
  cedula: "",                 // POR CONFIRMAR: número de cédula profesional
  foto: "",                   // Ej: "foto.jpg" (subir la foto a esta misma carpeta)
  frase: "Cada caso merece preparación, estrategia y precisión.",

  // ---------- Portada ----------
  portada: {
    titulo: ["En derecho,", "un detalle", "lo cambia todo."],
    texto: "Defensa penal, audiencias y amparos, criminalística y peritaje. Si tú o un familiar enfrentan un proceso, actuar a tiempo hace la diferencia."
  },

  // ---------- Contacto ----------
  whatsapp: "522351030317",   // 52 + número a 10 dígitos, sin espacios
  telefono: "2351030317",
  telefonoVisible: "235 103 03 17",
  correo: "",

  // Precio de la primera consulta. Ej: "$800" o "Sin costo". Vacío = "Te lo decimos al escribir".
  precioConsulta: "",

  // ---------- Áreas de práctica ----------
  areas: [
    {
      nombre: "Defensa penal",
      icono: "escudo",
      texto: "Cuando hay una detención, las primeras horas son decisivas. Revisamos la legalidad de cada actuación y construimos una defensa técnica desde el inicio del procedimiento.",
      puntos: ["Detenciones", "Vinculaciones", "Prisión preventiva"]
    },
    {
      nombre: "Audiencias y amparos",
      icono: "balanza",
      texto: "Te representamos en cada audiencia y promovemos el amparo cuando tus derechos están en riesgo, con una estrategia pensada para cada etapa del proceso.",
      puntos: ["Audiencias", "Juicio de amparo", "Apelaciones"]
    },
    {
      nombre: "Criminalística y peritaje",
      icono: "lupa",
      texto: "Contamos con laboratorio pericial propio. El análisis técnico de la evidencia permite sostener la defensa con datos, no solo con argumentos.",
      puntos: ["Análisis de indicios", "Dictámenes periciales", "Revisión técnica de pruebas"]
    }
  ],

  // ---------- Asistente "Cuéntanos tu caso" ----------
  // urgente: true muestra el botón de llamar de inmediato.
  situaciones: [
    { texto: "Hay una persona detenida en este momento", urgente: true },
    { texto: "Recibí un citatorio o una notificación", urgente: false },
    { texto: "Ya hay un proceso o una carpeta abierta", urgente: false },
    { texto: "Quiero asesoría antes de que pase algo", urgente: false }
  ],

  // ---------- Cómo trabajamos ----------
  pasos: [
    { titulo: "Escríbenos por WhatsApp", texto: "Cuéntanos brevemente qué pasó. Tu información se trata con confidencialidad." },
    { titulo: "Revisamos tu situación", texto: "Analizamos los hechos y los documentos que tengas, y te explicamos tus opciones con claridad." },
    { titulo: "Definimos la estrategia", texto: "Te acompañamos en cada etapa del proceso, con defensa jurídica y respaldo técnico pericial." }
  ],

  // ---------- Horario ----------
  // Formato 24 h. Día cerrado = null.  POR CONFIRMAR (son horarios de ejemplo)
  horario: {
    lunes: ["09:00", "19:00"],
    martes: ["09:00", "19:00"],
    miercoles: ["09:00", "19:00"],
    jueves: ["09:00", "19:00"],
    viernes: ["09:00", "19:00"],
    sabado: ["10:00", "14:00"],
    domingo: null
  },
  notaHorario: "Urgencias por detención: escríbenos a cualquier hora.", // POR CONFIRMAR

  // ---------- Oficinas ----------
  // Se pueden poner varias. Si la lista queda vacía, la sección se oculta.
  oficinas: [
    // { nombre: "Oficina principal", direccion: "Calle, número, colonia, ciudad, estado", referencia: "Frente a…" }
  ],

  // ---------- Redes sociales (pegar el enlace completo) ----------
  redes: {
    facebook: "",
    instagram: "",
    tiktok: "",
    youtube: "",
    linkedin: ""
  },

  // ---------- Preguntas frecuentes ----------
  preguntas: [
    {
      p: "¿Qué hago si detienen a un familiar?",
      r: "Mantén la calma y averigua a qué autoridad y a qué lugar lo trasladaron. La persona detenida tiene derecho a guardar silencio y a contar con un abogado. Escríbenos o llámanos de inmediato: las primeras horas son las más importantes."
    },
    {
      p: "¿Cuánto cuesta la primera asesoría?",
      r: "{precio}"
    },
    {
      p: "¿Qué documentos debo tener a la mano?",
      r: "Identificación, cualquier citatorio, notificación o documento que te hayan entregado, y los datos de la autoridad que lleva el asunto. Si no tienes nada, no te preocupes: igual podemos orientarte."
    },
    {
      p: "¿Atienden casos fuera de la ciudad?",
      r: "Cuéntanos dónde está el asunto. Según el caso, podemos atenderte en línea o en persona."
    },
    {
      p: "¿Lo que les cuento es confidencial?",
      r: "Sí. Todo lo que nos compartas se trata con estricta confidencialidad y secreto profesional."
    }
  ]
};
