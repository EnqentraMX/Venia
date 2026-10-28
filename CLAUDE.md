# Notas para Claude

- Proyecto de un emprendedor sin experiencia en programación. Explica en español sencillo, sin jerga, y pide confirmación antes de cambios grandes.
- Sitio estático sin build: `public/` se publica tal cual en Netlify (`netlify.toml`). No agregues frameworks ni pasos de compilación sin acordarlo.
- Cada despacho vive en `public/<slug>/` con `index.html` (idéntico a `plantilla/index.html`) y `datos.js` (`window.DATOS`). El motor es `public/assets/despacho.js`; los estilos `public/assets/liclink.css`.
- Las páginas de despacho SÍ se indexan en Google (a diferencia de Pizka): el abogado quiere que lo encuentren.
- Marca: LicLink, "Tu despacho, en un enlace.". Fondo casi negro `#09080a`, marfil `#ece6dc`, latón `#c8a46a`. Títulos en Newsreader, texto en Manrope.
- `vistaPrevia: true` marca datos "por confirmar"; `muestra: true` muestra el aviso de sitio de ejemplo. Nunca presentes datos inventados como reales en un cliente de verdad.
- Textos de cara al cliente: de tú, verbo primero en botones.
