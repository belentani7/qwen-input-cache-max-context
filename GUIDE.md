# Complemento Qwen Input Cache & Max Context

## Qué añade a la copia full stack

Este complemento es una copia independiente de la skill full stack, ampliada para reducir tokens de entrada y conservar el máximo contexto **útil**. No impone un máximo ficticio para frontend o full stack: el límite depende del modelo. En Model Studio, `qwen3-coder-plus` y `qwen3-coder-flash` figuran con 1M de contexto, mientras que `qwen3-coder-next` figura con 256k. Los modelos generales `qwen3.7-plus`, `qwen3.7-max` y `qwen3.6-flash` también figuran con 1M y son opciones válidas para codebases extensos con herramientas completas. [1]

## Instalación

Instala el directorio completo `qwen-input-cache-max-context` como una skill distinta. Conserva todos sus recursos: la copia sigue incluyendo protocolos full stack, seguridad y preparación de mercado, pero el núcleo activa perfiles de contexto y caché cuando el repositorio, la sesión o la tarea lo justifican.

Para Qwen Code, parte de `templates/qwen-code-cache-max-context.v3.json`. Es una plantilla de configuración para `qwen3-coder-plus` de 1M; cambia el ID, la ventana y el endpoint si usas otro modelo o plan. `contextWindowSize` corrige la detección de Qwen Code; no amplía la capacidad real del modelo. La plantilla conserva 200k tokens de margen mediante `sessionTokenLimit: 800000` y usa herramientas estables para favorecer el prefijo cacheable. [2]

## Perfiles de uso

| Perfil | Comando | Cuándo |
|---|---|---|
| Frontend | `context_pack.py --profile frontend` | Componentes, UI, rutas, accesibilidad, estilos y rendimiento |
| Full stack | `context_pack.py --profile fullstack` | UI + API + datos + auth + pruebas + despliegue |
| Repo amplio | `context_pack.py --profile repo-amplio` | Monorepo, refactor transversal, incidentes o contratos compartidos |
| Sesión API | Responses API + `previous_response_id` | Conversaciones de ingeniería largas reutilizando servidor |

Ejemplo:

```bash
python3 scripts/context_pack.py \
  --root . \
  --profile fullstack \
  --task "corregir permisos de edición entre API, base de datos y React" \
  --budget-tokens 256000
```

El resultado es una lista priorizada de archivos estables y dinámicos, con estimación de tamaño. No sustituye las métricas del modelo: sirve para seleccionar qué leer e inyectar primero.

## Reducir caché de entrada correctamente

Mantén idénticos el prompt estable, el orden de herramientas, los esquemas, los contratos y el mapa arquitectónico. Envía tarea, diff, salida de herramientas y error siempre al final. Para API Chat Completions o DashScope, utiliza `cache_control` solo con modelos y protocolos compatibles; el proveedor publica requisitos como umbral mínimo y vigencia limitada. [3]

Para Responses API, crea el cliente con `x-dashscope-session-cache: enable` y continúa con `previous_response_id`; la métrica de uso expone los tokens cacheados. El ejemplo ejecutable está en `templates/responses-session-cache.example.py`. [4]

La alternativa `qwen-code-lean-tools.override.json` activa herramientas bajo demanda. Puede reducir el prompt inicial, pero puede alterar la estabilidad del prefijo. Compara ambos modos con la misma tarea, modelo y prueba final antes de adoptar uno.

## Medir y decidir

Copia `templates/cache-report.txt`, completa tokens de entrada, tokens cacheados, salida, herramientas, vueltas y prueba final, y ejecuta:

```bash
python3 scripts/validate_cache_report.py --file cache-report.txt
```

Conserva una configuración solo si reduce coste o latencia sin aumentar fallos, omisiones, vueltas o pruebas no ejecutadas. No asumas que más contexto equivale a mejor calidad: el contexto estable debe ser reutilizable y el paquete dinámico debe ser causal.

## Referencias

[1] [Alibaba Cloud Model Studio — Text generation](https://www.alibabacloud.com/help/en/model-studio/text-generation-model)

[2] [Qwen Code — Configuration](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)

[3] [Alibaba Cloud Model Studio — Context Cache](https://www.alibabacloud.com/help/en/model-studio/context-cache)

[4] [Alibaba Cloud Model Studio — OpenAI-compatible Responses API](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-responses)
