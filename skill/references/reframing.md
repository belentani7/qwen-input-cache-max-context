# Replanteamiento: de «menos tokens» a «mejores decisiones por token»

## Diagnóstico del diseño anterior

El diseño anterior suponía que un flujo fijo —entender, inspeccionar, contratar, implementar y verificar— era eficiente para toda tarea. No lo es. En tareas sencillas impone una tasa de planificación innecesaria; en tareas ambiguas puede inducir una implementación prematura; y en tareas de alto riesgo puede generar una lista de control correcta pero no señalar qué incertidumbre debe resolverse primero.

También confundía tres mecanismos distintos: el comportamiento del agente, las capacidades del cliente y las capacidades de la API. Una plantilla con claves no verificadas no configura Qwen Code aunque exprese una política razonable. Por último, resumir cada ronda por obligación puede eliminar evidencia que aún es decisiva o gastar más tokens que la investigación que pretende ahorrar.

> La calidad no se conserva enviando menos contexto; se conserva conservando la evidencia mínima que cambia una decisión.

## Nuevo modelo: compilador de contexto guiado por decisiones

El agente no sigue una receta completa en cada turno. Opera un ciclo adaptativo:

```text
RESULTADO → DECISIÓN PENDIENTE → INCERTIDUMBRE → EVIDENCIA MÍNIMA
→ ACCIÓN REVERSIBLE → OBSERVACIÓN → ACTUALIZAR COMPROMISOS
```

La unidad de trabajo deja de ser «una tarea» y pasa a ser **la próxima decisión relevante**. Antes de leer un archivo, ejecutar una herramienta o producir un plan, el agente debe poder completar esta frase: `Necesito saber X porque decidiré Y; la evidencia más barata es Z.` Si no puede hacerlo, no debe cargar contexto todavía.

## Reglas de decisión

| Situación observada | Modo | Acción correcta |
|---|---|---|
| El resultado y los archivos son claros | Ejecutar | Modificar y ejecutar la prueba más cercana |
| Hay dos diseños plausibles con impacto distinto | Comparar | Inspeccionar contrato, consumidores y restricciones antes de elegir |
| Falta una preferencia reversible | Suponer | Elegir la convención existente y registrar el supuesto |
| Falta una preferencia irreversible o de seguridad | Bloquear | Formular una pregunta corta con alternativas y consecuencia |
| El contexto se vuelve antiguo o ruidoso | Comprimir | Conservar compromisos y evidencia; descartar transcripciones y salidas repetidas |
| La prueba falla | Diagnosticar | Reducir la siguiente lectura al síntoma, el contrato y el cambio reciente |

## Compromisos, no transcripciones

Mantén un registro de decisión breve solo cuando cambie el futuro de la tarea:

```text
DECISIÓN: [qué se eligió]
EVIDENCIA: [archivo, prueba, documentación o observación]
LÍMITE: [qué no cubre la decisión]
ESTADO: asumido | comprobado | bloqueado
```

No guardes planificaciones que ya no constriñen una acción, explicaciones del modelo, archivos sin relación causal ni salida completa de herramientas. Si una evidencia puede volver a ser necesaria, registra su ruta, símbolo, comando o hash; no la reenvíes completa.

## Economía de contexto

El presupuesto se asigna al mayor riesgo de equivocación, no a una cantidad fija de archivos o tokens. El agente debe preferir una búsqueda, un diff, una interfaz o una prueba focalizada a un archivo completo. Un resumen es válido solo si permite responder estas cuatro preguntas: qué se decidió, con qué evidencia, qué cambió y qué queda sin comprobar.

La caché mejora coste y latencia cuando se reutiliza un prefijo idéntico, pero no convierte en útil un contexto irrelevante. En Qwen/Alibaba, la caché explícita requiere una estructura de mensajes y un umbral de tokens; los marcadores, modelos y tiempos de vida deben verificarse por API y región. [1]

## Consecuencia para Qwen Code

La configuración debe utilizar claves que Qwen Code documenta realmente: `model.generationConfig.enableCacheControl`, límites de sesión y herramientas, compresión de conversación, filtrado de archivos y `tools.toolSearch`. Qwen Code reconoce settings por capas y permite skills de proyecto en `.qwen/skills/`; además ofrece `/compress`, `/summary` y `/stats` para controlar el estado sin inventar un protocolo paralelo. [2] [3]

No actives y desactives herramientas por intuición. `tools.toolSearch` reduce el prompt cargando herramientas bajo demanda, pero la propia documentación advierte que puede perjudicar cachés basadas en prefijo para ciertos modelos. Selecciona el modo según el modelo y verifica coste/latencia con `/stats` o las métricas del proveedor. [2]

## Referencias

[1] [Alibaba Cloud Model Studio — Context Cache](https://www.alibabacloud.com/help/en/model-studio/context-cache)

[2] [Qwen Code — Configuration](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)

[3] [Alibaba Cloud — Qwen Code](https://www.alibabacloud.com/help/en/model-studio/qwen-code)
