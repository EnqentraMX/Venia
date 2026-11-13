# Notas para Claude — LicLink

## Quién y cómo
- Proyecto de un emprendedor **sin experiencia en programación**. Háblale en español sencillo, sin jerga. Tú haces todo lo técnico; él solo manda datos e imágenes y copia los textos que le das.
- **LicLink — "la guía de abogados de México"** (estilo Doctoralia). La gente busca abogado por ciudad y materia y le escribe directo por WhatsApp. Los abogados pagan suscripción.
- Dominio: **https://liclink.com.mx** (comprado en GoDaddy, DNS en Cloudflare). El sitio se publica solo: cada `git push` a `main` de `EnqentraMX/Venia` lo despliega un Worker de Cloudflare llamado "liclink" (tarda ~1–2 min). Netlify ya no se usa; `netlify.toml` solo redirige todo a liclink.com.mx.
- Commits: `git -c user.name="LicLink" -c user.email="noreply@anthropic.com" commit` (más las líneas de atribución que indique el sistema).
- Sitio estático, sin frameworks ni pasos de compilación. `public/` se publica tal cual.

## Planes y precios
- **Básico:** $99 de alta + $49 al mes.
- **Premium:** $399 de alta + **$149 al mes**. "Socios fundadores" conservan ese precio mientras sigan activos.
- Se habló de subir a $249/mes más adelante; **no está decidido**. Usa $149 salvo que él diga otra cosa.

## Flujo típico: "da de alta a este abogado"
Él manda capturas de Facebook (logo, banner, anuncio) y datos (teléfono, ciudad, materias, redes).
1. Crea `public/<slug>/` y guarda las imágenes (con PIL desde los adjuntos):
   - `logo.jpg` (cuadrado ~1000px). Si el logo tiene fondo negro con bordes/rayos de luz grises, límpialo (oscurece lo casi negro y recorta al contenido) para que no se vea un cuadro.
   - `foto.jpg` si hay **foto real** del abogado. **Nunca uses fotos de modelos/bancos de imágenes** de sus anuncios.
2. Agrega su entrada a `prospectos/abogados.json` (copia la estructura de uno parecido, p. ej. `yulieth-alejandra` con foto o `servicio-juridico-sp` con logo). Campos clave: `slug, nombre, despacho, sufijo, despacho_largo, titulo, iniciales, foto, logo (bool), imagen_vista, fondo_logo, plantilla "v2", estilo "claro", ciudad, telefono, telefonos_extra [{numero, whatsapp}], direccion, referencia, correo, facebook, instagram, descripcion, modalidad, horario, nota_horario, portada [3 líneas], texto_portada, frase, compromisos, situaciones [{texto, urgente}], areas [{nombre, icono, texto, puntos}], equipo [{nombre, rol}], estado "vendido", plan "premium"|"basico", alta, fuente`.
   - Costo de consulta (opcional, solo si el abogado lo da): `"consultas": [{"modo": "Asesoría por WhatsApp", "precio": 0}, {"modo": "Asesoría presencial", "precio": 500, "unidad": "la hora"}]` (precio 0 = Gratis). En `guia.json` pon `"consulta": "Consulta desde $300"` o `"Asesoría gratis por WhatsApp"`.
   - Iconos válidos: `familia, maletin, escudo, documento, edificio, acuerdo, balanza, lupa`.
   - Horario 24/7: cada día `["00:00","23:59"]`.
   - Usa SOLO datos que él dio; no inventes direcciones, cédulas ni teléfonos.
3. Agrega su ficha a `prospectos/guia.json` (`slug, nombre, rol, ciudad, materias, plan, foto, logo, fondo, iniciales, whatsapp "52…", telefono, verificada false, pagina, redes, estado "activo", alta, vence, pago`).
   - Ciudades: `cdmx, edomex, guadalajara, puebla, monterrey, tijuana, leon, chihuahua, san-luis-potosi, los-cabos, yucatan, queretaro, gomez-palacio` (+ `otras_ciudades`). Para agregar una ciudad nueva: `CIUDADES` en `herramientas/guia.py`, `CIUDADES_GUIA` en `herramientas/generar.py` y `CIUDAD_PAL` en `public/assets/guia.js`.
   - Materias: `penal, familiar, laboral, civil, mercantil, sucesiones, amparo, fiscal, agrario`.
4. Genera:
   ```
   cd /home/claude/venia-repo   (o donde esté clonado)
   python3 herramientas/generar.py          # perfiles + qr.png de cada uno
   python3 herramientas/compartir.py <slug> # vista previa al compartir (compartir.png)
   python3 herramientas/guia.py             # guía, listados, sitemap
   ```
5. Revisa en teléfono:
   ```
   (python3 -m http.server 8097 -d public >/dev/null 2>&1 &); sleep 1.5
   python3 herramientas/revisar_v2.py <slug>   # capturas en capturas/v2_<slug>_1.png
   ```
   Mira también `public/<slug>/compartir.png`.
