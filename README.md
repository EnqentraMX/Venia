# LicLink · Tu despacho, en un enlace

Páginas para abogados y despachos, publicadas en Netlify desde este repositorio.

## Cómo dar de alta a un abogado nuevo
1. Copia la carpeta `plantilla/` dentro de `public/` y ponle el nombre del despacho, en minúsculas y con guiones. Ejemplo: `public/bufete-ramirez/`.
2. Abre `datos.js` y cambia los textos entre comillas. Si un dato queda vacío (`""`), esa parte se oculta sola.
3. Si hay foto, súbela a la misma carpeta y escribe su nombre en `foto`.
4. Cuando todo esté confirmado, pon `vistaPrevia: false` y `muestra: false`.
5. Guarda en GitHub. Netlify publica solo en uno o dos minutos: `tusitio.netlify.app/bufete-ramirez/`.

## Qué hay en cada carpeta
- `public/index.html`: la página de LicLink (para vender).
- `public/assets/`: el diseño y el funcionamiento que comparten todas las páginas. Un cambio aquí se aplica a todos los clientes.
- `public/<despacho>/`: `index.html` (igual para todos) y `datos.js` (lo único que cambia).
- `plantilla/`: la copia limpia para empezar un cliente nuevo.
