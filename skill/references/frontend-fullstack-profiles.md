# Perfiles de contexto para frontend y full stack

## Regla de selección

Incluye una fuente solo si puede modificar una decisión actual. El orden de inclusión es: contrato público, punto de entrada, tipo/interfaz, implementación causal, prueba, configuración de ejecución, consumidor directo y diff. Excluye artefactos generados, dependencias instaladas, binarios, mapas, minificados, capturas repetidas, logs sin error causal y lockfiles salvo que la tarea trate dependencias.

## Perfil `frontend`

Mantén estable el mapa de rutas, `package.json`, configuración de build, design tokens, componentes base, tipos de UI, estrategia de estado, i18n y reglas de accesibilidad. Para cada tarea dinámica incluye solo el componente/route, hook/store, contrato de datos, prueba relacionada, estilo afectado y diff.

| Problema | Contexto dinámico mínimo | Prueba que debe permanecer |
|---|---|---|
| Interacción rota | componente, handler, hook/store y selector | prueba de interacción o reproducción |
| Datos incorrectos | query/cliente API, tipo y estado de carga/error | contrato API y test de estado |
| Estilo/responsive | componente, tokens, CSS y viewport objetivo | captura/visual test solo si es causal |
| Accesibilidad | árbol interactivo, label/foco/roles y comportamiento teclado | prueba de teclado o criterio verificable |
| Rendimiento | frontera de render, datos, profiler/medición y bundle | métrica comparativa y presupuesto |

No cargues todo el design system para editar un botón. No omitas el componente base, token o regla de accesibilidad si el cambio los afecta.

## Perfil `fullstack`

Mantén estable la topología de servicio, contrato API, tipos compartidos, esquema/migraciones, auth/autorización, configuración, observabilidad y convenciones de error. Para la tarea incluye route/acción, validador, servicio, consulta/migración, consumidor UI, prueba y diff que formen el subgrafo causal.

| Cambio | Paquete dinámico mínimo | Escalar si |
|---|---|---|
| Endpoint | ruta, schema/validador, auth, servicio y test | hay consumidores externos o versionado |
| Esquema | entidad, migración, consulta, índices y consumidores | hay backfill, datos existentes o rollback |
| Permiso | middleware/política, recurso, UI y test de abuso | el permiso cruza tenants o roles |
| Integración | adaptador, contrato externo, timeout/retry y prueba simulada | hay pago, PII, idempotencia o webhook |
| Incidente | síntoma, métrica, último diff, ruta crítica y runbook | degradación sistémica o datos afectados |

## Perfil `repo-amplio`

Para monorepo o refactor de largo alcance, carga un **mapa**, no todos los archivos. El mapa debe contener paquetes, responsables, dependencias internas, entradas públicas, tipos/contratos compartidos, configuración de build y pruebas de integración. Después expande solo el subgrafo de los símbolos que cambian y sus consumidores. Si la relación no es conocida, ejecuta búsqueda dirigida; no abras paquetes completos por precaución.

## Actualización del paquete

Cuando cambie un contrato, invalida consumidores y pruebas relacionadas. Cuando cambie un archivo local, sustituye su versión anterior por el diff o el nuevo símbolo. Cuando falle una prueba, añade el fallo y la ruta causal, no todo el log. Cuando compactes, conserva contratos, decisiones, rutas, pruebas, comandos y bloqueos; descarta deliberación histórica.
