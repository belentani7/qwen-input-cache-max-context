#!/usr/bin/env python3
"""Validate a compact cache/context experiment report."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FIELDS = ("PERFIL:", "MODELO:", "RUTA_CACHÉ:", "ENTRADA:", "CACHEADOS:", "SALIDA:", "HERRAMIENTAS:", "VUELTAS:", "PRUEBA_FINAL:", "CONCLUSIÓN:")
PROFILE = re.compile(r"(?m)^PERFIL:\s*(frontend|fullstack|repo-amplio|api-session-cache)\s*$", re.IGNORECASE)
ROUTE = re.compile(r"(?m)^RUTA_CACHÉ:\s*(qwen-code|explícita|responses-session|ninguna)\s*$", re.IGNORECASE)
TEST = re.compile(r"(?m)^PRUEBA_FINAL:\s*(PASÓ|FALLÓ|NO EJECUTADO)\s*$", re.IGNORECASE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    text = Path(args.file).read_text(encoding="utf-8")
    missing = [field for field in FIELDS if field not in text]
    if missing:
        print("INVALID: faltan campos: " + ", ".join(missing))
        return 2
    if not PROFILE.search(text) or not ROUTE.search(text) or not TEST.search(text):
        print("INVALID: perfil, ruta de caché o prueba final no usan un valor admitido")
        return 2
    if re.search(r"(?im)^CONCLUSIÓN:\s*$", text):
        print("INVALID: falta conclusión accionable")
        return 2
    print("VALID: informe de caché completo; interpretar resultados junto a métricas del proveedor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
