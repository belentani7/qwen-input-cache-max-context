# Contexto, compresión y caché

## Orden correcto de optimización

Primero elimina contexto que no puede cambiar la siguiente decisión. Después evita repetir contexto que sí es útil. Solo al final reduce la longitud de la salida. Un límite fijo de archivos o tokens es una señal operativa, no una política de calidad.

## Paquete de decisión

Construye contexto con cuatro capas y omite cualquier capa vacía:

| Capa | Contenido | Cuándo conservarla |
|---|---|---|
| Estable | Prompt maestro, reglas de seguridad y formato | Toda la sesión; mantener idéntica para caché |
| Compromisos | Decisiones que restringen acciones futuras | Hasta que se invaliden o se comprueben |
| Evidencia | Interfaces, diffs, resultados de prueba y configuración que resuelven la decisión actual | Solo mientras siga abierta la decisión |
| Petición | Resultado observable y pregunta actual | En cada vuelta, al final |

Antes de incluir una fuente pregunta: `¿Qué decisión cambiaría si esta fuente dijera lo contrario?` Si la respuesta es ninguna, exclúyela. Si la fuente es necesaria únicamente para volver atrás, conserva ruta, símbolo, hash o comando, no el contenido entero.

## Compresión útil

Comprime cuando la conversación ya contiene transcripciones o resultados que no restringen el futuro. Conserva los compromisos, evidencia verificable, archivos/símbolos modificados, comandos con estado y bloqueos. Descarta planes vencidos, explicaciones repetidas, listados completos, salidas de herramientas exhaustivas y archivos que no tienen relación causal.

En Qwen Code, usa `/stats` para observar la sesión y `/compress` o `/summary` para controlar crecimiento de historial. Ajusta los límites de compresión con las claves de configuración documentadas en lugar de inventar un mecanismo paralelo. [1]

## Caché de prefijo

Un prefijo estable es útil solo si se reutiliza. Mantén constantes el orden y el texto del prompt estable; coloca tarea, evidencia reciente y resultados al final. Si usas caché explícita de Alibaba, verifica modelo, región, protocolo, longitud mínima, marcadores, límite de bloques y ventana de validez antes de adoptarla. La caché puede reducir coste y latencia de entradas repetidas sin cambiar la calidad de respuesta, pero su creación tiene coste y los aciertos no son universales. [2]

Las definiciones de herramientas también afectan la estabilidad de caché. Qwen Code ofrece `tools.toolSearch` para cargar herramientas bajo demanda y reducir el prompt, pero advierte que no conviene para modelos que dependan de caché KV de prefijo. Contrasta dos modos en tu modelo real: herramientas estables para maximizar hits, frente a herramientas diferidas para minimizar el prompt inicial. Mide con estadísticas, no por intuición. [1]

## Mediciones mínimas

Para una tarea representativa, registra `tokens de entrada`, `tokens cacheados si se exponen`, `tokens de salida`, `herramientas invocadas`, `vueltas`, `prueba final` y `defectos u omisiones`. Gana el modo que mantenga la prueba final y reduzca el coste total, no necesariamente el que tenga el prompt más corto.

## Referencias

[1] [Qwen Code — Configuration](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)

[2] [Alibaba Cloud Model Studio — Context Cache](https://www.alibabacloud.com/help/en/model-studio/context-cache)
