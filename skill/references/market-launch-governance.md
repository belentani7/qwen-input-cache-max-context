# Protocolo de preparación masiva de mercado

## Propósito y límite

Este protocolo habilita una **decisión interna de lanzamiento** para software, SaaS y productos de IA. No concede certificación, marcado, licencia ni autorización gubernamental. Si el producto entra en salud, finanzas reguladas, seguros, empleo, educación evaluada, biometría, menores, pagos, infraestructura crítica, dispositivo conectado, producto físico o decisión automatizada de alto impacto, el flujo debe activar la evaluación sectorial y de jurisdicción antes de cualquier campaña, venta o puesta a disposición pública.

> La puerta `GO` significa que existe evidencia suficiente para la salida definida; no significa que el producto esté aprobado por una autoridad.

## Modelo de puertas

Cada puerta debe tener un **responsable**, evidencia localizable, fecha, alcance de mercado y una de cuatro decisiones: `GO`, `GO_LIMITADO`, `NO_GO` o `BLOQUEADO`. Un `NO_GO` de seguridad, legal/regulatorio, privacidad, fraude o continuidad tiene prioridad sobre las demás puertas.

| Puerta | Resultado que aprueba | Evidencia mínima | Propietario sugerido |
|---|---|---|---|
| G0 — Alcance | Mercado, usuario, caso de uso, país y fecha definidos | manifiesto de lanzamiento y exclusiones | Product/CEO |
| G1 — Problema y valor | Problema validado y propuesta de valor no engañosa | entrevistas, métricas beta, hipótesis y claims | Producto/Growth |
| G2 — Producto | Flujos críticos y estados de error listos | criterios de aceptación, pruebas, accesibilidad | Producto/Ingeniería |
| G3 — Seguridad | Riesgos técnicos priorizados y controles verificados | threat model, SAST/dependencias, pruebas y plan de respuesta | Seguridad/CTO |
| G4 — Privacidad y datos | Inventario, base legal y controles de datos definidos | mapa de datos, retención, proveedores, DPIA si aplica | Privacidad/Legal |
| G5 — IA responsable | Riesgos de modelo, límites y supervisión resueltos | evaluación, red-team, trazabilidad, fallback | Responsable de IA |
| G6 — Operaciones | Soporte, observabilidad, continuidad y reversión listos | SLO, runbooks, on-call, rollback, incidentes | Operaciones/CTO |
| G7 — Comercial | Precio, canal, soporte comercial y claims aprobados | pricing, contratos, FAQ, aprobaciones de claims | Growth/Ventas/Legal |
| G8 — Cumplimiento | Triage regulatorio y obligaciones de mercado resueltas | matriz jurisdicción, asesoramiento y registros aplicables | Legal/Compliance |
| G9 — Go/No-Go | Riesgos aceptados por responsables y lanzamiento acotado | acta de decisión, plan de observación y kill switch | Dirección |

## Controles por dominio

### G0–G1: producto y mercado

Define una sola proposición de valor por segmento. Separa hechos demostrables, hipótesis y aspiraciones de marketing. Un claim de rendimiento, seguridad, precisión, ahorro, cumplimiento o impacto debe enlazar a su método de medición y alcance. No afirmes «aprobado», «certificado», «seguro», «sin sesgo», «compatible» o «garantizado» sin la evidencia y la autorización que correspondan.

Para un lanzamiento masivo, segmenta por país, idioma, edad, industria y canal. Cada segmento debe tener criterios de exclusión y una ruta de soporte. Si la evidencia de demanda es insuficiente, usa `GO_LIMITADO` con cohortes, límites de volumen y métricas de cancelación, conversión, activación y quejas; no simules certeza con una campaña global.

### G2: calidad de producto

Verifica el recorrido crítico desde alta, autenticación, permiso, activación, pago —si aplica—, recuperación, cancelación y eliminación/exportación de datos cuando corresponda. Comprueba carga, error, vacío, permisos, accesibilidad de teclado, mensajería y funcionamiento móvil en las plataformas objetivo. Establece criterio de aceptación para cada flujo comercialmente prometido.

### G3: seguridad

