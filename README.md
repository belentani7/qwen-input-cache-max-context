# Qwen Input Cache & Max Context

Complemento independiente para **Qwen Code** y **Alibaba Cloud Model Studio** que reduce tokens de entrada y maximiza el contexto útil en repositorios frontend y full stack. Parte de una copia compatible de la skill de ingeniería full stack y conserva sus protocolos de calidad, seguridad y preparación de mercado.

## Contenido

| Ruta | Propósito |
|---|---|
| `skill/` | Skill instalable con perfiles, referencias, plantillas y utilidades |
| `GUIDE.md` | Instalación, selección de modelo, caché, perfiles y medición |
| `qwen-input-cache-max-context.skill.zip` | Paquete distribuible de la skill |

## Principio

Separa el contexto en un núcleo estable, arquitectura semiestable, paquete causal de la tarea y cola volátil. Mantiene lo reutilizable en el prefijo, selecciona solo los archivos que afectan a la siguiente decisión y mide `input_tokens`, `cached_tokens`, salidas, herramientas, vueltas y prueba final antes de adoptar un perfil.

La ventana depende del modelo. Según la documentación vigente de Model Studio, `qwen3-coder-plus` y `qwen3-coder-flash` disponen de una ventana de 1M; `qwen3-coder-next` dispone de 256k. No configures una ventana superior a la capacidad del modelo activo. [1]

## Inicio rápido

```bash
python3 skill/scripts/context_pack.py \
  --root . \
  --profile fullstack \
  --task "corregir una autorización entre API y React" \
  --budget-tokens 256000

python3 skill/scripts/validate_cache_report.py --file cache-report.txt
```

La configuración de ejemplo para Qwen Code está en `skill/templates/qwen-code-cache-max-context.v3.json`; sustituye endpoint, región y credenciales mediante variables de entorno. No se incluyen secretos en este repositorio.

## Validación local

```bash
python3 /home/ubuntu/skills/skill-creator/scripts/quick_validate.py qwen-input-cache-max-context
python3 -m compileall -q skill/scripts
```

## Referencias

[1] [Alibaba Cloud Model Studio — Text generation](https://www.alibabacloud.com/help/en/model-studio/text-generation-model)
