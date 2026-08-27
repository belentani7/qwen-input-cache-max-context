# Protocolo full stack por decisiones

## Punto de entrada

No recorra capas por costumbre. Identifica primero dónde puede vivir la decisión: interfaz, contrato, servidor, datos, integración, operación o prueba. Abre la capa que pueda confirmar o descartar la hipótesis más barata.

| Señal | Primera evidencia | Escalar a |
|---|---|---|
| Error visual o interacción rota | Componente, estado y prueba de UI | Ruta/API si el estado depende de datos |
| Respuesta API incorrecta | Ruta, tipo/validador y prueba de endpoint | Persistencia e integración externa |
| Datos incoherentes | Esquema, consulta y migración reciente | Consumidores, backfill y compatibilidad |
| Fallo de permisos | Middleware, política y prueba de abuso | UI, auditoría y recursos relacionados |
| Lentitud o exceso de coste | Perfil/traza, consulta y límites | Caché, índices, paginación y arquitectura |

## Contratos solo cuando importan

Formaliza un contrato cuando el cambio cruce procesos, capas o consumidores. Para una API, especifica solo el método, identidad requerida, entrada, salida, errores observables y efecto de persistencia que la decisión pueda alterar. Para una interfaz, conserva carga, vacío, error, éxito, permisos y accesibilidad afectados. No redactes contratos paralelos para cambios puramente locales.

## Cambio reversible

Prefiere cambios que puedan retirarse mediante un diff, flag, migración reversible o adaptación de compatibilidad. Si la decisión destruye datos, altera una API pública, cambia identidad/autorización o reemplaza infraestructura, detén la implementación hasta confirmar consumidores, reversión y criterio de éxito.

## Verificación proporcional

Ejecuta la prueba que pueda invalidar la hipótesis principal. Si cambia un tipo compartido, escala a consumidores. Si cambia una ruta, escala a integración. Si cambia el build o configuración, ejecuta la comprobación del runtime. La build completa no sustituye una prueba de comportamiento, y una prueba unitaria no sustituye una revisión de autorización.

## Compromiso de entrega

Al cerrar una vuelta registra solamente: decisión tomada, evidencia que la soporta, limitación que sigue abierta y estado de la comprobación. Esa información debe permitir retomar el trabajo tras una compresión sin repetir investigación ni conservar toda la conversación.
