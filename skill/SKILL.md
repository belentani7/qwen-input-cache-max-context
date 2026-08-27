---
name: qwen-input-cache-max-context
description: Complemento independiente para Qwen Code y Model Studio que reduce coste de entrada mediante caché y maximiza contexto útil en repositorios frontend y full stack. Usar cuando una tarea incluya contexto largo, sesiones multi-turno, grandes codebases, análisis de UI, contratos de API o necesidad de conservar archivos y herramientas estables entre solicitudes.
---

# Qwen Input Cache & Max Context

Usa esta skill junto a, o en lugar de, la skill full stack original cuando el cuello de botella sea el **contexto de entrada**. No optimices por el prompt más corto: optimiza el número de decisiones correctas por token de entrada, preservando rutas, contratos, diffs y evidencia que puedan cambiar el resultado.

## Modelo de trabajo

Separa siempre la solicitud en cuatro bloques, en este orden:

```text
A. NÚCLEO ESTABLE: reglas, formato, arquitectura y herramientas constantes.
B. CONTEXTO SEMIESTABLE: manifiestos, rutas, tipos, contratos y convenciones de proyecto.
C. PAQUETE DE TAREA: archivos/símbolos/diffs que explican la decisión actual.
D. COLA VOLÁTIL: petición, resultado de herramienta, fallo y siguiente acción.
```

A y B deben conservar orden, texto y definiciones de herramientas idénticos cuando el proveedor use caché de prefijo. C debe cambiar únicamente si cambia la decisión de ingeniería. D debe ser corto y estar al final. Nunca insertes fechas, identificadores de turno, logs completos o estado mutable en A o B.

## Elegir modelo y ventana

No fijes `contextWindowSize` de forma universal. Verifica modelo, región y plan. En Model Studio, `qwen3-coder-plus` y `qwen3-coder-flash` exponen 1M de contexto; `qwen3-coder-next` expone 256k. Los modelos generales `qwen3.7-plus`, `qwen3.7-max` y `qwen3.6-flash` también exponen 1M, y pueden ser preferibles para repositorios grandes con herramientas completas. Consulta [qwen-context-catalog.md](references/qwen-context-catalog.md) antes de configurar un límite. [1]

Define un presupuesto operativo menor que el máximo del modelo. Reserva capacidad para instrucciones, herramientas, salida, pruebas y recuperación de fallos. Empieza con 128k–256k para desarrollo normal, 384k–512k para cambios transversales y usa 1M únicamente cuando el paquete completo —no una transcripción— requiera relaciones de largo alcance. Si el endpoint rechaza el tamaño, reduce el paquete, compacta la conversación o cambia a un modelo con una ventana mayor; no declares una ventana mayor que la admitida. [2]

## Perfiles de contexto

| Perfil | Cargar estable | Paquete dinámico | Uso |
|---|---|---|---|
| `frontend` | rutas, design system, tipos UI, i18n, a11y, build | componente, estado, prueba, captura o diff | UI, rendimiento, accesibilidad, errores de interacción |
| `fullstack` | contratos, esquema, auth, rutas, observabilidad, infraestructura | endpoint/acción, consumidor UI, migración, prueba y diff | cambios de datos, API, permisos, operaciones |
| `repo-amplio` | mapa de módulos, manifiestos, dependencias y contratos públicos | sólo subgrafo causal y consumidores | refactor, deuda, migración, incidentes transversales |
| `api-session-cache` | instrucciones, herramientas y corpus reutilizable | pregunta/acción con `previous_response_id` | API Responses con conversación larga |

Lee [frontend-fullstack-profiles.md](references/frontend-fullstack-profiles.md) para saber exactamente qué incluir y excluir en cada perfil.

## Estrategias de caché

1. **Qwen Code:** usa `model.generationConfig.enableCacheControl`, compresión, truncado de herramientas y filtrado del contexto conforme a la configuración documentada. Usa `tools.toolSearch` solo después de medir: reduce el prompt inicial, pero puede cambiar la lista de herramientas y perjudicar la estabilidad de algunos esquemas de caché. [3]
2. **Chat Completions/DashScope:** usa caché de contexto explícita únicamente con modelos/protocolos compatibles, contenido estable de al menos el umbral del proveedor y marcadores `cache_control` correctos. Mantén el prefijo y la definición de herramientas exactos. [4]
3. **Responses API:** para sesiones multi-turno, usa `previous_response_id`; para activar caché de sesión del servidor, añade `x-dashscope-session-cache: enable` y observa `usage.input_tokens_details.cached_tokens`. [5]

No mezcles modos de caché sin medir. La creación de caché puede tener un coste inicial, los aciertos dependen del proveedor y un contexto irrelevante sigue siendo desperdicio aunque esté cacheado.

## Compresión y recuperación

Cuando el contexto se acerque al presupuesto, conserva: decisiones, contratos, rutas/símbolos, hashes/diffs, evidencia de prueba, riesgos y bloqueos. Elimina planificación vencida, explicaciones repetidas, logs sin error causal, resultados antiguos de herramientas y archivos no relacionados. `scripts/context_pack.py` crea un paquete priorizado y estable sin leer todo el repositorio; úsalo antes de aumentar la ventana.

## Validación de eficacia

Mide en tareas representativas: tokens de entrada, tokens cacheados, tokens de salida, herramientas cargadas, rondas, tiempo y pruebas finales. El perfil correcto reduce coste total o latencia **sin aumentar** fallos, omisiones o rondas. No uses estimaciones de palabras como sustituto de métricas de uso reales.

## Recursos

| Necesidad | Recurso |
|---|---|
| Hechos, límites y compatibilidad de contexto Qwen | [qwen-context-catalog.md](references/qwen-context-catalog.md) |
| Selección de archivos por perfil frontend/full stack | [frontend-fullstack-profiles.md](references/frontend-fullstack-profiles.md) |
| Arquitectura de caché y medición | [input-cache-playbook.md](references/input-cache-playbook.md) |
| Ejemplo API Responses con caché de sesión | [responses-session-cache.example.py](templates/responses-session-cache.example.py) |
| Configuración Qwen Code v3 para contexto alto | [qwen-code-cache-max-context.v3.json](templates/qwen-code-cache-max-context.v3.json) |
| Variante para herramientas bajo demanda | [qwen-code-lean-tools.override.json](templates/qwen-code-lean-tools.override.json) |
| Paquete de contexto priorizado | `python3 scripts/context_pack.py --root . --profile frontend|fullstack --task "resultado"` |
| Informe y comprobación de eficiencia | [cache-report.txt](templates/cache-report.txt) y `python3 scripts/validate_cache_report.py --file cache-report.txt` |

## Interoperabilidad con la copia full stack

Esta copia conserva los protocolos de calidad, seguridad y preparación de mercado de la skill original. Cuando una tarea no necesite contexto amplio, usa el núcleo de decisiones verificables sin activar el perfil de contexto máximo. Cuando el cambio cruce UI, datos, auth, contratos o despliegue, activa `fullstack` y conserva la skill de mercado para cualquier salida comercial.

## Referencias

[1] [Alibaba Cloud Model Studio — Text generation](https://www.alibabacloud.com/help/en/model-studio/text-generation-model)

[2] [Alibaba Cloud Model Studio — Coding Plan FAQ](https://www.alibabacloud.com/help/en/model-studio/coding-plan-faq)

[3] [Qwen Code — Configuration](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)

[4] [Alibaba Cloud Model Studio — Context Cache](https://www.alibabacloud.com/help/en/model-studio/context-cache)

[5] [Alibaba Cloud Model Studio — OpenAI-compatible Responses API](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-responses)
