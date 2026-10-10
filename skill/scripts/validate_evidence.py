#!/usr/bin/env python3
"""Validate the compact decision report required by this skill."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED = ("MODO:", "DECISIÓN:", "EVIDENCIA:", "ACCIÓN:", "COMPROBACIÓN:", "RIESGO:")
VALID_MODE = re.compile(r"(?m)^MODO:\s*(ejecutar|comparar|suponer|preguntar|bloqueado)\s*$", re.IGNORECASE)
VALID_CHECK = re.compile(r"(?m)^COMPROBACIÓN:\s*.+—\s*(PASÓ|FALLÓ|NO EJECUTADO|NO APLICA)\s*—\s*.+$", re.IGNORECASE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    try:
        text = Path(args.file).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"INVALID: no se puede leer el informe — {exc}")
        return 2

    missing = [label for label in REQUIRED if label not in text]
    if missing:
        print("INVALID: faltan campos: " + ", ".join(missing))
        return 2
    if not VALID_MODE.search(text):
        print("INVALID: MODO debe ser ejecutar, comparar, suponer, preguntar o bloqueado")
        return 2
    if not VALID_CHECK.search(text):
        print("INVALID: COMPROBACIÓN debe incluir fuente/comando, estado y síntesis separados por —")
        return 2
    print("VALID: informe de decisión con evidencia y estado verificable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
