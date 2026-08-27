#!/usr/bin/env python3
"""Validate a claims register before internal market release. Not a legal opinion."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

REQUIRED = {
    "claim_id", "claim_text", "channel", "market", "segment", "evidence_path",
    "evidence_method", "scope_limit", "owner", "legal_review", "status", "review_date",
}
SENSITIVE = ("aprobado", "certificado", "garant", "seguro", "sin sesgo", "compatible", "cumple", "precisi", "ahorr")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claims", required=True)
    parser.add_argument("--mode", choices=("pilot", "public"), required=True)
    args = parser.parse_args()
    try:
        with Path(args.claims).open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = set(reader.fieldnames or [])
            rows = list(reader)
    except OSError as exc:
        print(f"BLOQUEADO: no se puede leer registro — {exc}")
        return 2
    missing = REQUIRED - columns
    issues: list[str] = []
    if missing:
        issues.append("faltan columnas: " + ", ".join(sorted(missing)))
    seen: set[str] = set()
    for number, row in enumerate(rows, start=2):
        claim_id = row.get("claim_id", "").strip()
        if not claim_id or claim_id in seen:
            issues.append(f"fila {number}: claim_id ausente o duplicado")
        seen.add(claim_id)
        for key in ("claim_text", "channel", "market", "segment", "evidence_path", "evidence_method", "scope_limit", "owner", "review_date"):
            value = row.get(key, "").strip()
            if not value or "REEMPLAZAR" in value or "YYYY-" in value:
                issues.append(f"fila {number}: {key} ausente o marcador sin sustituir")
        status = row.get("status", "").strip().lower()
        legal = row.get("legal_review", "").strip().lower()
        if status != "aprobado":
            issues.append(f"fila {number}: claim no aprobado")
        text = row.get("claim_text", "").lower()
        if any(word in text for word in SENSITIVE) and legal != "aprobado":
            issues.append(f"fila {number}: claim sensible requiere legal_review=aprobado")
        if args.mode == "public" and legal not in {"aprobado", "no_aplica"}:
            issues.append(f"fila {number}: lanzamiento público requiere revisión legal o no_aplica justificado")
    if not rows:
        issues.append("registro de claims vacío")
    decision = "GO" if not issues else "NO_GO"
    print(f"DECISIÓN_INTERNA_CLAIMS: {decision}")
    print("BLOQUEOS:")
    for item in issues or ["ninguno"]:
        print(f"- {item}")
    print("NOTA: el resultado verifica integridad interna del registro; no sustituye revisión legal o de publicidad aplicable.")
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
