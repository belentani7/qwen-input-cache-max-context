#!/usr/bin/env python3
"""Model Studio Responses API session-cache example for reusable engineering context."""
from __future__ import annotations

import os
from openai import OpenAI

MODEL = os.environ.get("QWEN_MODEL", "qwen3.7-plus")
BASE_URL = os.environ["QWEN_BASE_URL"]
API_KEY = os.environ["BAILIAN_API_KEY"]

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    default_headers={"x-dashscope-session-cache": "enable"},
)

stable_engineering_context = """<REEMPLAZAR_CON_CONTEXTO_ESTABLE>
Incluye instrucciones del agente, contratos de API, arquitectura y herramientas
que se reutilizarán en varias solicitudes. Mantén este texto idéntico entre turnos.
</REEMPLAZAR_CON_CONTEXTO_ESTABLE>"""

first = client.responses.create(
    model=MODEL,
    input=stable_engineering_context + "\n\nTAREA: analiza el módulo de autenticación y enumera solo los archivos que pueden cambiar la siguiente decisión.",
)
print(first.output_text)
print(f"primera entrada: {first.usage.input_tokens}")
print(f"primera cacheada: {first.usage.input_tokens_details.cached_tokens}")

second = client.responses.create(
    model=MODEL,
    previous_response_id=first.id,
    input="TAREA: ahora compara el contrato de sesión con los consumidores frontend y propone la prueba mínima de regresión.",
)
print(second.output_text)
print(f"segunda entrada: {second.usage.input_tokens}")
print(f"segunda cacheada: {second.usage.input_tokens_details.cached_tokens}")
