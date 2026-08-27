# Playbook de caché de entrada

## Decisión de ruta

| Entorno | Método principal | Cuándo escogerlo |
|---|---|---|
| Qwen Code interactivo | `enableCacheControl`, configuración de contexto y `/compress` | Desarrollo local con herramientas del cliente |
| API Chat Completions/DashScope | Caché explícita con `cache_control` | Prefijo grande y estable, control de mensajes y llamadas repetidas |
| API Responses | `previous_response_id` + cabecera de sesión | Sesión multi-turno con continuidad y servidor compatible |
| Trabajo aislado | Sin caché; paquete mínimo | Tarea única o evidencia que cambia cada vez |

No cambies de ruta en mitad de una sesión sin medir. Una caché de entrada optimiza repetición; no convierte contexto desordenado en contexto útil.

## Prefijo cacheable

Construye de forma determinista:

1. Instrucciones y formato del agente.
2. Herramientas y schemas, en idéntico orden, con campos y valores incluso si están vacíos.
3. Arquitectura estable: manifest, rutas, contratos públicos y convenciones.
4. Contexto de módulo estable: tipos y símbolos que se reutilizarán varias vueltas.
5. Marcador de caché según el protocolo.
6. Cola variable: tarea, diff, resultado de herramienta y pregunta.

No incluyas timestamps, IDs de sesión, estado de turno, contadores, logs, resultados de herramientas, datos personales, secrets ni orden no determinista antes del marcador. Cambiar una definición de herramienta puede invalidar la reutilización del prefijo.

## Contexto explícito de Model Studio

Para caché explícita, verifica que el modelo esté soportado por la región y API. Usa mensajes estructurados y marca un bloque de contenido con `cache_control: {"type":"ephemeral"}`. El proveedor documenta una longitud mínima de 1.024 tokens, hasta cuatro marcadores y una vigencia corta que se renueva mediante acierto. La creación de caché puede costar más que entrada estándar, por lo que se justifica cuando el bloque se reutilizará. [1]

Organiza varios marcadores cuando existan capas de distinto ritmo de cambio: instrucciones estables; arquitectura estable; corpus de módulo. No marques datos que cambian en cada vuelta. Después de crear el caché, espera la respuesta completa antes de depender del siguiente acierto.

## Responses API y caché de sesión

Para la API Responses compatible, inicia el cliente con `x-dashscope-session-cache: enable`. En la segunda y siguientes vueltas usa `previous_response_id` en lugar de reconstruir manualmente un historial entero. El proveedor gestiona el contexto de servidor y expone tokens cacheados en el uso. El ID de respuesta tiene una validez limitada según la documentación; persiste la información necesaria para recuperar la sesión si expira. [2]

## Qwen Code y herramientas

`model.generationConfig.enableCacheControl` permite habilitar el control de caché que el cliente transmite al proveedor cuando el modelo lo admite. `tools.truncateToolOutputThreshold` y `tools.truncateToolOutputLines` protegen contra resultados enormes; `context.fileFiltering` respeta ignores; la compactación retiene archivos recientes. [3]

`tools.toolSearch` tiene un intercambio: con `enabled: true` y umbral bajo, carga herramientas bajo demanda y reduce el prompt inicial; con `enabled: false`, preserva un conjunto de herramientas estable que puede favorecer un prefijo repetible. Ejecuta la misma tarea con ambas opciones y compara tokens cacheados, tiempo, número de herramientas y prueba final antes de fijar el perfil.

## Informe de medición

Después de cada experimento, conserva exactamente:

```text
PERFIL: frontend | fullstack | repo-amplio | api-session-cache
MODELO: id, región y endpoint
RUTA_CACHÉ: qwen-code | explícita | responses-session | ninguna
ENTRADA: tokens
CACHEADOS: tokens | no disponible
SALIDA: tokens
HERRAMIENTAS: número y nombres
VUELTAS: número
PRUEBA_FINAL: PASÓ | FALLÓ | NO EJECUTADO
CONCLUSIÓN: conservar | ajustar | revertir — motivo
```

Un experimento solo es válido si compara el mismo resultado, repo, modelo y alcance funcional. No concluyas que la caché mejoró la calidad: mide coste/latencia y valida calidad con pruebas y revisión.

## Referencias

[1] [Alibaba Cloud Model Studio — Context Cache](https://www.alibabacloud.com/help/en/model-studio/context-cache)

[2] [Alibaba Cloud Model Studio — OpenAI-compatible Responses API](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-responses)

[3] [Qwen Code — Configuration](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)