Usa la verificación técnica como línea base, no como una declaración de cumplimiento. OWASP ASVS ofrece una base para probar controles técnicos de aplicaciones y para establecer requisitos de desarrollo seguro. [1] Mantén inventario de dependencias, gestión de secretos, autenticación, autorización, validación de entradas, registro seguro, límites de abuso, copias de seguridad, restauración y respuesta a incidentes. Elige el nivel de profundidad conforme a la exposición y el riesgo; prueba el abuso más probable antes de abrir el canal masivo.

### G4: privacidad y datos

Documenta qué datos se recogen, para qué, dónde se procesan, quién accede, con qué proveedor, cuánto se retienen, cómo se eliminan y cómo se atienden derechos. No habilites una geografía si se desconoce la base jurídica, el aviso aplicable, las transferencias y el canal de derechos. En la UE, cuando un tratamiento sea probable que implique alto riesgo para derechos y libertades, debe evaluarse si procede una DPIA antes del tratamiento; si los riesgos no pueden mitigarse, se requiere consultar a la autoridad antes de continuar. [2]

### G5: IA responsable

Clasifica si el producto usa IA y si genera, recomienda, clasifica, perfila, toma decisiones o modifica contenido. Registra modelo, versión, proveedor, datos de entrada/salida, límites conocidos, evaluación por tarea, tasas de error relevantes, modo de supervisión humana, mecanismo de apelación y fallback. Para IA generativa, incluye prompt injection, fugas de datos, uso indebido, alucinaciones, moderación y trazabilidad. NIST SP 800-218A amplía prácticas de desarrollo seguro para modelos y sistemas de IA; úsalo junto al SSDF, no como sustituto de la evaluación legal aplicable. [3]

### G6: operaciones y confianza

Define SLO, capacidad esperada, alertas, propietario on-call, runbooks, backups, RTO/RPO si aplican, ventanas de mantenimiento, comunicación de incidentes y un mecanismo de desactivación o rollback. Antes de una campaña masiva, ejecuta un ensayo de degradación y de soporte: qué ocurre si el proveedor falla, aumenta el tráfico, se agotan límites, se detecta fraude o debe detenerse una funcionalidad.

### G7: comercialización y soporte

Alinea sitio, anuncios, contratos, precios, facturación, impuestos, términos, política de reembolsos, SLA, privacidad y soporte. Asegura que el equipo comercial no venda funcionalidades, disponibilidad, integraciones, certificaciones o resultados no verificados. Mantén un registro de claims, su prueba, titular y fecha de revisión.

### G8: triage de cumplimiento

Completa el triage de jurisdicción antes de liberar. No concluyas que «no aplica» sin un responsable y fundamento. Los detonantes incluyen: datos personales sensibles, menores, salud, empleo, crédito, seguros, biometría, identificación, pagos, ubicación, sectores críticos, marketing directo, cookies/analítica, exportación, cifrado, IA de alto impacto, producto físico y mercados con requisitos de accesibilidad o consumidor.

La salida de este paso es una de estas cuatro: `sin detonante identificado`, `revisión legal requerida`, `evaluación regulatoria requerida`, `autorización/certificación previa requerida`. Las tres últimas bloquean una salida masiva hasta obtener la decisión de los especialistas autorizados.

### G9: decisión y vigilancia

El acta de `GO` debe declarar versión, mercado, segmentos, fecha, responsables, riesgos aceptados, límites de exposición, métricas de alerta, canal de incidentes, condiciones de reversión y fecha de revisión. Para `GO_LIMITADO`, fija número de usuarios, países, canal, gasto, volumen de datos y una fecha de expiración. La herramienta debe detener la escalada si se cruza un umbral crítico de seguridad, privacidad, disponibilidad, fraude, quejas, error de IA o incumplimiento de claim.

## Referencias

[1] [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)

[2] [European Data Protection Board — Data Protection Impact Assessment](https://www.edpb.europa.eu/topics/accountability-and-compliance-tools/data-protection-impact-assessment_en)

[3] [NIST SP 800-218A — Secure Software Development Practices for Generative AI](https://www.nist.gov/publications/secure-software-development-practices-generative-ai-and-dual-use-foundation-models-ssdf)
