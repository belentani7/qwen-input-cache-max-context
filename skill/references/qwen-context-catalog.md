# Catálogo Qwen: contexto y caché

## Ventana de contexto por modelo

La ventana la determina el **modelo desplegado**, no el tipo de tarea. Frontend y full stack no tienen un máximo propio. La siguiente tabla reúne opciones de Model Studio relevantes para codebases; confirma siempre región, plan y catálogo activo antes de producción.

| Modelo | Contexto documentado | Uso de contexto alto |
|---|---:|---|
| `qwen3-coder-plus` | 1M | Cambios extensos de código con herramientas y contratos |
| `qwen3-coder-flash` | 1M | Exploración y edición de código con menor coste/latencia esperada |
| `qwen3-coder-next` | 256k | Codebase medio, tareas focalizadas y herramienta de código |
| `qwen3.7-plus` | 1M | Repositorio grande con herramientas completas y razonamiento equilibrado |
| `qwen3.7-max` | 1M | Cambios complejos donde la capacidad prima sobre coste |
| `qwen3.6-flash` | 1M | Clasificación, exploración o empaquetado barato de contexto |

La documentación de Model Studio recomienda `qwen3.7-plus` para herramientas de coding de gran codebase y publica una ventana de 1M para los modelos anteriores salvo `qwen3-coder-next`. [1]

## Presupuesto útil, no máximo nominal

Una ventana de 1M no significa que deba enviarse un millón de tokens. Reserva una parte para el prompt estable, definiciones de herramientas, razonamiento, salida, pruebas y nuevos resultados. Un punto de partida prudente es:

| Perfil | Presupuesto operativo inicial | Reserva recomendada |
|---|---:|---:|
| Frontend local | 128k | 32k para salida y herramientas |
| Full stack cruzando capas | 256k | 64k para pruebas, esquemas y fallos |
| Refactor/monorepo | 384k–512k | 128k para consumidores y recuperación |
| Análisis de largo alcance | hasta 1M | 20–30% sin usar para nuevas observaciones |

Estos valores son políticas del complemento, no límites del proveedor. Reduce el presupuesto si los tool schemas, capturas, logs, salida esperada o capacidad real del modelo dejan menos margen.

## Tres mecanismos distintos

| Mecanismo | Cuándo usarlo | Evidencia de acierto |
|---|---|---|
| Caché explícita de contexto | Prefijo grande y estable con API/protocolo compatible | `cached_tokens` y/o `cache_creation_input_tokens` |
| Caché implícita | Peticiones de prefijo repetido sin control manual | Métrica de uso; el acierto no está garantizado |
| Caché de sesión Responses | Conversación que continúa con `previous_response_id` | `usage.input_tokens_details.cached_tokens` |

El contexto explícito de Model Studio requiere modelos y protocolos compatibles. La caché explícita usa un marcador `cache_control`, admite hasta cuatro marcadores, exige al menos 1.024 tokens y conserva la entrada durante una ventana temporal corta; la caché implícita identifica prefijos comunes automáticamente. Las definiciones de herramientas se incluyen en el cálculo de caché y su orden y estructura deben mantenerse constantes si se busca estabilizar el prefijo. [2]

La Responses API puede usar `previous_response_id` para enlazar conversación y `x-dashscope-session-cache: enable` para caché de sesión del servidor. La documentación muestra cómo revisar los tokens cacheados en la métrica de uso. [3]

## Qwen Code

Qwen Code permite controlar `model.generationConfig.enableCacheControl`, `context`/filtrado de archivos, límites de sesión, compresión y carga de herramientas bajo demanda. `contextWindowSize` sirve para reemplazar una detección de ventana incorrecta, no para ampliar una ventana que el modelo no ofrece. `tools.toolSearch` reduce el tamaño inicial al diferir herramientas, pero puede ser contraproducente para modelos que dependen de caché KV de prefijo. [4]

## Referencias

[1] [Alibaba Cloud Model Studio — Text generation](https://www.alibabacloud.com/help/en/model-studio/text-generation-model)

[2] [Alibaba Cloud Model Studio — Context Cache](https://www.alibabacloud.com/help/en/model-studio/context-cache)

[3] [Alibaba Cloud Model Studio — OpenAI-compatible Responses API](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-responses)

[4] [Qwen Code — Configuration](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)
