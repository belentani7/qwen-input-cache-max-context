#!/usr/bin/env python3
"""Evaluate an internal market-launch manifest. It is not legal or regulatory approval."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GATES = [f"G{i}" for i in range(10)]
VALID_STATUSES = {"GO", "GO_LIMITADO", "NO_GO", "BLOQUEADO", "NO_APLICA"}
CRITICAL = {"G3", "G4", "G6", "G8"}
TRIGGERED_DECISIONS = {"revisado", "autorizacion_obtenida", "certificacion_obtenida"}
NO_TRIGGER_DECISION = "sin_detonante_identificado"


def has_placeholder(value: object) -> bool:
    if isinstance(value, str):
        return "REEMPLAZAR" in value or "YYYY-" in value or value.strip() == ""
    if isinstance(value, list):
        return any(has_placeholder(x) for x in value)
    if isinstance(value, dict):
        return any(has_placeholder(x) for x in value.values())
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"BLOQUEADO: manifiesto no legible — {exc}")
        return 2

    issues: list[str] = []
    warnings: list[str] = []
    product = data.get("product", {})
    scope = data.get("scope", {})
    regulatory = data.get("regulatory", {})
    controls = data.get("launch_controls", {})
    if has_placeholder(product) or not product.get("name") or not product.get("version"):
        issues.append("producto: nombre, versión y fecha deben estar definidos sin marcadores")
    if scope.get("launch_mode") not in {"pilot", "public"}:
        issues.append("scope.launch_mode debe ser pilot o public")
    if not scope.get("markets") or not scope.get("segments") or not scope.get("channels"):
        issues.append("scope: mercados, segmentos y canales son obligatorios")
    if has_placeholder(controls) or not controls.get("kill_switch") or not controls.get("rollback"):
        issues.append("launch_controls: kill_switch, rollback, incidente y revisión deben estar definidos")

    found = {gate.get("id"): gate for gate in data.get("gates", []) if isinstance(gate, dict)}
    missing = [gate for gate in GATES if gate not in found]
    if missing:
        issues.append("faltan puertas: " + ", ".join(missing))
    for gate_id in GATES:
        gate = found.get(gate_id)
        if not gate:
            continue
        status = gate.get("status")
        if status not in VALID_STATUSES:
            issues.append(f"{gate_id}: estado inválido")
            continue
        if not gate.get("owner") or has_placeholder(gate.get("owner")):
            issues.append(f"{gate_id}: falta propietario")
        if not gate.get("evidence") or has_placeholder(gate.get("evidence")):
            issues.append(f"{gate_id}: falta evidencia localizable")
        if status in {"NO_GO", "BLOQUEADO"}:
            issues.append(f"{gate_id}: estado {status}")
        if gate_id in CRITICAL and status not in {"GO", "NO_APLICA"}:
            issues.append(f"{gate_id}: puerta crítica debe estar en GO o NO_APLICA con evidencia")
        if scope.get("launch_mode") == "public" and status not in {"GO", "NO_APLICA"}:
            issues.append(f"{gate_id}: lanzamiento público requiere GO o NO_APLICA")
        elif scope.get("launch_mode") == "pilot" and status == "GO_LIMITADO":
            warnings.append(f"{gate_id}: alcance limitado; conservar límite y fecha de revisión")

    triggers = regulatory.get("triggers", [])
    assessment = regulatory.get("assessment")
    if not regulatory.get("owner") or not regulatory.get("evidence"):
        issues.append("regulatory: propietario y evidencia son obligatorios")
    if triggers and assessment not in TRIGGERED_DECISIONS:
        issues.append("regulatory: hay detonantes y falta revisión, autorización o certificación registrada")
    if not triggers and assessment != NO_TRIGGER_DECISION:
        warnings.append("regulatory: explicar por qué se seleccionó una evaluación pese a no registrar detonantes")
    if triggers:
        warnings.append("regulatory: la herramienta registra evidencia interna; no sustituye el dictamen de especialistas o autoridades")

    if issues:
        decision = "BLOQUEADO" if any("manifiesto" in x or "faltan" in x for x in issues) else "NO_GO"
    elif scope.get("launch_mode") == "pilot" and warnings:
        decision = "GO_LIMITADO"
    else:
        decision = "GO"

    print(f"DECISIÓN_INTERNA: {decision}")
    print(f"PRODUCTO: {product.get('name', '—')} {product.get('version', '—')}")
    print(f"ALCANCE: {scope.get('launch_mode', '—')} | mercados={','.join(scope.get('markets', []))}")
    print("BLOQUEOS:")
    for item in issues or ["ninguno"]:
        print(f"- {item}")
    print("ADVERTENCIAS:")
    for item in warnings or ["ninguna"]:
        print(f"- {item}")
    print("NOTA: esta decisión es interna y no constituye aprobación legal, regulatoria, certificación ni autorización de mercado.")
    return 0 if decision in {"GO", "GO_LIMITADO"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
