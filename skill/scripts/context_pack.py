#!/usr/bin/env python3
"""Select a stable and dynamic code-context packet without reading entire repositories."""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

EXCLUDED = {".git", "node_modules", "dist", "build", ".next", "coverage", "vendor", "__pycache__", ".turbo"}
MANIFESTS = {"package.json", "pnpm-workspace.yaml", "turbo.json", "tsconfig.json", "vite.config.ts", "next.config.js", "next.config.ts", "pyproject.toml", "go.mod", "Cargo.toml", "Dockerfile", "docker-compose.yml", "schema.prisma", "openapi.yaml", "openapi.yml", "README.md", ".env.example"}
SOURCE = {".ts", ".tsx", ".js", ".jsx", ".css", ".scss", ".py", ".go", ".rs", ".java", ".sql", ".graphql"}
PROFILE_PATHS = {
    "frontend": ("app", "pages", "routes", "components", "ui", "hooks", "store", "styles", "i18n", "locales", "test", "spec"),
    "fullstack": ("app", "pages", "routes", "components", "api", "server", "service", "controller", "db", "database", "prisma", "migration", "auth", "middleware", "schema", "test", "spec", "infra"),
    "repo-amplio": ("packages", "apps", "libs", "services", "shared", "api", "server", "web", "test", "spec"),
}


def listed_files(root: Path) -> list[Path]:
    try:
        proc = subprocess.run(["git", "-C", str(root), "ls-files", "-co", "--exclude-standard"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        paths = [root / item for item in proc.stdout.splitlines() if item]
    except (OSError, subprocess.CalledProcessError):
        paths = list(root.rglob("*"))
    return [p for p in paths if p.is_file() and not any(part in EXCLUDED for part in p.relative_to(root).parts)]


def terms(text: str) -> set[str]:
    return {x for x in re.findall(r"[a-zA-Z0-9_-]{2,}", text.lower()) if x not in {"para", "con", "desde", "the", "and", "del"}}


def estimated_tokens(path: Path) -> int:
    try:
        return max(1, (path.stat().st_size + 3) // 4)
    except OSError:
        return 0


def kind(path: Path, root: Path) -> str:
    rel = str(path.relative_to(root)).lower()
    if path.name in MANIFESTS:
        return "estable"
    if any(x in rel for x in ("test", "spec", "__tests__", "e2e")):
        return "prueba"
    if path.suffix.lower() in SOURCE:
        return "código"
    if path.suffix.lower() in {".json", ".yaml", ".yml", ".toml"}:
        return "config"
    return "otro"


def score(path: Path, root: Path, profile: str, task_terms: set[str]) -> int:
    rel = str(path.relative_to(root)).lower()
    value = {"estable": 100, "config": 35, "prueba": 28, "código": 20, "otro": 0}[kind(path, root)]
    value += sum(45 for term in task_terms if term in rel)
    value += sum(12 for marker in PROFILE_PATHS[profile] if marker in rel)
    value -= min(len(path.relative_to(root).parts), 12)
    if path.suffix.lower() not in SOURCE and path.name not in MANIFESTS:
        value -= 20
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--profile", choices=sorted(PROFILE_PATHS), required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--budget-tokens", type=int, default=128000)
    parser.add_argument("--limit", type=int, default=120)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    files = listed_files(root)
    query = terms(args.task)
    ranked = sorted(files, key=lambda p: (-score(p, root, args.profile, query), str(p)))
    stable = [p for p in ranked if kind(p, root) == "estable"]
    dynamic = [p for p in ranked if p not in stable]
    chosen: list[Path] = []
    used = 0
    for path in stable + dynamic:
        estimate = estimated_tokens(path)
        if estimate > args.budget_tokens // 2:
            continue
        if used + estimate > args.budget_tokens or len(chosen) >= args.limit:
            continue
        chosen.append(path)
        used += estimate
    print(f"PERFIL: {args.profile}")
    print(f"TAREA: {args.task}")
    print(f"PRESUPUESTO_APROX_TOKENS: {args.budget_tokens}")
    print(f"SELECCIÓN_APROX_TOKENS: {used}")
    print("ESTABLE:")
    for path in chosen:
        if path in stable:
            print(f"- {path.relative_to(root)} [{estimated_tokens(path)} t~]")
    print("DINÁMICO:")
    for path in chosen:
        if path not in stable:
            print(f"- {path.relative_to(root)} [{kind(path, root)}; {estimated_tokens(path)} t~]")
    print("NOTA: t~ es una aproximación de tamaño por bytes; confirma tokens reales en la métrica del proveedor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
