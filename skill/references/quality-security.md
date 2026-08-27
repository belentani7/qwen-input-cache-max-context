# Calidad y seguridad

## Definición de terminado

Una tarea está terminada solo si el comportamiento solicitado está implementado, los contratos afectados están actualizados, las validaciones pertinentes pasan o están documentadas como bloqueadas, el diff no contiene cambios accidentales y los riesgos residuales están explícitos.

## Lista de control

| Área | Comprobar |
|---|---|
| Tipos | No hay errores de tipos ni conversiones silenciosas peligrosas |
| Validación | Entrada, tamaño, formato y permisos se validan en servidor |
| Autorización | Cada recurso comprueba identidad y alcance; denegar por defecto |
| Datos | Consultas parametrizadas, migración coherente y secretos fuera del código |
| Errores | Mensajes seguros, códigos consistentes, timeouts y reintentos acotados |
| Frontend | Carga, vacío, error, permisos, teclado y foco cubiertos |
| Rendimiento | No se introduce N+1, payload ilimitado ni trabajo repetido evidente |
| Pruebas | Existe una prueba cercana al cambio y evidencia de ejecución |
| Operación | Logging útil sin credenciales ni datos personales innecesarios |

## Escalado de riesgo

Trata como alto riesgo los pagos, identidad, autorización, datos personales, migraciones destructivas, exposición pública, ejecución de comandos, subida de archivos, criptografía y cambios de compatibilidad. En alto riesgo, inspecciona consumidores, añade pruebas de abuso y solicita aclaración si falta una decisión de seguridad. En bajo riesgo, usa el cambio mínimo, una prueba cercana y una revisión de diff.

## Evidencia

Distingue siempre entre `PASÓ`, `FALLÓ`, `NO EJECUTADO` y `NO APLICA`. Incluye el comando exacto y una síntesis de su salida. Nunca conviertas una inspección visual en una prueba, ni una prueba parcial en una afirmación de cobertura completa.

## Revisión final

Busca secretos mediante patrones y revisa archivos nuevos. Comprueba que no se hayan relajado permisos, validaciones, CORS, cookies, cabeceras o políticas de acceso. Revisa dependencias nuevas y sus motivos. Si no puedes comprobar una propiedad, declárala como riesgo abierto.
