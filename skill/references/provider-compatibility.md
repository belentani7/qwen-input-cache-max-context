# Compatibilidad de proveedores

## Regla de portabilidad

Trata el prompt y el protocolo como portables, pero trata la configuración como específica del cliente. Antes de usar una opción, confirma que el modelo y el cliente la soportan. Si no existe, omítela; no la reemplaces con texto que el modelo pueda interpretar como una capacidad real.

| Capacidad | Qwen/Alibaba | OpenAI | Anthropic | Política de la skill |
|---|---|---|---|---|
| Caché de prefijo | Model Studio documenta Context Cache para prefijos repetidos | Prompt Caching está documentado para modelos compatibles | Prompt caching usa puntos de caché y prefijos reutilizables | Mantener prefijo estable y medir hits; no asumir equivalencia |
| Herramientas | Qwen Coder/Qwen Code puede usar herramientas según cliente | Tools/function calling depende del endpoint y modelo | Tools dependen de Messages/Claude Code | Cargar el mínimo y describir entradas brevemente |
| Salida estructurada | Verificar el modelo y la interfaz concreta | Structured Outputs usa JSON Schema en modelos compatibles | Usar el mecanismo admitido por la API/cliente | Preferir contratos pequeños; no forzar JSON si no está soportado |
| Razonamiento | Depende de modelo y parámetros Qwen | Depende del modelo y API | Extended/adaptive thinking depende del modelo/API | Escalar por riesgo; no fijar un parámetro universal |
| Cliente de código | Qwen Code tiene configuración propia | Un cliente compatible puede mapear variables | Claude Code tiene convenciones propias | Mantener adaptadores separados del prompt |

## Configuración segura

Usa variables de entorno para endpoint, clave, modelo y límites. No guardes tokens en `settings.json`, prompts, commits o logs. Valida el nombre del modelo contra el catálogo del proveedor antes de producción.

## Fuentes oficiales

[1] [Alibaba Cloud — Qwen Coder](https://www.alibabacloud.com/help/en/model-studio/qwen-coder): capacidades de generación de código y herramientas.

[2] [Alibaba Cloud — Qwen Code](https://www.alibabacloud.com/help/en/model-studio/qwen-code): conexión y modos de uso del cliente de terminal.

[3] [Alibaba Cloud — Context Cache](https://www.alibabacloud.com/help/en/model-studio/context-cache): reutilización de contexto común.

[4] [Qwen Code — Configuration](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/): configuración del cliente y carga bajo demanda de herramientas.

[5] [OpenAI — Prompt Caching](https://developers.openai.com/api/docs/guides/prompt-caching): condiciones y observabilidad de caché.

[6] [OpenAI — Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs): contratos JSON Schema cuando el modelo lo admite.

[7] [Anthropic — Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching): caché por prefijo y puntos de caché.

[8] [Anthropic — Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking): controles de razonamiento que no deben extrapolarse a Qwen.

Las URLs y capacidades deben revisarse contra la versión desplegada antes de fijar una configuración de producción.