6. Commit + push.
7. Imagen para su estado con QR:
   ```
   python3 herramientas/estado.py <slug> --titulo "Frase con <em>parte dorada.</em>" --chips "Penal,Familiar,Civil"
   ```
   Para que se vea llamativa (como la de Morningstar) pasa SIEMPRE: `--etiqueta "NOMBRE · CIUDAD"`, un `--titulo` largo de 2–3 líneas con buena parte en `<em>` dorado (p. ej. "Defensa jurídica estratégica. <em>Resultados con integridad.</em>"), 4–6 `--chips` y un `--info "Ciudad<br>frase gancho"`. Si la foto real tiene fondo revuelto (letreros, salón), usa `--modo logo` para que salga en tarjeta con marco dorado.
   Sale en `estados/Estado-<Slug>.png` y comprueba el QR. Modo `foto` si tiene foto real, `logo` si no (automático según `"logo"`). Míralo antes de enviarlo con SendUserFile.
7b. Flyer para su Facebook (1080×1350, crema, con su WhatsApp y QR):
   ```
   python3 herramientas/flyer.py <slug> --titulo "Frase <em>dorada.</em>" --servicios "A,B,C,D,E,F" --etiqueta "MÉRIDA · ATENCIÓN 24/7"
   ```
   Sale en `estados/Flyer-<Slug>.png`.
7c. Flyer estilo despacho (oscuro/dorado, más impactante, el que prefiere él):
   ```
   python3 herramientas/flyer_despacho.py <slug> --titulo "¿Detuvieron a un familiar?" --dorado "Cada hora cuenta." --sub "..." --servicios "A,B,C,D"
   ```
   Título = dolor del cliente + frase dorada concreta. Sale en `estados/Flyer-Despacho-<Slug>.png`.
8. Entrégale: el enlace `https://liclink.com.mx/<slug>/`, la imagen del estado y el **texto de muestra** (abajo).

Otros pedidos frecuentes:
- **"Da de baja"** (por teléfono o nombre): en `abogados.json` pon `"estado": "borrar"`; en `guia.json` quita su ficha. Regenera todo y haz push.
- **"Activar premium"**: `plan: "premium"` en ambos archivos.
- Cambiar logo, número o promoción: edita el JSON y regenera.

## Textos que funcionan (él copia y pega)
- **Mensaje de prospección** (el que sí vende, ~1 de cada 6): cercano, nada invasivo, que despierte curiosidad, **sin precio**. Idea central: *"Lic., ya no busque clientes. Nosotros lo hacemos por usted. Sea parte de LicLink…"*. Que diga que le conseguimos/atraemos clientes, pero sin prometer resultados garantizados.
- **Texto de muestra** — formato que él prefiere (nov 2026): cada punto en una frase completa y **personalizada con lo real de su perfil** (su estado/ciudad en la guía y en Google, "con su foto/logo, sus servicios, su horario…, sus N números" solo si es cierto). Ejemplo:
  "⚖️ Aparece en la guía de abogados de Yucatán, donde la gente busca abogado por ciudad y por materia. / 📲 Sus clientes le escriben directo a su WhatsApp con un solo toque, sin intermediarios. / ⭐ Perfil Premium destacado, con su foto, sus servicios, su horario 24/7 y sus 3 números. / 🔎 Su perfil está hecho para aparecer en Google cuando alguien busca abogado en Mérida. / 📢 Nosotros promocionamos la guía para atraerle clientes. / 🖼️ Incluye su código QR para estados y redes." Cierre: "*Plan Premium: $399 de alta y luego solo $149 al mes.* Como socio fundador conserva ese precio mientras siga activo. Si le gusta, se lo dejo activo hoy mismo. Si quiere cambiar algo, dígame y lo ajustamos."
- Formato anterior (más corto), con emojis:
  saludo + enlace → "Lo que gana con su espacio en LicLink":
  - ⚖️ aparece en la guía de su estado
  - 📲 clientes le escriben directo a su WhatsApp
  - ⭐ perfil Premium destacado
  - 🔎 hecho para aparecer en Google
  - 📢 nosotros promocionamos la guía
  - 🖼️ incluye QR para estados

  Después: "Plan Premium: $399 de alta y luego solo $149 al mes. Como socio fundador conserva ese precio mientras siga activo." y "Si le gusta, se lo dejo activo hoy mismo…". Trata de "usted" al abogado.
- Textos dentro de las páginas (para clientes): de tú, verbo primero en botones.

## Estilo visual actual
- Perfiles: plantilla `plantilla/v2.html` + `public/assets/v2.css` / `v2.js`, estilo **"claro"** (crema), letra Plus Jakarta Sans. `?estilo=oro` en la URL previsualiza otro estilo.
- Vista previa al compartir (`compartir.png`, 1200×630): crema, logo grande con marco dorado a la derecha.
- Imagen de estado: oscura, sello dorado "★ DESPACHO DESTACADO", tarjeta crema con QR.
- Las tipografías para capturas están en `herramientas/fuentes/` (no hace falta instalar nada salvo Playwright, que ya viene).

## Pendientes que él tiene (recuérdaselos si viene al caso)
- Borrar o redesplegar el sitio viejo de Netlify (salía duplicado en Google).
- Dar de alta liclink.com.mx en Google Search Console y mandar `sitemap.xml`.
- Cloudflare Web Analytics para reportes de visitas por abogado.
- Verificar cédulas; nombre legal en el aviso de privacidad; cobro (Mercado Pago); correo de contacto.
