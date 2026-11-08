# -*- coding: utf-8 -*-
"""Guías legales de LicLink: información general en palabras sencillas.
Cada guía: slug, título, descripción, materia (para enlazar a abogados), actualización y secciones.
Una sección es (encabezado, [párrafos]); un párrafo que empieza con "• " se muestra como lista.
Mantén el tono general y prudente: no sustituye asesoría y los plazos deben revisarse con un abogado."""

ACTUALIZADA = "8 de noviembre de 2026"

GUIAS = [
 {"slug": "detuvieron-a-un-familiar", "materia": "penal",
  "titulo": "Detuvieron a un familiar: qué hacer en las primeras horas",
  "desc": "Qué derechos tiene una persona detenida en México, cuánto tiempo la pueden retener y qué hacer mientras llega su abogado.",
  "resumen": "Mantén la calma, averigua dónde está, no firmes nada sin abogado y consigue un defensor cuanto antes.",
  "secciones": [
   ("Lo primero que debes hacer", [
     "• Averigua a qué Ministerio Público o agencia lo llevaron. Pregunta en la agencia más cercana al lugar de la detención o en la fiscalía de tu estado.",
     "• Consigue un abogado defensor lo antes posible. La persona detenida tiene derecho a un defensor desde el primer momento; si no tiene uno particular, el Estado debe asignarle un defensor público.",
     "• Reúne sus documentos: identificación oficial, comprobante de domicilio y, si aplica, recetas o datos médicos.",
     "• No firmes ni le pidas a tu familiar que firme o declare nada sin la presencia de su abogado."]),
   ("Sus derechos como persona detenida", [
     "• A saber por qué se le detiene.",
     "• A guardar silencio: no está obligado a declarar y su silencio no puede usarse en su contra.",
     "• A tener un abogado defensor desde la detención.",
     "• A comunicarse con un familiar o persona de confianza.",
     "• A no ser incomunicado, intimidado ni torturado.",
     "• A un intérprete si no habla español."]),
   ("¿Cuánto tiempo lo pueden retener?", [
     "Según la Constitución, el Ministerio Público puede retener a una persona hasta 48 horas. En ese tiempo debe dejarla en libertad o ponerla a disposición de un juez. En casos de delincuencia organizada el plazo puede ser mayor.",
     "Ante el juez hay una primera audiencia. Ahí se revisa si la detención fue legal y, después, el juez decide si inicia un proceso en su contra (vinculación a proceso) y qué medidas cautelares aplicar."]),
   ("Errores comunes", [
     "• Pagar a personas que prometen \"sacarlo\" sin ser abogados o sin darte un recibo.",
     "• Dejar que pase el tiempo: las primeras horas son las más importantes para la defensa.",
     "• Hablar del caso por mensajes o redes sociales."]),
  ]},
 {"slug": "me-despidieron", "materia": "laboral",
  "titulo": "Me despidieron: tus derechos y los plazos para reclamar",
  "desc": "Qué te corresponde si te despiden en México, la diferencia entre finiquito y liquidación, y cuánto tiempo tienes para reclamar.",
  "resumen": "Los plazos son cortos: no firmes tu renuncia y busca asesoría en cuanto te despidan.",
  "secciones": [
   ("Lo primero que debes hacer", [
     "• No firmes una renuncia ni hojas en blanco. Si te presionan, puedes negarte.",
     "• Anota la fecha, la hora y quién te despidió. Si hubo testigos, guarda sus nombres.",
     "• Guarda pruebas de tu trabajo: recibos de nómina, gafete, mensajes, correos, fotos o tu alta en el IMSS.",
     "• Busca asesoría cuanto antes: los plazos para reclamar empiezan a contar desde el despido."]),
   ("Finiquito y liquidación: no son lo mismo", [
     "El finiquito te corresponde siempre que termina tu trabajo, renuncies o te despidan: salarios pendientes y la parte proporcional de aguinaldo, vacaciones y prima vacacional.",
     "La liquidación (o indemnización) aplica cuando el despido es injustificado. Por ley incluye, entre otras cosas, tres meses de salario y, según el caso, prima de antigüedad y salarios que dejaste de recibir. El cálculo exacto depende de tu antigüedad y tu salario."]),
   ("¿Cuánto tiempo tengo para reclamar?", [
     "La Ley Federal del Trabajo da un plazo corto para reclamar un despido injustificado: dos meses contados desde el día siguiente al despido.",
     "Antes de ir a juicio, normalmente hay que acudir a una conciliación en el Centro de Conciliación Laboral. Presentar esa solicitud a tiempo es parte de proteger tus derechos. Un abogado laboral te dice exactamente qué hacer en tu caso."]),
   ("Errores comunes", [
     "• Esperar a que el patrón \"te llame\" y dejar pasar el plazo.",
     "• Aceptar un pago menor sin saber cuánto te corresponde.",
     "• Firmar documentos que no entiendes."]),
  ]},
 {"slug": "pension-alimenticia", "materia": "familiar",
  "titulo": "Pensión alimenticia: cómo pedirla para tus hijos",
  "desc": "Quién puede pedir pensión alimenticia en México, qué incluye, qué documentos necesitas y qué pasa si el otro padre no paga.",
  "resumen": "Puedes pedirla ante un juez de lo familiar, incluso de forma provisional desde el inicio del juicio.",
  "secciones": [
   ("¿Qué incluye la pensión?", [
     "Los \"alimentos\" no son solo comida: incluyen casa, ropa, atención médica, educación y lo necesario para el desarrollo de los hijos."]),
   ("¿Cómo se pide?", [
     "• Se presenta una demanda ante un juez de lo familiar del lugar donde viven los hijos.",
     "• Desde el inicio puedes pedir una pensión provisional mientras dura el juicio.",
     "• El juez decide el monto según las necesidades de los hijos y lo que gana quien debe pagar. No hay un porcentaje único para todo el país.",
     "• Si quien debe pagar tiene empleo formal, el juez puede ordenar que se descuente directo de su nómina."]),
   ("Documentos que te sirven", [
     "• Actas de nacimiento de los hijos.",
     "• Tu identificación y comprobante de domicilio.",
     "• Comprobantes de gastos: escuela, médico, renta, comida.",
     "• Datos de quien debe pagar: dónde trabaja o a qué se dedica, si lo sabes."]),
   ("¿Y si no paga?", [
     "Dejar de pagar la pensión tiene consecuencias legales. Se puede pedir el embargo de bienes o salario y, en algunos casos, existe responsabilidad penal. Además, hay registros de deudores alimentarios que pueden limitar ciertos trámites a quien no paga."]),
  ]},
 {"slug": "herencia-sin-testamento", "materia": "sucesiones",
  "titulo": "Herencia sin testamento: cómo se reparten los bienes",
  "desc": "Qué pasa con los bienes de una persona que murió sin testamento en México, quién hereda y cómo se hace el trámite.",
  "resumen": "Se hace un juicio sucesorio intestamentario; en algunos casos puede tramitarse ante notario.",
  "secciones": [
   ("¿Qué pasa si no hay testamento?", [
     "Cuando alguien fallece sin testamento, sus bienes se reparten según lo que dice la ley. Para eso se hace un trámite llamado juicio sucesorio intestamentario (o \"intestado\")."]),
   ("¿Quién hereda?", [
     "En general, la ley da preferencia primero a los hijos y al cónyuge o concubino; si no los hay, a los padres; después, a hermanos y otros parientes. Las reglas exactas cambian un poco según el estado."]),
   ("¿Ante quién se hace el trámite?", [
     "• Ante un juez de lo familiar, presentando la denuncia del intestado.",
     "• En muchos estados puede hacerse ante notario, si todos los herederos son mayores de edad y están de acuerdo. Suele ser más rápido."]),
   ("Documentos que te sirven", [
     "• Acta de defunción.",
     "• Actas que prueben el parentesco: nacimiento, matrimonio.",
     "• Documentos de los bienes: escrituras, facturas, estados de cuenta.",
     "• Constancia de que no existe testamento (la puede tramitar el abogado o el notario)."]),
  ]},
]
